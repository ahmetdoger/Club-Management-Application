from .base import AthleteBase
from datetime import datetime 
import random
class ProfessionalAthlete(AthleteBase):
    def __init__(self, athlete_id, name, age, sport_branch, status,salary,contract_end_date):
        super().__init__(athlete_id, name, age, sport_branch, status)
        self.__salary = salary
        self.__contract_end_date = contract_end_date
    
    def calculate_pro_athlete_cost(self):
        tax = self.calculate_pro_athlete_cost(self.__salary)
        insurance_cost = 0
        return self.__salary + tax + insurance_cost
    
    def athlete_strong_side(self):
        branch = self.sport_branch
        if "football" in branch:
            return f"Preferred Foot : {self.__athlete_strong_side}"
        elif "basketball" or "volleyball" in branch:
            return f"Shooting Hand: {self.__athlete_strong_side}"
        else:
            return f"Dominant Side: {self.__athlete_strong_side}"
        
@property
def salary(self):
    return self.__salary

@staticmethod
def calculate_tax(salary):
    if salary > 500000:
        return salary * 0.20
    return salary * 0.15

@classmethod
def renew_contract(cls, current_athlete_data, performance_stats):
        
        name = current_athlete_data.get("name")
        age = current_athlete_data.get("age")
        current_salary = current_athlete_data.get("salary")
          
        if age >= 38:
            print(f"Sözleşme Yenilenmedi: {name} emeklilik yaşına geldi.")
            return None

        matches_played = performance_stats.get("matches_played", 0)
        if matches_played < 20:
            print(f"Sözleşme Yenilenmedi: {name} yeterli maç sayısına ulaşamadı ({matches_played}).")
            return None
        
        rating = performance_stats.get("rating", 0) 
        if rating >= 8.5:
            new_salary = current_salary * 1.25 
            duration = 3 
        elif rating >= 6.0:
            new_salary = current_salary * 1.10 
            duration = 2
        else:
            new_salary = current_salary * 0.90 
            duration = 1

        new_end_date = f"{datetime.now().year + duration}-06-30"
        print(f"Sözleşme Yenilendi: {name} - Yeni Maaş: {new_salary:.2f} ({duration} Yıl)")

        return cls(
            athlete_id=current_athlete_data.get("id"), # ID değişmez
            name=name,
            age=age + 1, 
            sport_branch=current_athlete_data.get("branch"),
            status="Active",
            salary=new_salary,
            contract_end_date=new_end_date,
            dominant_side=current_athlete_data.get("dominant_side")
        )

class AmateurAthlete(AthleteBase):
    def __init__(self, athlete_id, name, age, sport_branch, status,licence_number):
        super().__init__(athlete_id, name, age, sport_branch, status)
        self.__licence_number = licence_number

    def calculate_amateur_athlete_cost(self):
        base_licence_fee = 0
        transport_support = 0

        return base_licence_fee + transport_support
     
    def athlete_strong_side(self):
        branch = self.sport_branch
        if "football" in branch:
            return f"Preferred Foot : {self.__athlete_strong_side}"
        elif "basketball" or "volleyball" in branch:
            return f"Shooting Hand: {self.__athlete_strong_side}"
        else:
            return f"Dominant Side: {self.__athlete_strong_side}"
    
    @staticmethod
    def check_transport_distance(distance_km):
        return distance_km > 10
     
    @classmethod
    def transfer_from_local_club(cls, name, age, branch, prev_club_doc):
        is_cleared = prev_club_doc.get("has_clearance", False)
        
        if not is_cleared:
            print(f"Transfer Reddedildi: {name} için {prev_club_doc.get('club_name')} kulübünden temiz kağıdı alınamadı.")
            return None
        
        penalty_points = prev_club_doc.get("penalty_points", 0)
        if penalty_points > 5:
            print(f"Transfer Reddedildi: {name} oyuncusunun disiplin cezası çok yüksek ({penalty_points}).")
            return None

        print(f"Transfer Onaylandı: {name} amatör takıma katıldı.")
        
        new_id = random.randint(3000, 4999)
        license_no = f"TUR-{branch[:3].upper()}-{random.randint(100,999)}"

        return cls(
            athlete_id=new_id,
            name=name,
            age=age,
            sport_branch=branch,
            status="Active",
            license_number=license_no,
            has_job=prev_club_doc.get("has_job", False)
        ) 
    
class YoungAthlete(AthleteBase):
    def __init__(self, athlete_id, name, age, sport_branch, status,guardian_name,scholarship_amount):
        super().__init__(athlete_id, name, age, sport_branch, status)
        self.__guardian_name = guardian_name
        self.__scholarship_amount = scholarship_amount    
    
    def calculuate_youth_athlete_cost(self):
        return self.__scholarship_amount
    
    def athlete_strong_side(self):
        branch = self.sport_branch
        if "football" in branch:
            return f"Preferred Foot : {self.__athlete_strong_side}"
        elif "basketball" or "volleyball" in branch:
            return f"Shooting Hand: {self.__athlete_strong_side}"
        else:
            return f"Dominant Side: {self.__athlete_strong_side}"
        
    @property
    def guardian_name(self):
        return self.__guardian_name
    
    @staticmethod
    def age_category(age):
        if age < 10 :
            return "Minik Takım"
        if age < 13 :
            return "U12"
        if age < 15:
            return "U14"
        if age < 17:
            return "U16"
        if age < 19:
            return "U19"
        return "As takım adayı"

    @classmethod
    def register_with_scholarship_calc(cls, student_info, exam_score):
        
        name = student_info.get("name")
        age = student_info.get("age")
        
        if age >= 18:
            print(f"Kayıt Başarısız: {name} (Yaş: {age}) altyapı yaş sınırını aşıyor.")
            return None

        scholarship = 0
        base_fee = 10000 
        
        if exam_score >= 90:
            scholarship = base_fee 
            print(f"{name} Tam Burs kazandı!")
        elif exam_score >= 75:
            scholarship = base_fee * 0.50 
            print(f"{name} %50 Burs kazandı.")
    
        if student_info.get("has_sibling", False):
            scholarship += base_fee * 0.10
            
        return cls(
            athlete_id=random.randint(500, 999),
            name=name,
            age=age,
            sport_branch=student_info.get("branch", "General"),
            status="Active",
            guardian_name=student_info.get("parent_name"),
            scholarship_amount=scholarship
        )
    











