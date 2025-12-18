class MainError(Exception):

    def __init__(self, message: str = "Bir hata meydana geldi.", error_code: int = 1000):
      
      """Ana hata sınıfı, tüm özel hata sınıflarının temelini oluşturur."""

      self.message = message
      self.error_code = error_code
      super().__init__(self.message)

    def __str__(self):
       
       """Hatanın kullanıcıya veya loglara nasıl yazılacağını belirler."""

       return (f"Hata {self.error_code}: {self.message}")
    
class InvalidTypeError(MainError):

    def __init__(self, veri_type: float):
        
        """Veri tipi hatalarını temsil eden özel hata sınıfı."""

    def __init__(self, expected_type, received_type):
        self.expected_type = expected_type
        self.received_type = received_type
        detail = f"Hatalı veri tipi! Beklenen: {expected_type}, Gelen: {received_type}."
        super().__init__(message=detail, error_code=1001)
    
class InvalidAmountError(MainError):

    """Negatif veya sıfır tutar girildiğinde fırlatılır."""
    
    def __init__(self, amount):
        detail = f"Hata: {amount} geçersiz bir tutardır. Tutar pozitif olmalıdır."
        super().__init__(message=detail, error_code=1002)