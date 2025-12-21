from abc import ABC, abstractmethod
import random

# Sporcular için temel özellikleri barındıran soyut sınıf
class AthleteBase(ABC):
    # Sınıfın temel özelliklerini ve değişkenleri başlatır
    def __init__(self,athlete_id,name,surname,age,gender,height,weight,sport_branch,status,strong_side):
        self.__athlete_id = athlete_id
        self.__name = name
        self.__surname = surname
        self.__age = age
        self.__height = height
        self.__weight = weight
        self.__gender = gender
        self.__sport_branch = sport_branch
        self.__status = status
        self.__strong_side = strong_side

    # Sporcunun ID sini döndürür
    @property
    def athlete_id(self):
        return self.__athlete_id
    
    # Sporcunun adını döndürür
    @property
    def name(self):
        return self.__name
    
    # Sporcunun soyadını döndürür
    @property
    def surname(self):
        return self.__surname
    
    # Sporcunun yaşını döndürür
    @property
    def age(self):
        return self.__age
    
    # Sporcunun cinsiyetini döndürür
    @property
    def gender(self):
        return self.__gender
    
    # Sporcunun boy bilgisini döndürür
    @property
    def height(self):
        return self.__height
    
    # Sporcunun kilo bilgisini döndürür
    @property
    def weight(self):
        return self.__weight 
    
    # Sporcunun yaşını belirli kurallara göre günceller
    @age.setter
    def age(self,new_age):
        if isinstance(new_age,int) and 10 < new_age < 50:
            self.__age = new_age
        else:
            print("Lütfen geçerli bir yaş giriniz.")       
    
    # Sporcunun branşını döndürür
    @property
    def sport_branch(self):
        return self.__sport_branch
    
    # Sporcunun güncel durumunu (aktif,cezalı,sakat) döndürür
    @property
    def status(self):
        return self.__status
    
    # Sporcunu durumununu izin verilen durumlara günceller
    @status.setter
    def status(self,new_status):
        current_status = ["Active","Injured","Suspended","Retired","TransferListed","Excluded"]

        if new_status in current_status:
            self.__status = new_status
        else:
            raise ValueError(f"Lütfen geçerli bir durum giriniz.") 

    # Sporcunun güçlü tarafını döndürür    
    @property
    def strong_side(self):
        return self.__strong_side
        
    # Sporcunun branşa özgü güçlü taraf bilgisini döndüren soyut bir metot ayrıca çok biçimlilik örneğidir
    @abstractmethod    
    def branch_strong_side(self):
       pass
    
    # Sporcunun maaşını hesaplamak için gereken soyut metot
    @abstractmethod
    def calculate_salary(self):
        pass

    # Boy ve kiloya göre Vücüt Kitle Endeksini hesaplar
    @staticmethod
    def calculate_bmi(weight, height):
        if height > 3.0: 
            height = height / 100
            
        if height <= 0:
            return 0.0
        return weight / (height ** 2)
    
    #  Rastgele özelliklere sahip bir sporcu nesnesi oluşturur
    @classmethod
    def create_random(cls):
        
        names = ["Ali", "Ayşe", "Mehmet", "Elif", "Can", "Zeynep"]
        surnames = ["Yılmaz", "Kaya", "Demir", "Çelik", "Şahin", "Öztürk"]
        branches = ["Football", "Basketball", "Volleyball",]
        statuses = ["Active", "Injured", "Suspended","TransferListed"]
        sides = ["Right", "Left","Both"]
        genders = ["Male", "Female"]

        random_id = random.randint(1000, 9999)
        random_name = random.choice(names)
        random_surname = random.choice(surnames)
        random_age = random.randint(16, 40)
        random_gender = random.choice(genders)
        random_height = random.randint(160, 205)
        random_weight = random.randint(55, 110)
        random_branch = random.choice(branches)
        random_status = random.choice(statuses)
        random_side = random.choice(sides)
        return cls(random_id, random_name,random_surname, random_age, random_gender,random_height, random_weight, random_branch, random_status, random_side)   

    # Sporcu bilgilerini sözlük formatına döndürür
    def to_dict(self):
        return {
            "athlete_id":self.__athlete_id,
            "name":self.__name,
            "surname":self.__surname,
            "age":self.__age,
            "gender":self.__gender,
            "height": self.__height,
            "weight": self.__weight,
            "sport_branch":self.__sport_branch,
            "strong_side":self.__strong_side,
            "status":self.__status
        }









        















