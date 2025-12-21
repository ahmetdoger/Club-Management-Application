from ..exceptions.errors import (
    InvalidAmountError, 
    TransactionLimitExceededError, 
    CategoryMismatchError
)

from .constants import TransactionType, IncomeCategory, ExpenseCategory

# Veri bütünlüğünü ve iş kurallarını denetleyen sınıf
class FinanceRules:
    def __init__(self):
        # Tek seferde en fazla 10 Milyon TL işlem yapılabilir
        self.MAX_TRANSACTION_AMOUNT = 10000000 

    # 1. KURAL: Tutar Limit Kontrolleri
    def check_business_limits(self, amount):
        # Negatif veya sıfır kontrolü
        if amount <= 0:
            raise InvalidAmountError(amount)

        # Üst limit kontrolü
        if amount > self.MAX_TRANSACTION_AMOUNT:
            raise TransactionLimitExceededError(amount, self.MAX_TRANSACTION_AMOUNT)

        # Hata yoksa sessizce devam (True)
        return True

    # 2. KURAL: Kategori ve Tip Tutarlılığı
    def validate_category_consistency(self, t_type, category):
        # Eğer Tip GELİR ise, kategori de GELİR listesinde olmalı
        if t_type == TransactionType.INCOME.value:
            valid_incomes = [i.value for i in IncomeCategory]
            if category not in valid_incomes:
                raise CategoryMismatchError(t_type, category)

        # Eğer Tip GİDER ise, kategori de GİDER listesinde olmalı
        elif t_type == TransactionType.EXPENSE.value:
            valid_expenses = [e.value for e in ExpenseCategory]
            if category not in valid_expenses:
                raise CategoryMismatchError(t_type, category)

        return True