import sys
import os
import time
import subprocess # Harici dosya çalıştırmak için

# =============================================================================
# 1. MODÜL AYARLARI
# =============================================================================

# --- A. FİNANS MODÜLÜ (Senin Modülün) ---
try:
    from modules.finance.services.manager import FinanceManager
    from modules.finance.services.analyzer import FinancialAnalyzer
    from modules.finance.services.calculator import SalaryCalculator, LateFeeCalculator
    from modules.finance.data.constants import TransactionType, IncomeCategory, ExpenseCategory
    FINANCE_OK = True
except ImportError as e:
    print(f"[HATA] Finans modülü yüklenemedi: {e}")
    FINANCE_OK = False

# --- B. BİLGİ (SPORCU) MODÜLÜ (Arkadaşının Modülü) ---
try:
    try:
        from modules.information.repository import AthleteRepository
    except ImportError:
        from modules.information.repostory import AthleteRepository
    INFO_OK = True
except ImportError:
    INFO_OK = False

# --- C. ANTRENMAN MODÜLÜ DOSYA YOLU (DÜZELTİLDİ) ---
# Burası senin söylediğin klasör: modules/match_point
# Dosya adı: console_app.py
TRAINING_SCRIPT_PATH = os.path.join("modules", "match_point", "console_app.py")


