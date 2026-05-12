#!/usr/bin/env python3
"""
Kiro Token GPU Miner — NVIDIA CUDA version
Sepolia Testnet | Contract: (will be updated after deploy)

Usage:
  cp .env.example .env   # set PRIVATE_KEY and CONTRACT_ADDRESS
  python3 kiro_gpu_miner.py

GPU tuning env:
  GPU_BLOCKS=65535
  GPU_THREADS=256
"""

from __future__ import annotations

import os
import secrets
import signal
import sys
import time
from pathlib import Path

# Load .env
_env_path = Path(__file__).parent / ".env"
if _env_path.exists():
    for _line in _env_path.read_text().splitlines():
        _line = _line.strip()
        if _line and not _line.startswith("#") and "=" in _line:
            _k, _v = _line.split("=", 1)
            os.environ.setdefault(_k.strip(), _v.strip())

CONTRACT = os.environ.get("CONTRACT_ADDRESS", "")
CHAIN_ID = 11155111  # Sepolia
RPC = os.environ.get("RPC_URL", "https://ethereum-sepolia-rpc.publicnode.com")
PRIVATE_KEY = os.environ.get("PRIVATE_KEY", "")
GAS_LIMIT = int(os.environ.get("GAS_LIMIT", "300000"))
PAUSE_BETWEEN_ROUNDS = int(os.environ.get("PAUSE_BETWEEN_ROUNDS", "3"))

GPU_BLOCKS = int(os.environ.get("GPU_BLOCKS", "65535"))
GPU_THREADS = int(os.environ.get("GPU_THREADS", "256"))
GPU_BATCHES_PER_STATUS = int(os.environ.get("GPU_BATCHES_PER_STATUS", "32"))

running = True
w3 = None

