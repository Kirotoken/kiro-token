const hre = require("hardhat");

async function main() {
  console.log("🚀 Deploying Kiro Token...\n");
  
  const [deployer] = await hre.ethers.getSigners();
  console.log("Deploying with account:", deployer.address);
  
  const balance = await hre.ethers.provider.getBalance(deployer.address);
  console.log("Account balance:", hre.ethers.formatEther(balance), "ETH\n");
  
  // Deploy
  const KiroToken = await hre.ethers.getContractFactory("KiroToken");
  const kiro = await KiroToken.deploy();
  
  await kiro.waitForDeployment();
  
  const address = await kiro.getAddress();
  console.log("✅ Kiro Token deployed to:", address);
  
  // Get contract info
  const maxSupply = await kiro.MAX_SUPPLY();
  const walletCap = await kiro.WALLET_CAP();
  const baseMint = await kiro.BASE_MINT_AMOUNT();
  const difficulty = await kiro.POW_DIFFICULTY_BITS();
  
  console.log("\n📊 Contract Info:");
  console.log("  Name:", await kiro.name());
  console.log("  Symbol:", await kiro.symbol());
  console.log("  Max Supply:", hre.ethers.formatEther(maxSupply), "KIRO");
  console.log("  Wallet Cap:", hre.ethers.formatEther(walletCap), "KIRO");
  console.log("  Base Mint:", hre.ethers.formatEther(baseMint), "KIRO");
  console.log("  Initial Difficulty:", difficulty.toString(), "bits");
  
  console.log("\n⏳ Waiting for block confirmations...");
  await kiro.deploymentTransaction().wait(5);
  
  console.log("\n🔍 Verifying on Etherscan...");
  try {
    await hre.run("verify:verify", {
      address: address,
      constructorArguments: [],
    });
    console.log("✅ Contract verified!");
  } catch (error) {
    console.log("⚠️  Verification failed:", error.message);
    console.log("   You can verify manually later with:");
    console.log(`   npx hardhat verify --network ${hre.network.name} ${address}`);
  }
  
  console.log("\n" + "=".repeat(70));
  console.log("🎉 DEPLOYMENT COMPLETE!");
  console.log("=".repeat(70));
  console.log("\n📝 Save this info:");
  console.log(`CONTRACT_ADDRESS=${address}`);
  console.log(`NETWORK=${hre.network.name}`);
  console.log(`CHAIN_ID=${(await hre.ethers.provider.getNetwork()).chainId}`);
  console.log("\n🔗 Links:");
  
  if (hre.network.name === "sepolia") {
    console.log(`  Etherscan: https://sepolia.etherscan.io/address/${address}`);
    console.log(`  Faucet: https://sepoliafaucet.com/`);
  } else if (hre.network.name === "base") {
    console.log(`  BaseScan: https://basescan.org/address/${address}`);
  }
  
  console.log("\n📖 Next steps:");
  console.log("  1. Update miner/.env with CONTRACT_ADDRESS");
  console.log("  2. Update frontend/.env with CONTRACT_ADDRESS");
  console.log("  3. Run miner: cd miner && python3 kiro_gpu_miner.py");
  console.log("  4. Run frontend: cd frontend && npm start");
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
