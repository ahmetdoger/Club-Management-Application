import json
import os
from typing import List, Dict, Union, Optional

class AthleteRepository:

    def __init__(self, filename: str = "athletes.json"):
        self.__filename = filename
        self.__athletes = self.__load_data()

    @property
    def filename(self):
        """Kullanılan veritabanı dosyasının adını döndürür."""
        return self.__filename

   
    @staticmethod
    def get_default_settings() -> Dict[str, str]:
     
        return {
            "default_filename": "athletes.json",
            "encoding": "utf-8",
            "backup_enabled": "True"
        }

    @classmethod
    def create_from_directory(cls, directory: str, env_mode: str):
        
        prefix = "prod_" if env_mode == "PROD" else "dev_"
        full_path = os.path.join(directory, f"{prefix}athletes.json")
        
        print(f"Repository başlatıldı: {full_path} (Mod: {env_mode})")
        return cls(full_path)

    
    def __load_data(self) -> List[Dict]:
       
        if not os.path.exists(self.__filename):
            print(f"Uyarı: {self.__filename} bulunamadı, yeni bir veritabanı oluşturulacak.")
            return []
        
        try:
            with open(self.__filename, 'r', encoding='utf-8') as file:
                data = json.load(file)
               
                if isinstance(data, list):
                    return data
                else:
                    print("Hata: Dosya içeriği beklendiği gibi bir liste değil.")
                    return []
        except json.JSONDecodeError:
            print(f"Kritik Hata: {self.__filename} dosyası bozuk veya okunamıyor.")
            return []
        except Exception as e:
            print(f"Bilinmeyen hata oluştu: {e}")
            return []

    def __save_data(self):
        
        try:
            with open(self.__filename, 'w', encoding='utf-8') as file:
                json.dump(self.__athletes, file, ensure_ascii=False, indent=4)
            print("Veritabanı güncellendi.")
        except IOError as e:
            print(f"Yazma Hatası: Veriler diske kaydedilemedi! {e}")

    
    def add(self, athlete_entity):
       
       
       
        new_id = getattr(athlete_entity, 'athlete_id', None)
        if self.get_by_id(new_id):
            print(f"Hata: {new_id} ID'li sporcu zaten mevcut!")
            return

       
        if hasattr(athlete_entity, 'to_dict'):
            data_to_save = athlete_entity.to_dict()
        else:
            
            print("Uyarı: 'to_dict' metodu bulunamadı, ham veri kaydediliyor.")
            data_to_save = athlete_entity

        self.__athletes.append(data_to_save)
        self.__save_data()
        print(f"Başarılı: Sporcu ({data_to_save.get('name')}) sisteme eklendi.")

   
    def delete_by_id(self, athlete_id: Union[int, str]) -> bool:
      
        original_count = len(self.__athletes)
        
        self.__athletes = [
            athlete for athlete in self.__athletes 
            if str(athlete.get('athlete_id')) != str(athlete_id)
        ]

        if len(self.__athletes) < original_count:
            self.__save_data()
            print(f"Bilgi: {athlete_id} ID'li kayıt silindi.")
            return True
        
        print(f"Hata: Silinecek kayıt bulunamadı (ID: {athlete_id}).")
        return False

  
    def get_all(self) -> List[Dict]:
        
        return self.__athletes

   
    def get_by_id(self, athlete_id: Union[int, str]) -> Optional[Dict]:
       
        for athlete in self.__athletes:
           
            if str(athlete.get('athlete_id')) == str(athlete_id):
                return athlete
        return None

    
    def get_by_branch(self, branch_name: str) -> List[Dict]:
      
        result = []
        search_term = branch_name.lower()
        
        for athlete in self.__athletes:
            current_branch = athlete.get('sport_branch', '').lower()
            if current_branch == search_term:
                result.append(athlete)
                
        return result

    def get_by_status(self, status: str) -> List[Dict]:
       
        return [
            athlete for athlete in self.__athletes
            if athlete.get('status', '').lower() == status.lower()
        ]

    def filter_by_salary_range(self, min_salary: float, max_salary: float) -> List[Dict]:
        
        result = []
        for athlete in self.__athletes:
            salary = athlete.get('salary')
            if salary is not None:
                if min_salary <= salary <= max_salary:
                    result.append(athlete)
        return result

    def clear_database(self):
      
        self.__athletes = []
        self.__save_data()
        print("Uyarı: Veritabanı sıfırlandı.")