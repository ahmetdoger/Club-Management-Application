# Tüm finansal hataların türetildiği temel hata sınıfı
class FinanceError(Exception):
    def __init__(self, message="Bir finans hatası oluştu.", error_code=1000):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)

# Veri tipi sayısal olmadığında gösterilir 
class InvalidDataTypeError(FinanceError):
    def __init__(self, expected_type, received_type):
        detail = f"Veri Tipi Hatası: '{expected_type}' beklenirken '{received_type}' alındı."
        super().__init__(message=detail, error_code=1001)

# Tutar 0 veya negatif girildiğinde gösterilir
class InvalidAmountError(FinanceError):
    def __init__(self, amount):
        detail = f"Geçersiz Tutar: {amount} TL. Tutar pozitif olmalıdır."
        super().__init__(message=detail, error_code=1002)

# Dosya okuma/yazma işlemlerinde sorun olduğunda gösterilir
class DataStorageError(FinanceError):
    def __init__(self, file_path, reason):
        detail = f"Veri Erişim Hatası: '{file_path}' dosyasına erişilemedi. Sebep: {reason}"
        super().__init__(message=detail, error_code=1003)


# Belirlenen tek seferlik işlem limiti aşıldığında gösterilir
class TransactionLimitExceededError(FinanceError):
    def __init__(self, amount, limit):
        detail = f"Limit Aşımı: {amount} TL tutarı, belirlenen {limit} TL limitini aşıyor."
        super().__init__(message=detail, error_code=1004)

# İşlem tipi ile kategori uyuşmadığında gösterilir 
class CategoryMismatchError(FinanceError):
    def __init__(self, t_type, category):
        detail = f"Kategori Uyuşmazlığı: '{t_type}' işlem türü, '{category}' kategorisi ile eşleşmiyor."
        super().__init__(message=detail, error_code=1005)