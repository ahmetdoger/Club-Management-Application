import unittest
import os
import json
from unittest.mock import MagicMock 
from modules.finance.services.manager import FinanceManager
from modules.finance.data.constants import TransactionType, IncomeCategory, ExpenseCategory

class TestFinanceManager(unittest.TestCase):
    """
    Bu test sınıfı:
    1. İşlem Ekleme/Silme/Güncelleme (CRUD)
    2. Modüller Arası Entegrasyon (Maaş Ödeme)
    senaryolarını test eder.
    """

    def setUp(self):
        # 1. Test için geçici veritabanı ayarla
        self.test_db_file = "test_manager_data.json"
        
        # 2. Manager sınıfını başlat
        self.manager = FinanceManager()
        self.manager.repo.file_path = self.test_db_file
        
        # 3. Dosyayı temizle
        with open(self.test_db_file, 'w') as f:
            json.dump([], f)

        # 4. Test için sahte veriler

        self.manager.info_repo = MagicMock()

    def tearDown(self):
        # Test bitince çöp dosyayı sil
        if os.path.exists(self.test_db_file):
            os.remove(self.test_db_file)

    def test_add_transaction_success(self):
        success, message = self.manager.add_transaction(
            TransactionType.INCOME.value,
            IncomeCategory.SPONSORSHIP.value, # Enum kullandık
            5000.0,
            "Ana Sponsor"
        )
        self.assertTrue(success)
        records = self.manager.get_all_transactions()
        self.assertEqual(len(records), 1)

    def test_transaction_limit_fail(self):
        # Limit aşımı testi (10 Milyon üzeri)
        success, message = self.manager.add_transaction(
            TransactionType.INCOME.value,
            IncomeCategory.SPONSORSHIP.value,
            15000000, 
            "Limit Testi"
        )
        self.assertFalse(success)
        self.assertIn("Limit", message) # Mesajda "Limit" kelimesi geçiyor mu?

    def test_category_mismatch_fail(self):
        # Gelir tipine Gider kategorisi girme hatası
        success, message = self.manager.add_transaction(
            TransactionType.INCOME.value,
            ExpenseCategory.SALARY.value, # Hata! Gelir tipinde Maaş olamaz
            100
        )
        self.assertFalse(success)

    def test_process_monthly_salaries_success(self):
        """
        Senaryo: Arkadaşının modülünden 2 kişilik düzgün veri geliyor.
        Beklenen: 2 tane Gider kaydı oluşmalı.
        """
        # 1. SAHTE VERİ 
        fake_data = [
            {"name": "Muslera", "salary": 20000, "id": "GS-01"},
            {"name": "Icardi", "salary": 30000, "id": "GS-09"}
        ]
        self.manager.info_repo.get_all.return_value = fake_data

        # 2. Fonksiyonu Çalıştır
        success, msg = self.manager.process_monthly_salaries()

        # 3. Kontrol Et
        self.assertTrue(success)
        self.assertIn("2 Kişiye", msg) # Mesajda "2 Kişiye" yazıyor mu?

        # 4. Kayıtlar gerçekten oluştu mu?
        records = self.manager.get_all_transactions()
        self.assertEqual(len(records), 2)
        # Maaşlardan vergi/kesinti düşülmüş olmalı (SalaryCalculator işliyor mu?)
        # 20000 brüt - net daha düşük olmalı
        self.assertTrue(records[0]['tutar'] < 20000)
        self.assertEqual(records[0]['kategori'], ExpenseCategory.SALARY.value)

    def test_process_monthly_salaries_mixed_data(self):
        """
        Senaryo: Biri düzgün, biri hatalı (string maaş), biri eksik maaş.
        Beklenen: Hatalıları atlayıp sadece düzgün olanı (1 kişi) ödemeli.
        """
        fake_data = [
            {"name": "Düzgün Oyuncu", "salary": 10000, "id": "01"}, # OK
            {"name": "Hatalı Oyuncu", "salary": "yirmibin", "id": "02"}, # String Hata
            {"name": "Bedava Oyuncu", "salary": 0, "id": "03"} # 0 Maaş atlanmalı
        ]
        self.manager.info_repo.get_all.return_value = fake_data

        success, msg = self.manager.process_monthly_salaries()

        self.assertTrue(success) # İşlem genel olarak başarılı sayılır
        
        # Sadece 1 kişi kaydedilmeli
        records = self.manager.get_all_transactions()
        self.assertEqual(len(records), 1)
        self.assertIn("Düzgün Oyuncu", records[0]['aciklama'])

    def test_process_monthly_salaries_empty(self):
        """
        Senaryo: Karşı taraftan boş liste geliyor.
        Beklenen: False dönmeli ve uyarı vermeli.
        """
        self.manager.info_repo.get_all.return_value = [] # Boş liste
        
        success, msg = self.manager.process_monthly_salaries()
        
        self.assertFalse(success)
        self.assertIn("bulunamadı", msg)