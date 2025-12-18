from ..data.transaction import Transaction
from ..data.json_db_rules import FinanceRepository

class FinanceManager:
    def __init__(self):
        self.repo = FinanceRepository()

    def add_entry(self, t_type, category, amount, description=""):
        """
        UI'dan gelen verileri doğrular, objeye çevirir ve JSON'a yazar.
        """
        # 1. Kontrol: Sayısal doğrulama (Servis katmanında yapılır)
        try:
            val_amount = float(amount)
            if val_amount <= 0:
                return False, "Hata: Tutar 0'dan büyük olmalıdır!"
        except ValueError:
            return False, "Hata: Lütfen geçerli bir sayı giriniz!"

        # 2. Veriyi Model kalıbına sok
        new_transaction = Transaction(
            t_type=t_type,
            category=category,
            amount=val_amount,
            description=description
        )

        # 3. JSON'a kaydet (Hocanın kuralı: Veri burada birikmez, direkt dosyaya gider)
        try:
            # Önce mevcut verileri çek
            data = self.repo.load()
            # Yeni sözlüğü listeye ekle
            data.append(new_transaction.to_dict())
            # Dosyayı güncelle
            self.repo.save(data)
            return True, "İşlem başarıyla kaydedildi."
        except Exception as e:
            return False, f"Sistemsel Hata: {str(e)}"