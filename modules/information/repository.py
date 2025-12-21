import json
import os
from typing import List, Optional
from .base import AthleteBase
from .errors import raise_duplicate_error, raise_not_found_error

# Sporcu verilerinin dosya tabanlı yönetimini sağlar
class AthleteRepository:
    # Repository nesnesini ve dosya yolunu başlatır
    def __init__(self, filename="athletes.json"):
        self.__filename = filename
        self.__athletes: List[dict] = self.load_data()

    # JSON dosyasından verileri okur
    def load_data(self) -> List[dict]:
        if not os.path.exists(self.__filename):
            return []
        try:
            with open(self.__filename, 'r', encoding='utf-8') as file:
                return json.load(file)
        except (json.JSONDecodeError, IOError):
            return []

    # Güncel verileri JSON dosyasına kaydeder
    def save_data(self):
        try:
            with open(self.__filename, 'w', encoding='utf-8') as file:
                json.dump(self.__athletes, file, ensure_ascii=False, indent=4)
        except IOError as e:
            print(f"Dosya kaydetme hatası: {e}")

    # Yeni bir sporcu kaydını veritabanına ekler
    def add(self, athlete_entity):
        if hasattr(athlete_entity, 'to_dict'):
            data = athlete_entity.to_dict()
        else:
            data = athlete_entity
            
        if self.get_by_id(data.get("athlete_id")):
            raise_duplicate_error(data.get("athlete_id"))
        
        self.__athletes.append(data)
        self.save_data()
        print(f"Repository: {data.get('name')} {data.get('surname', '')} başarıyla kaydedildi.")

    # ID numarasına göre sporcu arar
    def get_by_id(self, athlete_id: int) -> Optional[dict]:
        for athlete in self.__athletes:
            if str(athlete.get("athlete_id")) == str(athlete_id):
                return athlete
        return None

   # Tüm sporcu kayıtlarını listeler
    def get_all(self) -> List[dict]:
        return self.__athletes

    # ID numarasına göre kayıt siler
    def delete_by_id(self, athlete_id: int) -> bool:
        athlete = self.get_by_id(athlete_id)
        if not athlete:
            raise_not_found_error(athlete_id)
        self.__athletes.remove(athlete)
        self.save_data()
        print(f"Repository: {athlete_id} ID'li kayıt silindi.")
        return True

    # Mevcut bir kaydı günceller
    def update(self, athlete_id: int, update_data: dict):
        athlete = self.get_by_id(athlete_id)
        if athlete:
            athlete.update(update_data)
            self.save_data()
            print(f"Repository: {athlete_id} ID'li kayıt güncellendi.")
        else:
            raise_not_found_error(athlete_id)
            
    # Belirli bir branştaki sporcuları getirir
    def get_by_branch(self, branch: str) -> List[dict]:
        return [a for a in self.__athletes if a.get("sport_branch", "").lower() == branch.lower()]

    # Belirli bir durumdaki sporcuları getirir
    def get_by_status(self, status: str) -> List[dict]:
        return [a for a in self.__athletes if a.get("status", "").lower() == status.lower()]
    
    # Veritabanı türü hakkında bilgi verir
    @staticmethod
    def get_database_info():
        return "JSON tabanlı dosya sistemi kullanılıyor."
    
    # Yedek dosyasından repository başlatır
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