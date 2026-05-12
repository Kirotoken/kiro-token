#!/usr/bin/env python3
"""
PENTA Mining on Kaggle with lolMiner
PentaChain Ethash Mining
"""

import os
import subprocess
import time

# Configuration
WALLET = "0xe81Cb1184A55fA17Db786C8761D955c5838B2675"
WORKER = "kaggle-t4"
POOL = "stratum+tcp://pool.pentamine.org:3030"
ALGO = "ETHASH"

print("="*70)
print("⛏️  PENTA MINER - PentaChain")
print("="*70)
print(f"Wallet: {WALLET}")
print(f"Worker: {WORKER}")
print(f"Pool: {POOL}")
print(f"Algorithm: {ALGO}")
print("="*70)
print()

# Install dependencies
print("📦 Installing dependencies...")
subprocess.run(["apt-get", "update", "-qq"], check=False)
subprocess.run(["apt-get", "install", "-y", "-qq", "wget", "curl"], check=False)

# Download lolMiner
print("⬇️  Downloading lolMiner...")
LOLMINER_URL = "https://github.com/Lolliedieb/lolMiner-releases/releases/download/1.88/lolMiner_v1.88_Lin64.tar.gz"
subprocess.run(["wget", "-q", LOLMINER_URL, "-O", "/tmp/lolminer.tar.gz"], check=True)

print("📦 Extracting lolMiner...")
subprocess.run(["tar", "-xzf", "/tmp/lolminer.tar.gz", "-C", "/tmp/"], check=True)

# Find lolMiner binary
lolminer_path = "/tmp/1.88/lolMiner"
if not os.path.exists(lolminer_path):
    print("❌ lolMiner not found!")
    exit(1)

# Make executable
subprocess.run(["chmod", "+x", lolminer_path], check=True)

print("✅ lolMiner ready!")
print()

# Check GPU
print("🎮 Checking GPU...")
try:
    result = subprocess.run(["nvidia-smi", "--query-gpu=name,memory.total", "--format=csv,noheader"], 
                          capture_output=True, text=True, check=True)
    print(f"GPU: {result.stdout.strip()}")
except:
    print("⚠️  No GPU detected! Mining will be slow.")

print()
print("="*70)
print("🚀 STARTING PENTA MINING...")
print("="*70)
print()

# Start mining
cmd = [
    lolminer_path,
    "--algo", ALGO,
    "--pool", POOL,
    "--user", f"{WALLET}.{WORKER}",
    "--pass", "x",
    "--ethstratum", "ETHV1",
    "--keepfree", "2",
    "--watchdog", "exit"
]

print(f"Command: {' '.join(cmd)}")
print()

try:
    subprocess.run(cmd, check=True)
except KeyboardInterrupt:
    print("\n⛔ Mining stopped by user")
except Exception as e:
    print(f"\n❌ Error: {e}")
