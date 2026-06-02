# 🦾 Inverse Kinematics Planar Robot 3-DOF
### Pendekatan Machine Learning & Deep Learning

> **Nama:** Sistra Amanda Sinaga  
> **NIM:** 42223O1O11  
> **Mata Kuliah:** Praktikum Kinematika dan Kontrol Robot — IK ML / DL

---

## 📌 Deskripsi Proyek

Repositori ini berisi implementasi penyelesaian masalah **Inverse Kinematics (IK)** pada robot planar 3-DOF (*Degree of Freedom*) menggunakan pendekatan **Machine Learning (Supervised)** dan **Deep Learning (PyTorch MLP)**. Proyek ini dikembangkan untuk memenuhi tugas praktikum dengan pembaruan dimensi robot dan optimasi metode prediksi sudut sendi.

### Apa itu Inverse Kinematics?

| | Forward Kinematics (FK) | Inverse Kinematics (IK) |
|---|---|---|
| **Input** | Sudut sendi `[θ1, θ2, θ3]` | Posisi target `(x, y)` |
| **Output** | Posisi end-effector `(x, y)` | Sudut sendi `[θ1, θ2, θ3]` |
| **Sifat** | Mudah ✅, solusi unik | Sulit ⚠️, solusi bisa banyak |

### Persamaan Forward Kinematics:
```
x = L1·cos(θ1) + L2·cos(θ1+θ2) + L3·cos(θ1+θ2+θ3)
y = L1·sin(θ1) + L2·sin(θ1+θ2) + L3·sin(θ1+θ2+θ3)
```

---

## 🤖 Spesifikasi Robot

```
Base (0,0) ──── Link 1 ──── Link 2 ──── Link 3 ──── End-Effector
               L1 = 0.5m   L2 = 0.4m   L3 = 0.3m
```

| Parameter | Nilai |
|-----------|-------|
| Panjang Link 1 (`L1`) | `0.5 m` |
| Panjang Link 2 (`L2`) | `0.4 m` |
| Panjang Link 3 (`L3`) | `0.3 m` |
| Jumlah DOF | `3` |
| Batas Sudut per Sendi | `±π rad` |
| Jangkauan Maksimum (`MAX_REACH`) | `1.2 m` |

---

## 🛠 Instalasi & Dependensi

```bash
pip install gymnasium stable-baselines3 scikit-learn torch matplotlib numpy tqdm pandas
```

| Library | Fungsi |
|---------|--------|
| `numpy` | Komputasi numerik & operasi matriks |
| `matplotlib` | Visualisasi dan animasi robot |
| `scikit-learn` | Model ML (Extra Trees, Ridge, MLP) |
| `torch` (PyTorch) | Deep Learning — IKNet |
| `gymnasium` | Environment untuk RL (PPO) |
| `stable-baselines3` | Algoritma RL |

---

## 🗺️ Workspace & Geometri Robot

Setelah dimensi link diperbarui, ruang kerja robot melebar menjadi radius lingkaran maksimal **1.2 meter**. Fungsi keselamatan dinamis disematkan untuk membedakan area reachable dan unreachable sebelum prediksi dilakukan.

<p align="center">
  <img src="image/Workspace Robot Planar 3-DOF.png" width="31%" alt="Workspace Robot">
  <img src="image/Fungsi Reachability Check.png" width="31%" alt="Reachability Check">
  <img src="image/Demo Visualisasi Robot.png" width="31%" alt="Demo Visualisasi Robot">
</p>
<p align="center"><em>Gambar 1: Analisis Geometri Robot — (Kiri) Workspace 18.000 titik FK sampling, (Tengah) Validasi Reachability Check, (Kanan) Tiga Konfigurasi Postur Lengan Robot</em></p>

---

## 📊 Dataset

Dataset dibuat menggunakan **FK Sampling** — menghasilkan pasangan `(θ, end-effector)` secara acak:

```python
N = 18.000 sampel
theta  ~ Uniform(-π, π)    # Random sampling sudut sendi
ee_pos = FK(theta)          # Hitung posisi via Forward Kinematics
```

| Properti | Nilai |
|----------|-------|
| Total sampel | 18.000 |
| Input model (`X`) | Posisi end-effector `(x, y)` |
| Output model (`y`) | Sudut sendi `(θ1, θ2, θ3)` |
| Split Train / Test | 80% / 20% → 14.400 / 3.600 |
| Preprocessing | `StandardScaler` (normalisasi input) |

