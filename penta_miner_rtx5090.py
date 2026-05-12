#!/usr/bin/env python3
"""
PENTA Mining on GPUHub - RTX 5090 Optimized
PentaChain Ethash Mining with RTX 5090
"""

import os
import subprocess
import time
import sys

# Configuration
WALLET = "0x25769925ee761c708696c85980ac4da84eebfa33"
WORKER = "gpuhub-rtx5090"
POOL = "stratum+tcp://pool.pentamine.org:3030"
ALGO = "ETHASH"
LOLMINER_VERSION = "1.98a"

print("="*70)
print("⛏️  PENTA MINER - RTX 5090 MODE")
print("="*70)
print(f"💎 Wallet: {WALLET}")
print(f"🏷️  Worker: {WORKER}")
print(f"🌐 Pool: {POOL}")
print(f"⚙️  Algorithm: {ALGO}")
print(f"🎮 Target: RTX 5090 (32GB)")
print(f"📦 lolMiner: v{LOLMINER_VERSION}")
print("="*70)
print()

# Download lolMiner 1.98a
print(f"⬇️  Downloading lolMiner v{LOLMINER_VERSION}...")
LOLMINER_URL = f"https://github.com/Lolliedieb/lolMiner-releases/releases/download/{LOLMINER_VERSION}/lolMiner_v{LOLMINER_VERSION}_Lin64.tar.gz"

os.chdir("/root")

# Remove old version
if os.path.exists("1.88"):
    print("🗑️  Removing old lolMiner 1.88...")
    subprocess.run(["rm", "-rf", "1.88", "lolMiner_v1.88_Lin64.tar.gz"], 
                   check=False, stdout=subprocess.DEVNULL)

# Download new version
if not os.path.exists(f"/root/lolminer_{LOLMINER_VERSION}.tar.gz"):
    result = subprocess.run(["wget", "-q", "--show-progress", LOLMINER_URL, 
                           "-O", f"/root/lolminer_{LOLMINER_VERSION}.tar.gz"], check=False)
    if result.returncode != 0:
        print("❌ Download failed! Trying alternative method...")
        subprocess.run(["curl", "-L", "-o", f"/root/lolminer_{LOLMINER_VERSION}.tar.gz", 
                       LOLMINER_URL], check=True)

print("📦 Extracting lolMiner...")
subprocess.run(["tar", "-xzf", f"/root/lolminer_{LOLMINER_VERSION}.tar.gz"], 
               check=True, stdout=subprocess.DEVNULL)

# Find lolMiner binary
lolminer_path = f"/root/{LOLMINER_VERSION}/lolMiner"
if not os.path.exists(lolminer_path):
    print(f"❌ lolMiner not found at {lolminer_path}!")
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
    
    if "5090" not in result.stdout:
        print("⚠️  Warning: RTX 5090 not detected!")
        print("   Make sure you're on the correct instance")
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

# List devices first
print("📋 Checking lolMiner device compatibility...")
try:
    subprocess.run([lolminer_path, "--list-devices"], check=False)
except:
    pass

print()
print("="*70)
print("🚀 STARTING RTX 5090 MINING...")
print("="*70)
print()

# Mining command optimized for RTX 5090
cmd = [
    lolminer_path,
    "--algo", ALGO,
    "--pool", POOL,
    "--user", f"{WALLET}.{WORKER}",
    "--pass", "x",
    "--ethstratum", "ETHV1",
    "--devices", "0",              # Single RTX 5090
    "--keepfree", "8",             # Keep 8GB free (32GB total)
    "--watchdog", "exit",
    "--apiport", "0",              # Disable API
    "--shortstats", "60",          # Stats every 60s
    "--longstats", "300",          # Detailed stats every 5min
    "--digits", "3",               # 3 decimal places
    "--connectattempts", "3",      # Retry 3 times
    "--4g-alloc-size", "4080",     # Optimize for large DAG
]

print("📋 Command:")
print(f"   {' '.join(cmd)}")
print()
print("💡 Tips:")
print("   • Expected hashrate: 150-180 MH/s (RTX 5090)")
print("   • First shares may take 1-2 minutes")
print("   • Check stats: https://pool.pentamine.org")
print(f"   • Your wallet: {WALLET}")
print("   • Monitor GPU: watch -n 1 nvidia-smi")
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
    print("   1. Check GPU: nvidia-smi")
    print("   2. Verify pool: https://pool.pentamine.org")
    print("   3. Check lolMiner version supports RTX 5090")
    print("   4. Try updating to latest lolMiner")
except Exception as e:
    print("\n" + "="*70)
    print(f"❌ Unexpected error: {e}")
    print("="*70)
