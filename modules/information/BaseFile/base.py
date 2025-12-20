from abc import ABC, abstractmethod
import random

class AthleteBase(ABC):
    def __init__(self,athlete_id,name,age,gender,height,weight,sport_branch,status,strong_side):
        self.__athlete_id = athlete_id
        self.__name = name
        self.__age = age
        self.height = height
        self.weight = weight
        self.__gender = gender
        self.__sport_branch = sport_branch
        self.__status = status
        self.__strong_side = strong_side

    @property
    def athlete_id(self):
        return self.__athlete_id

    @property
    def name(self):
        return self.__name
    
    @property
    def age(self):
        return self.__age
    
    @property
    def gender(self):
        return self.__gender
    
    @property
    def height(self):
        return self.__height

    @property
    def weight(self):
        return self.__weight 
    
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
        
    @property
    def strong_side(self):
        return self.__strong_side    

    @abstractmethod    
    def athlete_strong_side(self):
       pass
    
    @abstractmethod
    def calculate_salary(self):
        pass

    @staticmethod
    def calculate_bmi(weight, height):
        if height > 3.0: 
            height = height / 100
            
        if height <= 0:
            return 0.0
        return weight / (height ** 2)
    
    @classmethod
    def create_random(cls):
        
        names = ["Ali", "Ayşe", "Mehmet", "Elif", "Can", "Zeynep"]
        surnames = ["Yılmaz", "Kaya", "Demir", "Çelik", "Şahin", "Öztürk"]
        branches = ["Football", "Basketball", "Volleyball",]
        statuses = ["Active", "Injured", "Suspended","TransferListed"]
        sides = ["Right", "Left","Both"]
        genders = ["Male", "Female"]

        random_id = random.randint(1000, 9999)
        random_name = f"{random.choice(names)} {random.choice(surnames)}"
        random_age = random.randint(16, 40)
        random_gender = random.choice(genders)
        random_height = random.randint(160, 205)
        random_weight = random.randint(55, 110)
        random_branch = random.choice(branches)
        random_status = random.choice(statuses)
        random_side = random.choice(sides)
        return cls(random_id, random_name, random_age, random_gender,random_height, random_weight, random_branch, random_status, random_side)   

    
    def to_dict(self):
        return {
            "athlete_id":self.__athlete_id,
            "name":self.__name,
            "age":self.__age,
            "gender":self.__gender,
            "height": self.__height,
            "weight": self.__weight,
            "sport_branch":self.__sport_branch,
            "athlete_strong_side":self.__strong_side,
            "status":self.__status
        }









        