# CUDA kernel (same as PFFT)
CUDA_SOURCE = r'''
#include <stdint.h>

#define ROL64(a, offset) (((a) << (offset)) ^ ((a) >> (64 - (offset))))

__device__ __constant__ uint64_t RC[24] = {
    0x0000000000000001ULL, 0x0000000000008082ULL,
    0x800000000000808aULL, 0x8000000080008000ULL,
    0x000000000000808bULL, 0x0000000080000001ULL,
    0x8000000080008081ULL, 0x8000000000008009ULL,
    0x000000000000008aULL, 0x0000000000000088ULL,
    0x0000000080008009ULL, 0x000000008000000aULL,
    0x000000008000808bULL, 0x800000000000008bULL,
    0x8000000000008089ULL, 0x8000000000008003ULL,
    0x8000000000008002ULL, 0x8000000000000080ULL,
    0x000000000000800aULL, 0x800000008000000aULL,
    0x8000000080008081ULL, 0x8000000000008080ULL,
    0x0000000080000001ULL, 0x8000000080008008ULL
};

__device__ __forceinline__ uint64_t load64_le(const unsigned char *x) {
    uint64_t r = 0;
    #pragma unroll
    for (int i = 0; i < 8; i++) {
        r |= ((uint64_t)x[i]) << (8 * i);
    }
    return r;
}

__device__ __forceinline__ uint64_t bswap64(uint64_t x) {
    return ((x & 0x00000000000000ffULL) << 56) |
           ((x & 0x000000000000ff00ULL) << 40) |
           ((x & 0x0000000000ff0000ULL) << 24) |
           ((x & 0x00000000ff000000ULL) << 8)  |
           ((x & 0x000000ff00000000ULL) >> 8)  |
           ((x & 0x0000ff0000000000ULL) >> 24) |
           ((x & 0x00ff000000000000ULL) >> 40) |
           ((x & 0xff00000000000000ULL) >> 56);
}

__device__ void keccakf(uint64_t st[25]) {
    const int piln[24] = {
        10, 7, 11, 17, 18, 3, 5, 16,
        8, 21, 24, 4, 15, 23, 19, 13,
        12, 2, 20, 14, 22, 9, 6, 1
    };
    const int rotc[24] = {
        1, 3, 6, 10, 15, 21, 28, 36,
        45, 55, 2, 14, 27, 41, 56, 8,
        25, 43, 62, 18, 39, 61, 20, 44
    };

    for (int round = 0; round < 24; round++) {
        uint64_t bc[5];

        #pragma unroll
        for (int i = 0; i < 5; i++) {
            bc[i] = st[i] ^ st[i + 5] ^ st[i + 10] ^ st[i + 15] ^ st[i + 20];
        }

        #pragma unroll
        for (int i = 0; i < 5; i++) {
            uint64_t t = bc[(i + 4) % 5] ^ ROL64(bc[(i + 1) % 5], 1);
            st[i] ^= t;
            st[i + 5] ^= t;
            st[i + 10] ^= t;
            st[i + 15] ^= t;
            st[i + 20] ^= t;
        }

        uint64_t t = st[1];
        #pragma unroll
        for (int i = 0; i < 24; i++) {
            int j = piln[i];
            uint64_t tmp = st[j];
            st[j] = ROL64(t, rotc[i]);
            t = tmp;
        }

        #pragma unroll
        for (int j = 0; j < 25; j += 5) {
            uint64_t row0 = st[j + 0];
            uint64_t row1 = st[j + 1];
            uint64_t row2 = st[j + 2];
            uint64_t row3 = st[j + 3];
            uint64_t row4 = st[j + 4];
            st[j + 0] = row0 ^ ((~row1) & row2);
            st[j + 1] = row1 ^ ((~row2) & row3);
            st[j + 2] = row2 ^ ((~row3) & row4);
            st[j + 3] = row3 ^ ((~row4) & row0);
            st[j + 4] = row4 ^ ((~row0) & row1);
        }

        st[0] ^= RC[round];
    }
}

__device__ __forceinline__ unsigned char digest_byte(uint64_t st[25], int idx) {
    uint64_t lane = st[idx / 8];
    return (unsigned char)((lane >> (8 * (idx % 8))) & 0xff);
}

__device__ bool digest_le_target(uint64_t st[25], const unsigned char *target) {
    #pragma unroll
    for (int i = 0; i < 32; i++) {
        unsigned char d = digest_byte(st, i);
        unsigned char t = target[i];
        if (d < t) return true;
        if (d > t) return false;
    }
    return true;
}

extern "C" __global__ void mine_kernel(
    const unsigned char *challenge,
    const unsigned char *target,
    unsigned long long start_nonce,
    unsigned long long *nonce_out,
    int *found
) {
    unsigned long long idx = blockIdx.x * blockDim.x + threadIdx.x;
    unsigned long long nonce = start_nonce + idx;

    if (found[0] != 0) return;

    uint64_t st[25];
    #pragma unroll
    for (int i = 0; i < 25; i++) st[i] = 0ULL;

    st[0] = load64_le(challenge + 0);
    st[1] = load64_le(challenge + 8);
    st[2] = load64_le(challenge + 16);
    st[3] = load64_le(challenge + 24);
    st[4] = 0ULL;
    st[5] = 0ULL;
    st[6] = 0ULL;
    st[7] = bswap64(nonce);

    st[8] ^= 0x0000000000000001ULL;
    st[16] ^= 0x8000000000000000ULL;

    keccakf(st);

    if (digest_le_target(st, target)) {
        if (atomicCAS(found, 0, 1) == 0) {
            nonce_out[0] = nonce;
        }
    }
}
'''

