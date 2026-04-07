# Mengimpor fungsi dari file lain
try:
    from Forward_Kinematics import run_fk_manual
    from Inverse_Kinematics import run_pro_simulation
except ImportError:
    print("Error: Pastikan nama file sudah diubah menggunakan underscore (_)")

def main():
    print("=========================================")
    print("   SIMULASI ROBOT 3-DOF - SISTRA AMANDA  ")
    print("=========================================")
    print("1. Forward Kinematics (Kontrol Manual)")
    print("2. Inverse Kinematics (Animasi Lintasan)")
    print("3. Keluar")
    print("-----------------------------------------")
    
    choice = input("Pilih menu (1/2/3): ")

    if choice == "1":
        print("\nMenjalankan Forward Kinematics...")
        run_fk_manual()
    elif choice == "2":
        print("\nMenjalankan Inverse Kinematics...")
        run_pro_simulation()
    elif choice == "3":
        print("Program selesai. Sampai jumpa!")
    else:
        print("Pilihan tidak valid. Silakan coba lagi.")

if __name__ == "__main__":
    main()