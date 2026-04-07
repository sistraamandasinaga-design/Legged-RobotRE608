<div align="center">

# 🤖 3-Link Planar Robot Kinematics Simulation
### SISTRA AMANDA SINAGA (2243411xxx)
**Program Studi Teknik Robotika - Politeknik Negeri Batam**

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![Status](https://img.shields.io/badge/Status-Active-success.svg)](https://github.com/sistraamandasinaga-design/WEEK-2)
[![Course](https://img.shields.io/badge/Course-Legged_Robot-red.svg)](#)

[English](#english-version) | [Bahasa Indonesia](#bahasa-indonesia)

</div>

---

<a name="bahasa-indonesia"></a>

## 📖 Deskripsi Proyek (Bahasa Indonesia)

Proyek ini merupakan simulasi pergerakan lengan robot planar dengan 3 derajat kebebasan (3-DOF). Simulasi ini dikembangkan menggunakan Python untuk memvisualisasikan dua konsep utama dalam robotika: **Forward Kinematics** dan **Inverse Kinematics**.

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

### 🎥 Demo & Animasi (Bahasa Indonesia)

#### 1. Forward Kinematics (Eksplorasi Workspace)
![Forward Kinematics](WEEK%202/fk_auto_animation.gif)

#### 2. Inverse Kinematics (Mengejar Target)
Robot menghitung solusi sudut secara *real-time* untuk mengikuti koordinat target tertentu.
![Inverse Kinematics](WEEK%202/simulation_3dof.gif)

---

### 🎥 Demos & Animations (English)

#### 1. Forward Kinematics - Auto Movement
![Forward Kinematics](WEEK%202/fk_auto_animation.gif)

#### 2. Inverse Kinematics - Trajectory Tracking
The robot arm calculates joint angles in real-time to follow a predefined trajectory.
![Inverse Kinematics](WEEK%202/simulation_3dof.gif)



---

## 🤖 Konfigurasi Robot
| Parameter | Nilai |
|-----------|-------|
| Link 1    | 8.0 m |
| Link 2    | 6.0 m |
| Link 3    | 4.0 m |
| **Total Reach** | **18.0 m** |

---

## 📂 Struktur Folder
WEEK 2/
├── 📄 Forward_Kinematics.py     # Simulasi Gerak Otomatis
├── 📄 Inverse_Kinematics.py     # Simulasi Ikuti Lintasan (IK)
├── 🖼️ forward_animation.gif     # Rekaman Hasil FK
└── 🖼️ kinematik_simulation_3dof.gif       # Rekaman Hasil IK
