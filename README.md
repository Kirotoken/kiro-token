# ⛏️ Kiro Token

**Proof-of-Work mineable ERC20 token with fair launch mechanism**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Solidity](https://img.shields.io/badge/Solidity-0.8.20-blue)](https://soliditylang.org/)

## 🎯 Features

- ✅ **Free Mint** - Only pay gas, no token cost
- ✅ **Proof-of-Work** - Mine tokens by solving keccak256 puzzles
- ✅ **Fair Launch** - No pre-mine, everyone starts equal
- ✅ **Dynamic Difficulty** - Adjusts as supply grows
- ✅ **Per-Wallet Cap** - Max 10,000 KIRO per wallet
- ✅ **Decay Rewards** - Rewards decrease over time
- ✅ **GPU Mining** - CUDA-accelerated miner included

## 📊 Token Economics

| Parameter | Value |
|-----------|-------|
| **Max Supply** | 21,000,000 KIRO |
| **Wallet Cap** | 10,000 KIRO |
| **Base Mint** | 1,000 KIRO |
| **Initial Difficulty** | 24-bit (6 hex zeros) |
| **Final Difficulty** | 40-bit (10 hex zeros) |
| **Decay Rate** | 1% per 1M minted |

## 🚀 Quick Start

### 1. Deploy Contract

```bash
# Install dependencies
npm install

# Copy and configure .env
cp .env.example .env
# Edit .env with your PRIVATE_KEY and ETHERSCAN_API_KEY

# Deploy to Sepolia testnet
npm run deploy:sepolia

# Or deploy to Base mainnet
npm run deploy:base
```

### 2. Mine Tokens

```bash
cd miner

# Install Python dependencies
pip install -r requirements.txt

# Configure miner
cp .env.example .env
# Edit .env with CONTRACT_ADDRESS and PRIVATE_KEY

# Run GPU miner
python3 kiro_gpu_miner.py
```

## 📖 Documentation

### Contract Address

**Sepolia Testnet:** `0x48D1B2aE9234345fD2e2a4b82Ccb3A922583A3C8`
**Etherscan:** https://sepolia.etherscan.io/address/0x48D1B2aE9234345fD2e2a4b82Ccb3A922583A3C8
**Base Mainnet:** (TBD)

### Difficulty Stages

| Stage | Supply Threshold | Hex Zeros | Bits | Avg Time (GPU) |
|-------|------------------|-----------|------|----------------|
| 0 | 0 - 5M | 6 | 24 | ~1 sec |
| 1 | 5M - 10M | 7 | 28 | ~5 sec |
| 2 | 10M - 15M | 8 | 32 | ~30 sec |
| 3 | 15M - 18M | 9 | 36 | ~5 min |
| 4 | 18M - 21M | 10 | 40 | ~1 hour |

### GPU Performance

| GPU | Hashrate | 24-bit | 32-bit |
|-----|----------|--------|--------|
| Tesla T4 | ~1.5 GH/s | <1s | ~30s |
| RTX 3090 | ~2.5 GH/s | <1s | ~15s |
| RTX 4090 | ~4.4 GH/s | <1s | ~5s |

## 🛠️ Development

### Project Structure

```
kiro-token/
├── contracts/          # Solidity smart contracts
│   └── KiroToken.sol
├── scripts/            # Deployment scripts
│   └── deploy.js
├── miner/              # GPU miner
│   ├── kiro_gpu_miner.py
│   └── requirements.txt
├── test/               # Contract tests
├── hardhat.config.js   # Hardhat configuration
└── package.json
```

### Testing

```bash
# Run tests
npm test

# Run with coverage
npm run coverage
```

### Deployment Networks

| Network | Chain ID | RPC |
|---------|----------|-----|
| Sepolia | 11155111 | https://ethereum-sepolia-rpc.publicnode.com |
| Base | 8453 | https://mainnet.base.org |
| Polygon | 137 | https://polygon-rpc.com |

## 🔒 Security

- ✅ OpenZeppelin contracts
- ✅ No admin functions
- ✅ Immutable supply cap
- ✅ Per-wallet limits
- ✅ Challenge-based PoW

## 📝 License

MIT License - see [LICENSE](LICENSE) file for details

## 🤝 Contributing

Contributions welcome! Please open an issue or PR.

## 🔗 Links

- **Contract:** (TBD after deployment)
- **Etherscan:** (TBD)
- **GitHub:** https://github.com/anansetiawan40-oss/kiro-token
- **Telegram:** (TBD)

## ⚠️ Disclaimer

This is experimental software. Use at your own risk. Always verify contract code before interacting.

## 🙏 Credits

- Inspired by PFFT (Pow Free Fair Token)
- Built with OpenZeppelin, Hardhat, and PyCUDA
- Created by [@anansetiawan40-oss](https://github.com/anansetiawan40-oss)

---

**Happy Mining! ⛏️**
