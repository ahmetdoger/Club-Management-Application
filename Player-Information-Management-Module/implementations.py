from .base import AthleteBase
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











