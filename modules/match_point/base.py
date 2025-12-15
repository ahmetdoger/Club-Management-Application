from abc import ABC, abstractmethod
from datetime import datetime

  #Tüm maç türleri için temel soyut sınıf (Abstract Base Class).
class MatchBase(ABC):
    
    _total_match_objects = 0

    def __init__(self, match_id, home_team, away_team, match_type, date_time):
        
        self.__match_id = match_id
        self.__home_team = home_team
        self.__away_team = away_team
        self.__match_type = match_type
        self.__date_time = date_time
        

        self.__status = "Scheduled"
        
        # Score varsayilan olarak '0-0' veya baslar
        self.__score = "0-0"

        # Her nesne olusturuldugunda sinif sayacini artir
        MatchBase.increase_object_count()

    # Abstract Methods (Soyut Metotlar) 
    @abstractmethod
    def simulate_match(self):
        
         pass
    
    @abstractmethod
    def update_status(self, new_status):
    
        pass

    @abstractmethod
     #Mac ile ilgili ozet bilgileri dondurur. Polimorfizm ornegi olarak her alt sinif farkli formatta donebilir.
    def get_match_info(self):
        
        pass


    # Encapsulation: Getter & Setter Methods
    #  Private degiskenlere erisim sadece metotlarla yapilmalidir.

    def get_match_id(self):
        return self.__match_id

    def set_match_id(self, new_id):
        self.__match_id = new_id

    def get_home_team(self):
        return self.__home_team

    def set_home_team(self, team):
        self.__home_team = team

    def get_away_team(self):
        return self.__away_team

    def set_away_team(self, team):
        self.__away_team = team

    def get_match_type(self):
        return self.__match_type

    def set_match_type(self, m_type):
        self.__match_type = m_type

    def get_date_time(self):
        return self.__date_time

    def set_date_time(self, dt):
        self.__date_time = dt

    def get_status(self):
        return self.__status

    # Status guncellemesi icin ozel setter, abstract metot uzerinden de cagrilabilir
    def _set_status_internal(self, status):
        # Bu metot sinif ici (protected) kullanim icindir
        self.__status = status

    def get_score(self):
        return self.__score

    def set_score(self, score):
        self.__score = score



    # Class & Static Methods

    @classmethod
    def increase_object_count(cls):
        cls._total_match_objects += 1

    @classmethod
    def get_total_objects(cls):
        return cls._total_match_objects


     #[Static Method] Ev sahibi ve deplasman takiminin ayni olup olmadigini kontrol eder.Data validasyonu icin kullanilir.
    @staticmethod
    def validate_teams(home, away):
       
        if home == away:
            print("Hata: Bir takim kendi kendine mac yapamaz!")
            return False
        return True


   # [Static Method] Tarih nesnesini okunabilir string formatina cevirir.
    @staticmethod
    def format_match_date(dt_obj):
        
        if isinstance(dt_obj, datetime):
            return dt_obj.strftime("%Y-%m-%d %H:%M")
        return str(dt_obj)

































