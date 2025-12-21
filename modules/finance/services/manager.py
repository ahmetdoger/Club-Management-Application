import sys
import os

# Kendi modüllerimiz
from ..data import (
    FinanceRepository, 
    FinanceRules, 
    Transaction, 
    TransactionType,
    ExpenseCategory
)
from ..services.calculator import SalaryCalculator
from ..exceptions.errors import (
    FinanceError, 
    InvalidAmountError, 
    InvalidDataTypeError
)

from modules.information.repository import AthleteRepository

class FinanceManager:
    
    def __init__(self):
        self.repo = FinanceRepository()
        self.rules = FinanceRules()
        
        self.info_repo = AthleteRepository()

    # --- STANDART METOTLAR ---
    
    def add_transaction(self, t_type_val, category_val, amount_val, description=""):
        try:
            try:
                val_amount = float(amount_val)
            except ValueError:
                raise InvalidDataTypeError("Sayısal Tutar", type(amount_val).__name__)

            self.rules.check_business_limits(val_amount)
            self.rules.validate_category_consistency(t_type_val, category_val)

            new_transaction = Transaction(
                t_type=t_type_val,
                category=category_val,
                amount=val_amount,
                description=description
            )
            self.repo.save_record(new_transaction.to_dict())
            return True, "İşlem başarıyla kaydedildi."
        except FinanceError as e:
            return False, f"Engel: {e.message}"
        except Exception as e:
            return False, f"Sistem Hatası: {str(e)}"

    def delete_transaction(self, transaction_id):
        try:
            all_data = self.repo.load_all()
            new_data = [t for t in all_data if t["id"] != transaction_id]
            if len(all_data) == len(new_data):
                raise FinanceError("Silinecek kayıt bulunamadı.", error_code=404)
            self.repo._save_to_file(new_data)
            return True, "Kayıt silindi."
        except Exception as e:
            return False, f"Hata: {str(e)}"

    def update_transaction(self, transaction_id, new_amount=None, new_desc=None):
        try:
            all_data = self.repo.load_all()
            found = False
            for item in all_data:
                if item["id"] == transaction_id:
                    found = True
                    if new_amount:
                        val = float(new_amount)
                        self.rules.check_business_limits(val)
                        item["tutar"] = val
                    if new_desc:
                        item["aciklama"] = new_desc
                    break
            if not found: return False, "Kayıt bulunamadı."
            self.repo._save_to_file(all_data)
            return True, "Güncellendi."
        except Exception as e:
            return False, f"Hata: {str(e)}"

    def get_all_transactions(self):
        return self.repo.load_all()

    # --- MAAŞ ÖDEME ---

    def process_monthly_salaries(self):
        """
        Information modülünden verileri çeker ve ödeme yapar.
        Bağlantı hatası olursa program hata fırlatır.
        """
        try:
            # Veriyi çek
            data_list = self.info_repo.get_all()
            
            if not data_list:
                return False, "Sistemde ödenecek kişi bulunamadı (Liste boş)."

            success_count = 0
            fail_count = 0
            total_paid = 0
            salary_calc = SalaryCalculator()

            for person in data_list:
                try:

                    name = person.get("name", person.get("ad", "İsimsiz"))
                    p_id = person.get("id", "??")
                    gross = person.get("salary", person.get("maas", 0))

                    if isinstance(gross, str):
                        try:
                            gross = float(gross)
                        except ValueError:
                            gross = 0

                    if gross <= 0:
                        continue

                    # Hesapla
                    net_salary = salary_calc.calculate(gross)
                    
                    # Kaydet
                    desc = f"Maaş Ödemesi: {name} ({p_id})"
                    new_trans = Transaction(
                        t_type=TransactionType.EXPENSE.value,
                        category=ExpenseCategory.SALARY.value,
                        amount=net_salary,
                        description=desc
                    )
                    self.repo.save_record(new_trans.to_dict())
                    
                    success_count += 1
                    total_paid += net_salary
                    
                except Exception as inner_e:
                    print(f"[ATLANDI] {name}: {inner_e}")
                    fail_count += 1

            return True, (f"İşlem Tamamlandı.\n"
                          f"✔ {success_count} Kişiye {total_paid:.2f} TL ödendi.\n"
                          f"⚠ {fail_count} Hatalı kayıt atlandı.")

        except Exception as e:
            # Burada yakalanan hata, veri çekme veya işleme hatasıdır.
            return False, f"İşlem Hatası: {str(e)}"

    # --- RAPORLAMA ---
    def get_financial_summary(self):
        data = self.repo.load_all()
        inc = sum(t["tutar"] for t in data if t["tip"] == TransactionType.INCOME.value)
        exp = sum(t["tutar"] for t in data if t["tip"] == TransactionType.EXPENSE.value)
        return {"toplam_gelir": inc, "toplam_gider": exp, "bakiye": inc - exp}

    def get_category_breakdown(self):
        data = self.repo.load_all()
        bd = {}
        for t in data:
            k = f"{t['tip']} - {t['kategori']}"
            bd[k] = bd.get(k, 0) + t['tutar']
        return bd