# ⛏️ PENTA MINING GUIDE

Complete guide untuk mining PENTA di PentaChain menggunakan Kaggle GPU.

---

## 📊 MINING INFO

**Network:** PentaChain  
**Algorithm:** Ethash  
**Pool:** pool.pentamine.org  
**Port PPLNS:** 3030 (recommended)  
**Port SOLO:** 3031 (high risk)  
**Pool Fee:** 1.5%  
**Min Payout:** 30 PENTA  

**Your Wallet:** `0xe81Cb1184A55fA17Db786C8761D955c5838B2675`  
**Worker Name:** `kaggle-t4`

---

## 🎯 QUICK START (KAGGLE)

### 1. Create Kaggle Notebook

1. Go to: https://www.kaggle.com/code
2. Click "New Notebook"
3. Settings → Accelerator → **GPU T4 x2**
4. Settings → Internet → **ON**

### 2. Copy Mining Script

Paste this into Kaggle cell:

```python
!wget -q https://raw.githubusercontent.com/Kirotoken/kiro-token/main/penta_miner_kaggle.py -O penta_miner.py
!python3 penta_miner.py
```

**OR** copy full script from `/home/ubuntu/penta_miner_kaggle.py`

### 3. Run & Monitor

- Click "Run All"
- Wait for lolMiner to download & start
- Monitor hashrate in output
- Check stats: https://pool.pentamine.org

---

## 📡 NETWORK DETAILS

Add PentaChain to MetaMask/wallet:

```
Network Name: PentaChain
Chain ID: 7777
RPC URL: https://rpc.pentamine.org
Currency Symbol: PENTA
Block Explorer: (check pool.pentamine.org)
```

---

## 💰 EXPECTED EARNINGS

**Kaggle Tesla T4 x2:**
- Hashrate: ~60-80 MH/s (estimated)
- Power: FREE (Kaggle provides)
- Runtime: 12 hours per session
- Earnings: Depends on network difficulty

**Check your stats:**
1. Go to: https://pool.pentamine.org
2. Enter wallet: `0xe81Cb1184A55fA17Db786C8761D955c5838B2675`
3. Click "Check Miner Stats"

---

## 🔧 TROUBLESHOOTING

### GPU Not Detected
- Make sure Kaggle accelerator is set to "GPU T4 x2"
- Restart notebook if needed

### Connection Failed
- Check pool status: https://pool.pentamine.org
- Verify RPC is online: https://rpc.pentamine.org

### Low Hashrate
- Normal for first few minutes (warmup)
- Check GPU utilization with `!nvidia-smi`

### Session Timeout
- Kaggle limits: 12 hours per session
- Restart notebook to continue mining

---

## 📊 MONITORING

### Pool Stats
https://pool.pentamine.org

Enter your wallet to see:
- ✅ Current hashrate
- ✅ Active workers
- ✅ Shares submitted
- ✅ Pending balance
- ✅ Payment history

### Kaggle Output
Monitor in notebook:
```
[INFO] GPU detected: Tesla T4
[INFO] Hashrate: 45.2 MH/s
[INFO] Shares: 12 accepted, 0 rejected
[INFO] Pool: Connected
```

---

## 🎯 OPTIMIZATION TIPS

### 1. Use PPLNS (Not SOLO)
- Port 3030 for PPLNS
- More consistent payouts
- Lower variance

### 2. Multiple Workers
Run on multiple Kaggle accounts:
- Worker names: `kaggle-t4-1`, `kaggle-t4-2`, etc.
- Same wallet address
- Combine hashrate

### 3. Monitor Regularly
- Check pool stats every few hours
- Restart if hashrate drops
- Verify shares are accepted

---

## 💡 FUTURE: ETC MINING

PentaPool is preparing ETC (Ethereum Classic) mining:

**Coming Soon:**
- ETC PPLNS pool
- Manual split mining (PENTA + ETC)
- Dual mining support

**When available:**
- Same lolMiner setup
- Different pool/port
- Split hashrate between PENTA & ETC

---

## ⚠️ IMPORTANT NOTES

### Security
- ✅ Never share private key
- ✅ Only share wallet address (public)
- ✅ Use different wallet for testing

### Kaggle Limits
- ⏱️ 12 hours per session
- 🔄 30 hours per week GPU quota
- 📊 Monitor usage in Kaggle settings

### Pool Rules
- Min payout: 30 PENTA
- Fee: 1.5%
- Payouts: Automatic when threshold reached

---

## 📞 SUPPORT

**Pool:** https://pool.pentamine.org  
**RPC:** https://rpc.pentamine.org  
**Wallet:** `0xe81Cb1184A55fA17Db786C8761D955c5838B2675`

---

## 🚀 START MINING NOW!

1. Open Kaggle notebook
2. Copy script from `/home/ubuntu/penta_miner_kaggle.py`
3. Run and monitor
4. Check stats on pool.pentamine.org

**Good luck mining!** ⛏️💎
