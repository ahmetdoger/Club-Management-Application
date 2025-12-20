import unittest
import os
import json
from modules.finance.services.manager import FinanceManager
from modules.finance.services.analyzer import FinancialAnalyzer
from modules.finance.data.constants import TransactionType, IncomeCategory, ExpenseCategory

# Analiz ,raporlama fonksiyonlarını test eder
class TestFinancialAnalyzer(unittest.TestCase):

    def setUp(self):
        self.test_db_file = "test_analysis_data.json"
        
        # Manager ve Analyzer aynı test veritabanını kullanmalı
        self.manager = FinanceManager()
        self.manager.repo.file_path = self.test_db_file
        
        self.analyzer = FinancialAnalyzer()
        self.analyzer.repo.file_path = self.test_db_file
        
        # Dosyayı sıfırla
        with open(self.test_db_file, 'w') as f:
            json.dump([], f)
            
        # --- TEST VERİLERİNİ YÜKLE (SEED DATA) ---
        
        # 1. Gelir: 1000 TL (Kategori: MAÇ BİLETİ)
        self.manager.add_transaction(
            TransactionType.INCOME.value, 
            IncomeCategory.MATCH_TICKET.value, 
            1000, 
            "Derbi Bileti"
        )
        
        # 2. Gelir: 500 TL (Kategori: SPONSORLUK)
        self.manager.add_transaction(
            TransactionType.INCOME.value, 
            IncomeCategory.SPONSORSHIP.value, 
            500, 
            "Forma Sponsoru"
        )
        
        # 3. Gider: 400 TL (Oyuncu Ödemesi)
        # ExpenseCategory Enum'ından bir değer seçiyoruz
        self.manager.add_transaction(
            TransactionType.EXPENSE.value, 
            ExpenseCategory.SALARY.value, 
            400, 
            "Ödeme: SPORCU_AHMET"
        )

    def tearDown(self):
        if os.path.exists(self.test_db_file):
            os.remove(self.test_db_file)

    def test_financial_summary_balance(self):
        """
        Genel Bakiye Testi.
        Toplam Gelir: 1000 + 500 = 1500
        Toplam Gider: 400
        Beklenen Bakiye: 1100
        """
        summary = self.manager.get_financial_summary()
        
        self.assertEqual(summary['toplam_gelir'], 1500)
        self.assertEqual(summary['toplam_gider'], 400)
        self.assertEqual(summary['bakiye'], 1100)

    def test_budget_status(self):
        """
        Bütçe Durumu (Kâr/Zarar) Testi.
        Bakiye pozitif olduğu için 'KÂR' dönmeli.
        """
        status_report = self.analyzer.get_budget_status()
        self.assertEqual(status_report['durum'], "KÂR")
        self.assertEqual(status_report['net_bakiye'], 1100)

    def test_athlete_cost_search(self):
        """
        Sporcu Maliyet Analizi Testi.
        'SPORCU_AHMET' için yapılan harcamalar bulunmalı.
        """
        result = self.analyzer.calculate_athlete_total_cost("SPORCU_AHMET")
        
        self.assertEqual(result['total_cost'], 400)
        self.assertEqual(result['transaction_count'], 1)
        self.assertEqual(result['athlete_id'], "SPORCU_AHMET")

    #Kategori Bazlı Dağılım Testi.
    def test_category_breakdown(self):
        
        breakdown = self.manager.get_category_breakdown()

        # Enum değerlerini string'e çevirip kontrol eder
        ticket_key = f"{TransactionType.INCOME.value} - {IncomeCategory.MATCH_TICKET.value}"
        salary_key = f"{TransactionType.EXPENSE.value} - {ExpenseCategory.SALARY.value}"
        
        self.assertIn(ticket_key, breakdown)
        self.assertIn(salary_key, breakdown)
        
        # Değer kontrolü
        self.assertEqual(breakdown[ticket_key], 1000)