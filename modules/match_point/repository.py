import json
import os
from datetime import datetime

class MatchRepository:
    """
    Veri Erişim Katmanı (Data Access Layer).
    PDF Gereksinimleri: Kaydetme, Silme, ID ve Tarih Filtreleme.
    """
    def __init__(self, data_file="matches_data.json", log_file="system_history.log"):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.__data_file_path = os.path.join(current_dir, data_file)
        self.__log_file_path = os.path.join(current_dir, log_file)
        self.__ensure_files_exist()

    def __ensure_files_exist(self):
        if not os.path.exists(self.__data_file_path):
            with open(self.__data_file_path, 'w', encoding='utf-8') as f:
                json.dump([], f)
        
        if not os.path.exists(self.__log_file_path):
            with open(self.__log_file_path, 'w', encoding='utf-8') as f:
                f.write(f"--- SİSTEM BAŞLATILDI: {datetime.now()} ---\n")

    def log_operation(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            with open(self.__log_file_path, 'a', encoding='utf-8') as f:
                f.write(f"[{timestamp}] INFO: {message}\n")
        except: pass

    # --- JSON İŞLEMLERİ (KAYDETME / OKUMA) ---

    def save_matches_to_json(self, match_list):
        data_to_save = []
        for match in match_list:
            match_data = {
                "id": str(getattr(match, "_MatchBase__match_id", "0")),
                "type": getattr(match, "_MatchBase__match_type", "Generic"),
                "home": match.get_home_team().get_name(),
                "away": match.get_away_team().get_name(),
                "score": match.get_score(),
                "status": match.get_status(),
                "date": getattr(match, "_MatchBase__date_time", str(datetime.now()))
            }
            data_to_save.append(match_data)

        try:
            with open(self.__data_file_path, 'w', encoding='utf-8') as f:
                json.dump(data_to_save, f, indent=4, ensure_ascii=False)
            self.log_operation(f"{len(match_list)} maç kaydedildi.")
            return True
        except Exception as e:
            print(f"Kayıt Hatası: {e}")
            return False

    def load_raw_data(self):
        """JSON dosyasındaki ham veriyi okur."""
        try:
            with open(self.__data_file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except: return []

    # --- EKSİK OLAN VE HATAYA SEBEP OLAN FONKSİYON ---
    def clear_database(self):
        """Veritabanını sıfırlar (Demo dosyası bunu kullanıyor)."""
        try:
            with open(self.__data_file_path, 'w', encoding='utf-8') as f:
                json.dump([], f)
            self.log_operation("Veritabanı sıfırlandı.")
        except Exception as e:
            print(f"Sıfırlama Hatası: {e}")

    # --- PDF GEREKSİNİMLERİ (FİLTRELEME) ---

    def find_match_by_id(self, match_id):
        data = self.load_raw_data()
        for match in data:
            if str(match.get("id")) == str(match_id):
                return match
        return None

    def filter_matches_by_date(self, date_str):
        data = self.load_raw_data()
        return [m for m in data if m.get("date", "").startswith(date_str)]

    def filter_matches_by_type(self, match_type):
        data = self.load_raw_data()
        return [m for m in data if m.get("type") == match_type]