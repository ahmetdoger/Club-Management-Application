import unittest
import os
import json
from modules.finance.services.manager import FinanceManager
from modules.finance.data.constants import TransactionType, IncomeCategory, ExpenseCategory

# Manager sınıfı özelliklerini test eder
class TestFinanceManager(unittest.TestCase):

    def setUp(self):
        # 1. Test için geçici bir JSON dosyası adı belirle
        self.test_db_file = "test_manager_data.json"
        
        # 2. Manager sınıfını başlat
        self.manager = FinanceManager()
        
        # 3. Manager'ın repo dosyasını test dosyasına yönlendir (Mocking)
        self.manager.repo.file_path = self.test_db_file
        
        # 4. Dosyayı temizle/oluştur
        with open(self.test_db_file, 'w') as f:
            json.dump([], f)

    def tearDown(self):
        # Her testten sonra çöp dosyasını sil
        if os.path.exists(self.test_db_file):
            os.remove(self.test_db_file)

    def test_add_transaction_success(self):
        """
        Madde 178: Başarılı ödeme oluşturma testi.
        """
        success, message = self.manager.add_transaction(
            t_type_val=TransactionType.INCOME.value,
            category_val=IncomeCategory.SPONSORSHIP.value,
            amount_val=5000.0,
            description="Ana Sponsorluk Ödemesi"
        )
        
        # 1. İşlem başarılı döndü mü?
        self.assertTrue(success, f"İşlem başarısız oldu: {message}")
        
        # 2. Kayıt gerçekten dosyaya yazıldı mı?
        records = self.manager.get_all_transactions()
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]['tutar'], 5000.0)

    def test_transaction_limit_fail(self):
        """
        Madde 179: Hata durumu testi (Limit Aşımı).
        10 Milyon TL üzeri işlem reddedilmeli.
        """
        success, message = self.manager.add_transaction(
            t_type_val=TransactionType.INCOME.value,
            category_val=IncomeCategory.SPONSORSHIP.value,
            amount_val=15000000, # Çok yüksek tutar
            description="Limit Testi"
        )
        
        # İşlem başarısız olmalı 
        self.assertFalse(success)
        # Hata mesajı doğru mu?
        self.assertIn("Limit Aşımı", message)

    # Gelire gider girilirse hata vermeli
    def test_category_mismatch_fail(self):
    
        success, message = self.manager.add_transaction(
            t_type_val=TransactionType.INCOME.value,
            category_val="Personel Maaşı", # Bu bir gider kategorisidir
            amount_val=100
        )
        
        self.assertFalse(success)
        self.assertIn("Kategori Uyuşmazlığı", message)

    def test_delete_transaction(self):
        """
        Kayıt silme testi.
        """
        # Önce bir kayıt ekler
        self.manager.add_transaction("Gelir", "Sponsorluk", 100)
        records = self.manager.get_all_transactions()
        target_id = records[0]['id']
        
        # Sonra siler
        success, msg = self.manager.delete_transaction(target_id)
        self.assertTrue(success)
        
        # Silindiğini doğrular (Liste boş olmalı)
        records_after = self.manager.get_all_transactions()
        self.assertEqual(len(records_after), 0)