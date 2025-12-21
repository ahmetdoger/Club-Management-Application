import unittest
import os
import sys
sys.path.append(os.getcwd())
from modules.information.base import AthleteBase
from modules.information.implementations import ProfessionalAthlete, AmateurAthlete, YouthAthlete
from modules.information.repository import AthleteRepository
from modules.information.services import AthleteService
from modules.information.errors import ClubManagerError

# Sporcu yönetim sistemi modülünün fonksiyonel gereksinimlerini doğrulayan birim test sınıfı
class TestAthleteSystem(unittest.TestCase):
    # Her testten önce çalışarak temiz bir test veritabanı ve servis örneği oluşturur
    def setUp(self):
        self.test_db = "test_database.json"
        if os.path.exists(self.test_db):
            os.remove(self.test_db)  
        self.repo = AthleteRepository(self.test_db)
        self.service = AthleteService(self.repo)

    # Her testten sonra çalışarak oluşturulan geçici test dosyalarını sistemden temizler
    def tearDown(self):
        if os.path.exists(self.test_db):
            os.remove(self.test_db)   
        if os.path.exists("backup_test.json"):
            os.remove("backup_test.json")
        if os.path.exists("athletes_2099.json"):
            os.remove("athletes_2099.json")

    # Profesyonel sporcu sınıfının özelliklerini, maaş hesaplamasını ve metotlarını test eder
    def test_01_create_professional_athlete(self):
        print("\n[TEST 1] Profesyonel Sporcu Testi...")
        pro = ProfessionalAthlete(
            athlete_id=1, name="Mauro", surname="İcardi", age=32, gender="Male",
            height=180, weight=75, sport_branch="Football", status="Active",
            strong_side="Right", salary=600000, contract_end_date="2025"
        )
        self.assertEqual(pro.calculate_salary(), 725000)
        self.assertIn("Preferred Foot", pro.branch_strong_side())
        print("Başarılı.")

    # Amatör sporcu sınıfının transfer metodunu ve lisans numarası formatını test eder
    def test_02_create_amateur_athlete(self):
        print("\n[TEST 2] Amatör Sporcu Testi...")
        docs = {"has_clearance": True, "strong_side": "Right"}
        amateur = AmateurAthlete.transfer_from_local_club(
            "Ali", "Yılmaz", 19, "Male", 170, 65, "Basketball", docs
        )
        self.assertIsNotNone(amateur)
        self.assertTrue(amateur.licence_number.startswith("TUR-BAS"))
        print("Başarılı.")

    # Altyapı sporcusu için burs hesaplamasını ve yaş kategorisi belirleme mantığını test eder
    def test_03_create_youth_scholarship(self):
        print("\n[TEST 3] Altyapı Burs Testi...")
        info = {
            "name": "Can", "surname": "Kaya", "age": 12, "gender": "Male",
            "height": 150, "weight": 40, "strong_side": "Right",
            "branch": "Basketball", "parent_name": "Veli", "has_sibling": True
        }
        
        youth = YouthAthlete.register_with_scholarship_calc(info, exam_score=95)
        self.assertEqual(youth.calculate_salary(), 11000)
        self.assertEqual(YouthAthlete.age_category(12), "U14") 
        print("Başarılı.")

    # Servis katmanı üzerinden sporcu kaydı yapma ve arama işlevlerini test eder
    def test_04_service_operations(self):
        print("\n[TEST 4] Servis Kayıt/Arama Testi...")
        msg = self.service.register_athlete(
            "Servis", "Test", 20, "Female", 170, 60, "Volleyball", 
            "Professional", "Right", salary=5000
        )
        self.assertIn("sisteme eklendi", msg)
        results = self.service.search_athlete("Servis")
        self.assertEqual(len(results), 1)
        print("Başarılı.")

    # Repository sınıfındaki verilere dışarıdan doğrudan erişimin engellendiğini test eder
    def test_05_repository_private_access(self):
        print("\n[TEST 5] Kapsülleme Kontrolü...")
        with self.assertRaises(AttributeError):
            _ = self.repo.athletes  
        print("Başarılı (Gizli değişkene erişilemedi).")

    # Sınıf metotlarının doğru çalışıp çalışmadığını ve dosya işlemlerini test eder
    def test_06_class_methods_check(self):
        print("\n[TEST 6] Class Method ve Senaryo Testi...")
        season_service = AthleteService.start_season_mode(2025)
        self.assertIsInstance(season_service, AthleteService)
        with open("athletes.json", "w") as f:
            f.write("[]")
        backup_repo = AthleteRepository.from_backup("backup_test.json")
        self.assertTrue(os.path.exists("backup_test.json"))
        if os.path.exists("athletes.json"):
            os.remove("athletes.json")
        print("Başarılı (Sezon modu ve Yedekleme çalışıyor).")

    # Hatalı veri girişlerinde ve çakışmalı kayıtlarda sistemin doğru hata fırlattığını test eder
    def test_07_error_handling(self):
        print("\n[TEST 7] Hata Yönetimi (Error Handling)...")
        with self.assertRaises(ClubManagerError) as context:
            self.service.register_athlete("Hata", "Test", 150, "M", 180, 80, "Golf", "Professional", "R")
        self.assertEqual(context.exception.error_code, 2001) 
        self.repo.add(ProfessionalAthlete(100, "İlk", "Kayıt", 25, "M", 180, 80, "Golf", "Active", "R", 100, "2025"))
        with self.assertRaises(ClubManagerError) as context:
            self.repo.add(ProfessionalAthlete(100, "Kopya", "Kayıt", 25, "M", 180, 80, "Golf", "Active", "R", 100, "2025"))
        self.assertEqual(context.exception.error_code, 3001) 
        print(" Başarılı (Özel hatalar doğru fırlatılıyor).")

if __name__ == "__main__":
    unittest.main()