import os
import sys

# Proje ana dizinini yola ekle
sys.path.append(os.getcwd())

from modules.information.implementations import ProfessionalAthlete, AmateurAthlete, YouthAthlete
from modules.information.services import AthleteService
# YENİ: Hata sınıfını import ediyoruz ki demo sırasında yakalayabilelim
from modules.information.errors import ClubManagerError

def run_demo_scenario():
    print("================================================================")
    print("      SPOR KULÜBÜ YÖNETİM SİSTEMİ - DEMO SENARYOSU")
    print("================================================================\n")

    print("[1] SİSTEM KURULUMU VE CLASS METHOD KULLANIMI")
    
    # SENARYO: Sezonluk yönetim modunu (Class Method) kullanarak sistemi başlatıyoruz.
    service = AthleteService.start_season_mode(2025)
    print(f"   -> Sistem 2025 sezonu için hazırlandı.\n")

    
    print("[2] SPORCU NESNELERİNİN OLUŞTURULMASI (SUBCLASSES)")
    
    # Profesyonel Sporcu (Maaşlı)
    pro_athlete = ProfessionalAthlete(
        athlete_id=101, name="Mauro", surname="Icardi", age=31, gender="Male",
        height=181, weight=75, sport_branch="Football", status="Active",
        strong_side="Right", salary=10000000.0, contract_end_date="2026-06-30"
    )
    print(f"   -> Profesyonel Eklendi: {pro_athlete.name} (Maaşlı)")

    # Amatör Sporcu (Lisanslı)
    amateur_athlete = AmateurAthlete(
        athlete_id=102, name="Filenin", surname="Sultanı", age=24, gender="Female",
        height=190, weight=70, sport_branch="Volleyball", status="Active",
        strong_side="Right", licence_number="VOL-TR-001"
    )
    print(f"   -> Amatör Eklendi: {amateur_athlete.name} (Sadece Lisans Bedeli)")

    # Altyapı Sporcusu (Burslu)
    youth_athlete = YouthAthlete(
        athlete_id=103, name="Geleceğin", surname="Yıldızı", age=14, gender="Male",
        height=175, weight=60, sport_branch="Basketball", status="Active",
        strong_side="Left", guardian_name="Veli Bey", scholarship_amount=7500.0
    )
    print(f"   -> Altyapı Eklendi: {youth_athlete.name} (Burslu)\n")

 
    print("[3] POLİMORFİZM ÖRNEĞİ (ÇOK BİÇİMLİLİK)")
    print("   (Aynı listedeki farklı türden nesnelerin 'calculate_salary' metoduna farklı tepki vermesi)")
    print("-" * 75)
    print(f"   {'İSİM':<20} | {'STATÜ':<20} | {'MALİYET HESABI'}")
    print("-" * 75)

    roster = [pro_athlete, amateur_athlete, youth_athlete]

    for athlete in roster:
        # Polimorfizm burada gerçekleşiyor: Hepsi aynı metodu çağırıyor ama farklı hesap yapıyor
        cost = athlete.calculate_salary()
        role = type(athlete).__name__
        
        print(f"   {athlete.name:<20} | {role:<20} | {cost:,.2f} TL")
        print(f"      -> Detay: {athlete.branch_strong_side()}")
    
    print("-" * 75 + "\n")

    
    print("[4] VERİTABANI İŞLEMLERİ VE HATA YÖNETİMİ")
    
    try:
        # Service içindeki repository özelliğini kullanarak ekleme yapıyoruz
        service.repository.add(pro_athlete)
        service.repository.add(amateur_athlete)
        service.repository.add(youth_athlete)
        print(f"   -> Sporcular başarıyla veritabanına kaydedildi.")
        
        # --- YENİ: Mükerrer Kayıt Hatası Testi ---
        print("   -> TEST: Aynı ID (101) ile tekrar ekleme deneniyor...")
        service.repository.add(pro_athlete) # Bu hata fırlatmalı!
        
    except ClubManagerError as e:
        # Hata yakalandığında program çökmez, mesaj verir
        print(f"   [HATA YAKALANDI] {e.message}")
        print(f"   -> Hata Kodu: {e.error_code} (Sistem çalışmaya devam ediyor.)")

    print("\n[5] İŞ MANTIĞI VE KURAL İHLALİ TESTİ")
    print(f"   -> {pro_athlete.name} başlangıç durumu: {pro_athlete.status}")
    
    # 1. Başarılı Güncelleme
    service.update_athlete_status(101, "Suspended")
    print(f"   -> Durum güncellendi: Active -> Suspended")
    
    # 2. Hatalı Güncelleme Denemesi (Cezalı -> Sakat yasaktır)
    print("   -> TEST: Cezalı oyuncu 'Sakat' (Injured) statüsüne alınmaya çalışılıyor...")
    
    try:
        service.update_athlete_status(101, "Injured")
    except ClubManagerError as e:
        print(f"   [HATA YAKALANDI] {e.message}")
        print(f"   -> İş kuralı başarıyla korundu.")
    
    print("\n================================================================")
    print("      DEMO BAŞARIYLA TAMAMLANDI")
    print("================================================================")
    
    # Temizlik (Oluşan dosya silinsin)
    if os.path.exists("athletes_2025.json"):
        os.remove("athletes_2025.json")

if __name__ == "__main__":
    run_demo_scenario()