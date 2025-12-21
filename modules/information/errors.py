from datetime import datetime
import inspect

# Proje genelindeki özel hata durumlarını yönetir
class ClubManagerError(Exception):
    # Hata mesajını ve detaylarını başlatır
    def __init__(self, message: str, error_type: str = "GeneralError", error_code: int = 1000):
        self.__message = message
        self.__error_type = error_type
        self.__error_code = error_code
        self.__timestamp = datetime.now()
        
        try:
            curframe = inspect.currentframe()
            calframe = inspect.getouterframes(curframe, 2)
            self.__source_function = calframe[1][3]
        except Exception:
            self.__source_function = "Unknown"

        full_msg = f"[{self.__error_type}] {self.__message}"
        super().__init__(full_msg)
    
    # Hata mesajını döndürür
    @property
    def message(self):
        return self.__message
    
    # Hata türünü döndürür
    @property
    def error_type(self):
        return self.__error_type
    
    # Hata kodunu döndürür
    @property
    def error_code(self):
        return self.__error_code
    
    # Hata zamanını döndürür
    @property
    def timestamp(self):
        return self.__timestamp
    
    # Hata kaynağını döndürür
    @property
    def source_function(self):
        return self.__source_function
    
    # Hata detaylarını sözlük olarak döndürür
    def get_details(self) -> dict:
        return {
            "type": self.__error_type,
            "code": self.__error_code,
            "message": self.__message,
            "timestamp": self.__timestamp.isoformat(),
            "source": self.__source_function
        }
    
    # Hatanın okunabilir formatta çıktısını verir
    def __str__(self):
        return (f"\n=== HATA DETAYI ===\n"
                f"TÜR     : {self.__error_type}\n"
                f"KOD     : {self.__error_code}\n"
                f"MESAJ   : {self.__message}\n"
                f"KAYNAK  : {self.__source_function}\n"
                f"ZAMAN   : {self.__timestamp.strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"===================\n")
# Geçersiz yaş durumunda hata fırlatır
def raise_invalid_age_error(age):
    msg = f"Girilen yaş ({age}) geçersiz. 5 ile 100 arasında olmalıdır."
    raise ClubManagerError(msg, "ValidationError", 2001)

# Zorunlu alan eksikliğinde hata fırlatır
def raise_missing_field_error(field_name: str):
    msg = f"Zorunlu alan eksik: '{field_name}' doldurulmalıdır."
    raise ClubManagerError(msg, "ValidationError", 2002)

# Geçersiz isim formatında hata fırlatır
def raise_invalid_name_error(value: str):
    msg = f"Geçersiz isim formatı: '{value}'. Sadece harf içermelidir."
    raise ClubManagerError(msg, "ValidationError", 2003)

# Geçersiz branş durumunda hata fırlatır
def raise_invalid_branch_error(branch: str):
    msg = f"Bilinmeyen spor branşı: '{branch}'. Lütfen geçerli bir branş seçiniz."
    raise ClubManagerError(msg, "ValidationError", 2008)

# ID çakışması durumunda hata fırlatır
def raise_duplicate_error(athlete_id):
    msg = f"Kayıt Çakışması: {athlete_id} ID numarası başka bir sporcuya ait."
    raise ClubManagerError(msg, "RepositoryError", 3001)

# Kayıt bulunamadığında hata fırlatır
def raise_not_found_error(identifier):
    msg = f"İşlem Başarısız: '{identifier}' kriterine uygun sporcu bulunamadı."
    raise ClubManagerError(msg, "RepositoryError", 3002)

# Veritabanı bağlantı sorununda hata fırlatır
def raise_database_connection_error(details=""):
    msg = f"Veritabanı bağlantı hatası. {details}"
    raise ClubManagerError(msg, "RepositoryError", 3003)

# Emeklilik yaşı sınırında hata fırlatır
def raise_retirement_error(name, age):
    msg = f"{name} ({age} yaşında), emeklilik yaşı sınırını doldurmuştur."
    raise ClubManagerError(msg, "BusinessRuleError", 4001)

# Yetersiz performans durumunda hata fırlatır
def raise_performance_error(name, played):
    msg = f"{name} yetersiz maç sayısı ({played}) nedeniyle kriterleri sağlamıyor."
    raise ClubManagerError(msg, "BusinessRuleError", 4002)

# Temiz kağıdı eksikliğinde hata fırlatır
def raise_clearance_error(name):
    msg = f"Transfer Engeli: {name} için 'Temiz Kağıdı' (Clearance) belgesi eksik."
    raise ClubManagerError(msg, "TransferError", 4003)

# Yüksek ceza puanı durumunda hata fırlatır
def raise_penalty_error(points):
    msg = f"Disiplin Engeli: Ceza puanı ({points}), limiti aşmıştır."
    raise ClubManagerError(msg, "TransferError", 4004)

# Yasaklı statü değişiminde hata fırlatır
def raise_status_error(current_status, new_status):
    msg = f"Statü Değişikliği Reddedildi: {current_status} -> {new_status}."
    raise ClubManagerError(msg, "BusinessRuleError", 4006)

# Bütçe aşımı durumunda hata fırlatır
def raise_budget_exceeded_error(amount: float, budget: float):
    msg = f"Bütçe Yetersiz: Talep edilen {amount}, kalan bütçeyi ({budget}) aşıyor."
    raise ClubManagerError(msg, "FinancialError", 4009)

# Dosya bulunamadığında hata fırlatır
def raise_file_not_found_error(filename: str):
    msg = f"Kritik Hata: '{filename}' dosyası sistemde bulunamadı."
    raise ClubManagerError(msg, "FileSystemError", 5001)

# JSON format hatasında hata fırlatır    
def raise_json_decode_error(filename: str):
    msg = f"Veri Hatası: '{filename}' dosyası bozuk veya geçersiz JSON formatında."
    raise ClubManagerError(msg, "FileSystemError", 5004)