# PENTA Mining - Dual GPU Setup (Kaggle)

## 🎯 Quick Start

Copy and paste this into a Kaggle notebook cell:

```python
# Download and run PENTA miner
!wget -q https://raw.githubusercontent.com/Kirotoken/kiro-token/main/penta_miner_dual_gpu.py -O penta_miner.py
!python3 penta_miner.py
```

## ⚙️ Kaggle Settings

**IMPORTANT:** Configure these settings before running:

1. **Accelerator:** GPU T4 x2 ⚡
2. **Internet:** ON 🌐
3. **Persistence:** Session only (12h limit)

### How to Set:

1. Click **Settings** (right sidebar)
2. Under **Accelerator** → Select **GPU T4 x2**
3. Under **Internet** → Toggle **ON**
4. Click **Save**

---

## 📊 Expected Performance

| GPU | Model | Hashrate | Total |
|-----|-------|----------|-------|
| GPU 0 | Tesla T4 | ~40 MH/s | |
| GPU 1 | Tesla T4 | ~40 MH/s | |
| **TOTAL** | **2x T4** | **~80 MH/s** | ⛏️ |

**Power Cost:** FREE (Kaggle provides)  
**Session Limit:** 12 hours  
**Weekly Quota:** 30 GPU hours

---

## 🔍 Monitor Your Mining

### 1. In Kaggle Output

Watch for:
```
✅ Found 2 GPU(s):
   • 0, Tesla T4, 15360 MiB
   • 1, Tesla T4, 15360 MiB

🚀 STARTING DUAL GPU MINING...

GPU 0: 39.8 MH/s
GPU 1: 40.1 MH/s
Total: 79.9 MH/s

Shares: 15 accepted, 0 rejected
```

### 2. On Pool Website

1. Go to: **https://pool.pentamine.org**
2. Enter wallet: `0xe81Cb1184A55fA17Db786C8761D955c5838B2675`
3. Click **"Check Miner Stats"**

You'll see:
- ✅ Current hashrate (~80 MH/s)
- ✅ Worker: `kaggle-dual-t4`
- ✅ Shares submitted
- ✅ Pending balance
- ✅ Payment history

---

## 🎮 Alternative: Manual Setup

If you want more control:

```python
# Cell 1: Install dependencies
!apt-get update -qq
!apt-get install -y -qq wget curl

# Cell 2: Download lolMiner
!wget -q https://github.com/Lolliedieb/lolMiner-releases/releases/download/1.88/lolMiner_v1.88_Lin64.tar.gz
!tar -xzf lolMiner_v1.88_Lin64.tar.gz

# Cell 3: Check GPUs
!nvidia-smi --query-gpu=index,name,memory.total --format=csv

# Cell 4: Start mining
!./1.88/lolMiner \
  --algo ETHASH \
  --pool stratum+tcp://pool.pentamine.org:3030 \
  --user 0xe81Cb1184A55fA17Db786C8761D955c5838B2675.kaggle-dual-t4 \
  --pass x \
  --ethstratum ETHV1 \
  --devices 0,1 \
  --keepfree 2 \
  --watchdog exit
```

---

## 🔧 Troubleshooting

### GPU Not Detected

**Problem:** Only 1 GPU or no GPU found

**Solution:**
1. Stop notebook
2. Settings → Accelerator → **GPU T4 x2**
3. Save and restart

### Connection Failed

**Problem:** Cannot connect to pool

**Solution:**
1. Check internet is ON in settings
2. Verify pool status: https://pool.pentamine.org
3. Try restarting notebook

### Low Hashrate

**Problem:** Getting <60 MH/s total

**Solution:**
1. Wait 2-3 minutes for warmup
2. Check GPU usage: `!nvidia-smi`
3. Verify both GPUs are active
4. Restart if one GPU is idle

### Session Timeout

**Problem:** Kaggle stops after 12 hours

**Solution:**
1. This is normal (Kaggle limit)
2. Restart notebook to continue
3. Your balance is saved on pool
4. Use multiple accounts for 24/7

---

## 💰 Earnings Calculator

**Assumptions:**
- Hashrate: 80 MH/s
- Uptime: 12h/day (1 Kaggle session)
- Pool fee: 1.5%
- Network difficulty: Variable

**Check real-time estimates:**
- Pool stats page
- Enter your wallet
- See "Estimated Earnings"

**Min payout:** 30 PENTA

---

## 🎯 Optimization Tips

### 1. Multiple Workers

Run on multiple Kaggle accounts:

```python
# Account 1
WORKER = "kaggle-dual-t4-1"

# Account 2  
WORKER = "kaggle-dual-t4-2"

# Account 3
WORKER = "kaggle-dual-t4-3"
```

All use same wallet → Combined hashrate!

### 2. Monitor Regularly

- Check pool stats every 2-3 hours
- Verify shares are accepted
- Restart if hashrate drops

### 3. Maximize Uptime

- Start new session immediately after timeout
- Use multiple accounts (rotate)
- Track weekly GPU quota (30h limit)

---

## 📱 Mobile Monitoring

**Pool Stats on Phone:**
1. Open: pool.pentamine.org
2. Bookmark the page
3. Enter wallet once
4. Refresh to check anytime

**Kaggle on Phone:**
1. Install Kaggle app
2. Check notebook status
3. Restart if needed

---

## ⚠️ Important Notes

### Kaggle Rules
- ✅ Mining is allowed (computational task)
- ✅ Free GPU quota provided
- ⚠️ Don't abuse (follow limits)
- ⚠️ 12h session, 30h/week quota

### Security
- ✅ Script only uses public address
- ✅ No private key needed
- ✅ Safe to share notebook
- ❌ Never share private key!

### Pool Rules
- Min payout: 30 PENTA
- Fee: 1.5%
- Payouts: Automatic
- PPLNS: Shares-based rewards

---

## 🚀 Ready to Mine!

**Steps:**
1. ✅ Open Kaggle notebook
2. ✅ Set GPU T4 x2 + Internet ON
3. ✅ Copy script from above
4. ✅ Run and monitor!

**Check stats:**
- Kaggle output (live hashrate)
- Pool website (balance & payouts)

**Good luck mining!** ⛏️💎

---

## 📞 Links

- **Pool:** https://pool.pentamine.org
- **RPC:** https://rpc.pentamine.org
- **GitHub:** https://github.com/Kirotoken/kiro-token
- **Wallet:** `0xe81Cb1184A55fA17Db786C8761D955c5838B2675`
