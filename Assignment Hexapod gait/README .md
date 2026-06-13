# 🤖 RE608 — Legged Robot | Week 7: Gait Planning

> **Program Studi Teknologi Rekayasa Robotika — Politeknik Negeri Batam**

---

## 📋 Identitas Mahasiswa

| | |
|---|---|
| **Nama** | Sistra Amanda Sinaga |
| **NIM** | 4222301011 |
| **Kelas** | Robotika A |
| **Mata Kuliah** | RE608 – Legged Robot |
| **Minggu** | 7 – Gait Planning |

---

## 📖 Deskripsi Proyek

Notebook ini mengimplementasikan dan memvisualisasikan **Gait Scheduler** untuk dua jenis robot berkaki:

- **Quadruped (4 kaki)** → Trot Gait & Crawl Gait
- **Hexapod (6 kaki)** → Tripod Gait *(tugas utama)*

Mencakup pemodelan jadwal fase gerak (*gait scheduler*), visualisasi diagram gait, lintasan kaki (*foot trajectory*), serta verifikasi stabilitas statis.

---

## 📁 Struktur File

```
📦 RE608-Week7-GaitPlanning/
 ┣ 📓 Gait_assignment_SISTRA.ipynb   ← Notebook utama (semua tugas)
 ┗ 📄 README.md                      ← Dokumentasi ini
```

---

## 🧩 Isi Notebook

| Cell | Tipe | Konten |
|:---:|---|---|
| 1 | Markdown | Cover & identitas mahasiswa |
| 2–3 | Markdown + Code | Import library & konfigurasi environment |
| 4 | Markdown | Teori parameter gait (T, β, φ) |
| 5–6 | Markdown + Code | `QuadrupedGaitScheduler` — Trot & Crawl Gait |
| 7–8 | Markdown + Code | Foot Trajectory — lintasan kaki stance & swing |
| 9–10 | Markdown | Konsep Tripod Gait & penjelasan assignment |
| 11 | Code | **Tugas 1 & 2** — `HexapodGaitScheduler` + matriks offsets |
| 12–13 | Markdown + Code | **Tugas 3** — Plot gait diagram & verifikasi stabilitas |
| 14 | Markdown | **Tugas 4** — Analisis stabilitas Trot vs Tripod |
| 15 | Markdown | Penutup & catatan implementasi lanjutan |

---

## ✅ Tugas Praktikum

### Tugas 1 — Modifikasi Kelas untuk 6 Kaki
Dibuat kelas `HexapodGaitScheduler` yang menangani 6 kaki:

```
L1 (depan kiri)    L2 (tengah kiri)    L3 (belakang kiri)
R1 (depan kanan)   R2 (tengah kanan)   R3 (belakang kanan)
```

Method yang tersedia:
- `get_phase(t, offset)` — normalisasi fase ke [0, 1)
- `is_stance(phase, duty_factor)` — deteksi stance/swing
- `plot_gait_diagram(...)` — visualisasi diagram Gantt
- `verify_stability(...)` — verifikasi jumlah kaki stance

---

### Tugas 2 — Matriks Offsets & Duty Factor

**Tripod Gait** membagi 6 kaki menjadi 2 kelompok segitiga bergantian:

| Kelompok | Kaki | Phase Offset | Aksi di t = 0 |
|---|---|:---:|---|
| **Grup A** | L1, R2, L3 | `0.0` | Stance (di tanah) |
| **Grup B** | R1, L2, R3 | `0.5` | Swing (di udara) |

```python
tripod_offsets = [0.0,  # L1 → Grup A
                  0.5,  # L2 → Grup B
                  0.0,  # L3 → Grup A
                  0.5,  # R1 → Grup B
                  0.0,  # R2 → Grup A
                  0.5]  # R3 → Grup B

tripod_duty = 0.5  # β = 0.5 (standar Tripod Gait)
```

---

### Tugas 3 — Plot Diagram Gait & Verifikasi Stabilitas

**Diagram Gait:**
- Biru tua = Grup A stance
- Oranye = Grup B stance
- Abu-abu = Swing phase

**Hasil Verifikasi:**

| Parameter | Nilai |
|---|:---:|
| Min kaki stance per saat | **3** |
| Max kaki stance per saat | **3** |
| Selalu ≥ 3 kaki | ✅ Ya |
| Status | **STABIL STATIS** |

---

### Tugas 4 — Analisis Stabilitas Trot vs Tripod

| Aspek | Trot Quadruped | Tripod Hexapod |
|---|:---:|:---:|
| Jumlah kaki | 4 | 6 |
| Kaki stance minimum | **2** | **3** |
| Bentuk tumpuan | Garis (1D) | Segitiga (2D) |
| Jenis stabilitas | **Dinamis** | **Statis** |
| Bisa berhenti kapanpun | ❌ | ✅ |
| Duty Factor β | 0.5 | 0.5 |
| Toleransi terrain kasar | Rendah | Tinggi |

**Kesimpulan:** Tripod Hexapod lebih stabil secara statis karena selalu memiliki 3 titik tumpu yang membentuk *support polygon* (segitiga), sehingga robot dapat berhenti kapan saja tanpa risiko jatuh. Trot Quadruped bersifat *dynamically stable* — hanya aman saat bergerak.

---

## 🚀 Cara Menjalankan

### Google Colab (Disarankan)

1. Buka [Google Colab](https://colab.research.google.com)
2. Upload file `Gait_assignment_SISTRA.ipynb`
3. Klik **Runtime → Run All**

### Lokal (Jupyter)

```bash
# Install dependencies
pip install numpy matplotlib

# Jalankan Jupyter
jupyter notebook Gait_assignment_SISTRA.ipynb
```

---

## 📦 Dependencies

| Library | Versi | Kegunaan |
|---|---|---|
| `numpy` | ≥ 1.21 | Komputasi numerik & array |
| `matplotlib` | ≥ 3.4 | Visualisasi diagram gait |

---

## 📝 Catatan Implementasi Lanjutan

Saat mengintegrasikan gait scheduler ke simulasi IK/FK:

1. **Paksa sendi coxa** beroperasi konstan pada bidang XY → mencegah matriks singular.
2. **Hapus titik koordinat base** dari matriks simulasi kaki → mempercepat konvergensi IK.
3. **Transisi stance → swing** lakukan tepat di titik `x_lift` → hindari discontinuity.

---

*Dibuat untuk memenuhi tugas praktikum RE608 — Legged Robot, Minggu 7.*
*Politeknik Negeri Batam — Program Studi Teknologi Rekayasa Robotika*
