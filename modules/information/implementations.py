from .base import AthleteBase
import random
import datetime
from .errors import (
    raise_retirement_error, 
    raise_performance_error, 
    raise_clearance_error, 
    raise_penalty_error
)

# Profesyonel sporcu özelliklerini ve kurallarını barındıran sınıf
class ProfessionalAthlete(AthleteBase):
    # Profesyonel sporcu nesnesini başlatır
    def __init__(self, athlete_id, name, surname, age, gender, height, weight, sport_branch, status, strong_side, salary, contract_end_date):
        super().__init__(athlete_id, name, surname, age, gender, height, weight, sport_branch, status, strong_side)
        self.__salary = salary
        self.__contract_end_date = contract_end_date
            
    # Maaş üzerinden vergi miktarını hesaplar
    @staticmethod
    def calculate_tax(salary):
        if salary > 500000: return salary * 0.20
        return salary * 0.15

    # Maaşa vergi ve sigorta masrafını ekleyerek toplam maliyeti hesaplar
    def calculate_salary(self):
        tax = self.calculate_tax(self.__salary)
        insurance_cost = 2500
        return self.__salary + tax + insurance_cost

    # Branşa göre güçlü tarafı yorumlar  
    def branch_strong_side(self):
        branch = self.sport_branch.lower()
        side = self.strong_side
        if "football" in branch:
            return f"Preferred Foot : {side}"
        elif "basketball" in branch or "volleyball" in branch:
            return f"Shooting Hand: {side}"
        else:
            return f"Dominant Side: {side}"
            
    # Nesneyi sözlük formatına çevirir
    def to_dict(self):
        data = super().to_dict()
        data.update({"type": "ProfessionalAthlete",
            "salary": self.__salary,
            "contract_end_date": self.__contract_end_date,
            "total_cost": self.calculate_salary()
        })
        return data    
        
    # Profesyonel sporcunun net maaşını döndürür       
    @property
    def salary(self):
        return self.__salary

    # Performansa dayalı sözleşme yenileme işlemini yapar
    @classmethod
    def renew_contract(cls, current_athlete_data, performance_stats):
        name = current_athlete_data.get("name")
        surname = current_athlete_data.get("surname", "")
        age = current_athlete_data.get("age")
        current_salary = current_athlete_data.get("salary")

        if "gender" not in current_athlete_data:
            raise ValueError(f"Hata: {name} için 'gender' verisi eksik!")
        gender = current_athlete_data["gender"]
        
        if "height" not in current_athlete_data or "weight" not in current_athlete_data:
             raise ValueError(f"Hata: {name} için boy/kilo verisi eksik!")
        height = current_athlete_data["height"]
        weight = current_athlete_data["weight"]

        if "strong_side" not in current_athlete_data:
             raise ValueError(f"Hata: {name} için 'strong_side' verisi eksik!")
        strong_side = current_athlete_data["strong_side"]
          
        if age >= 38:
            raise_retirement_error(name, age)

        matches_played = performance_stats.get("matches_played", 0)
        if matches_played < 20:
            raise_performance_error(name, matches_played)
        
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
        print(f"Sözleşme Yenilendi: {name} {surname} - Yeni Maaş: {new_salary:.2f}")

        return cls(
            athlete_id=current_athlete_data.get("athlete_id"),
            name=name, surname=surname, age=age + 1, gender=gender,
            height=height, weight=weight,
            sport_branch=current_athlete_data.get("sport_branch"),
            status="Active", strong_side=strong_side,
            salary=new_salary, contract_end_date=new_end_date
        )