---

## 🤖 Metode yang Digunakan

### 1. Machine Learning (Supervised)

Tiga metode ML dilatih dan dibandingkan menggunakan data yang sama:

| No | Metode | Cara Kerja Singkat |
|----|--------|--------------------|
| 1 | **Extra Trees** | Ensemble pohon keputusan acak, split dipilih secara random — lebih cepat & robust dari RF |
| 2 | **Ridge Regression** | Regresi linear + regularisasi L2 — baseline paling cepat, interpretable |
| 3 | **MLP Regressor (sklearn)** | Neural network ringan bawaan sklearn — tanpa GPU, cocok pembanding DL |

```python
# Extra Trees
ExtraTreesRegressor(n_estimators=150, max_features='sqrt', n_jobs=-1)

# Ridge Regression
MultiOutputRegressor(Ridge(alpha=1.0), n_jobs=-1)

# MLP Regressor
MLPRegressor(hidden_layer_sizes=(256,256), activation='relu', solver='adam',
             max_iter=300, early_stopping=True)
```

---

### 2. Deep Learning — IKNet (PyTorch)

Model kustom yang dioptimasi langsung di **ruang end-effector (Cartesian)**. Loss dihitung sebagai jarak antara posisi prediksi dan target, bukan di ruang sudut.

#### Arsitektur IKNet

```
Input (2,) ── x, y posisi target

Linear(2→256) + BatchNorm1d + ReLU
Linear(256→512) + BatchNorm1d + ReLU + Dropout(0.1)
Linear(512→512) + BatchNorm1d + ReLU + Dropout(0.1)
Linear(512→256) + BatchNorm1d + ReLU
Linear(256→3)

Output: tanh(out) × π  →  θ ∈ [-π, π]
```

| Konfigurasi | Nilai |
|-------------|-------|
| Optimizer | Adam (`lr=1e-3`, `weight_decay=1e-5`) |
| Scheduler | CosineAnnealingLR (`T_max=100`) |
| Loss Function | MSELoss di ruang **Cartesian** (bukan sudut) |
| Epochs | 100 |
| Batch Size | 512 |

> **Kenapa loss di ruang Cartesian?**  
> IK bersifat redundant — banyak kombinasi sudut yang valid untuk satu posisi target. Loss di ruang sudut membingungkan model. Loss di Cartesian memastikan model dievaluasi berdasarkan **akurasi fisis** seberapa dekat robot ke target.

#### Kurva Training

<p align="center">
  <img src="image/Training Curve — Deep Learning (IKNet).png" width="70%" alt="Training Curve IKNet">
</p>
<p align="center"><em>Gambar 2: Kurva Penurunan MSE Loss — Train vs Validation selama 100 epoch (skala log)</em></p>

---

## 📈 Hasil Evaluasi & Perbandingan

### Error Distribusi — Metode ML

<p align="center">
  <img src="image/Perbandingan Error End-Effector — Metode ML Baru.png" width="90%" alt="Error ML">
</p>
<p align="center"><em>Gambar 3: Distribusi Error End-Effector per Metode ML — Histogram Frekuensi dengan Garis Mean (merah)</em></p>

### Perbandingan Akurasi Semua Metode

<p align="center">
  <img src="image/Perbandingan Akurasi IK Baru — ML vs DL.png" width="65%" alt="Bar Chart Perbandingan">
</p>
<p align="center"><em>Gambar 4: Bar Chart Perbandingan Mean Error End-Effector (cm) — ML vs Deep Learning</em></p>

### Distribusi Error — Semua Metode

<p align="center">
  <img src="image/Analisis Distribusi Error End-Effector — Semua Metode Baru.png" width="85%" alt="Histogram Semua Metode">
</p>
<p align="center"><em>Gambar 5: Analisis Distribusi Error End-Effector — Perbandingan Lengkap Semua Metode (Extra Trees, Ridge, MLP, IKNet DL)</em></p>

---

## 🏆 Ringkasan Hasil

