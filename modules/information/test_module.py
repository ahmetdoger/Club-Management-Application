import unittest
import os
import sys

# Modül yolunu ekle
sys.path.append(os.getcwd())

from modules.information.base import AthleteBase
from modules.information.implementations import ProfessionalAthlete, AmateurAthlete, YouthAthlete
from modules.information.repository import AthleteRepository
from modules.information.services import AthleteService

class TestAthleteSystem(unittest.TestCase):
    
    def setUp(self):
        """Her testten önce çalışır: Temiz bir ortam hazırlar."""
        self.test_db = "test_database.json"
        
       
        if os.path.exists(self.test_db):
            os.remove(self.test_db)
            
        
        self.repo = AthleteRepository(self.test_db)
        self.service = AthleteService(self.repo)

    def tearDown(self):
        
        if os.path.exists(self.test_db):
            os.remove(self.test_db)
            
        
        if os.path.exists("backup_test.json"):
            os.remove("backup_test.json")
        if os.path.exists("athletes_2099.json"):
            os.remove("athletes_2099.json")

    def test_01_create_professional_athlete(self):
        print("\n[TEST 1] Profesyonel Sporcu Testi...")
        
        pro = ProfessionalAthlete(
            athlete_id=1, name="Test", surname="Pro", age=25, gender="Male",
            height=180, weight=75, sport_branch="Football", status="Active",
            strong_side="Left", salary=100.0, contract_end_date="2025"
        )
        
        self.assertEqual(pro.calculate_salary(), 115.0)
        self.assertIn("Preferred Foot", pro.branch_strong_side())
        print("   -> Başarılı.")

    def test_02_create_amateur_athlete(self):
        print("\n[TEST 2] Amatör Sporcu Testi...")
        
        docs = {"has_clearance": True, "strong_side": "Right"}
        amateur = AmateurAthlete.transfer_from_local_club(
            "Ali", "Veli", 19, "Male", 170, 65, "Tennis", docs
        )
        
        self.assertIsNotNone(amateur)
        self.assertTrue(amateur.licence_number.startswith("TUR-TEN"))
        print("   -> Başarılı.")

    def test_03_create_youth_scholarship(self):
        print("\n[TEST 3] Altyapı Burs Testi...")
        
        info = {
            "name": "Can", "surname": "Su", "age": 12, "gender": "Male",
            "height": 150, "weight": 40, "strong_side": "Right",
            "branch": "Basketball", "parent_name": "Veli", "has_sibling": True
        }
        
        youth = YouthAthlete.register_with_scholarship_calc(info, exam_score=95)
        
        self.assertEqual(youth.calculate_salary(), 11000)
        self.assertEqual(YouthAthlete.age_category(12), "U14") # 12 yaş U14'e girer (12 < 14)
        print("   -> Başarılı.")

    def test_04_service_operations(self):
        print("\n[TEST 4] Servis Kayıt/Arama Testi...")
        
        msg = self.service.register_athlete(
            "Servis", "Test", 20, "Female", 170, 60, "Volleyball", 
            "Professional", "Right", salary=5000
        )
        
        self.assertIn("sisteme eklendi", msg)
        results = self.service.search_athlete("Servis")
        self.assertEqual(len(results), 1)
        print("   -> Başarılı.")

    def test_05_repository_private_access(self):
        print("\n[TEST 5] Kapsülleme Kontrolü...")
        
        with self.assertRaises(AttributeError):
            _ = self.repo.athletes 
            
        print("   -> Başarılı (Gizli değişkene erişilemedi).")

    def test_06_class_methods_check(self):
        """Yeni eklenen Class Method'ların testi (YENİ)."""
        print("\n[TEST 6] Class Method ve Senaryo Testi...")
        
        season_service = AthleteService.start_season_mode(2099)
        self.assertIsInstance(season_service, AthleteService)
        
        self.repo.add(ProfessionalAthlete(99, "Yedek", "Test", 30, "M", 180, 80, "Golf", "Active", "R", 100, "2025"))
        
        backup_repo = AthleteRepository.from_backup("backup_test.json")
        self.assertTrue(os.path.exists("backup_test.json"))
        self.assertIsNotNone(backup_repo.get_by_id(99))
        
        print("   -> Başarılı (Sezon modu ve Yedekleme çalışıyor).")

if __name__ == "__main__":
    unittest.main()