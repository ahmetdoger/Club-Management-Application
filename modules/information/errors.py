from datetime import datetime
import inspect

# =============================================================================
# 1. BASE CLASS (TEK HATA SINIFI)
# =============================================================================

class ClubManagerError(Exception):
    """
    Projedeki TEK hata sınıfıdır.
    Kapsülleme kurallarına tam uyar.
    """
    def __init__(self, message: str, error_type: str = "GeneralError", error_code: int = 1000):
        self.__message = message
        self.__error_type = error_type
        self.__error_code = error_code
        self.__timestamp = datetime.now()
        
        # Hatanın nereden geldiğini bul
        try:
            curframe = inspect.currentframe()
            calframe = inspect.getouterframes(curframe, 2)
            self.__source_function = calframe[1][3]
        except Exception:
            self.__source_function = "Unknown"

        full_msg = f"[{self.__error_type}] {self.__message}"
        super().__init__(full_msg)

    @property
    def message(self):
        return self.__message

    @property
    def error_type(self):
        return self.__error_type

    @property
    def error_code(self):
        return self.__error_code

    @property
    def timestamp(self):
        return self.__timestamp
    
    @property
    def source_function(self):
        return self.__source_function

    def get_details(self) -> dict:
        return {
            "type": self.__error_type,
            "code": self.__error_code,
            "message": self.__message,
            "timestamp": self.__timestamp.isoformat(),
            "source": self.__source_function
        }

    def __str__(self):
        return (f"\n=== HATA DETAYI ===\n"
                f"TÜR     : {self.__error_type}\n"
                f"KOD     : {self.__error_code}\n"
                f"MESAJ   : {self.__message}\n"
                f"KAYNAK  : {self.__source_function}\n"
                f"ZAMAN   : {self.__timestamp.strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"===================\n")

# =============================================================================
# 2. YARDIMCI FONKSİYONLAR (İsimler diğer dosyalarla uyumlu hale getirildi)
# =============================================================================

def raise_invalid_age_error(age):
    """Yaş geçersizse fırlatılır."""
    msg = f"Girilen yaş ({age}) geçersiz. 5 ile 100 arasında olmalıdır."
    raise ClubManagerError(msg, "ValidationError", 2001)

def raise_missing_field_error(field_name: str):
    """Zorunlu alan eksikse fırlatılır."""
    msg = f"Zorunlu alan eksik: '{field_name}' doldurulmalıdır."
    raise ClubManagerError(msg, "ValidationError", 2002)

def raise_invalid_name_error(value: str):
    """İsim formatı hatalıysa fırlatılır."""
    msg = f"Geçersiz isim formatı: '{value}'. Sadece harf içermelidir."
    raise ClubManagerError(msg, "ValidationError", 2003)

def raise_invalid_branch_error(branch: str):
    """Branş geçersizse fırlatılır."""
    msg = f"Bilinmeyen spor branşı: '{branch}'. Lütfen geçerli bir branş seçiniz."
    raise ClubManagerError(msg, "ValidationError", 2008)

def raise_duplicate_error(athlete_id):
    """(DÜZELTİLDİ) ID çakışması varsa fırlatılır."""
    msg = f"Kayıt Çakışması: {athlete_id} ID numarası başka bir sporcuya ait."
    raise ClubManagerError(msg, "RepositoryError", 3001)

def raise_not_found_error(identifier):
    """(DÜZELTİLDİ) Kayıt bulunamazsa fırlatılır."""
    msg = f"İşlem Başarısız: '{identifier}' kriterine uygun sporcu bulunamadı."
    raise ClubManagerError(msg, "RepositoryError", 3002)

def raise_database_connection_error(details=""):
    """Veritabanı bağlantı hatası."""
    msg = f"Veritabanı bağlantı hatası. {details}"
    raise ClubManagerError(msg, "RepositoryError", 3003)

def raise_retirement_error(name, age):
    """(DÜZELTİLDİ) Emeklilik yaşı hatası."""
    msg = f"{name} ({age} yaşında), emeklilik yaşı sınırını doldurmuştur."
    raise ClubManagerError(msg, "BusinessRuleError", 4001)

def raise_performance_error(name, played):
    """(DÜZELTİLDİ) Performans yetersizliği hatası."""
    msg = f"{name} yetersiz maç sayısı ({played}) nedeniyle kriterleri sağlamıyor."
    raise ClubManagerError(msg, "BusinessRuleError", 4002)

def raise_clearance_error(name):
    """(DÜZELTİLDİ) Temiz kağıdı eksik hatası."""
    msg = f"Transfer Engeli: {name} için 'Temiz Kağıdı' (Clearance) belgesi eksik."
    raise ClubManagerError(msg, "TransferError", 4003)

def raise_penalty_error(points):
    """(DÜZELTİLDİ) Ceza puanı yüksek hatası."""
    msg = f"Disiplin Engeli: Ceza puanı ({points}), limiti aşmıştır."
    raise ClubManagerError(msg, "TransferError", 4004)

def raise_status_error(current_status, new_status):
    """(DÜZELTİLDİ) Statü değiştirme hatası."""
    msg = f"Statü Değişikliği Reddedildi: {current_status} -> {new_status}."
    raise ClubManagerError(msg, "BusinessRuleError", 4006)

def raise_budget_exceeded_error(amount: float, budget: float):
    """Bütçe yetersiz hatası."""
    msg = f"Bütçe Yetersiz: Talep edilen {amount}, kalan bütçeyi ({budget}) aşıyor."
    raise ClubManagerError(msg, "FinancialError", 4009)

def raise_file_not_found_error(filename: str):
    """Dosya bulunamadı hatası."""
    msg = f"Kritik Hata: '{filename}' dosyası sistemde bulunamadı."
    raise ClubManagerError(msg, "FileSystemError", 5001)

def raise_json_decode_error(filename: str):
    """JSON hatası."""
    msg = f"Veri Hatası: '{filename}' dosyası bozuk veya geçersiz JSON formatında."
    raise ClubManagerError(msg, "FileSystemError", 5004)