# Amatör sporcu özelliklerini ve kurallarını barındıran sınıf
class AmateurAthlete(AthleteBase):
    # Amatör sporcu nesnesini başlatır
    def __init__(self, athlete_id, name, surname, age, gender, height, weight, sport_branch, status, strong_side, licence_number):
        super().__init__(athlete_id, name, surname, age, gender, height, weight, sport_branch, status, strong_side)
        self.__licence_number = licence_number
    
    # Sporcunun lisans numarasını döndürür
    @property
    def licence_number(self):
        return self.__licence_number
    
    # Amatör sporcunun toplam maliyetini hesaplar
    def calculate_salary(self):
        base_licence_fee = 1000
        transport_support = 100
        return base_licence_fee + transport_support

    # Branşa göre güçlü tarafı yorumlar
    def branch_strong_side(self):
        branch = self.sport_branch.lower()
        if "football" in branch:
            return f"Preferred Foot : {self.strong_side}"
        elif "basketball" in branch or "volleyball" in branch:
            return f"Shooting Hand: {self.strong_side}"
        else:
            return f"Dominant Side: {self.strong_side}"
        
    # Nesneyi sözlük formatına çevirir
    def to_dict(self):
        data = super().to_dict()
        data.update({
            "type": "AmateurAthlete",
            "licence_number": self.__licence_number
        })
        return data    
    
    # Ulaşım mesafesine göre desteği kontrol eder
    @staticmethod
    def check_transport_distance(distance_km):
        return distance_km > 10
    
    # Amatör transfer işlemlerini yönetir
    @classmethod
    def transfer_from_local_club(cls, name, surname, age, gender, height, weight, branch, prev_club_doc):
        is_cleared = prev_club_doc.get("has_clearance", False)
        if not is_cleared:
            raise_clearance_error(name)
        
        if "strong_side" not in prev_club_doc:
            raise ValueError(f"Hata: Transfer için 'strong_side' bilgisi girilmemiş!")
        strong_side = prev_club_doc["strong_side"]
        penalty_points = prev_club_doc.get("penalty_points", 0)
        if penalty_points > 5:
            raise_penalty_error(penalty_points)
        print(f"Transfer Onaylandı: {name} {surname} amatör takıma katıldı.")
        
        return cls(
            athlete_id=random.randint(3000, 4999),
            name=name, surname=surname, age=age, gender=gender,
            height=height, weight=weight, sport_branch=branch,
            status="Active", strong_side=strong_side,
            licence_number=f"TUR-{branch[:3].upper()}-{random.randint(100,999)}"
        )
   
# Altyapı sporcusu özelliklerini ve kurallarını barındıran sınıf
class YouthAthlete(AthleteBase):
    # Altyapı sporcusu nesnesini başlatır
    def __init__(self, athlete_id, name, surname, age, gender, height, weight, sport_branch, status, strong_side, guardian_name, scholarship_amount):
        super().__init__(athlete_id, name, surname, age, gender, height, weight, sport_branch, status, strong_side)
        self.__guardian_name = guardian_name
        self.__scholarship_amount = scholarship_amount

    # Burs miktarını maaş olarak döndürür
    def calculate_salary(self):
        return self.__scholarship_amount
    
    # Branşa göre güçlü tarafı yorumlar
    def branch_strong_side(self):
        branch = self.sport_branch
        if "football" in branch:
            return f"Preferred Foot : {self.strong_side}"
        elif "basketball" in branch or "volleyball" in branch:
            return f"Shooting Hand: {self.strong_side}"
        else:
            return f"Dominant Side: {self.strong_side}"
            
    # Nesneyi sözlük formatına çevirir
    def to_dict(self):
        data = super().to_dict()
        data.update({
            "type": "YouthAthlete",
            "guardian_name": self.__guardian_name,
            "scholarship_amount": self.__scholarship_amount
        })
        return data    
    
    # Veli adını döndürür
    @property
    def guardian_name(self):
        return self.__guardian_name
    
    # Yaşa göre altyapı kategorisini belirler
    @staticmethod
    def age_category(age):
        if age < 10 :
            return "Minik Takım"
        if age < 12:
            return "U12"
        if age < 14:
            return "U14"
        if age < 16:
            return "U16"
        if age < 18:
            return "U18"
        return "As takım adayı"
    
    # Sınav puanına göre burs hesaplayıp kayıt oluşturur
    @classmethod
    def register_with_scholarship_calc(cls, student_info, exam_score):
        required_fields = ["gender", "strong_side", "height", "weight"]
        for field in required_fields:
            if field not in student_info:
                raise ValueError(f"Hata: Burs kaydı için '{field}' bilgisi eksik!")
            
        name = student_info.get("name")
        surname = student_info.get("surname", "")
        age = student_info.get("age")
        gender = student_info.get("gender")
        strong_side = student_info.get("strong_side")
        height = student_info["height"] 
        weight = student_info["weight"]
        
        if age >= 18:
            print(f"Kayıt Başarısız: {name} (Yaş: {age}) altyapı yaş sınırını aşıyor.")
            return None

        scholarship = 500
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
            surname=surname,
            age=age,
            gender=gender,
            height=height,
            weight=weight,
            sport_branch=student_info.get("branch", "General"),
            status="Active",
            strong_side=strong_side,
            guardian_name=student_info.get("parent_name"),
            scholarship_amount=scholarship
        )







