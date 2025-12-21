import os
import sys

# Proje ana dizinini yola ekle
sys.path.append(os.getcwd())

from modules.information.implementations import ProfessionalAthlete, AmateurAthlete, YouthAthlete
from modules.information.repository import AthleteRepository
from modules.information.services import AthleteService

def run_demo_scenario():
    print("================================================================")
    print("      SPOR KULÜBÜ YÖNETİM SİSTEMİ - DEMO SENARYOSU")
    print("================================================================\n")

    print("[1] SİSTEM KURULUMU VE CLASS METHOD KULLANIMI")
    
    # SENARYO: Sezonluk yönetim modunu (Class Method) kullanarak sistemi başlatıyoruz.
    # Bu özellik hocanın istediği 'Class Method' şartını sağlar.
    service = AthleteService.start_season_mode(2025)
    
    # Servis içindeki repository'ye erişmek için property kullanılabilir veya
    # demo olduğu için direkt repo üzerinden işlem yapılabilir.
    # Ancak burada servis üzerinden gidiyoruz.
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

    
    print("[4] VERİTABANI İŞLEMLERİ (ENCAPSULATION TESTİ)")
    
    # Servis üzerinden kayıt (Servis repository'yi gizlediği için kendi metoduyla ekliyoruz)
    # Not: Demo'da doğrudan repo.add yapmak yerine servisi kullanmak daha doğrudur.
    # Ancak manuel ekleme yapmak istersek, servise bir 'add_direct' metodu gerekebilir
    # veya service.register_athlete metodu parametrelerle çalışır.
    
    # Burada nesneleri doğrudan repository'e eklemek için servise geçici bir erişim yolu açıyoruz
    # (Veya service.register_athlete ile tek tek ekleyebiliriz ama nesneleri yukarıda oluşturduk)
    
    # Hızlı çözüm: Servis sınıfına (services.py) şu property'yi eklediğini varsayıyoruz:
    # @property
    # def repository(self): return self.__repository
    
    # EĞER services.py'ye property eklemediysen hata almamak için exception handle ediyoruz:
    try:
        service.repository.add(pro_athlete)
        service.repository.add(amateur_athlete)
        service.repository.add(youth_athlete)
        print(f"   -> Sporcular başarıyla veritabanına kaydedildi.")
    except AttributeError:
        print("   UYARI: Service içinde repository gizli (private). Erişim için property eklenmeli.")
        print("   Alternatif olarak service.register_athlete() kullanılmalı.")

    print("\n[5] İŞ MANTIĞI (BUSINESS LOGIC) - STATÜ GÜNCELLEME")
    print(f"   -> {pro_athlete.name} şu anki durumu: {pro_athlete.status}")
    
    service.update_athlete_status(101, "Injured")
    
    # Kontrol etmek için tekrar çekiyoruz
    updated_athlete = service.search_athlete("101")
    if updated_athlete:
        print(f"   -> {pro_athlete.name} yeni durumu: {updated_athlete[0]['status']}")
    
    print("\n================================================================")
    print("      DEMO BAŞARIYLA TAMAMLANDI")
    print("================================================================")

if __name__ == "__main__":
    run_demo_scenario()