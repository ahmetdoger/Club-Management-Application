import json
import os

class FinanceRules:

    """JSON veri yapısının kurallarını ve limitlerini belirleyen sınıf."""

    def __init__(self):
        
        self.MAX_TRANSACTION_AMOUNT = 10000000  
        self.REQUIRED_FIELDS = ["islem_id", "tarih", "tip", "kategori", "tutar"]

    def validate_data_structure(self, data_list):

        """JSON'dan okunan verinin bozuk olup olmadığını kontrol eder."""

        if not isinstance(data_list, list):
            return False, "Veri formatı hatalı (Liste bekleniyor)."
        
        for record in data_list:
            for field in self.REQUIRED_FIELDS:
                if field not in record:
                    return False, f"Eksik alan tespit edildi: {field}"
        return True, "Veri yapısı sağlam."

    def check_business_limits(self, amount):

        """İşlemin finansal kurallara uyup uymadığını kontrol eder."""
        
        if amount > self.MAX_TRANSACTION_AMOUNT:
            return False, f"İşlem tutarı sınırı ({self.MAX_TRANSACTION_AMOUNT}) aşıyor!"
        return True, "Limit uygun."