require("@nomicfoundation/hardhat-toolbox");
require("@nomicfoundation/hardhat-verify");
require("dotenv").config();

const PRIVATE_KEY = process.env.PRIVATE_KEY || "0x0000000000000000000000000000000000000000000000000000000000000000";
const ETHERSCAN_API_KEY = process.env.ETHERSCAN_API_KEY || "";

module.exports = {
  solidity: {
    version: "0.8.20",
    settings: {
      optimizer: {
        enabled: true,
        runs: 200
      }
    }
  },
  networks: {
    sepolia: {
      url: "https://ethereum-sepolia-rpc.publicnode.com",
      accounts: [PRIVATE_KEY],
      chainId: 11155111
    },
    base: {
      url: "https://mainnet.base.org",
      accounts: [PRIVATE_KEY],
      chainId: 8453
    },
    polygon: {
      url: "https://polygon-rpc.com",
      accounts: [PRIVATE_KEY],
      chainId: 137
    }
  },
  etherscan: {
    apiKey: {
      sepolia: ETHERSCAN_API_KEY,
      base: ETHERSCAN_API_KEY,
      polygon: ETHERSCAN_API_KEY
    }
  },
  sourcify: {
    enabled: true
  }
};
