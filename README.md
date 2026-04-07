<div align="center">

# 🤖 3-Link Planar Robot Kinematics Simulation
### SISTRA AMANDA SINAGA (2243411xxx)
**Program Studi Teknik Robotika - Politeknik Negeri Batam**

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![Status](https://img.shields.io/badge/Status-Active-success.svg)](https://github.com/sistraamandasinaga-design/WEEK-2)
[![Course](https://img.shields.io/badge/Course-Legged_Robot-red.svg)](#)


</div>

---
## 🛠️ Langkah-Langkah Pengerjaan (Workflow)

Berikut adalah tahapan teknis dalam membangun simulasi ini:

### **Langkah 1: Persiapan Environment**
Menyiapkan perangkat lunak dan library pendukung agar simulasi berjalan lancar:
* **Python & VS Code**: Sebagai bahasa pemrograman dan editor utama.
* **NumPy**: Digunakan untuk perhitungan trigonometri (sin, cos) dan operasi matriks.
* **Matplotlib**: Digunakan untuk plotting grafik robot dan pembuatan animasi.
* **Pillow**: Library tambahan untuk menyimpan hasil simulasi ke format GIF.

### **Langkah 2: Perhitungan Forward Kinematics (FK)**
Menghitung posisi ujung robot ($x, y$) berdasarkan sudut joint yang diberikan.
* **Parameter Link**: $L_1=8, L_2=6, L_3=4$.
* **Visualisasi**: Menggambar struktur lengan robot dari *Base* (0,0) hingga ke *End-Effector*.

### **Langkah 3: Perhitungan Inverse Kinematics (IK)**
Mencari solusi sudut joint $(\theta_1, \theta_2, \theta_3)$ agar robot mencapai target koordinat tertentu.
* **Metode**: Menggunakan pendekatan analitis dan Hukum Kosinus.
* **Target**: Membuat robot mengikuti lintasan geometris (seperti lingkaran atau garis).

### **Langkah 4: Pembuatan Animasi & Export GIF**
Mengubah data koordinat menjadi tampilan visual yang bergerak:
* Menggunakan fungsi `FuncAnimation` dari Matplotlib.
* Menyimpan rekaman pergerakan secara otomatis ke folder proyek dalam format `.gif`.

### **Langkah 5: Dokumentasi & Publikasi GitHub**
Mengunggah seluruh hasil kerja ke GitHub agar terdokumentasi dengan baik:
* Membuat repositori publik.
* Mengatur struktur folder agar rapi.
* Menyusun file `README.md` ini sebagai laporan teknis.

---

## 📖 Deskripsi Proyek 

Proyek ini merupakan simulasi pergerakan lengan robot planar dengan 3 derajat kebebasan (3-DOF). Simulasi ini dikembangkan menggunakan Python untuk memvisualisasikan dua konsep utama dalam robotika: **Forward Kinematics** dan **Inverse Kinematics**.

## 📊 Perbandingan Fitur: FK vs IK

Berikut adalah perbedaan mendasar antara konsep Forward dan Inverse Kinematics yang diterapkan dalam simulasi ini:

| Fitur | Forward Kinematics (FK) | Inverse Kinematics (IK) |
| :--- | :--- | :--- |
| **Pertanyaan Utama** | "Ke mana robot pergi?" | "Gimana cara ke titik itu?" |
| **Input** | Sudut Joint ($\theta$) | Koordinat Target ($X, Y$) |
| **Output** | Posisi End-Effector ($X, Y$) | Sudut Joint ($\theta_1, \theta_2, \theta_3$) |
| **Rumus** | Trigonometri Langsung | Trigonometri Terbalik |
| **Tingkat Kesulitan** | Mudah | Menantang |

### 🎥 Demo & Animasi

#### 1. Forward Kinematics - Auto Movement
![Forward Kinematics](WEEK%202/fk_auto_animation.gif)

#### 2. Inverse Kinematics - Trajectory Tracking
![Inverse Kinematics](WEEK%202/simulation_3dof.gif)

---

## 📐 Penjelasan Matematis

### 1. Forward Kinematics (FK)
Menghitung posisi ujung robot ($X, Y$) jika sudut setiap joint ($\theta$) diketahui.


**Rumus:**
$$x = L_1 \cos(\theta_1) + L_2 \cos(\theta_1 + \theta_2) + L_3 \cos(\theta_1 + \theta_2 + \theta_3)$$
$$y = L_1 \sin(\theta_1) + L_2 \sin(\theta_1 + \theta_2) + L_3 \sin(\theta_1 + \theta_2 + \theta_3)$$

### 2. Inverse Kinematics (IK)
Menghitung sudut yang diperlukan ($\theta_1, \theta_2, \theta_3$) untuk mencapai posisi target ($X, Y$).


**Langkah Penyelesaian:**
1. Tentukan posisi *wrist* ($x_w, y_w$) dengan mengurangi Link 3 dari target.
2. Gunakan **Hukum Kosinus** untuk mencari $\theta_2$:
   $$\cos(\theta_2) = \frac{x_w^2 + y_w^2 - L_1^2 - L_2^2}{2 L_1 L_2}$$
3. Hitung $\theta_1$ menggunakan fungsi `atan2`.
4. Hitung $\theta_3$ berdasarkan orientasi akhir yang diinginkan ($\phi$).

---

## 🤖 Konfigurasi Robot
| Parameter | Nilai |
|-----------|-------|
| Link 1    | 8.0 m |
| Link 2    | 6.0 m |
| Link 3    | 4.0 m |
| **Total Reach** | **18.0 m** |

---
📂 Struktur Proyek
Plaintext
```
📂 githublengan/
└── 📂 WEEK 2/
    ├── 📄 Forward_Kinematics.py         # Simulasi gerak otomatis (FK)
    ├── 📄 Inverse_Kinematics.py         # Simulasi mengikuti lintasan (IK)
    ├── 🖼️ forward_auto_animation.gif    # Demo Visual: Forward Kinematics
    └── 🖼️ inverse_simulation_3dof.gif   # Demo Visual: Inverse Kinematics
---
