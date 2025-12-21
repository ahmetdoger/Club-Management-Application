import unittest
from datetime import datetime

# Hesaplayıcı modüllerini import ediyoruz
from modules.finance.services.calculator import (
    LateFeeCalculator, 
    TaxDeductionCalculator, 
    SalaryCalculator
)
from modules.finance.exceptions.errors import InvalidRateError, InvalidAmountError

# Hesaplayıcı fonksiyonlarını test eder
class TestFinancialCalculators(unittest.TestCase):

    def setUp(self):
        # Her testten önce yeni nesneler oluşturulur
        self.late_fee_calc = LateFeeCalculator()
        self.tax_calc = TaxDeductionCalculator()
        self.salary_calc = SalaryCalculator()

    # --- GECİKME FAİZİ TESTLERİ (Madde 180) ---
    def test_late_fee_standard(self):
        """
        Senaryo: 1000 TL aidat, 30 gün gecikme (6 aydan az).
        Beklenen: Normal faiz oranı (%0.5) uygulanmalı.
        Hesap: 1000 + (1000 * 0.005 * 30) = 1150 TL
        """
        amount = 1000
        days = 30
        expected_total = 1150.0
        
        result = self.late_fee_calc.calculate(amount, days_late=days)
        self.assertEqual(result, expected_total, "Standart gecikme faizi hatalı hesaplandı.")

    def test_late_fee_penalty_scenario(self):
        """
        Senaryo: 1000 TL aidat, 200 gün gecikme (6 ayı geçmiş).
        Beklenen: Ceza faizi oranı (%2.0) devreye girmeli.
        Hesap: 1000 + (1000 * 0.020 * 200) = 5000 TL
        """
        amount = 1000
        days = 200 # 180 günü geçtiği için ceza faizi uygulanır
        expected_total = 5000.0
        
        result = self.late_fee_calc.calculate(amount, days_late=days)
        self.assertEqual(result, expected_total, "Ceza faizi (6 ay üzeri) devreye girmedi.")

    def test_no_late_fee(self):
        """
        Senaryo: Gecikme yok (0 gün).
        Beklenen: Ana para değişmemeli.
        """
        result = self.late_fee_calc.calculate(500, days_late=0)
        self.assertEqual(result, 500.0)

    # --- VERGİ VE MAAŞ TESTLERİ ---
    def test_tax_deduction(self):
        """
        Senaryo: 10.000 TL Brüt Gelir, %18 Vergi.
        Beklenen: 8200 TL Net Gelir.
        """
        # Vergi oranını manuel set eder , test için
        self.tax_calc.tax_rate = 0.18
        result = self.tax_calc.calculate(10000)
        self.assertEqual(result, 8200.0)

    def test_salary_net_calculation(self):
        """
        Senaryo: Personel maaş hesaplaması.
        Brüt maaştan sigorta ve gelir vergisi düşülerek net bulunur.
        """
        gross_salary = 20000
        net_salary = self.salary_calc.calculate(gross_salary)
        # Net maaş, brüt maaştan düşük olmalıdır
        self.assertTrue(net_salary < gross_salary)
        self.assertIsInstance(net_salary, float)

    # --- HATA YÖNETİMİ TESTLERİ ---
    def test_invalid_amount_input(self):
        """
        Senaryo: Negatif tutar girilmesi.
        Beklenen: InvalidAmountError fırlatmalı.
        """
        with self.assertRaises(InvalidAmountError):
            self.tax_calc.calculate(-100)

    def test_invalid_rate_input(self):
        """
        Senaryo: Vergi oranının 1'den büyük girilmesi.
        Beklenen: InvalidRateError fırlatmalı.
        """
        with self.assertRaises(InvalidRateError):
            self.tax_calc.tax_rate = 1.5