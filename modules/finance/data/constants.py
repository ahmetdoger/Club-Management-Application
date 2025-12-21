from enum import Enum

# İşlem Türleri (Gelir / Gider)
class TransactionType(Enum):
    INCOME = "Gelir"
    EXPENSE = "Gider"

# Gelir Kategorileri
class IncomeCategory(Enum):
    MEMBERSHIP_FEE = "Üyelik Aidatı"   
    MATCH_TICKET = "Maç Bileti"        
    SPONSORSHIP = "Sponsorluk"         
    DONATION = "Bağış"
    PRODUCT_SALE = "Ürün Satışı"
    OTHER = "Diğer Gelir"

# Gider Kategorileri
class ExpenseCategory(Enum):
    SALARY = "Maaş Ödemesi"           
    EQUIPMENT = "Ekipman"
    MAINTENANCE = "Tesis Bakım"
    TRAVEL = "Deplasman/Seyahat"
    TAX = "Vergi Ödemesi"
    UTILITIES = "Fatura (Elk/Su)"
    OTHER = "Diğer Gider"