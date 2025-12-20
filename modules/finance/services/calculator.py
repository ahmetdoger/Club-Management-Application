from abc import ABC, abstractmethod
from datetime import datetime
from ..exceptions.errors import (
    InvalidAmountError, 
    InvalidDataTypeError,
    InvalidRateError,
    InvalidCurrencyError,
    InvalidDateFormatError
)

# Tüm finansal hesaplayıcıların türetileceği soyut ata sınıf
class BaseFinancialCalculator(ABC):
    
    __default_currency = "TRY"

    def __init__(self):
        # Her hesaplayıcı işlem anındaki zamanı tutar
        self._calculation_date = datetime.now()

    # Soyut Metot (Polymorphism)
    @abstractmethod
    def calculate(self, amount, **kwargs):
        pass

    # Class Method (Para birimi okuma)
    @classmethod
    def get_currency(cls):
        return cls.__default_currency

    # Class Method (Para birimi değiştirme - Hata Kontrollü)
    @classmethod
    def set_currency(cls, new_code):
        # Para birimi kodu string mi?
        if not isinstance(new_code, str):
            raise InvalidDataTypeError("String", type(new_code).__name__)
        
        # Para birimi kodu uzunluğunu kontrol eder
        if len(new_code) != 3:
            raise InvalidCurrencyError(new_code)
            
        cls.__default_currency = new_code.upper()

    # Static Method (Tutar Validasyonu - Hata Kontrollü)
    @staticmethod
    def validate_amount(value):
        # Sayısal mı?
        if not isinstance(value, (int, float)):
            raise InvalidDataTypeError("Sayı (int/float)", type(value).__name__)
        
        # Pozitif mi
        if value < 0:
            raise InvalidAmountError(value)
            
        return float(value)

# Üyelik Aidatı Gecikme Hesaplayıcısı
class LateFeeCalculator(BaseFinancialCalculator):
    
    # Varsayılan günlük faiz %0.5, Ceza faizi %2.0
    def __init__(self, daily_rate=0.005, penalty_rate=0.020):
        super().__init__()
        # Değerleri setter üzerinden atayarak kontrolü sağlıyoruz
        self.daily_rate = daily_rate
        self.penalty_rate = penalty_rate

    # Property: Normal Oran
    @property
    def daily_rate(self):
        return self.__daily_rate

    # Setter: Normal Oran (Hata Kontrollü)
    @daily_rate.setter
    def daily_rate(self, new_rate):
        if not isinstance(new_rate, (int, float)):
            raise InvalidDataTypeError("Oran (float)", type(new_rate).__name__)
        
        if not (0 <= new_rate <= 1):
            raise InvalidRateError(new_rate)
            
        self.__daily_rate = new_rate

    # Property: Ceza Oranı
    @property
    def penalty_rate(self):
        return self.__penalty_rate

    # Setter: Ceza Oranı (Hata Kontrollü)
    @penalty_rate.setter
    def penalty_rate(self, new_rate):
        if not isinstance(new_rate, (int, float)):
            raise InvalidDataTypeError("Oran (float)", type(new_rate).__name__)
            
        if not (0 <= new_rate <= 1):
            raise InvalidRateError(new_rate)
            
        self.__penalty_rate = new_rate

    # Polymorphism: Kademeli Gecikme Faizi Hesabı
    def calculate(self, base_amount, **kwargs):
        days = kwargs.get('days_late', 0)
        
        # Tutar kontrolü 
        valid_amount = self.validate_amount(base_amount)
        
        if not isinstance(days, int):
            raise InvalidDataTypeError("Gün Sayısı (int)", type(days).__name__)
        
        if days <= 0:
            return valid_amount
            
        # Gecikme 6 ayı geçtiğinde ceza faizi uygulanır
        if days > 180:
            active_rate = self.__penalty_rate
        else:
            active_rate = self.__daily_rate
            
        interest = valid_amount * active_rate * days
        return round(valid_amount + interest, 2)

    # Static Method: Tarih farkı hesabı (Hata Kontrollü)
    @staticmethod
    def calculate_days_overdue(due_date_str):
        try:
            due = datetime.strptime(due_date_str, "%d-%m-%Y")
            delta = datetime.now() - due
            return max(0, delta.days)
        except ValueError:
           #Tarih farkı hatalı gelirse hata döndürür
            raise InvalidDateFormatError(due_date_str)

    @classmethod
    def create_strict_calculator(cls):
        return cls(daily_rate=0.010, penalty_rate=0.050)

# Vergi Hesaplayıcısı
class TaxDeductionCalculator(BaseFinancialCalculator):
    
    def __init__(self, tax_rate=0.18):
        super().__init__()
        self.tax_rate = tax_rate 

    @property
    def tax_rate(self):
        return self.__tax_rate

    @tax_rate.setter
    def tax_rate(self, new_rate):
        if not (0 <= new_rate <= 1):
            raise InvalidRateError(new_rate)
        self.__tax_rate = new_rate

    # Polymorphism: Net Gelir Hesabı
    def calculate(self, gross_amount, **kwargs):
        valid_amount = self.validate_amount(gross_amount)
        tax_amount = valid_amount * self.__tax_rate
        return round(valid_amount - tax_amount, 2)

    @staticmethod
    def get_tax_bracket_info(amount):
        if amount > 100000:
            return "Yüksek Gelir Vergisi Dilimi (%20)"
        return "Standart Vergi Dilimi (%18)"

    @classmethod
    def corporate_tax_calculator(cls):
        return cls(tax_rate=0.20)

# Maaş Hesaplayıcısı
class SalaryCalculator(BaseFinancialCalculator):
    
    def __init__(self):
        super().__init__()
        self.__insurance_rate = 0.15 
        self.__income_tax_rate = 0.15

    # Polymorphism: Net Maaş Hesabı
    def calculate(self, gross_salary, **kwargs):
        valid_salary = self.validate_amount(gross_salary)
        
        insurance = valid_salary * self.__insurance_rate
        tax_base = valid_salary - insurance
        income_tax = tax_base * self.__income_tax_rate
        
        return round(valid_salary - (insurance + income_tax), 2)

    @staticmethod
    def estimate_annual_cost(monthly_gross):
        try:
            valid_val = BaseFinancialCalculator.validate_amount(monthly_gross)
            return valid_val * 12
        except InvalidAmountError:
           #Hesap negatif gelirse hata döndürür
            raise 

    @classmethod
    def manager_salary_calculator(cls):
        return cls()