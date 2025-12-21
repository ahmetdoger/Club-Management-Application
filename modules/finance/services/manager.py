from ..data import (
    FinanceRepository, 
    FinanceRules, 
    Transaction, 
    TransactionType
)
from ..exceptions.errors import FinanceError

# Kullanıcı ile backend arasındaki finansal işlemleri yöneten servis sınıfı
class FinanceManager:
    # Gerekli bileşenleri başlatır
    def __init__(self):
        self.repo = FinanceRepository()
        self.rules = FinanceRules()

    # Yeni işlem ekler (Hataları yakalar ve kullanıcıya mesaj döner)
    def add_transaction(self, t_type_val, category_val, amount_val, description=""):
        try:
            # 1. Veri Tipi Kontrolü
            try:
                val_amount = float(amount_val)
            except ValueError:
                return False, "Hata: Tutar sayısal olmalıdır."

            # 2. İş Kuralları Kontrolü (Limit ve Negatiflik) - Hata varsa fırlatır
            self.rules.check_business_limits(val_amount)

            # 3. Kategori Tutarlılık Kontrolü (Gelir seçip Gider girmesin)
            self.rules.validate_category_consistency(t_type_val, category_val)

            # 4. Modeli Oluştur (Data katmanındaki Transaction sınıfı)
            new_transaction = Transaction(
                t_type=t_type_val,
                category=category_val,
                amount=val_amount,
                description=description
            )

            # 5. Kaydet (Repository hata verirse yakalanır)
            self.repo.save_record(new_transaction.to_dict())
            return True, "İşlem başarıyla kaydedildi."

        except FinanceError as e:
            # Bizim tanımladığımız hatalar (Limit aşıldı, Dosya yok vb.)
            return False, f"Engel: {e.message}"
        except Exception as e:
            # Hiç beklemediğimiz sistemsel hatalar
            return False, f"Beklenmeyen Hata: {str(e)}"

    # ID'si verilen işlemi siler
    def delete_transaction(self, transaction_id):
        try:
            all_data = self.repo.load_all()
            # Silinecek ID haricindekileri filtrele
            new_data = [t for t in all_data if t["id"] != transaction_id]
            
            if len(all_data) == len(new_data):
                return False, "Silinecek kayıt bulunamadı."
                
            # Repository'nin private metodunu kullanarak kaydet
            self.repo._save_to_file(new_data)
            return True, "Kayıt silindi."
        except FinanceError as e:
            return False, f"Veri Hatası: {e.message}"
        except Exception as e:
            return False, f"Silme Hatası: {str(e)}"

    # İşlem güncelleme
    def update_transaction(self, transaction_id, new_amount=None, new_desc=None):
        try:
            all_data = self.repo.load_all()
            found = False
            
            for item in all_data:
                if item["id"] == transaction_id:
                    found = True
                    # Tutar değişiyorsa kuralları tekrar işlet
                    if new_amount is not None:
                        val_amt = float(new_amount)
                        self.rules.check_business_limits(val_amt)
                        item["tutar"] = val_amt
                    
                    if new_desc is not None:
                        item["aciklama"] = new_desc
                    break
            
            if not found:
                return False, "Kayıt bulunamadı."
                
            self.repo._save_to_file(all_data)
            return True, "Güncelleme başarılı."
            
        except ValueError:
            return False, "Yeni tutar geçersiz."
        except FinanceError as e:
            return False, f"Güncelleme Engeli: {e.message}"
        except Exception as e:
            return False, f"Hata: {str(e)}"

    # Tüm kayıtları getir
    def get_all_transactions(self):
        # Okuma hatası olursa boş liste dönmek yerine hatayı UI'ya iletebiliriz
        # Ama şimdilik boş liste dönmek daha güvenli
        try:
            return self.repo.load_all()
        except FinanceError:
            return []

    # Genel finansal özeti hesaplar
    def get_financial_summary(self):
        try:
            transactions = self.repo.load_all()
            total_inc = sum(t["tutar"] for t in transactions if t["tip"] == TransactionType.INCOME.value)
            total_exp = sum(t["tutar"] for t in transactions if t["tip"] == TransactionType.EXPENSE.value)
            return {
                "toplam_gelir": total_inc,
                "toplam_gider": total_exp,
                "bakiye": total_inc - total_exp
            }
        except Exception:
            return {"toplam_gelir": 0, "toplam_gider": 0, "bakiye": 0}

    # Kategori bazlı harcama raporu
    def get_category_breakdown(self):
        try:
            data = self.repo.load_all()
            breakdown = {}
            for t in data:
                key = f"{t['tip']} - {t['kategori']}"
                breakdown[key] = breakdown.get(key, 0) + t['tutar']
            return breakdown
        except Exception:
            return {}