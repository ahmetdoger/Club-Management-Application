import sys
import os
import time
import subprocess 

# =============================================================================
# MODÜL YOLLARI
# =============================================================================
# Her modülün kendi 'console_app.py' dosyasına giden yollar.

INFO_SCRIPT_PATH = os.path.join("modules", "information", "console_app.py")
FINANCE_SCRIPT_PATH = os.path.join("modules", "finance", "console_app.py")
TRAINING_SCRIPT_PATH = os.path.join("modules", "match_point", "console_app.py")

# =============================================================================
# YARDIMCI SINIF
# =============================================================================
class ClubApp:
    def __init__(self):
        self.clear_screen()
        
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def header(self):
        self.clear_screen()
        print("################################################################")
        print("#                                                              #")
        print("#             SPOR KULÜBÜ YÖNETİM SİSTEMİ (v3.0)               #")
        print("#                    ANA KONTROL PANELİ                        #")
        print("#                                                              #")
        print("################################################################")

    def run_module(self, script_path, module_name):
        """Belirtilen modül dosyasını bağımsız bir süreç olarak çalıştırır."""
        
        # 1. Dosya var mı kontrol et
        if not os.path.exists(script_path):
            print(f"\n[HATA] Modül dosyası bulunamadı!")
            print(f"Yol: {script_path}")
            print(f"Lütfen '{module_name}' modülünün eksiksiz olduğundan emin olun.")
            input("\nDevam etmek için Enter'a basınız...")
            return

        self.clear_screen()
        print(f">> {module_name} Başlatılıyor...")
        print(f">> Dosya: {script_path}\n")
        time.sleep(0.8)

        try:
            # 2. Dış dosyayı çalıştır (Ana Python yorumlayıcısı ile)
            subprocess.call([sys.executable, script_path])
            
            # Modülden çıkınca buraya döner
            print(f"\n>> {module_name} kapatıldı. Ana menüye dönülüyor...")
            time.sleep(1)
            
        except Exception as e:
            print(f"\n[KRİTİK HATA] Modül çalıştırılırken sorun oluştu.")
            print(f"Hata Detayı: {e}")
            input("\nDevam etmek için Enter'a basınız...")

    def run(self):
        while True:
            self.header()
            print("\nLütfen erişmek istediğiniz modülü seçiniz:\n")
            
            print("1. ⚽ SPORCU BİLGİ SİSTEMİ (Information)")
            print("     -> Kayıt, Arama, Filtreleme, Sezon Yönetimi\n")
            
            print("2. 💰 FİNANS YÖNETİM MERKEZİ (Finance)")
            print("     -> Gelir/Gider, Bütçe Raporu, Maaş Ödeme\n")
            
            print("3. 🏆 MAÇ VE ANTRENMAN (Match Point)")
            print("     -> Antrenman Programı, Maç Yönetimi\n")
            
            print("4. 🚪 ÇIKIŞ (Exit)")
            print("-" * 64)
            
            choice = input("Seçiminiz: ").strip()
            
            if choice == '1': 
                self.run_module(INFO_SCRIPT_PATH, "Sporcu Bilgi Sistemi")
                
            elif choice == '2': 
                self.run_module(FINANCE_SCRIPT_PATH, "Finans Yönetim Merkezi")
                
            elif choice == '3': 
                self.run_module(TRAINING_SCRIPT_PATH, "Maç ve Antrenman Modülü")
                
            elif choice == '4': 
                print("\nSistemden güvenli çıkış yapılıyor... İyi günler!")
                sys.exit()
            else:
                print("\n   [!] Geçersiz seçim!")
                time.sleep(1)

if __name__ == "__main__":
    app = ClubApp()
    app.run()