| Metode | Kategori | Butuh Dataset | Kelebihan Utama |
|--------|----------|---------------|-----------------|
| **Extra Trees** | ML | ✅ Ya | Robust, ensemble, cepat training |
| **Ridge Regression** | ML | ✅ Ya | Training tercepat, interpretable |
| **MLP Regressor** | ML | ✅ Ya | Neural network tanpa GPU |
| **IKNet (PyTorch DL)** | DL | ✅ Ya | Akurasi fisis tertinggi |
| **PPO (RL)** | RL | ❌ Tidak | Adaptif, tanpa dataset |

### Rekomendasi Pemilihan Metode

| Kondisi | Rekomendasi |
|---------|-------------|
| Training paling cepat, data besar | **Ridge Regression** |
| Akurasi ML terbaik, robust | **Extra Trees** |
| Neural network tanpa GPU | **MLP Regressor (sklearn)** |
| Akurasi fisis tertinggi | **Deep Learning (IKNet PyTorch)** |
| Tidak ada dataset, perlu hindari rintangan | **RL (PPO)** |
| Real-time pada hardware rendah | **Extra Trees / Ridge** |

---

## 💬 Diskusi

**1. Mengapa Deep Learning lebih akurat dari ML tradisional?**  
DL secara otomatis mempelajari representasi fitur berlapis. Hubungan IK melibatkan fungsi trigonometri non-linear (sin/cos) yang sulit ditangkap KNN atau Ridge. IKNet juga dioptimasi langsung di ruang Cartesian (physical loss).

**2. Mengapa waktu training RL meningkat saat workspace diperbesar?**  
RL belajar melalui eksplorasi. Workspace lebih besar = state space lebih besar, reward lebih jarang (*sparse reward*), sehingga konvergensi lebih lama.

**3. Apa kelemahan Supervised Learning untuk konfigurasi baru?**  
Model bersifat statis setelah training. Kondisi *Out-of-Distribution (OOD)* — seperti panjang link berubah — menyebabkan prediksi tidak akurat. Diperlukan retraining dengan data baru.

**4. Mengapa SVR bisa lebih baik dari Random Forest di workspace besar?**  
SVR dengan kernel RBF mampu generalisasi lebih baik ke area yang jarang tercakup data training (ekstrapolasi). Random Forest kuat untuk interpolasi tetapi kurang untuk ekstrapolasi.

---

## ▶️ Cara Menjalankan

```bash
# Install semua dependensi
pip install gymnasium stable-baselines3 scikit-learn torch matplotlib numpy tqdm pandas

# Jalankan notebook
jupyter notebook Assignment_IK_ML__DL__RL.ipynb
```

**Urutan eksekusi sel yang benar:**
1. Install & Import Library
2. Konfigurasi Robot (L1, L2, L3)
3. Generate Dataset (FK Sampling — 18.000 sampel)
4. Split Train/Test (80/20)
5. Training ML (Extra Trees → Ridge → MLP)
6. Training DL (IKNet PyTorch — 100 epoch)
7. Evaluasi & Perbandingan Semua Metode
8. Visualisasi & Animasi Robot

> ⚠️ Jalankan sel secara berurutan. Sel perbandingan bergantung pada variabel dari sel sebelumnya (`ml_results`, `dl_err`).

---

## 📁 Struktur Repositori

```
📦 Assignment_IK_ML__DL__RL
 ┣ 📓 Assignment_IK_ML__DL__RL.ipynb   ← Notebook utama
 ┣ 📂 image/
 ┃ ┣ 🖼️ Workspace Robot Planar 3-DOF.png
 ┃ ┣ 🖼️ Fungsi Reachability Check.png
 ┃ ┣ 🖼️ Demo Visualisasi Robot.png
 ┃ ┣ 🖼️ Training Curve — Deep Learning (IKNet).png
 ┃ ┣ 🖼️ Perbandingan Error End-Effector — Metode ML Baru.png
 ┃ ┣ 🖼️ Perbandingan Akurasi IK Baru — ML vs DL.png
 ┃ ┗ 🖼️ Analisis Distribusi Error End-Effector — Semua Metode Baru.png
 ┗ 📄 README.md
```

---

*Dibuat untuk Tugas Praktikum Inverse Kinematics — Pendekatan ML & DL pada Robot Planar 3-DOF*  
*Nama: Sistra Amanda Sinaga | NIM: 42223O1O11*
