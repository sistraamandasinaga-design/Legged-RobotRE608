import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class RoboticsPro3DOF:
    def __init__(self, L1, L2, L3):
        self.L = [L1, L2, L3]
        
    def fk(self, t1, t2, t3):
        # Forward Kinematics: Menghitung posisi tiap sendi
        x = [0]
        y = [0]
        # Joint 1
        x.append(self.L[0] * np.cos(t1))
        y.append(self.L[0] * np.sin(t1))
        # Joint 2
        x.append(x[1] + self.L[1] * np.cos(t1 + t2))
        y.append(y[1] + self.L[1] * np.sin(t1 + t2))
        # End-Effector (Joint 3)
        x.append(x[2] + self.L[2] * np.cos(t1 + t2 + t3))
        y.append(y[2] + self.L[2] * np.sin(t1 + t2 + t3))
        return x, y

    def ik(self, xt, yt, phi_deg):
        # Inverse Kinematics: Menghitung sudut penggerak
        phi = np.radians(phi_deg)
        L1, L2, L3 = self.L
        
        # 1. Cari posisi Wrist (sebelum Link 3)
        xw = xt - L3 * np.cos(phi)
        yw = yt - L3 * np.sin(phi)
        
        # 2. Cari Sudut Siku (Theta 2)
        dist_sq = xw**2 + yw**2
        cos_t2 = (dist_sq - L1**2 - L2**2) / (2 * L1 * L2)
        cos_t2 = np.clip(cos_t2, -1, 1)
        
        t2 = np.arccos(cos_t2)
        # 3. Cari Sudut Bahu (Theta 1)
        t1 = np.arctan2(yw, xw) - np.arctan2(L2 * np.sin(t2), L1 + L2 * np.cos(t2))
        # 4. Cari Sudut Akhir (Theta 3)
        t3 = phi - t1 - t2
        return t1, t2, t3

def run_pro_simulation():
    arm = RoboticsPro3DOF(8, 6, 4)
    # Lintasan Target (X, Y, Phi)
    path_points = [
        (12, 5, 0), (10, -8, -45), (-5, -10, 90), (-12, 5, 180), (12, 5, 0)
    ]
    
    steps = 50
    tx_p, ty_p, tphi_p = [], [], []
    for i in range(len(path_points)-1):
        tx_p.extend(np.linspace(path_points[i][0], path_points[i+1][0], steps))
        ty_p.extend(np.linspace(path_points[i][1], path_points[i+1][1], steps))
        tphi_p.extend(np.linspace(path_points[i][2], path_points[i+1][2], steps))

    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_xlim(-22, 22); ax.set_ylim(-22, 22)
    ax.set_aspect('equal')
    ax.grid(color='#333333', linestyle='--', alpha=0.5)

    # Objek Visual
    workspace = plt.Circle((0,0), sum(arm.L), color='cyan', fill=False, ls='--', alpha=0.2)
    ax.add_patch(workspace)
    
    line, = ax.plot([], [], 'o-', lw=6, color='#00FFCC', mec='white', mew=2, zorder=5)
    target_mark, = ax.plot([], [], 'rx', markersize=12, mew=3, label='Target')
    trail, = ax.plot([], [], color='yellow', lw=1, alpha=0.5)
    
    # Label Interaktif
    txt_target = ax.text(0, 0, '', color='red', fontweight='bold', fontsize=10)
    txt_ee = ax.text(0, 0, '', color='#00FFCC', fontweight='bold', fontsize=10)
    
    # Dashboard Status
    status_box = ax.text(-21, 21, '', family='monospace', fontsize=9,
                         bbox=dict(facecolor='black', alpha=0.8, edgecolor='cyan'))

    hx, hy = [], []

    def update(i):
        tx, ty, tp = tx_p[i], ty_p[i], tphi_p[i]
        try:
            t1, t2, t3 = arm.ik(tx, ty, tp)
            xs, ys = arm.fk(t1, t2, t3)
            
            line.set_data(xs, ys)
            target_mark.set_data([tx], [ty])
            
            hx.append(xs[-1]); hy.append(ys[-1])
            trail.set_data(hx[-200:], hy[-200:])
            
            # Update Label Posisi
            txt_target.set_text(f" TARGET ({tx:.1f}, {ty:.1f})")
            txt_target.set_position((tx, ty))
            
            txt_ee.set_text(f" END-EFFECTOR")
            txt_ee.set_position((xs[-1], ys[-1]))
            
            # Update Dashboard
            status_box.set_text(
                f"--- ROBOT 3-DOF PRO STATUS ---\n"
                f"POSISI TARGET : [{tx:>5.1f}, {ty:>5.1f}]\n"
                f"POSISI AKTUAL : [{xs[-1]:>5.1f}, {ys[-1]:>5.1f}]\n"
                f"ORIENTASI PHI : {tp:>5.1f}°\n"
                f"-------------------------------\n"
                f"PENGGERAK (SUDUT MOTOR):\n"
                f"JOINT 1 (BAHU): {np.degrees(t1):>6.1f}°\n"
                f"JOINT 2 (SIKU): {np.degrees(t2):>6.1f}°\n"
                f"JOINT 3 (WRIST): {np.degrees(t3):>6.1f}°"
            )
        except:
            status_box.set_text("STATUS: TARGET OUT OF WORKSPACE!")

        return line, target_mark, trail, txt_target, txt_ee, status_box

    ani = FuncAnimation(fig, update, frames=len(tx_p), interval=30, blit=True)
    plt.title("SISTRA AMANDA SINAGA - ROBOTICS SIMULATION V2.0", color='cyan', fontsize=14, pad=20)
    plt.show()

run_pro_simulation()