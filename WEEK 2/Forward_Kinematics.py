import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# ==========================================================
# 1. CLASS FORWARD KINEMATICS (MURNI)
# ==========================================================
class ForwardKinematics3DOF:
    def __init__(self, L1, L2, L3):
        self.L = [L1, L2, L3]

    def calculate(self, t1_deg, t2_deg, t3_deg):
        # Konversi derajat ke radian
        t1 = np.radians(t1_deg)
        t2 = np.radians(t2_deg)
        t3 = np.radians(t3_deg)
        
        # Titik 0: Base
        x = [0]
        y = [0]
        
        # Titik 1: Joint 1 (L1 * cos(t1))
        x.append(self.L[0] * np.cos(t1))
        y.append(self.L[0] * np.sin(t1))
        
        # Titik 2: Joint 2 (x1 + L2 * cos(t1+t2))
        x.append(x[1] + self.L[1] * np.cos(t1 + t2))
        y.append(y[1] + self.L[1] * np.sin(t1 + t2))
        
        # Titik 3: End-Effector (x2 + L3 * cos(t1+t2+t3))
        x.append(x[2] + self.L[2] * np.cos(t1 + t2 + t3))
        y.append(y[2] + self.L[2] * np.sin(t1 + t2 + t3))
        
        return x, y

# ==========================================================
# 2. SETUP VISUALISASI DENGAN KONTROL MANUAL
# ==========================================================
def run_fk_manual():
    robot = ForwardKinematics3DOF(8, 6, 4)
    
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(8, 8))
    plt.subplots_adjust(bottom=0.25) # Ruang untuk slider
    
    ax.set_xlim(-20, 20); ax.set_ylim(-20, 20)
    ax.set_aspect('equal')
    ax.grid(color='#333333', linestyle='--', alpha=0.5)
    
    line, = ax.plot([], [], 'o-', lw=6, color='#00FFCC', mec='white', mew=1)
    txt_info = ax.text(-19, 18, '', color='yellow', family='monospace')

    # Tambahkan Slider untuk kontrol sudut manual
    ax_t1 = plt.axes([0.2, 0.15, 0.65, 0.03])
    ax_t2 = plt.axes([0.2, 0.10, 0.65, 0.03])
    ax_t3 = plt.axes([0.2, 0.05, 0.65, 0.03])

    s_t1 = Slider(ax_t1, 'Joint 1', -180.0, 180.0, valinit=45)
    s_t2 = Slider(ax_t2, 'Joint 2', -180.0, 180.0, valinit=45)
    s_t3 = Slider(ax_t3, 'Joint 3', -180.0, 180.0, valinit=0)

    def update(val):
        t1, t2, t3 = s_t1.val, s_t2.val, s_t3.val
        xs, ys = robot.calculate(t1, t2, t3)
        line.set_data(xs, ys)
        
        txt_info.set_text(
            f"FORWARD KINEMATICS MODE\n"
            f"-----------------------\n"
            f"End-Effector Pos:\n"
            f"X: {xs[-1]:.2f}\n"
            f"Y: {ys[-1]:.2f}"
        )
        fig.canvas.draw_idle()

    s_t1.on_changed(update)
    s_t2.on_changed(update)
    s_t3.on_changed(update)

    update(0) # Inisialisasi tampilan pertama
    plt.title("MANUAL CONTROL: FORWARD KINEMATICS 3-DOF", pad=30)
    plt.show()

if __name__ == "__main__":
    run_fk_manual()