# 🔧 KAGGLE PERMISSION ERROR - COMPLETE FIX GUIDE

## ❌ ERROR: "Permission 'users.get' was denied"

Ini terjadi karena **Internet setting belum ON** di Kaggle!

---

## ✅ STEP-BY-STEP FIX:

### STEP 1: BUKA SETTINGS

**Di Mobile:**
1. Klik **hamburger menu (☰)** di kiri atas
2. Scroll ke bawah
3. Klik **"Settings"** atau **"Pengaturan"**

**Di Desktop:**
1. Klik **"Settings"** di sidebar kanan
2. Atau klik icon gear (⚙️)

---

### STEP 2: ENABLE INTERNET

**PENTING!** Ini yang paling sering dilupakan!

1. Di halaman Settings, scroll ke bawah
2. Cari section **"Internet"**
3. **Toggle ke ON** (warna biru/hijau)
4. Pastikan ada tulisan "Internet: ON"

**Tanpa ini, wget dan download tidak akan jalan!**

---

### STEP 3: SET GPU

Masih di Settings:

1. Cari section **"Accelerator"**
2. Klik dropdown
3. Pilih **"GPU T4 x2"**
4. Jangan pilih "None" atau "TPU"

---

### STEP 4: SAVE SETTINGS

1. Scroll ke bawah
2. Klik tombol **"Save"** atau **"Simpan"**
3. Tunggu konfirmasi (biasanya ada notif hijau)

---

### STEP 5: RESTART SESSION

**Penting untuk apply settings!**

1. Klik icon **"Session Options"** di kanan atas (3 titik vertikal)
2. Pilih **"Restart Session"**
3. Tunggu notebook restart (~10-30 detik)
4. Halaman akan reload otomatis

---

### STEP 6: RUN MINING SCRIPT

**Method 1: One-Line Command (Recommended)**

Paste ini di cell baru:

```python
!wget -q https://raw.githubusercontent.com/Kirotoken/kiro-token/main/penta_miner_dual_gpu.py && python3 penta_miner_dual_gpu.py
```

Klik **Run** (▶️) atau tekan **Shift+Enter**

---

**Method 2: Manual Copy-Paste (Kalau wget gagal)**

1. Buka: https://github.com/Kirotoken/kiro-token/blob/main/penta_miner_dual_gpu.py
2. Klik tombol **"Raw"** (kanan atas)
3. **Select All** (Ctrl+A atau Cmd+A)
4. **Copy** (Ctrl+C atau Cmd+C)
5. Balik ke Kaggle
6. Paste di cell (Ctrl+V atau Cmd+V)
7. Klik **Run**

---

## ✅ EXPECTED OUTPUT:

Kalau berhasil, kamu akan lihat:

```
⛏️  PENTA MINER - DUAL GPU MODE
======================================================================
💎 Wallet: 0xe81Cb1184A55fA17Db786C8761D955c5838B2675
🏷️  Worker: kaggle-dual-t4
🌐 Pool: stratum+tcp://pool.pentamine.org:3030
⚙️  Algorithm: ETHASH
🎮 Target: 2x Tesla T4 GPUs
======================================================================

📦 Installing dependencies...
✅ Dependencies installed!

⬇️  Downloading lolMiner v1.88...
📦 Extracting lolMiner...
✅ lolMiner ready!

🎮 Detecting GPUs...
✅ Found 2 GPU(s):
   • 0, Tesla T4, 15360 MiB
   • 1, Tesla T4, 15360 MiB

🌐 Testing pool connectivity...
✅ Pool is reachable!

======================================================================
🚀 STARTING DUAL GPU MINING...
======================================================================

GPU 0: 39.8 MH/s
GPU 1: 40.1 MH/s
Total: 79.9 MH/s ⛏️

Shares: 15 accepted, 0 rejected ✅
```

---

## 🔍 TROUBLESHOOTING:

### ❌ "Permission denied" (masih muncul)

**Solusi:**
- Internet belum ON → Cek Settings lagi
- Restart session belum dilakukan → Restart dulu
- Browser cache → Clear cache atau pakai Incognito

---

### ❌ "wget: command not found"

**Solusi:**
- Gunakan Method 2 (manual copy-paste)
- Atau install wget dulu:
  ```python
  !apt-get update -qq && apt-get install -y wget
  ```

---

### ❌ "No GPU detected"

**Solusi:**
- Accelerator belum di-set → Set ke GPU T4 x2
- Quota habis → Cek usage di Settings
- Restart session → Kadang GPU perlu restart

---

### ❌ "Connection failed" atau "Pool unreachable"

**Solusi:**
- Internet belum ON → Enable di Settings
- Pool down → Cek https://pool.pentamine.org
- Firewall → Coba restart session

---

### ❌ "Low hashrate" (<60 MH/s)

**Solusi:**
- Tunggu 2-3 menit (warmup period)
- Check GPU usage: `!nvidia-smi`
- Restart jika salah satu GPU idle

---

## 📱 MOBILE TIPS:

**Kalau pakai HP:**

1. **Rotate ke landscape** (horizontal) untuk UI lebih luas
2. **Zoom out** kalau tombol terpotong
3. **Refresh page** kalau UI stuck
4. **Use Chrome/Firefox** (bukan browser bawaan)

---

## 💡 PRO TIPS:

### 1. **Bookmark Settings Page**
Supaya gampang akses next time

### 2. **Save Notebook**
Klik "Save Version" setelah setup

### 3. **Monitor via Pool**
Buka pool.pentamine.org di tab lain

### 4. **Set Reminder**
12 jam kemudian untuk restart session

---

## 🎯 CHECKLIST:

Sebelum run, pastikan:

- [ ] Internet: **ON** ✅
- [ ] Accelerator: **GPU T4 x2** ✅
- [ ] Settings: **Saved** ✅
- [ ] Session: **Restarted** ✅
- [ ] Script: **Ready to run** ✅

---

## 📊 MONITOR MINING:

**Pool Stats:**
- URL: https://pool.pentamine.org
- Wallet: `0xe81Cb1184A55fA17Db786C8761D955c5838B2675`
- Worker: `kaggle-dual-t4`

**Expected:**
- Hashrate: ~80 MH/s
- Shares: Accepted (green)
- Balance: Accumulating

---

## 🆘 STILL STUCK?

**Try these:**

1. **Clear browser cache**
2. **Use Incognito/Private mode**
3. **Try different browser** (Chrome → Firefox)
4. **Restart phone/computer**
5. **Create new notebook** (fresh start)

---

**Good luck mining!** ⛏️💎

Kalau masih error, screenshot dan kirim ke saya!
