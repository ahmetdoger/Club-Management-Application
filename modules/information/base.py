from abc import ABC, abstractmethod
import random

class AthleteBase(ABC):
    def __init__(self,athlete_id,name,age,sport_branch,status):
        self.__athlete_id = athlete_id
        self.__name = name
        self.__age = age
        self.__sport_branch = sport_branch
        self.__status = status

    @property
    def athlete_id(self):
        return self.__athlete_id

    @property
    def name(self):
        return self.__name
    
    @property
    def age(self):
        return self.__age
    
    @age.setter
    def age(self,new_age):
        if isinstance(new_age,int) and 0 < new_age < 100:
            self.__age = new_age
        else:
            print("Lütfen geçerli bir yaş giriniz.")

    @property
    def sport_branch(self):
        return self.__sport_branch

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self,new_status):
        current_status = ["Active","Injured","Suspended","Retired","TransferListed","Excluded"]

        if new_status in current_status:
            self.__status = new_status
        else:
            raise ValueError(f"Lütfen geçerli bir durum giriniz.") 
        
    @staticmethod
    def calculate_bmi(weight,height):
        if height <= 0:
            return 0.0

        bmi = weight / height ** 2
        return bmi
    
    @classmethod
    def create_random(cls):
        names = []
        surnames = []
        branches = []
        statuses = []

        random_id = random.randint(0,9999)
        random_name = f"{random.choice(names),random.choice(surnames)}"
        random_age = random.randint(16,40)
        random_branch = random.choice(branches)
        random_status = random.choice(statuses)

        return cls(random_id,random_name,random_age,random_branch,random_status)









        