ABI = [
    {"inputs":[],"name":"currentPowHexZeros","outputs":[{"type":"uint256"}],"stateMutability":"view","type":"function"},
    {"inputs":[],"name":"POW_TARGET","outputs":[{"type":"uint256"}],"stateMutability":"view","type":"function"},
    {"inputs":[],"name":"POW_DIFFICULTY_BITS","outputs":[{"type":"uint256"}],"stateMutability":"view","type":"function"},
    {"inputs":[],"name":"totalMinted","outputs":[{"type":"uint256"}],"stateMutability":"view","type":"function"},
    {"inputs":[],"name":"MAX_SUPPLY","outputs":[{"type":"uint256"}],"stateMutability":"view","type":"function"},
    {"inputs":[],"name":"WALLET_CAP","outputs":[{"type":"uint256"}],"stateMutability":"view","type":"function"},
    {"inputs":[{"name":"requested","type":"uint256"}],"name":"calculateActualMint","outputs":[{"type":"uint256"}],"stateMutability":"view","type":"function"},
    {"inputs":[{"name":"user","type":"address"}],"name":"currentPowChallenge","outputs":[{"type":"bytes32"}],"stateMutability":"view","type":"function"},
    {"inputs":[{"name":"user","type":"address"},{"name":"powNonce","type":"uint256"}],"name":"isValidPow","outputs":[{"type":"bool"}],"stateMutability":"view","type":"function"},
    {"inputs":[{"name":"powNonce","type":"uint256"}],"name":"freeMint","outputs":[],"stateMutability":"nonpayable","type":"function"},
    {"inputs":[],"name":"initChallenge","outputs":[],"stateMutability":"nonpayable","type":"function"},
    {"inputs":[{"name":"user","type":"address"}],"name":"mintedByAddress","outputs":[{"type":"uint256"}],"stateMutability":"view","type":"function"},
    {"inputs":[{"name":"account","type":"address"}],"name":"balanceOf","outputs":[{"type":"uint256"}],"stateMutability":"view","type":"function"},
    {"inputs":[],"name":"getInfo","outputs":[{"type":"uint256"},{"type":"uint256"},{"type":"uint256"},{"type":"uint256"},{"type":"uint256"}],"stateMutability":"view","type":"function"},
    {"inputs":[{"name":"user","type":"address"}],"name":"getUserInfo","outputs":[{"type":"uint256"},{"type":"uint256"},{"type":"uint256"},{"type":"bytes32"},{"type":"bool"}],"stateMutability":"view","type":"function"},
]


def handle_signal(sig, frame):
    del sig, frame
    global running
    print("\n  ⚠️  Stopping GPU miner...")
    running = False


def require_gpu():
    try:
        import numpy as np
        import pycuda.autoinit
        import pycuda.driver as cuda
        from pycuda.compiler import SourceModule
    except ImportError as exc:
        print("❌ Missing NVIDIA GPU dependency:")
        print("   python3 -m pip install pycuda numpy")
        print(f"   Import error: {exc}")
        sys.exit(1)

    device = cuda.Device(0)
    print(f"✅ CUDA GPU: {device.name()}")
    print(f"   Compute capability: {device.compute_capability()}")

    module = SourceModule(CUDA_SOURCE, no_extern_c=True)
    kernel = module.get_function("mine_kernel")
    return np, cuda, kernel


def load_contract(web3):
    return web3.eth.contract(address=web3.to_checksum_address(CONTRACT), abi=ABI)


def get_status(web3, contract, wallet_addr):
    info = contract.functions.getInfo().call()
    user_info = contract.functions.getUserInfo(wallet_addr).call()
    
    return {
        "total_minted": info[0],
        "remaining_supply": info[1],
        "difficulty_bits": info[2],
        "next_mint": info[3],
        "stage": info[4],
        "wallet_minted": user_info[0],
        "wallet_balance": user_info[1],
        "wallet_remaining": user_info[2],
        "has_challenge": user_info[4],
    }


def get_challenge(contract, wallet_addr):
    challenge = contract.functions.currentPowChallenge(wallet_addr).call()
    return challenge if isinstance(challenge, bytes) else challenge.to_bytes(32, "big")


