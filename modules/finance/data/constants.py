from enum import Enum

class TransactionType(Enum):
    INCOME = "Gelir"
    EXPENSE = "Gider"

class IncomeCategory(Enum):
    SPONSOR = "Sponsorluk"
    MEMBERSHIP = "Üyelik Aidatı"
    TICKET = "Bilet Satışı"
    BROADCAST = "Yayın Hakları"
    OTHER = "Diğer Gelir"

class ExpenseCategory(Enum):
    SALARY = "Personel Maaşı"
    FACILITY = "Tesis Gideri"
    TRAVEL = "Seyahat/Konaklama"
    EQUIPMENT = "Ekipman"
    OTHER = "Diğer Gider"