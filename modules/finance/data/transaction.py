import uuid
from datetime import datetime
from ..exceptions.errors import InvalidAmountError, InvalidDataTypeError

class Transaction:
    def __init__(self, t_type, category, amount, description=""):
        # 1. KONTROL: Veri Tipi float/int mi?
        if not isinstance(amount, (int, float)):
        
            raise InvalidDataTypeError(expected_type="Sayı (int/float)", received_type=type(amount).__name__)

        # 2. KONTROL:  Negatif mi?
        if amount <= 0:
            raise InvalidAmountError(amount)

        # Veri temizse atamaları yap
        self.transaction_id = str(uuid.uuid4())[:8]
        self.timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        self.type = t_type
        self.category = category
        self.amount = float(amount)
        self.description = description if description else "Açıklama yok"

    def to_dict(self):
        return {
            "id": self.transaction_id,
            "tarih": self.timestamp,
            "tip": self.type,
            "kategori": self.category,
            "tutar": self.amount,
            "aciklama": self.description
        }