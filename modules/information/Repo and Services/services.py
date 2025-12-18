import json 
import os
class AthleteRepository:
    def __init__(self,filename = "athletes.json"):
        self.filename = filename
        self.athletes = self.load_data()
        
    def load_data(self):
        if not os.path.exists(self.filename):
            return []
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                return json.load(file)
        except Exception as e:
            print(f"Veri yükleme hatası: {e}")
            return []

    def save_data(self):
        try:
            with open(self.filename, 'w', encoding='utf-8') as file:
                json.dump(self.athletes, file, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Kayıt hatası: {e}")


    def get_all(self):
        return self.athletes
    
    def get_by_id(self,athlete_id):
        for athlete in self.athletes:
            if str(athlete.get('athlete_id')) == str(athlete_id):
                return athlete
        return None
    
    def get_by_branch(self,branch):
        result = []
        for athlete in self.athletes:
         if athlete.get('sport_branch', '').lower() == branch.lower():
                result.append(athlete)
        return result
    
    def get_by_status(self, status):
        result = []
        for athlete in self.athletes:
            if athlete.get('status', '').lower() == status.lower():
                result.append(athlete)
        return result
    def add(self,athete_data):
        self.athletes.append(athete_data)
        self.save_data()





