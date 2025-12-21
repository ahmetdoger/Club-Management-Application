import os
import sys

# Dosya yollarını ayarlıyoruz (Proje ana dizinini görmesi için)
sys.path.append(os.getcwd())

from modules.information.implementations import ProfessionalAthlete, AmateurAthlete, YouthAthlete
from modules.information.repository import AthleteRepository
from modules.information.services import AthleteService

def run_demo_scenario():
    print("================================================================")
    print("      PLAYER INFORMATION MODULE - SCENARIO DEMO")
    print("================================================================\n")

    # 1. SETUP: Demo için geçici bir servis başlatalım
    print("[1] SYSTEM SETUP")
    demo_db = "demo_scenario.json"
    if os.path.exists(demo_db): os.remove(demo_db) # Temiz başlangıç
    
    repo = AthleteRepository(demo_db)
    service = AthleteService(repo)
    print(f"   -> Repository connected to {demo_db}")
    print(f"   -> Service initialized.\n")

    # 2. SUBCLASS INSTANTIATION (Farklı Sınıf Örnekleri)
    print("[2] CREATING ATHLETE INSTANCES (SUBCLASSES)")
    
    # A. Profesyonel Sporcu (Yüksek maaş, sözleşmeli)
    pro_athlete = ProfessionalAthlete(
        athlete_id=101, name="Cristiano", surname="Ronaldo", age=38, gender="Male",
        height=187, weight=83, sport_branch="Football", status="Active",
        strong_side="Right", salary=200000000.0, contract_end_date="2025-06-30"
    )
    print(f"   -> Professional Created: {pro_athlete.name} (Salary based)")

    # B. Amatör Sporcu (Maaş yok, sadece lisans var)
    amateur_athlete = AmateurAthlete(
        athlete_id=102, name="Local", surname="Hero", age=22, gender="Male",
        height=175, weight=70, sport_branch="Tennis", status="Active",
        strong_side="Right", licence_number="TENNIS-TR-001"
    )
    print(f"   -> Amateur Created: {amateur_athlete.name} (No Salary)")

    # C. Altyapı Sporcusu (Burslu)
    youth_athlete = YouthAthlete(
        athlete_id=103, name="Future", surname="Star", age=14, gender="Female",
        height=165, weight=55, sport_branch="Volleyball", status="Active",
        strong_side="Left", guardian_name="Mother Star", scholarship_amount=5000.0
    )
    print(f"   -> Youth Created: {youth_athlete.name} (Scholarship based)\n")

    # 3. POLYMORPHISM SHOWCASE (Polimorfizm Gösterimi)
    # Hocanın "Polimorfizm gösteren bir liste" isteği burada karşılanıyor.
    print("[3] POLYMORPHISM IN ACTION")
    print("   (Iterating through a single list, calling same methods, getting different behaviors)")
    print("-" * 70)
    print(f"   {'NAME':<20} | {'ROLE':<20} | {'CALCULATED COST'}")
    print("-" * 70)

    # Hepsini tek bir listeye atıyoruz (Base class referansı gibi davranırlar)
    roster_list = [pro_athlete, amateur_athlete, youth_athlete]

    for athlete in roster_list:
        # DİKKAT: Hepsi için aynı metodu (.calculate_salary) çağırıyoruz.
        # Ama Pro vergi hesabı yapıyor, Amatör 0 dönüyor, Youth burs dönüyor.
        # İŞTE POLİMORFİZM BUDUR.
        cost = athlete.calculate_salary()
        role = type(athlete).__name__ # Sınıf ismini alır
        
        print(f"   {athlete.name:<20} | {role:<20} | {cost:,.2f} TL")
        
        # Ayrıca güçlü taraf (strong_side) da branşa göre değişiyor
        print(f"      -> Detail: {athlete.branch_strong_side()}")
    print("-" * 70 + "\n")

    # 4. PERSISTENCE (Veritabanına Kayıt)
    print("[4] SAVING TO DATABASE via SERVICE")
    # Oluşturduğumuz nesneleri servise gönderip kaydediyoruz
    service.repository.add(pro_athlete)
    service.repository.add(amateur_athlete)
    service.repository.add(youth_athlete)
    
    saved_count = len(service.repository.get_all())
    print(f"   -> {saved_count} athletes successfully saved to JSON.\n")

    # 5. BUSINESS LOGIC DEMO (Transfer / Durum Güncelleme)
    print("[5] BUSINESS LOGIC: STATUS UPDATE")
    print(f"   -> Current Status of {pro_athlete.name}: {pro_athlete.status}")
    
    service.update_athlete_status(101, "Injured")
    updated_pro = service.repository.get_by_id(101)
    
    print(f"   -> New Status: {updated_pro['status']}")
    print("   -> Status update logic verified.\n")

    print("================================================================")
    print("      DEMO COMPLETED SUCCESSFULLY")
    print("================================================================")

    # Temizlik (İsteğe bağlı, dosyayı görmek istersen burayı silebilirsin)
    # if os.path.exists(demo_db): os.remove(demo_db)

if __name__ == "__main__":
    run_demo_scenario()