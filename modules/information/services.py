import random
from typing import List, Optional
from .repository import AthleteRepository
from .implementations import ProfessionalAthlete, AmateurAthlete, YouthAthlete

class AthleteService:
    def __init__(self, repository: AthleteRepository):
        self.__repository = repository

    def register_athlete(self, name: str, surname: str, age: int, gender: str, height: int, weight: int, branch: str, category: str, strong_side: str, **kwargs):
        if not self.validate_athlete_age(age):
            raise ValueError(f"Hata: {age} yaşı kayıt için uygun değil (5-100 arası).")
        
        if height < 100 or height > 250:
            print(f"Uyarı: Girilen boy ({height} cm) olağandışı.")
        
        new_id = random.randint(10000, 99999)
        default_status = "Active"
        new_athlete = None

        if category == "Professional":
            salary = kwargs.get("salary", 0.0)
            contract_end_date = kwargs.get("contract_end_date", "2025-12-31")
            new_athlete = ProfessionalAthlete(new_id, name, surname, age, gender, height, weight, branch, default_status, strong_side, salary, contract_end_date)

        elif category == "Amateur":
            licence_number = kwargs.get("licence_number", "PENDING-001")
            new_athlete = AmateurAthlete(new_id, name, surname, age, gender, height, weight, branch, default_status, strong_side, licence_number)

        elif category == "Youth":
            guardian_name = kwargs.get("guardian_name", "Bilinmiyor")
            scholarship_amount = kwargs.get("scholarship_amount", 0.0)
            new_athlete = YouthAthlete(new_id, name, surname, age, gender, height, weight, branch, default_status, strong_side, guardian_name, scholarship_amount)
        else:
            raise ValueError(f"Geçersiz Kategori: {category}")

        self.__repository.add(new_athlete)
        return f"{name} {surname} ({category}) sisteme eklendi."

    def update_athlete_status(self, athlete_id: int, new_status: str):
        athlete = self.__repository.get_by_id(athlete_id)
        if not athlete:
            return False
        if athlete.get('status') == "Suspended" and new_status == "Injured":
            print("İş Kuralı İhlali.")
            return False
        try:
            self.__repository.update(athlete_id, {"status": new_status})
            return True
        except ValueError:
            return False

    def list_athletes_by_branch(self, branch: str):
        return self.__repository.get_by_branch(branch)

    def search_athlete(self, keyword):
        all_athletes = self.__repository.get_all()
        results = []
        for athlete in all_athletes:
            
            a_id = str(athlete.get('athlete_id', ''))
            a_name = athlete.get('name', '').lower()
            a_surname = athlete.get('surname', '').lower() 
            
            search_key = str(keyword).lower()

            
            if str(keyword).isdigit() and a_id == str(keyword):
                results.append(athlete)
            
            elif search_key in a_name or search_key in a_surname:
                results.append(athlete)
                
        return results

    def filter_athletes_by_criteria(self, min_age=0, status=None, gender=None):
        all_athletes = self.__repository.get_all()
        filtered = []
        for a in all_athletes:
            if a.get('age', 0) < min_age: continue
            if status and a.get('status') != status: continue
            if gender and a.get('gender', '').lower() != gender.lower(): continue
            filtered.append(a)
        return filtered

    @staticmethod
    def validate_athlete_age(age: int) -> bool:
        return 5 <= age <= 100