import json
import os
from typing import List, Optional
from .base import AthleteBase

class AthleteRepository:
    
    def __init__(self, filename="athletes.json"):
        self.__filename = filename
        self.athletes: List[dict] = self.load_data()

    
    def load_data(self) -> List[dict]:
        if not os.path.exists(self.__filename):
            return []
        try:
            with open(self.__filename, 'r', encoding='utf-8') as file:
                return json.load(file)
        except (json.JSONDecodeError, IOError):
            return []

  
    def save_data(self):
        try:
            with open(self.__filename, 'w', encoding='utf-8') as file:
                json.dump(self.__athletes, file, ensure_ascii=False, indent=4)
        except IOError as e:
            print(f"Dosya kaydetme hatası: {e}")

    
    def add(self, athlete_entity):
        if hasattr(athlete_entity, 'to_dict'):
            data = athlete_entity.to_dict()
        else:
            data = athlete_entity
            
        if self.get_by_id(data.get("athlete_id")):
            print(f"Hata: {data.get('athlete_id')} ID'li sporcu zaten var.")
            return
        
        self.__athletes.append(data)
        self.save_data()
        print(f"Repository: {data.get('name')} {data.get('surname', '')} başarıyla kaydedildi.")

    
    def get_by_id(self, athlete_id: int) -> Optional[dict]:
        for athlete in self.__athletes:
            if str(athlete.get("athlete_id")) == str(athlete_id):
                return athlete
        return None

   
    def get_all(self) -> List[dict]:
        return self.__athletes

    
    def delete_by_id(self, athlete_id: int) -> bool:
        athlete = self.get_by_id(athlete_id)
        if athlete:
            self.__athletes.remove(athlete)
            self.save_data()
            print(f"Repository: {athlete_id} ID'li kayıt silindi.")
            return True
        return False

    
    def update(self, athlete_id: int, update_data: dict):
        athlete = self.get_by_id(athlete_id)
        if athlete:
            athlete.update(update_data)
            self.save_data()
            print(f"Repository: {athlete_id} ID'li kayıt güncellendi.")
        else:
            print("Hata: Güncellenecek kayıt bulunamadı.")
            
    
    def get_by_branch(self, branch: str) -> List[dict]:
        return [a for a in self.__athletes if a.get("sport_branch", "").lower() == branch.lower()]


    def get_by_status(self, status: str) -> List[dict]:
        return [a for a in self.__athletes if a.get("status", "").lower() == status.lower()]
    
    @staticmethod
    def get_database_info():
        return "JSON tabanlı dosya sistemi kullanılıyor."
    
    @classmethod
    def from_backup(cls, backup_filename="backup_athletes.json"):
        
        import shutil
        original_file = "athletes.json"
        
        
        if os.path.exists(original_file):
            shutil.copy2(original_file, backup_filename)
            print(f"Sistem GÜVENLİ MODDA başlatıldı. Yedek: {backup_filename}")
        else:
            print("Ana veri bulunamadı, boş bir yedek dosyası ile başlanıyor.")
            
        
        return cls(filename=backup_filename)
