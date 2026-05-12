#!/usr/bin/env python3
"""
PENTA Mining on Kaggle - Dual GPU Optimized
PentaChain Ethash Mining with 2x Tesla T4
"""

import os
import subprocess
import time
import sys

# Configuration
WALLET = "0xe81Cb1184A55fA17Db786C8761D955c5838B2675"
WORKER = "kaggle-dual-t4"
POOL = "stratum+tcp://pool.pentamine.org:3030"
ALGO = "ETHASH"

print("="*70)
print("⛏️  PENTA MINER - DUAL GPU MODE")
print("="*70)
print(f"💎 Wallet: {WALLET}")
print(f"🏷️  Worker: {WORKER}")
print(f"🌐 Pool: {POOL}")
print(f"⚙️  Algorithm: {ALGO}")
print(f"🎮 Target: 2x Tesla T4 GPUs")
print("="*70)
print()

# Install dependencies
print("📦 Installing dependencies...")
subprocess.run(["apt-get", "update", "-qq"], check=False, 
               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
subprocess.run(["apt-get", "install", "-y", "-qq", "wget", "curl", "screen"], 
               check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
print("✅ Dependencies installed!")

# Download lolMiner
print("⬇️  Downloading lolMiner v1.88...")
LOLMINER_URL = "https://github.com/Lolliedieb/lolMiner-releases/releases/download/1.88/lolMiner_v1.88_Lin64.tar.gz"

if not os.path.exists("/tmp/lolminer.tar.gz"):
    result = subprocess.run(["wget", "-q", "--show-progress", LOLMINER_URL, 
                           "-O", "/tmp/lolminer.tar.gz"], check=False)
    if result.returncode != 0:
        print("❌ Download failed! Trying alternative method...")
        subprocess.run(["curl", "-L", "-o", "/tmp/lolminer.tar.gz", LOLMINER_URL], check=True)

print("📦 Extracting lolMiner...")
subprocess.run(["tar", "-xzf", "/tmp/lolminer.tar.gz", "-C", "/tmp/"], 
               check=True, stdout=subprocess.DEVNULL)

# Find lolMiner binary
lolminer_path = "/tmp/1.88/lolMiner"
if not os.path.exists(lolminer_path):
    print("❌ lolMiner not found!")
    sys.exit(1)

# Make executable
subprocess.run(["chmod", "+x", lolminer_path], check=True)
print("✅ lolMiner ready!")
print()

# Check GPUs
print("🎮 Detecting GPUs...")
try:
    result = subprocess.run(["nvidia-smi", "--query-gpu=index,name,memory.total", 
                           "--format=csv,noheader"], 
                          capture_output=True, text=True, check=True)
    gpus = result.stdout.strip().split('\n')
    print(f"✅ Found {len(gpus)} GPU(s):")
    for gpu in gpus:
        print(f"   • {gpu}")
    
    if len(gpus) < 2:
        print("⚠️  Warning: Less than 2 GPUs detected!")
        print("   Make sure Kaggle accelerator is set to 'GPU T4 x2'")
except Exception as e:
    print(f"❌ GPU detection failed: {e}")
    print("⚠️  Continuing anyway...")

print()

# Check pool connectivity
print("🌐 Testing pool connectivity...")
try:
    result = subprocess.run(["ping", "-c", "2", "pool.pentamine.org"], 
                          capture_output=True, text=True, timeout=10)
    if result.returncode == 0:
        print("✅ Pool is reachable!")
    else:
        print("⚠️  Pool ping failed, but will try to connect anyway...")
except:
    print("⚠️  Could not test connectivity, proceeding...")

print()
print("="*70)
print("🚀 STARTING DUAL GPU MINING...")
print("="*70)
print()

# Mining command optimized for 2 GPUs
cmd = [
    lolminer_path,
    "--algo", ALGO,
    "--pool", POOL,
    "--user", f"{WALLET}.{WORKER}",
    "--pass", "x",
    "--ethstratum", "ETHV1",
    "--devices", "0,1",           # Use both GPUs
    "--keepfree", "2",            # Keep 2GB free per GPU
    "--watchdog", "exit",
    "--apiport", "0",             # Disable API (not needed)
    "--shortstats", "60",         # Stats every 60s
    "--longstats", "300",         # Detailed stats every 5min
    "--digits", "3",              # 3 decimal places
    "--connectattempts", "3",     # Retry 3 times
]

print("📋 Command:")
print(f"   {' '.join(cmd)}")
print()
print("💡 Tips:")
print("   • First shares may take 1-2 minutes")
print("   • Check stats: https://pool.pentamine.org")
print("   • Enter your wallet to see hashrate")
print("   • Kaggle session limit: 12 hours")
print()
print("="*70)
print("⛏️  MINING IN PROGRESS...")
print("="*70)
print()

# Start mining
try:
    subprocess.run(cmd, check=True)
except KeyboardInterrupt:
    print("\n" + "="*70)
    print("⛔ Mining stopped by user")
    print("="*70)
except subprocess.CalledProcessError as e:
    print("\n" + "="*70)
    print(f"❌ Mining error: {e}")
    print("="*70)
    print("\n💡 Troubleshooting:")
    print("   1. Check GPU availability: !nvidia-smi")
    print("   2. Verify pool status: https://pool.pentamine.org")
    print("   3. Check Kaggle internet is enabled")
    print("   4. Try restarting the notebook")
except Exception as e:
    print("\n" + "="*70)
    print(f"❌ Unexpected error: {e}")
    print("="*70)
