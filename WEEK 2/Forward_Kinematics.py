import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# ==========================================================
# 1. CLASS FORWARD KINEMATICS (SISTRA AMANDA SINAGA)
# ==========================================================
class ForwardKinematics3DOF:
    def __init__(self, L1, L2, L3):
        self.L = [L1, L2, L3]

    def calculate(self, t1_deg, t2_deg, t3_deg):
        t1, t2, t3 = np.radians(t1_deg), np.radians(t2_deg), np.radians(t3_deg)
        x = [0]
        y = [0]
        x.append(self.L[0] * np.cos(t1))
        y.append(self.L[0] * np.sin(t1))
        x.append(x[1] + self.L[1] * np.cos(t1 + t2))
        y.append(y[1] + self.L[1] * np.sin(t1 + t2))
        x.append(x[2] + self.L[2] * np.cos(t1 + t2 + t3))
        y.append(y[2] + self.L[2] * np.sin(t1 + t2 + t3))
        return x, y

# ==========================================================
# 2. SETUP ANIMASI OTOMATIS & GENERATE GIF
# ==========================================================
def run_fk_animation():
    robot = ForwardKinematics3DOF(8, 6, 4)
    
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_xlim(-20, 20); ax.set_ylim(-20, 20)
    ax.set_aspect('equal')
    ax.grid(color='#333333', linestyle='--', alpha=0.5)
    
    line, = ax.plot([], [], 'o-', lw=6, color='#00FFCC', mec='white', mew=1, zorder=5)
    trail, = ax.plot([], [], color='yellow', lw=1.5, alpha=0.6, label='Trajectory')
    txt_info = ax.text(-19, 18, '', color='cyan', family='monospace', 
                         bbox=dict(facecolor='black', alpha=0.7, edgecolor='cyan'))

    hx, hy = [], [] # Untuk menyimpan jejak (trail)

    def update(frame):
        # Membuat variasi sudut otomatis berdasarkan frame
        t1 = 45 * np.sin(0.05 * frame)
        t2 = 60 * np.cos(0.05 * frame)
        t3 = 30 * np.sin(0.1 * frame)
        
        xs, ys = robot.calculate(t1, t2, t3)
        
        # Simpan jejak posisi End-Effector
        hx.append(xs[-1])
        hy.append(ys[-1])
        
        line.set_data(xs, ys)
        trail.set_data(hx[-100:], hy[-100:]) # Tampilkan 100 titik terakhir
        
        txt_info.set_text(
            f"--- FORWARD KINEMATICS AUTO ---\n"
            f"SISTRA AMANDA SINAGA\n"
            f"JOINT 1: {t1:>6.1f}°\n"
            f"JOINT 2: {t2:>6.1f}°\n"
            f"JOINT 3: {t3:>6.1f}°\n"
            f"-------------------------------\n"
            f"EE POS : [{xs[-1]:.2f}, {ys[-1]:.2f}]"
        )
        return line, trail, txt_info

    ani = FuncAnimation(fig, update, frames=200, interval=30, blit=True)

    # Simpan sebagai GIF
    print("Sisca, sedang merekam animasi Forward Kinematics... Mohon tunggu.")
    ani.save('fk_auto_animation.gif', writer='pillow', fps=30)
    print("Selesai! File 'fk_auto_animation.gif' sudah ada di folder kamu.")

    plt.title("ANIMATED: FORWARD KINEMATICS 3-DOF", color='cyan', pad=20)
    plt.show()

if __name__ == "__main__":
    run_fk_animation()