def solve_pow_gpu(np, cuda, kernel, challenge: bytes, target: int, start_nonce_seed: int | None = None):
    challenge_np = np.frombuffer(challenge, dtype=np.uint8).copy()
    target_np = np.frombuffer(target.to_bytes(32, "big"), dtype=np.uint8).copy()
    found_np = np.zeros(1, dtype=np.int32)
    nonce_np = np.zeros(1, dtype=np.uint64)

    challenge_gpu = cuda.mem_alloc(challenge_np.nbytes)
    target_gpu = cuda.mem_alloc(target_np.nbytes)
    found_gpu = cuda.mem_alloc(found_np.nbytes)
    nonce_gpu = cuda.mem_alloc(nonce_np.nbytes)

    cuda.memcpy_htod(challenge_gpu, challenge_np)
    cuda.memcpy_htod(target_gpu, target_np)

    max_start = (2**64 - 1) - (GPU_BLOCKS * GPU_THREADS * GPU_BATCHES_PER_STATUS)
    start_nonce = start_nonce_seed if start_nonce_seed is not None else secrets.randbelow(max_start)
    total_hashes = 0
    start_time = time.time()
    last_report = start_time
    batch_size = GPU_BLOCKS * GPU_THREADS

    while running:
        found_np[0] = 0
        nonce_np[0] = 0
        cuda.memcpy_htod(found_gpu, found_np)
        cuda.memcpy_htod(nonce_gpu, nonce_np)

        for _ in range(GPU_BATCHES_PER_STATUS):
            kernel(
                challenge_gpu,
                target_gpu,
                np.uint64(start_nonce),
                nonce_gpu,
                found_gpu,
                block=(GPU_THREADS, 1, 1),
                grid=(GPU_BLOCKS, 1),
            )
            cuda.Context.synchronize()
            cuda.memcpy_dtoh(found_np, found_gpu)

            total_hashes += batch_size
            if found_np[0]:
                cuda.memcpy_dtoh(nonce_np, nonce_gpu)
                elapsed = time.time() - start_time
                rate = total_hashes / elapsed if elapsed > 0 else 0
                nonce = int(nonce_np[0])
                print(
                    f"\n  ✅ FOUND nonce={nonce} | "
                    f"{total_hashes:,} checked | {rate/1e6:.1f} MH/s"
                )
                return nonce

            start_nonce += batch_size

        now = time.time()
        if now - last_report >= 2:
            elapsed = now - start_time
            rate = total_hashes / elapsed if elapsed > 0 else 0
            print(
                f"  ⚡ GPU {rate/1e6:.1f} MH/s | "
                f"checked {total_hashes/1e6:.0f}M | next nonce {start_nonce:,}",
                end="\r",
            )
            last_report = now

    return None


def submit_mint(web3, wallet, contract, nonce: int) -> bool:
    try:
        fn = contract.functions.freeMint(nonce)
        tx = fn.build_transaction(
            {
                "from": wallet.address,
                "nonce": web3.eth.get_transaction_count(wallet.address),
                "chainId": CHAIN_ID,
                "gas": GAS_LIMIT,
            }
        )
        if "maxFeePerGas" not in tx and "maxPriorityFeePerGas" not in tx:
            tx["gasPrice"] = web3.eth.gas_price

        signed = wallet.sign_transaction(tx)
        tx_hash = web3.eth.send_raw_transaction(signed.raw_transaction)
        print(f"  📤 TX: https://sepolia.etherscan.io/tx/0x{tx_hash.hex()}")

        receipt = web3.eth.wait_for_transaction_receipt(tx_hash, timeout=180)
        if receipt.status == 1:
            print(f"  ✅ MINT OK | Block {receipt.blockNumber} | Gas {receipt.gasUsed}")
            return True

        print(f"  ❌ REVERTED | Gas {receipt.gasUsed}")
        return False
    except Exception as exc:
        print(f"  ❌ TX error: {exc}")
        return False


