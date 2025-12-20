import random
from typing import List, Optional
from .repository import AthleteRepository
from .implementations import ProfessionalAthlete, AmateurAthlete, YouthAthlete

class AthleteService:
    def __init__(self, repository: AthleteRepository):
        self.repository = repository

    def register_athlete(self, name: str, age: int, gender: str,height: int, weight: int, branch: str, category: str, strong_side: str, **kwargs):
    
        
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
            
            new_athlete = ProfessionalAthlete(
                athlete_id=new_id,
                name=name,
                age=age,
                gender=gender,
                height=height, 
                weight=weight,  
                sport_branch=branch,
                status=default_status,
                strong_side=strong_side,
                salary=salary,
                contract_end_date=contract_end_date
            )

        elif category == "Amateur":
            licence_number = kwargs.get("licence_number", "PENDING-001")
            
            new_athlete = AmateurAthlete(
                athlete_id=new_id,
                name=name,
                age=age,
                gender=gender,
                height=height, 
                weight=weight,  
                sport_branch=branch,
                status=default_status,
                strong_side=strong_side,
                licence_number=licence_number
            )

        elif category == "Youth":
            guardian_name = kwargs.get("guardian_name", "Bilinmiyor")
            scholarship_amount = kwargs.get("scholarship_amount", 0.0)
            
            new_athlete = YouthAthlete(
                athlete_id=new_id,
                name=name,
                age=age,
                gender=gender,
                height=height, 
                weight=weight,  
                sport_branch=branch,
                status=default_status,
                strong_side=strong_side,
                guardian_name=guardian_name,
                scholarship_amount=scholarship_amount
            )

        else:
            raise ValueError(f"Geçersiz Kategori: {category}. (Beklenen: Professional, Amateur, Youth)")

        
        self.repository.add(new_athlete)
        return f"{name} ({gender}, {category},{height}cm,{weight}kg) başarıyla sisteme eklendi."

    def update_athlete_status(self, athlete_id: int, new_status: str):
        athlete = self.repository.get_by_id(athlete_id)
        if not athlete:
            print("Hata: Sporcu bulunamadı.")
            return False
        
        if athlete.status == "Suspended" and new_status == "Injured":
            print("İş Kuralı İhlali: Cezalı oyuncu cezası bitmeden sakat listesine alınamaz.")
            return False

        try:
            athlete.status = new_status
            self.repository.update(athlete_id, {"status": new_status})
            return True
        except ValueError as e:
            print(f"Güncelleme Hatası: {e}")
            return False

    def list_athletes_by_branch(self, branch: str):
        return self.repository.filter_by_branch(branch)

    def search_athlete(self, keyword: str):
        all_athletes = self.repository.get_all()
        results = []
        for athlete in all_athletes:
            if str(keyword).isdigit() and athlete.athlete_id == int(keyword):
                results.append(athlete)
            elif str(keyword).lower() in athlete.name.lower():
                results.append(athlete)
        return results

    def filter_athletes_by_criteria(self, min_age=0, status=None, gender=None):
        """
        [GÜNCELLEME] Gender kriteri de eklendi.
        """
        all_athletes = self.repository.get_all()
        filtered = []
        for a in all_athletes:
            if a.age < min_age:
                continue
            if status is not None and a.status != status:
                continue
            if gender is not None and a.gender.lower() != gender.lower():
                continue
            filtered.append(a)
        return filtered

    @staticmethod
    def validate_athlete_age(age: int) -> bool:
        return 5 <= age <= 100

    @classmethod
    def get_service_info(cls):
        return "AthleteService - Sporcu Kayıt ve Takip Modülü v1.0"



     