# =============================================================================
# 2. ANA UYGULAMA
# =============================================================================
class ClubApp:
    def __init__(self):
        self.clear_screen()
        
        # Modülleri Başlat
        if FINANCE_OK:
            self.fin_manager = FinanceManager()
            self.fin_analyzer = FinancialAnalyzer()
            self.salary_calc = SalaryCalculator()
            self.fee_calc = LateFeeCalculator()
        
        if INFO_OK:
            self.athlete_repo = AthleteRepository()

    # --- YARDIMCILAR ---
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def header(self, text):
        self.clear_screen()
        print("=" * 70)
        print(f" {text} ".center(70, "*"))
        print("=" * 70 + "\n")

    def pause(self):
        input("\nDevam etmek için Enter'a basınız...")

    # =========================================================================
    # MENÜ 1: SPORCU BİLGİ SİSTEMİ (Detaylı - Bizim Tarafımızdan Filtreli)
    # =========================================================================
    def menu_info(self):
        while True:
            self.header("SPORCU DETAYLI ARAMA VE LİSTELEME")
            if not INFO_OK: print("⚠ Modül Yok!"); self.pause(); break

            print("1. Tüm Sporcuları Listele")
            print("2. ID'ye Göre Ara")
            print("3. İsme Göre Ara")
            print("4. En Yüksek Maaşlı Sporcu")
            print("5. Ana Menüye Dön")

            c = input("\nSeçiminiz: ")

            try:
                # Veriyi çekiyoruz
                all_data = self.athlete_repo.get_all()
            except:
                print("Veri çekilemedi."); self.pause(); continue

            if c == '1':
                self._info_list(all_data)
            
            elif c == '2': # ID ARAMA
                sid = input("Aranacak ID: ").strip()
                # Arkadaşının verisinde ID key'i 'id' mi 'athlete_id' mi bilmiyoruz, hepsine bakıyoruz
                filtered = [x for x in all_data if str(x.get('id', x.get('athlete_id', ''))).strip() == sid]
                if filtered: self._info_list(filtered)
                else: print("❌ Bulunamadı.")
                self.pause()

            elif c == '3': # İSİM ARAMA
                sname = input("Aranacak İsim: ").lower()
                filtered = [x for x in all_data if sname in x.get('name', x.get('ad', '')).lower()]
                if filtered: self._info_list(filtered)
                else: print("❌ Bulunamadı.")
                self.pause()

            elif c == '4': # ANALİZ
                if all_data:
                    top = max(all_data, key=lambda x: x.get('salary', x.get('maas', 0)))
                    print(f"\n🏆 Lider: {top.get('name', top.get('ad'))} -> {top.get('salary', top.get('maas'))} TL")
                    self.pause()

            elif c == '5': break

    def _info_list(self, data):
        print(f"\n{'ID':<10} | {'İSİM':<25} | {'MAAŞ':<15}")
        print("-" * 55)
        for d in data:
            name = d.get('name', d.get('ad', 'Bilinmiyor'))
            uid = d.get('id', d.get('athlete_id', '-'))
            sal = d.get('salary', d.get('maas', 0))
            print(f"{uid:<10} | {name:<25} | {sal:,.2f} TL")
        if len(data) > 5: self.pause()

    # =========================================================================
    # MENÜ 2: FİNANS YÖNETİMİ (Detaylı/Filtreli)
    # =========================================================================
    def menu_finance(self):
        while True:
            self.header("FİNANS YÖNETİM MERKEZİ")
            if not FINANCE_OK: print("⚠ Modül Yok!"); self.pause(); break

            print("1. Gelir Ekle")
            print("2. Gider Ekle")
            print("3. Tüm İşlemleri Listele")
            print("4. Tarihe Göre Filtrele")
            print("5. Kategoriye Göre Filtrele")
            print("6. Bütçe Raporu")
            print("7. Hesaplayıcılar (Net Maaş / Faiz)")
            print("8. MAAŞLARI ÖDE")
            print("9. Ana Menüye Dön")

            c = input("\nSeçiminiz: ")

            if c == '1': self._fin_add(TransactionType.INCOME)
            elif c == '2': self._fin_add(TransactionType.EXPENSE)
            elif c == '3': 
                self._fin_list(self.fin_manager.get_all_transactions())
                self.pause()
            
            elif c == '4': # TARİH FİLTRESİ
                date_in = input("Tarih (Yıl-Ay-Gün): ")
                all_t = self.fin_manager.get_all_transactions()
                filt = [t for t in all_t if date_in in str(t.get('tarih', ''))]
                self._fin_list(filt)
                self.pause()

            elif c == '5': # KATEGORİ FİLTRESİ
                cat_in = input("Kategori: ").lower()
                all_t = self.fin_manager.get_all_transactions()
                filt = [t for t in all_t if cat_in in str(t.get('kategori', '')).lower()]
                self._fin_list(filt)
                self.pause()

            elif c == '6':
                s = self.fin_manager.get_financial_summary()
                status = self.fin_analyzer.get_budget_status()
                print(f"\nGelir: {s['toplam_gelir']:,.2f} TL")
                print(f"Gider: {s['toplam_gider']:,.2f} TL")
                print(f"Net:   {s['bakiye']:,.2f} TL")
                print(f"Durum: {status.get('durum', '-')}")
                self.pause()

            elif c == '7':
                print("\n1. Net Maaş Hesapla\n2. Gecikme Faizi Hesapla")
                sc = input("Seçim: ")
                if sc == '1':
                    try: print(f"Net: {self.salary_calc.calculate(float(input('Brüt: '))):,.2f} TL")
                    except: pass
                elif sc == '2':
                    try: print(f"Toplam: {self.fee_calc.calculate(float(input('Borç: ')), int(input('Gün: '))):,.2f} TL")
                    except: pass
                self.pause()

            elif c == '8':
                print("\nİşlem yapılıyor...")
                ok, msg = self.fin_manager.process_monthly_salaries()
                print(f"\nSONUÇ:\n{msg}")
                self.pause()

            elif c == '9': break

    def _fin_add(self, t_type):
        cats = IncomeCategory if t_type == TransactionType.INCOME else ExpenseCategory
        clist = [x.value for x in cats]
        print(f"\n--- {t_type.value} ---")
        for i, v in enumerate(clist, 1): print(f"{i}. {v}")
        try:
            sel = int(input("No: ")) - 1
            self.fin_manager.add_transaction(t_type.value, clist[sel], input("Tutar: "), input("Açıklama: "))
            print("✔ Eklendi.")
        except: print("❌ Hata.")
        time.sleep(0.5)

    def _fin_list(self, data):
        if not data: print("Kayıt yok."); return
        print(f"\n{'TARİH':<12} | {'TİP':<8} | {'KATEGORİ':<15} | {'TUTAR':<10}")
        print("-" * 55)
        for t in data:
            print(f"{t.get('tarih','-'):<12} | {t['tip']:<8} | {t['kategori']:<15} | {t['tutar']}")

    # =========================================================================
    # MENÜ 3: ANTRENMAN VE MAÇ (DIŞ DOSYA ÇALIŞTIRMA)
    # =========================================================================
    def menu_training(self):
        # Dosya yolu kontrolü (modules/match_point/console_app.py)
        if not os.path.exists(TRAINING_SCRIPT_PATH):
            print(f"\n[HATA] Dosya bulunamadı: {TRAINING_SCRIPT_PATH}")
            print("Lütfen 'modules/match_point' klasöründe 'console_app.py' olduğundan emin ol.")
            self.pause()
            return

        self.clear_screen()
        print(">> Antrenman Modülü (console_app) Başlatılıyor...")
        print(f">> Dosya Yolu: {TRAINING_SCRIPT_PATH}\n")
        time.sleep(1)

        try:
            # Arkadaşının dosyasını sanki terminalden çalıştırıyormuş gibi açıyoruz.
            subprocess.call([sys.executable, TRAINING_SCRIPT_PATH])
            
            print("\n>> Ana sisteme dönülüyor...")
            time.sleep(1)
            
        except Exception as e:
            print(f"\n[HATA] Modül çalıştırılırken sorun oluştu: {e}")
            self.pause()

    # =========================================================================
    # ANA ÇALIŞTIRMA
    # =========================================================================
    def run(self):
        while True:
            self.header("KULÜP YÖNETİM SİSTEMİ v2.0")
            
            print(f"1. ⚽ Sporcu Bilgi Sistemi   [AKTİF]")
            print(f"2. 💰 Finans Yönetimi        [AKTİF]")
            print(f"3. 🏆 Maç ve Antrenman       [AKTİF]")
            print("4. 🚪 Çıkış")
            
            c = input("\nModül Seçiniz: ")
            
            if c == '1': self.menu_info()
            elif c == '2': self.menu_finance()
            elif c == '3': self.menu_training() # console_app.py çalışacak
            elif c == '4': 
                print("Çıkış yapılıyor..."); sys.exit()

if __name__ == "__main__":
    app = ClubApp()
    app.run()