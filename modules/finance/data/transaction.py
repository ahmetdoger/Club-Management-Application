import uuid
from datetime import datetime

class Transaction:
    """
    Kulübün her bir finansal hareketini temsil eden temel sınıf.
    """
    def __init__(self, t_type, category, amount, description=""):
       
        self.transaction_id = str(uuid.uuid4())[:8]
        
       
        self.timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        
        self.type = t_type          
        self.category = category    
        self.amount = float(amount) 
        
        
        self.description = description if description.strip() else "Açıklama belirtilmedi."

    def to_dict(self):

        """Veriyi JSON dosyasına yazılacak 'Sözlük' formatına çevirir."""
        
        return {
            "islem_id": self.transaction_id,
            "tarih": self.timestamp,
            "tip": self.type,
            "kategori": self.category,
            "tutar": self.amount,
            "aciklama": self.description
        }