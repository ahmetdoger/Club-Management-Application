import time
from .services.manager import FinanceManager
from .services.analyzer import FinancialAnalyzer
from .services.calculator import (
    LateFeeCalculator, 
    TaxDeductionCalculator, 
    SalaryCalculator
)
from .data.constants import TransactionType, IncomeCategory, ExpenseCategory

def print_step(step_name):
    print(f"\n{'='*10} {step_name} {'='*10}")
    time.sleep(0.5)

# Tüm özellikleri test eden demoyu başlatan fonksiyon
def run_demo_scenario():

    print(">>> FİNANS MODÜLÜ DEMO SENARYOSU BAŞLATILIYOR... <<<")
    
    # 1. YÖNETİCİ BAŞLATILIYOR
    manager = FinanceManager()
    analyzer = FinancialAnalyzer()
    
    # 2. VERİ GİRİŞİ SİMÜLASYONU
    print_step("ADIM 1: İşlem Kayıtları (Transaction)")
    
    # Gelir Ekleme
    print("- Sponsorluk geliri ekleniyor...")
    manager.add_transaction(
        TransactionType.INCOME.value,
        IncomeCategory.SPONSORSHIP.value,
        15000,
        "Ana Sponsor: TechCorp"
    )
    
    # Gider Ekleme
    print("- Personel maaşı ekleniyor...")
    manager.add_transaction(
        TransactionType.EXPENSE.value,
        ExpenseCategory.SALARY.value,
        8500,
        "Antrenör Maaşı (Ekim)"
    )
    
    print("✔ Veri girişi tamamlandı.")

    # 3. POLİMORFİZM GÖSTERİMİ 
    print_step("ADIM 2: Polimorfizm (Çok Biçimlilik) Gösterimi")
    print("Farklı hesaplayıcılar aynı 'calculate' metodunu farklı yorumluyor:\n")
    
    # Farklı sınıflardan nesneleri tek bir listede tutuyor
    calculators = [
        LateFeeCalculator(daily_rate=0.01),      # Gecikme Faizi Hesaplayıcı
        TaxDeductionCalculator(tax_rate=0.18),   # Vergi Hesaplayıcı
        SalaryCalculator()                       # Maaş Hesaplayıcı
    ]
    
    base_amount = 5000
    print(f"Baz Tutar: {base_amount} TL")
    
    for calc in calculators:
        # Hepsi BaseFinancialCalculator'dan türediği için calculate metoduna sahip
        # Ama hepsi farklı sonuç üretiyor > Polimorfizm
        result = calc.calculate(base_amount, days_late=10)
        
        # Sınıf ismini alıp ekrana yazar
        class_name = type(calc).__name__
        print(f" -> {class_name:<25} Sonuç: {result:>10.2f} TL")

    print_step("ADIM 3: Raporlama ve Analiz")
    
    summary = manager.get_financial_summary()
    status = analyzer.get_budget_status()
    
    print(f"Toplam Gelir: {summary['toplam_gelir']} TL")
    print(f"Toplam Gider: {summary['toplam_gider']} TL")
    print(f"BÜTÇE DURUMU: {status['durum']} ({status['net_bakiye']} TL)")
    
    print("\n>>> DEMO BAŞARIYLA TAMAMLANDI <<<")

if __name__ == "__main__":
    run_demo_scenario()