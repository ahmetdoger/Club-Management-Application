from abc import ABC, abstractmethod
from datetime import datetime, timedelta

# Tüm finansal hesaplayıcıların türetileceği soyut ana sınıf
class FinancialCalculator(ABC):
    
    __default_currency = "TL"

    def __init__(self):
        # Her hesaplayıcı için işlem tarihini o an olarak belirle
        self._calculation_date = datetime.now()

    # Soyut Metot (Polymorphism)
    @abstractmethod
    def calculate(self, amount, **kwargs):
        pass

    #Para birimi yönetimi
    @classmethod
    def get_currency(cls):
        # Private değişkene erişim sağlayan sınıf metodu
        return cls.__default_currency

    
    @classmethod
    def set_currency(cls, new_code):
        # Para birimini değiştiren güvenli metot
        if isinstance(new_code, str) and len(new_code) <= 3:
            cls.__default_currency = new_code

    # Static Method (Validasyon)
    @staticmethod
    def validate_amount(value):
        # Girilen tutarın sayısal ve pozitif olduğunu doğrular
        if not isinstance(value, (int, float)):
            raise ValueError("Hesaplanacak tutar sayısal olmalıdır.")
        if value < 0:
            raise ValueError("Tutar negatif olamaz.")
        return float(value)

#Üyelik Aidatı Gecikme Hesaplayıcısı
class LateFeeCalculator(FinancialCalculator):
    
    # Varsayılan günlük gecikme faiz oranı: %0.5
    def __init__(self, daily_rate=0.005):
        super().__init__()
        self.__daily_rate = daily_rate

    @property
    def daily_rate(self):
        return self.__daily_rate

    #Oranı değiştirmek için (Güvenlik kontrolü ile)
    @daily_rate.setter
    def daily_rate(self, new_rate):
        if 0 <= new_rate <= 1:
            self.__daily_rate = new_rate
        else:
            raise ValueError("Faiz oranı 0 ile 1 arasında olmalıdır.")


class LateFeeCalculator(FinancialCalculator):
    
    # Varsayılan günlük faiz %0.5, Ceza faizi %2.0 olarak ayarlandı
    def __init__(self, daily_rate=0.005, penalty_rate=0.020):
        super().__init__()
        # Kapsülleme: Normal faiz ve ceza faizi gizli değişkenlerde
        self.__daily_rate = daily_rate
        self.__penalty_rate = penalty_rate

    # Property (Getter): Normal oranı okumak için
    @property
    def daily_rate(self):
        return self.__daily_rate

    # Setter: Normal oranı değiştirmek için
    @daily_rate.setter
    def daily_rate(self, new_rate):
        if 0 <= new_rate <= 1:
            self.__daily_rate = new_rate
        else:
            raise ValueError("Faiz oranı 0 ile 1 arasında olmalıdır.")
        
    @property
    def penalty_rate(self):
        return self.__penalty_rate
    
    @penalty_rate.setter
    def penalty_rate(self , new_penalty_rate):
        if 0 <= new_penalty_rate <= 1:
            self.__penalty_rate = new_penalty_rate
        else:
            raise ValueError("Faiz oranı 0 ile 1 arasında olmalıdır.")

    # Polymorphism: Calculate metodu burada 'Kademeli Gecikme Faizi' hesaplar
    def calculate(self, base_amount, **kwargs):
        # kwargs içinden 'days_late' parametresini alıyoruz
        days = kwargs.get('days_late', 0)
        
        # Validasyonlar
        valid_amount = self.validate_amount(base_amount)
        if not isinstance(days, int) or days < 0:
            return valid_amount 
            
        # Eğer 180 günü geçerse, __penalty_rate (yüksek faiz) devreye girer
        if days > 180:
            active_rate = self.__penalty_rate
        else:
            active_rate = self.__daily_rate
            
        interest = valid_amount * active_rate * days
        total = valid_amount + interest
        
        return round(total, 2)

    @staticmethod
    def calculate_days_overdue(due_date_str):
        # 'GG-AA-YYYY' formatındaki tarihten bugüne kaç gün geçtiğini bulur
        try:
            due = datetime.strptime(due_date_str, "%d-%m-%Y")
            delta = datetime.now() - due
            return max(0, delta.days)
        except ValueError:
            return 0

    @classmethod
    def create_strict_calculator(cls):
        # Normali %1, Cezası %5 olan gecikme faizi döner
        return cls(daily_rate=0.010, penalty_rate=0.050)
    
#Sponsor ve Bilet Gelirleri için Vergi Hesaplayıcısı
class TaxDeductionCalculator(FinancialCalculator):
    
    def __init__(self, tax_rate=0.18):
        super().__init__()
        self.__tax_rate = tax_rate

    
    @property
    def tax_rate(self):
        return self.__tax_rate

    # Polymorphism: Calculate metodu burada 'Net Gelir' hesaplar (Vergi düşülmüş)
    def calculate(self, gross_amount, **kwargs):
        valid_amount = self.validate_amount(gross_amount)
        
        # Vergi Tutarı
        tax_amount = valid_amount * self.__tax_rate
        # Net Ele Geçen
        net_amount = valid_amount - tax_amount
        
        return round(net_amount, 2)

    # Vergi dilimi bilgisi
    @staticmethod
    def get_tax_bracket_info(amount):
        # Tutara göre hangi vergi dilimine girdiğini söyler (Simülasyon)
        
        if amount > 100000:
            return "Yüksek Gelir Vergisi (%20)"
        return "Standart Vergi (%18)"

    # Class Method: Şirketler için farklı hesaplayıcı
    @classmethod
    def corporate_tax_calculator(cls):
        return cls(tax_rate=0.20)

# Oyuncu Maaş Hesaplayıcısı (Brüt -> Net Dönüşümü)
class SalaryCalculator(FinancialCalculator):
    
    def __init__(self):
        super().__init__()
        # Sabit kesintiler 
        self.__insurance_rate = 0.15 
        self.__income_tax_rate = 0.15

    # Polymorphism: Calculate metodu burada 'Maaş' hesaplar
    def calculate(self, gross_salary, **kwargs):
        valid_salary = self.validate_amount(gross_salary)
        
        insurance = valid_salary * self.__insurance_rate
        tax_base = valid_salary - insurance
        income_tax = tax_base * self.__income_tax_rate
        
        net_salary = valid_salary - (insurance + income_tax)
        return round(net_salary, 2)

    # Yıllık maliyet tahmini
    @staticmethod
    def estimate_annual_cost(monthly_gross):
        return monthly_gross * 12

    def manager_salary_calculator(cls):
        # Yöneticilerde oranlar farklı olabilir
        instance = cls()
        return instance