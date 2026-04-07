<div align="center">

# 🤖 3-Link Planar Robot Kinematics Simulation
### (Forward & Inverse Kinematics)

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![Course](https://img.shields.io/badge/Course-Legged_Robot-red.svg)](https://www.polibatam.ac.id/)
[![Status](https://img.shields.io/badge/Status-Completed-success.svg)]()

**Author: SISTRA AMANDA SINAGA** *Robotika Polibatam | Semester 6 - Legged Robot Course (RE608)*

[English](#english) | [Bahasa Indonesia](#bahasa-indonesia)

</div>

---

<a name="english"></a>

## 📖 Project Overview
This repository contains a comprehensive simulation of a **3-Link Planar Robot Arm**. The project focuses on solving the fundamental robotics problem: finding the relationship between joint angles and the end-effector's position in 2D space.

### 🎯 Objectives (Based on Assignment)
According to the course requirements:
1. **Forward Kinematics**: Calculate the $(X, Y)$ position of the end-effector based on given joint angles ($\theta_1, \theta_2, \theta_3$).
2. **Inverse Kinematics**: Determine the required joint angles to reach a specific target position $(X_{target}, Y_{target})$.

---

<a name="bahasa-indonesia"></a>

## 📖 Dokumentasi Bahasa Indonesia

### 📐 Dasar Matematika & Rumus

Berdasarkan struktur robot 3-link planar, berikut adalah formulasi yang digunakan dalam kode ini:

#### 1. Forward Kinematics (FK)
Menghitung posisi ujung robot (End-Effector) jika sudut setiap motor diketahui:

$$x = L_1 \cos(\theta_1) + L_2 \cos(\theta_1 + \theta_2) + L_3 \cos(\theta_1 + \theta_2 + \theta_3)$$
$$y = L_1 \sin(\theta_1) + L_2 \sin(\theta_1 + \theta_2) + L_3 \sin(\theta_1 + \theta_2 + \theta_3)$$

#### 2. Inverse Kinematics (IK)
Menghitung sudut motor yang dibutuhkan untuk mencapai koordinat target $(x, y)$.
- **Langkah 1**: Tentukan posisi pergelangan (*Wrist*) $(x_w, y_w)$ dengan orientasi $\phi$.
  $$x_w = x - L_3 \cos(\phi)$$
  $$y_w = y - L_3 \sin(\phi)$$
- **Langkah 2**: Gunakan hukum kosinus untuk mencari $\theta_2$ (Siku).
  $$\cos(\theta_2) = \frac{x_w^2 + y_w^2 - L_1^2 - L_2^2}{2 L_1 L_2}$$
- **Langkah 3**: Hitung $\theta_1$ (Bahu) dan $\theta_3$ (Wrist) menggunakan fungsi `atan2`.

---

### 🤖 Konfigurasi Simulasi
Robot ini dikonfigurasi dengan panjang link sebagai berikut:
- **Link 1 (Bahu)**: 8.0 unit
- **Link 2 (Siku)**: 6.0 unit
- **Link 3 (Wrist)**: 4.0 unit

---

### 💻 Cara Mengerjakan & Menjalankan
Proyek ini dibagi menjadi dua modul utama agar mudah dipelajari:

#### A. Menjalankan Forward Kinematics (Kontrol Manual)
Gunakan file ini untuk menggerakkan robot secara manual menggunakan slider.
```bash
python "WEEK 2/Forward_Kinematics.py"
