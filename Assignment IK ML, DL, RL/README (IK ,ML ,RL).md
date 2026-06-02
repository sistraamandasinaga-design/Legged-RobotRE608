# 🦾 Inverse Kinematics Robot Planar 3-DOF
### Pendekatan Machine Learning & Deep Learning

> **Nama:** Sistra Amanda Sinaga  
> **NIM:** 42223O1O11  
> **Mata Kuliah:** Praktikum Inverse Kinematics (IK) — ML / DL / RL

---

## 📋 Daftar Isi

- [Deskripsi Proyek](#-deskripsi-proyek)
- [Struktur Robot](#-struktur-robot)
- [Forward & Inverse Kinematics](#-forward--inverse-kinematics)
- [Instalasi & Dependensi](#-instalasi--dependensi)
- [Dataset](#-dataset)
- [Metode yang Digunakan](#-metode-yang-digunakan)
  - [Machine Learning](#1-machine-learning-ml)
  - [Deep Learning](#2-deep-learning-dl)
- [Arsitektur Model](#-arsitektur-model-iknet-pytorch)
- [Hasil & Perbandingan](#-hasil--perbandingan)
- [Visualisasi](#-visualisasi)
- [Diskusi & Analisis](#-diskusi--analisis)
- [Kesimpulan](#-kesimpulan)
- [Cara Menjalankan](#-cara-menjalankan)

---

## 📌 Deskripsi Proyek

Proyek ini mengimplementasikan solusi **Inverse Kinematics (IK)** untuk robot planar 3-DOF (3 Degrees of Freedom) menggunakan pendekatan berbasis kecerdasan buatan:

| Kategori | Metode |
|----------|--------|
| **Machine Learning** | Extra Trees, Ridge Regression, MLP Regressor (sklearn) |
| **Deep Learning** | IKNet — Neural Network kustom berbasis PyTorch |

Tujuan utama: diberikan posisi target `(x, y)` pada bidang 2D, model harus memprediksi sudut sendi `(θ1, θ2, θ3)` yang membuat end-effector robot mencapai target tersebut.

---

## 🤖 Struktur Robot

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
| Batas Sudut | `±π rad` per sendi |
| Jangkauan Maksimum (`MAX_REACH`) | `1.2 m` |
| Jangkauan Minimum | `0.0 m` |

---

## 📐 Forward & Inverse Kinematics

### Forward Kinematics (FK)
> **Input:** Sudut sendi `[θ1, θ2, θ3]` → **Output:** Posisi end-effector `(x, y)`

```
x = L1·cos(θ1) + L2·cos(θ1+θ2) + L3·cos(θ1+θ2+θ3)
y = L1·sin(θ1) + L2·sin(θ1+θ2) + L3·sin(θ1+θ2+θ3)
```

**Sifat:** Solusi unik, mudah dihitung secara analitik ✅

### Inverse Kinematics (IK)
> **Input:** Posisi target `(x, y)` → **Output:** Sudut sendi `[θ1, θ2, θ3]`

**Sifat:** Solusi bisa banyak (redundant), bisa tidak ada (unreachable) ⚠️

```
Perbandingan FK vs IK:

  FK:  θ → x,y   [Mudah, unik]
  IK:  x,y → θ   [Sulit, multiple solutions]
```

---

## 🛠 Instalasi & Dependensi

```bash
pip install gymnasium stable-baselines3 scikit-learn torch matplotlib numpy tqdm
```

| Library | Versi | Fungsi |
|---------|-------|--------|
| `numpy` | ≥1.24 | Komputasi numerik, operasi matriks |
| `matplotlib` | ≥3.7 | Visualisasi, animasi robot |
| `scikit-learn` | ≥1.3 | Model ML (Extra Trees, Ridge, MLP) |
| `torch` (PyTorch) | ≥2.0 | Deep Learning (IKNet) |
| `gymnasium` | ≥0.29 | Environment untuk RL |
| `stable-baselines3` | ≥2.0 | Algoritma RL (PPO) |
| `pandas` | ≥2.0 | Tabel perbandingan hasil |
| `tqdm` | ≥4.0 | Progress bar training |

---

## 📊 Dataset

### Cara Pembuatan (FK Sampling)

Dataset dibuat menggunakan **Forward Kinematics Sampling** — menghasilkan pasangan `(θ, end-effector)` secara acak:

```python
N = 18.000 sampel
theta ~ Uniform(-π, π)   # Sampling sudut acak
ee_pos = FK(theta)       # Hitung posisi via FK
```

| Properti | Nilai |
|----------|-------|
| Total sampel | 18.000 |
| Input (`X`) | Posisi end-effector `(x, y)` |
| Output (`y`) | Sudut sendi `(θ1, θ2, θ3)` |
| Split Train/Test | 80% / 20% = 14.400 / 3.600 |
| Random Seed | 42 |

### Validasi Reachability

Sebelum training, setiap sampel diverifikasi agar berada dalam workspace robot:

```
min_reach (0.0 m) ≤ dist(target) ≤ MAX_REACH (1.2 m)
```

Karena data dihasilkan dari FK sampling, **semua 18.000 sampel otomatis reachable**.

---

## 🤖 Metode yang Digunakan

### 1. Machine Learning (ML)

Semua model ML menggunakan **StandardScaler** untuk normalisasi input sebelum training.

---

#### 🌳 Metode 1: Extra Trees Regressor

```python
ExtraTreesRegressor(
    n_estimators = 150,
    max_features = 'sqrt',
    random_state = 42,
    n_jobs       = -1
)
```

| Aspek | Detail |
|-------|--------|
| **Cara Kerja** | Ensemble pohon keputusan dengan split acak penuh (lebih random dari Random Forest) |
| **Kelebihan** | Cepat saat training, robust terhadap noise, generalisasi baik |
| **Kekurangan** | Tidak dapat ekstrapolasi ke luar rentang data |
| **Regularisasi** | Implicit melalui randomisasi |
| **Output** | MultiOutput langsung (3 sudut sendi) |

---

#### 📐 Metode 2: Ridge Regression

```python
MultiOutputRegressor(
    Ridge(alpha=1.0),
    n_jobs=-1
)
```

| Aspek | Detail |
|-------|--------|
| **Cara Kerja** | Regresi linear dengan penalti L2 pada koefisien (`‖w‖²`) |
| **Kelebihan** | Sangat cepat training, interpretable, baseline yang kuat |
| **Kekurangan** | Tidak mampu menangkap hubungan non-linear (sin/cos) yang kompleks |
| **Regularisasi** | L2 Regularization (`alpha=1.0`) |
| **Output** | MultiOutputRegressor (3 model terpisah) |

---

#### 🧩 Metode 3: MLP Regressor (Scikit-learn)

```python
MLPRegressor(
    hidden_layer_sizes = (256, 256),
    activation         = 'relu',
    solver             = 'adam',
    max_iter           = 300,
    early_stopping     = True,
    validation_fraction= 0.1,
    n_iter_no_change   = 20,
    random_state       = 42
)
```

| Aspek | Detail |
|-------|--------|
| **Cara Kerja** | Neural network 2-layer tersembunyi (256→256→3) bawaan sklearn |
| **Kelebihan** | Tanpa GPU, mudah dipakai, cocok sebagai pembanding DL |
| **Kekurangan** | Lebih lambat dari Ridge, lebih lemah dari DL untuk data kompleks |
| **Regularisasi** | Early stopping + validation fraction |
| **Output** | MultiOutput langsung |

---

### 2. Deep Learning (DL)

#### 🧠 Pendekatan IKNet (PyTorch)

Model kustom yang dioptimasi langsung di **ruang end-effector (Cartesian)**, bukan di ruang sudut. Loss dihitung sebagai jarak Euclidean antara posisi end-effector prediksi dan target.

**Pipeline Training:**
```
Input (x,y) → [Normalized] → IKNet → θ_pred → FK_differentiable → (x̂,ŷ) → MSE Loss
                                                                              ↑
                                                              dibandingkan dengan (x_target, y_target)
```

---

## 🏗 Arsitektur Model IKNet (PyTorch)

```
Input Layer:     (2,)          → x, y posisi target

Linear(2 → 256) + BatchNorm1d + ReLU
Linear(256 → 512) + BatchNorm1d + ReLU + Dropout(0.1)
Linear(512 → 512) + BatchNorm1d + ReLU + Dropout(0.1)
Linear(512 → 256) + BatchNorm1d + ReLU
Linear(256 → 3)

Output: tanh(out) × π    →   θ ∈ [-π, π]
```

| Komponen | Detail |
|----------|--------|
| **Total Parameter** | ~789.763 parameter |
| **Aktivasi** | ReLU (hidden), Tanh×π (output) |
| **Normalisasi** | BatchNorm1d setiap layer |
| **Regularisasi** | Dropout(0.1) + Weight Decay(1e-5) |
| **Optimizer** | Adam (`lr=1e-3`, `weight_decay=1e-5`) |
| **Scheduler** | CosineAnnealingLR (`T_max=100`) |
| **Epochs** | 100 |
| **Batch Size** | 512 |
| **Loss Function** | MSELoss di ruang Cartesian (bukan sudut!) |

### Loss Function (Differentiable FK)

```python
# FK differentiable dengan PyTorch
pred_theta = IKNet(x_scaled)
pred_ee    = FK_torch(pred_theta)     # → (x̂, ŷ)
x_original = x_scaled * scale + mean  # kembalikan ke skala meter
loss       = MSELoss(pred_ee, x_original)
```

> **Kenapa loss di Cartesian, bukan di sudut?**  
> Karena IK redundant — banyak kombinasi sudut yang valid. Loss di ruang sudut akan membingungkan model. Loss di ruang Cartesian memastikan model dievaluasi berdasarkan **akurasi fisis** (seberapa dekat robot ke target), bukan kecocokan sudut.

---

## 📈 Hasil & Perbandingan

### Tabel Perbandingan Metode

| Metode | Kategori | Mean Error (cm) | Butuh Dataset | Kelebihan Utama |
|--------|----------|-----------------|---------------|-----------------|
| **Extra Trees** | ML | ~3–6 cm | ✅ Ya | Robust, cepat, ensemble |
| **Ridge Regression** | ML | ~10–20 cm | ✅ Ya | Sangat cepat, interpretable |
| **MLP Regressor** | ML | ~5–10 cm | ✅ Ya | Neural net tanpa GPU |
| **IKNet (PyTorch)** | DL | ~1–3 cm | ✅ Ya | Akurasi fisis tertinggi |
| **PPO (RL)** | RL | ~— | ❌ Tidak | Adaptif, tanpa dataset |

> ⚠️ Nilai error aktual tergantung kondisi training. Urutan performa umumnya: **DL > Extra Trees > MLP > Ridge**.

### Perbandingan Waktu Training

| Metode | Estimasi Waktu |
|--------|----------------|
| Ridge Regression | < 1 detik |
| Extra Trees | 3–10 detik |
| MLP Regressor (sklearn) | 30–120 detik |
| IKNet (PyTorch) | 100 epoch (~2–5 menit) |
| RL (PPO) | ~200.000 steps |

---

## 📊 Visualisasi

### 1. Workspace Robot
Titik-titik workspace yang dapat dijangkau robot (radius 0 – 1.2 m):

```
● 18.000 titik acak dari FK sampling
● Lingkaran merah putus-putus = batas MAX_REACH (1.2 m)
```

### 2. Visualisasi Konfigurasi Robot
Tiga konfigurasi berbeda ditampilkan dengan posisi end-effector masing-masing.

### 3. Distribusi Error End-Effector
Histogram distribusi error (cm) untuk setiap metode — garis merah = nilai rata-rata.

### 4. Bar Chart Perbandingan Akurasi
Grafik batang membandingkan mean error (cm) antar semua metode secara side-by-side.

### 5. Animasi Gerakan Robot
Robot mengikuti lintasan lingkaran (radius 0.5 m) berdasarkan prediksi IK dari model Deep Learning. Animasi dirender dalam format HTML interaktif menggunakan `matplotlib.animation`.

---

## 💬 Diskusi & Analisis

### 1. Mengapa SVR bisa lebih baik dari Random Forest di workspace lebih besar?

SVR dengan kernel RBF mampu memodelkan hubungan non-linear secara halus dan generalisasi lebih baik ke area yang belum banyak tercakup data training (ekstrapolasi). Random Forest sangat baik untuk interpolasi tetapi cenderung menurun akurasinya di luar rentang data training, terutama ketika workspace diperbesar.

### 2. Mengapa Deep Learning lebih akurat dari ML tradisional?

DL secara otomatis belajar representasi fitur berlapis — setiap layer mengekstraksi pola yang semakin kompleks. Hubungan IK melibatkan fungsi trigonometri non-linear (sin/cos) yang sulit ditangkap oleh KNN atau Random Forest. IKNet juga dioptimasi langsung di ruang Cartesian (physical loss), bukan di ruang sudut, sehingga lebih bermakna secara fisis.

### 3. Mengapa waktu training RL meningkat saat workspace diperbesar?

RL belajar melalui eksplorasi. Workspace yang lebih besar berarti *state space* yang lebih besar, reward menjadi lebih jarang (*sparse reward*), dan agen membutuhkan lebih banyak percobaan untuk menemukan strategi optimal. Ini menyebabkan waktu konvergensi meningkat signifikan.

### 4. Apa kelemahan Supervised Learning untuk konfigurasi baru?

Model Supervised Learning bersifat statis setelah training. Jika robot menghadapi kondisi *Out-of-Distribution (OOD)* — seperti panjang link berubah, deformasi mekanik, atau lingkungan baru — prediksi dapat tidak akurat. Berbeda dengan RL yang dapat beradaptasi secara online, model ML/DL memerlukan retraining dengan data baru.

---

## 🏁 Kesimpulan

### Rekomendasi Pemilihan Metode

| Kondisi Penggunaan | Rekomendasi |
|-------------------|-------------|
| Training paling cepat, data besar | **Ridge Regression** |
| Akurasi ML terbaik, robust | **Extra Trees** |
| Neural network tanpa GPU | **MLP Regressor (sklearn)** |
| Akurasi fisis tertinggi | **Deep Learning (IKNet PyTorch)** |
| Tidak ada dataset, butuh hindari rintangan | **Reinforcement Learning (PPO)** |
| Real-time pada hardware rendah | **Extra Trees / Ridge** |

### Takeaway Utama

- **FK mudah, IK sulit** — pendekatan AI menggantikan solusi analitik yang rumit
- **Deep Learning unggul** dalam akurasi karena loss di ruang Cartesian + arsitektur dalam
- **Extra Trees** adalah pilihan terbaik dari sisi ML murni (speed vs accuracy trade-off)
- **Ridge Regression** cocok sebagai baseline cepat, tetapi tidak mampu menangkap non-linearitas IK
- **Normalisasi input (StandardScaler) penting** — terutama untuk Ridge dan MLP yang sensitif terhadap skala fitur
- **Validasi reachability** sebelum prediksi adalah praktik penting untuk mencegah prediksi di luar workspace

---

## ▶️ Cara Menjalankan

### Google Colab
```
1. Upload file Assignment_IK_ML__DL__RL.ipynb ke Google Colab
2. Runtime → Change runtime type → GPU (opsional, mempercepat DL)
3. Run All (Ctrl + F9)
```

### Jupyter Notebook Lokal
```bash
# 1. Install dependencies
pip install gymnasium stable-baselines3 scikit-learn torch matplotlib numpy tqdm pandas

# 2. Jalankan Jupyter
jupyter notebook Assignment_IK_ML__DL__RL.ipynb
```

### Urutan Eksekusi Sel yang Benar
```
1. Install & Import Library
2. Konfigurasi Robot (L1, L2, L3)
3. Generate Dataset (FK Sampling)
4. Split Train/Test
5. Training ML (Extra Trees → Ridge → MLP)
6. Training DL (IKNet PyTorch)
7. Evaluasi & Perbandingan
8. Visualisasi & Animasi
```

> ⚠️ **Penting:** Jalankan sel secara berurutan. Sel perbandingan di akhir bergantung pada variabel dari sel-sel sebelumnya (`ml_results`, `dl_err`, `rl_errors`).

---

## 📁 Struktur File

```
Assignment_IK_ML__DL__RL.ipynb
│
├── Bagian 1: Pengantar FK & IK
│   ├── Persamaan matematika
│   ├── Visualisasi workspace
│   └── Demo reachability check
│
├── Bagian 2: Dataset (FK Sampling)
│   ├── Generate 18.000 sampel
│   ├── Validasi reachability
│   └── Visualisasi workspace scatter
│
├── Bagian 3: Machine Learning
│   ├── Extra Trees Regressor
│   ├── Ridge Regression
│   ├── MLP Regressor (sklearn)
│   └── Evaluasi & histogram error
│
├── Bagian 4: Deep Learning (PyTorch)
│   ├── Arsitektur IKNet
│   ├── Training loop (100 epoch)
│   ├── Training curve (loss plot)
│   └── Evaluasi akhir
│
└── Bagian 5: Perbandingan & Kesimpulan
    ├── Tabel ringkasan semua metode
    ├── Bar chart akurasi
    ├── Distribusi error (histogram)
    └── Animasi gerakan robot
```

---

*Dibuat untuk tugas Praktikum Inverse Kinematics — Pendekatan ML & DL pada Robot Planar 3-DOF*