def main():
    from eth_account import Account
    from web3 import Web3

    np, cuda, kernel = require_gpu()

    print("=" * 60)
    print("  🚀 Kiro Token GPU Miner — NVIDIA CUDA")
    print(f"  Contract: {CONTRACT}")
    print(f"  RPC: {RPC}")
    print(f"  GPU grid: {GPU_BLOCKS} blocks x {GPU_THREADS} threads")
    print("=" * 60)

    if not CONTRACT or CONTRACT == "":
        print("❌ CONTRACT_ADDRESS not set!")
        print("   Update miner/.env after deploying contract")
        sys.exit(1)

    global w3
    w3 = Web3(Web3.HTTPProvider(RPC, request_kwargs={"timeout": 30}))
    if not w3.is_connected():
        print("❌ Cannot connect to RPC")
        sys.exit(1)
    print(f"✅ Connected | Block #{w3.eth.block_number}")

    private_key = PRIVATE_KEY.strip()
    if not private_key or private_key == "your_private_key_here":
        print("❌ PRIVATE_KEY not set!")
        print("   Copy .env.example → .env and set your private key")
        sys.exit(1)
    if not private_key.startswith("0x"):
        private_key = "0x" + private_key

    wallet = Account.from_key(private_key)
    print(f"✅ Wallet: {wallet.address}")

    eth_bal = w3.eth.get_balance(wallet.address) / 1e18
    print(f"💰 ETH: {eth_bal:.6f}")
    if eth_bal < 0.001:
        print("⚠️  Low ETH! Get testnet ETH from https://sepoliafaucet.com/")

    contract = load_contract(w3)
    
    # Initialize challenge if needed
    status = get_status(w3, contract, wallet.address)
    if not status["has_challenge"]:
        print("\n🔧 Initializing challenge...")
        init_tx = contract.functions.initChallenge().build_transaction({
            "from": wallet.address,
            "nonce": w3.eth.get_transaction_count(wallet.address),
            "chainId": CHAIN_ID,
        })
        signed = wallet.sign_transaction(init_tx)
        tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
        w3.eth.wait_for_transaction_receipt(tx_hash)
        print("✅ Challenge initialized")
    
    total_mints = 0
    total_kiro = 0.0
    round_num = 0
    global_start = time.time()

    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)

    while running:
        round_num += 1
        print(f"\n{'─' * 60}")
        print(f"  GPU Round #{round_num}")
        print(f"{'─' * 60}")

        try:
            status = get_status(w3, contract, wallet.address)
            print(
                f"  Supply: {status['total_minted'] / 1e18:,.0f} / 21M "
                f"({status['total_minted'] * 100 / (21_000_000 * 1e18):.1f}%) | "
                f"Next: ~{status['next_mint'] / 1e18:.2f} KIRO | "
                f"Diff: {status['difficulty_bits']}-bit"
            )
            print(
                f"  Wallet: {status['wallet_minted'] / 1e18:,.2f} / 10K KIRO "
                f"({status['wallet_remaining'] / 1e18:,.2f} remaining)"
            )

            if status["total_minted"] >= 21_000_000 * 1e18:
                print("  🏁 Max supply reached!")
                break
            if status["wallet_minted"] >= 10_000 * 1e18:
                print("  🏁 Wallet cap (10,000 KIRO) reached!")
                break

        except Exception as e:
            print(f"  ⚠️  Status error: {e}, retrying in 15s...")
            time.sleep(15)
            continue

        challenge = get_challenge(contract, wallet.address)
        target = contract.functions.POW_TARGET().call()

        print(f"  ⛏️  Mining ({status['difficulty_bits']}-bit)...")
        nonce = solve_pow_gpu(np, cuda, kernel, challenge, target)

        if nonce is None:
            print("  Mining interrupted")
            continue

        # Verify before submitting
        try:
            is_valid = contract.functions.isValidPow(wallet.address, nonce).call()
            if not is_valid:
                print("  ⚠️  Nonce invalid on-chain, re-mining...")
                continue
        except Exception as e:
            print(f"  ⚠️  Verify error: {e}, submitting anyway...")

        success = submit_mint(w3, wallet, contract, nonce)
        if success:
            total_mints += 1
            earned = status["next_mint"] / 1e18
            total_kiro += earned
            print(f"  💰 +{earned:,.2f} KIRO | Total: {total_kiro:,.2f} KIRO from {total_mints} mints")

            try:
                bal = contract.functions.balanceOf(wallet.address).call()
                print(f"  💎 KIRO balance: {bal / 1e18:,.2f}")
            except:
                pass

        elapsed = time.time() - global_start
        print(f"\n  📈 Session: {total_mints} mints | {total_kiro:,.2f} KIRO | {elapsed / 60:.1f} min")

        if running:
            print(f"  ⏳ {PAUSE_BETWEEN_ROUNDS}s cooldown...")
            time.sleep(PAUSE_BETWEEN_ROUNDS)

    print(f"\n{'=' * 60}")
    print(f"  Session Summary")
    print(f"  Mints: {total_mints}")
    print(f"  KIRO earned: {total_kiro:,.2f}")
    print(f"  Runtime: {(time.time() - global_start) / 60:.1f} min")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
