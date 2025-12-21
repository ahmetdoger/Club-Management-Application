print("--- TEST PROCESS STARTING ---")

import unittest
import os
import sys


sys.path.append(os.getcwd())


from .base import AthleteBase
from .implementations import ProfessionalAthlete, AmateurAthlete, YouthAthlete
from .repository import AthleteRepository
from .services import AthleteService

class TestAthleteSystem(unittest.TestCase):
    
    
    def setUp(self):
        self.test_db_name = "test_database.json"
        
       
        if os.path.exists(self.test_db_name):
            os.remove(self.test_db_name)
            
       
        self.repo = AthleteRepository(self.test_db_name)
        self.service = AthleteService(self.repo)

    def tearDown(self):
        if os.path.exists(self.test_db_name):
            os.remove(self.test_db_name)

  
    def test_create_professional_icardi(self):
        print("\n[TEST 1] Creating Professional Profile (Icardi)...")
        
        # Sporcuyu oluşturuyoruz
        icardi = ProfessionalAthlete(
            athlete_id=99,
            name="Mauro",
            surname="Icardi",
            age=30,
            gender="Male",
            height=181,
            weight=75,
            sport_branch="Football",
            status="Active",
            strong_side="Right",
            salary=10000000.0,
            contract_end_date="2026-05-30"
        )

    
        self.assertEqual(icardi.name, "Mauro")
        self.assertEqual(icardi.surname, "Icardi")
        self.assertEqual(icardi.age, 30)
        self.assertEqual(icardi.gender, "Male")
        self.assertEqual(icardi.height, 181)
        self.assertEqual(icardi.weight, 75)
        self.assertEqual(icardi.sport_branch, "Football")
        
        # Maaş hesabı kontrolü (Salary + 20% Tax)
        expected_salary = 10000000.0 + (10000000.0 * 0.20)
        self.assertEqual(icardi.calculate_salary(), expected_salary)
        
        # Futbolcu olduğu için 'Preferred Foot' yazmalı
        strong_side_msg = icardi.branch_strong_side()
        self.assertIn("Preferred Foot", strong_side_msg)
        print("   -> Icardi test passed.")

   
    def test_create_amateur_eda(self):
        print("\n[TEST 2] Creating Amateur Profile (Eda Erdem)...")
        
       
        prev_club_docs = {
            "has_clearance": True,      #
            "penalty_points": 0,        
            "strong_side": "Right"      
        }
        
        # Transfer işlemini deniyoruz
        eda = AmateurAthlete.transfer_from_local_club(
            name="Eda",
            surname="Erdem",
            age=35,
            gender="Female",
            height=190,
            weight=74,
            branch="Volleyball",
            prev_club_doc=prev_club_docs
        )
        
        
        self.assertIsNotNone(eda)
        
        
        self.assertEqual(eda.name, "Eda")
        self.assertEqual(eda.surname, "Erdem")
        self.assertEqual(eda.branch_strong_side(), "Shooting Hand: Right")
        
      
        self.assertEqual(eda.calculate_salary(), 0)
        print("   -> Eda Erdem test passed.")


    def test_create_youth_scholarship(self):
        print("\n[TEST 3] Youth Scholarship Exam Test...")
        
        # Öğrenci bilgileri
        student_info = {
            "name": "Cedi",
            "surname": "Osman",
            "age": 14,
            "gender": "Male",
            "height": 195,
            "weight": 85,
            "strong_side": "Right",
            "branch": "Basketball",
            "parent_name": "Father Osman",
            "has_sibling": False # Kardeşi yok
        }
        
       
        youth_player = YouthAthlete.register_with_scholarship_calc(student_info, exam_score=95)
        
        
        self.assertEqual(youth_player.calculate_salary(), 10000)
        self.assertEqual(youth_player.guardian_name, "Father Osman")
        
       
        category = YouthAthlete.age_category(14)
        self.assertEqual(category, "U16")
        print("   -> Youth scholarship test passed.")

  
    def test_service_register_and_search(self):
        print("\n[TEST 4] Service Registration & Search Scenario...")
        
        
        result_message = self.service.register_athlete(
            name="Fernando",
            surname="Muslera",
            age=36,
            gender="Male",
            height=190,
            weight=84,
            branch="Football",
            category="Professional",
            strong_side="Right",
            salary=5000000.0
        )
        
       
        self.assertIn("başarıyla", result_message)
        
        
        search_results = self.service.search_athlete("Muslera")
        
        
        self.assertEqual(len(search_results), 1)
        
       
        found_athlete = search_results[0]
        self.assertEqual(found_athlete['surname'], "Muslera")
        print("   -> Service register/search test passed.")

   
    def test_update_and_delete(self):
        print("\n[TEST 5] CRUD (Update & Delete) Scenario...")
        
       
        self.service.register_athlete(
            "DeleteMe", "Person", 20, "Male", 180, 80, "Tennis", "Amateur", "Right"
        )
        
      
        athlete_list = self.service.search_athlete("DeleteMe")
        athlete_data = athlete_list[0]
        athlete_id = athlete_data['athlete_id']
        
        
        update_success = self.service.update_athlete_status(athlete_id, "Injured")
        self.assertTrue(update_success)
        
        
        updated_data = self.repo.get_by_id(athlete_id)
        self.assertEqual(updated_data['status'], "Injured")
        
      
        delete_success = self.repo.delete_by_id(athlete_id)
        self.assertTrue(delete_success)
        
       
        deleted_data = self.repo.get_by_id(athlete_id)
        self.assertIsNone(deleted_data)
        print("   -> Update & Delete test passed.")


if __name__ == "__main__":
    unittest.main()