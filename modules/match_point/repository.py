import json
import os
from datetime import datetime

class MatchRepository:
    """
    Veri Erişim Katmanı (Data Access Layer).
    Bu sınıf, maç verilerinin kalıcı olarak saklanmasından (JSON) ve
    işlem geçmişinin loglanmasından sorumludur.
    """
    def __init__(self, data_file="matches_data.json", log_file="system_history.log"):
        # Dosya yollarını belirle (Modül klasörü içine kaydetsin)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.__data_file_path = os.path.join(current_dir, data_file)
        self.__log_file_path = os.path.join(current_dir, log_file)
        
        # Başlangıçta dosyaları kontrol et
        self.__ensure_files_exist()

    def __ensure_files_exist(self):
        """Dosyalar yoksa oluşturur."""
        if not os.path.exists(self.__data_file_path):
            with open(self.__data_file_path, 'w', encoding='utf-8') as f:
                json.dump([], f) # Boş liste ile başlat
        
        if not os.path.exists(self.__log_file_path):
            with open(self.__log_file_path, 'w', encoding='utf-8') as f:
                f.write(f"--- SİSTEM BAŞLATILDI: {datetime.now()} ---\n")


    # LOGLAMA İŞLEMLERİ (Satır Sayısı ve Takip İçin)
    
    def log_operation(self, message):
        """Yapılan işlemi tarihçeye kaydeder."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] INFO: {message}\n"
        
        try:
            with open(self.__log_file_path, 'a', encoding='utf-8') as f:
                f.write(log_entry)
        except Exception as e:
            print(f"Loglama Hatası: {e}")

    def log_error(self, error_message):
        """Hataları ayrı bir formatta kaydeder."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] ERROR: {error_message}\n"
        
        try:
            with open(self.__log_file_path, 'a', encoding='utf-8') as f:
                f.write(log_entry)
        except Exception as e:
            print(f"Loglama Hatası: {e}")

    def get_logs(self):
        """Tüm geçmişi okur ve döner."""
        if os.path.exists(self.__log_file_path):
            with open(self.__log_file_path, 'r', encoding='utf-8') as f:
                return f.read()
        return "Henüz kayıt yok."

    # =========================================================================
    # JSON VERİ KAYDETME VE OKUMA
    # =========================================================================

    def save_matches_to_json(self, match_list):
        """
        Match nesnelerini JSON formatına çevirip dosyaya yazar.
        Not: Python nesneleri doğrudan JSON olmaz, dict'e çevirmemiz lazım.
        """
        data_to_save = []
        
        for match in match_list:
            # Her maç nesnesinden temel verileri çekiyoruz
            match_data = {
                "id": getattr(match, "_MatchBase__match_id", "Unknown"), # Private variable erişimi
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
            
            self.log_operation(f"{len(match_list)} adet maç veritabanına kaydedildi.")
            return True
        except Exception as e:
            self.log_error(f"Kayıt Hatası: {e}")
            return False

    def load_matches_from_json(self):
        """
        JSON dosyasındaki verileri okur.
        Not: Buradan dönen veri saf sözlüktür (Dictionary), nesne değildir.
        Nesneye çevirmek için Factory kullanılabilir ama şimdilik raporlama için yeterli.
        """
        try:
            with open(self.__data_file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.log_operation("Veriler başarıyla yüklendi.")
            return data
        except Exception as e:
            self.log_error(f"Okuma Hatası: {e}")
            return []

    def clear_database(self):
        """Veritabanını sıfırlar."""
        try:
            with open(self.__data_file_path, 'w', encoding='utf-8') as f:
                json.dump([], f)
            self.log_operation("Veritabanı sıfırlandı.")
        except Exception as e:
            self.log_error(f"Sıfırlama Hatası: {e}")





