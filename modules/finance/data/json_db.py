import json
import os
# Kendi özel hata sınıfımızı çağırıyoruz
from ..exceptions.errors import DataStorageError

# JSON dosyası ile kod arasındaki veri alışverişini yöneten sınıf
class FinanceRepository:
    def __init__(self, filename="finance.json"):

        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.file_path = os.path.join(current_dir, filename)
        
        # Başlangıçta dosya kontrolü yapar
        self._ensure_file_exists()

    # Dosya yoksa boş bir liste olarak oluşturur, hata varsa yakalar
    def _ensure_file_exists(self):
        try:
            if not os.path.exists(self.file_path):
                with open(self.file_path, 'w', encoding='utf-8') as f:
                    json.dump([], f)
        except OSError as e:
            # Disk hatası, izin hatası vb. olursa
            raise DataStorageError(self.file_path, f"Dosya oluşturulamadı: {str(e)}")

    # Tek bir kaydı listeye ekler ve dosyayı günceller
    def save_record(self, record_dict):
        # Önce mevcut veriyi çek (Burada hata olursa load_all )
        data = self.load_all()
        data.append(record_dict)
        # Sonra kaydet (Burada hata olursa _save_to_file )
        self._save_to_file(data)

    # Tüm kayıtları okur ve liste olarak döner
    def load_all(self):
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            # Dosya yoksa boş liste döner
            return []
        except json.JSONDecodeError as e:
            # Bozuk dosya yapısında
            raise DataStorageError(self.file_path, f"JSON formatı bozuk, okunamadı: {str(e)}")
        except Exception as e:
            # Beklenmeyen tüm okuma hataları
            raise DataStorageError(self.file_path, f"Okuma hatası: {str(e)}")

    # Veriyi dosyaya yazar (Private method)
    def _save_to_file(self, data):
        try:
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except OSError as e:
            # Disk dolu, yazma izni yok vb.
            raise DataStorageError(self.file_path, f"Yazma hatası: {str(e)}")