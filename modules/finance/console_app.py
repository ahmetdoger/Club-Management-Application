import os
import sys
import time

# =============================================================================
# OTO-YOL BULUCU (ROBUST PATH FINDER)
# =============================================================================
current_file = os.path.abspath(__file__)
current_dir = os.path.dirname(current_file)
root_dir = current_dir
found = False

# "modules" klasörünü bulana kadar yukarı çık
while True:
    if os.path.exists(os.path.join(root_dir, "modules")):
        found = True
        break
    parent = os.path.dirname(root_dir)
    if parent == root_dir: break
    root_dir = parent

if found:
    if root_dir not in sys.path: sys.path.insert(0, root_dir)
else:
    # Bulamazsa manuel 2 üst dizini dene
    sys.path.insert(0, os.path.abspath(os.path.join(current_dir, '..', '..')))

# =============================================================================

try:
    from modules.finance.services.manager import FinanceManager
    from modules.finance.services.analyzer import FinancialAnalyzer
    from modules.finance.services.calculator import SalaryCalculator, LateFeeCalculator
    from modules.finance.data.constants import TransactionType, IncomeCategory, ExpenseCategory
except ImportError as e:
    print(f"\n[KRİTİK HATA] Finans modülleri yüklenemedi: {e}")
    sys.exit(1)

# Servisleri Başlat
manager = FinanceManager()
analyzer = FinancialAnalyzer()
salary_calc = SalaryCalculator()
fee_calc = LateFeeCalculator()

# --- YARDIMCILAR ---

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_input(prompt, type_func=str):
    while True:
        try:
            val = input(prompt).strip()
            if not val: return None
            return type_func(val)
        except ValueError:
            print("   [!] Hatalı giriş.")

def print_header():
    clear_screen()
    print("================================================================")
    print("           FİNANS YÖNETİM SİSTEMİ (FINANCE MODULE)")
    print("================================================================")

# --- MENÜLER ---

def menu_add_transaction():
    print("\n--- İŞLEM EKLE ---")
    print("1. Gelir (Income)")
    print("2. Gider (Expense)")
    choice = get_input("Tip Seçiniz (1-2): ", int)
    
    if choice == 1:
        t_type = TransactionType.INCOME
        categories = [c.value for c in IncomeCategory]
    elif choice == 2:
        t_type = TransactionType.EXPENSE
        categories = [c.value for c in ExpenseCategory]
    else:
        return

    print("\nKategori Seçiniz:")
    for i, cat in enumerate(categories, 1):
        print(f"{i}. {cat}")
    
    cat_idx = get_input("Kategori No: ", int)
    if not cat_idx or cat_idx < 1 or cat_idx > len(categories):
        print("   [!] Geçersiz kategori.")
        return
    
    category = categories[cat_idx - 1]
    amount = get_input("Tutar (TL): ", float)
    desc = get_input("Açıklama: ")

    if amount:
        manager.add_transaction(t_type.value, category, amount, desc)
        print("\n   [BAŞARILI] İşlem kaydedildi.")
    input("\nDevam etmek için Enter...")

def menu_list_transactions():
    print("\n--- İŞLEM LİSTESİ ---")
    print("1. Tümü")
    print("2. Gelirler")
    print("3. Giderler")
    filter_choice = get_input("Filtre (1-3): ", int)
    
    all_data = manager.get_all_transactions()
    filtered = []
    
    if filter_choice == 1: filtered = all_data
    elif filter_choice == 2: filtered = [t for t in all_data if t['tip'] == TransactionType.INCOME.value]
    elif filter_choice == 3: filtered = [t for t in all_data if t['tip'] == TransactionType.EXPENSE.value]
    else: return

    if not filtered:
        print("\n   [!] Kayıt bulunamadı.")
    else:
        print(f"\n{'TARİH':<12} | {'TİP':<8} | {'KATEGORİ':<20} | {'TUTAR':<12} | {'AÇIKLAMA'}")
        print("-" * 80)
        for t in filtered:
            print(f"{t.get('tarih', '-'):<12} | {t['tip']:<8} | {t['kategori']:<20} | {t['tutar']:<12} | {t.get('aciklama', '')}")
            
    input("\nDevam etmek için Enter...")

def menu_financial_report():
    print("\n--- MALİ DURUM RAPORU ---")
    summary = manager.get_financial_summary()
    status = analyzer.get_budget_status()
    
    print(f"\nTOPLAM GELİR : {summary['toplam_gelir']:,.2f} TL")
    print(f"TOPLAM GİDER : {summary['toplam_gider']:,.2f} TL")
    print("-" * 30)
    print(f"NET BAKİYE   : {summary['bakiye']:,.2f} TL")
    
    print(f"\nBÜTÇE DURUMU : {status.get('durum', 'Bilinmiyor')}")
    if status.get('tavsiye'):
        print(f"TAVSİYE      : {status['tavsiye']}")
        
    input("\nDevam etmek için Enter...")

def menu_calculators():
    print("\n--- HESAPLAYICILAR ---")
    print("1. Net Maaş Hesapla")
    print("2. Gecikme Faizi Hesapla")
    c = get_input("Seçim: ", int)
    
    if c == 1:
        gross = get_input("Brüt Maaş: ", float)
        if gross:
            net = salary_calc.calculate(gross)
            print(f"   -> Net Maaş: {net:,.2f} TL")
            
    elif c == 2:
        debt = get_input("Ana Borç: ", float)
        days = get_input("Gecikme Günü: ", int)
        if debt and days:
            total = fee_calc.calculate(debt, days)
            print(f"   -> Faizli Toplam: {total:,.2f} TL")
            
    input("\nDevam etmek için Enter...")

def menu_process_salaries():
    print("\n--- MAAŞ ÖDEMELERİ ---")
    print("Bu işlem, sistemdeki tüm personelin maaşlarını gider olarak kaydeder.")
    confirm = get_input("Onaylıyor musunuz? (e/h): ")
    
    if confirm and confirm.lower() == 'e':
        success, msg = manager.process_monthly_salaries()
        if success:
            print(f"\n   [BAŞARILI] {msg}")
        else:
            print(f"\n   [UYARI] {msg}")
    else:
        print("\n   [İPTAL] İşlem yapılmadı.")
        
    input("\nDevam etmek için Enter...")

# --- ANA DÖNGÜ ---

def start_app():
    while True:
        print_header()
        print("1. İşlem Ekle (Gelir/Gider)")
        print("2. İşlemleri Listele")
        print("3. Mali Durum Raporu")
        print("4. Hesaplayıcılar")
        print("5. Maaşları Öde")
        print("6. Ana Menüye Dön")
        print("-" * 64)
        
        choice = get_input("Seçiminiz: ", int)
        
        if choice == 1: menu_add_transaction()
        elif choice == 2: menu_list_transactions()
        elif choice == 3: menu_financial_report()
        elif choice == 4: menu_calculators()
        elif choice == 5: menu_process_salaries()
        elif choice == 6: 
            print("\nFinans modülünden çıkılıyor..."); break
        else:
            pass

if __name__ == "__main__":
    start_app()