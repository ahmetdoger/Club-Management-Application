from datetime import datetime, timedelta
from ..data import FinanceRepository, TransactionType

# Finansal verileri analiz ederek raporlar üreten servis sınıfı
class FinancialAnalyzer:
    
    # Raporlama dili (Varsayılan Türkçe)
    __report_language = "TR"

    def __init__(self):
        self.repo = FinanceRepository()
        # Analiz sonuçlarını geçici olarak hafızada tutmak için (Encapsulation)
        self.__analysis_cache = {}

    # (Rapor dili değiştirme)
    @classmethod
    def set_report_language(cls, lang_code):
        if lang_code in ["TR", "EN"]:
            cls.__report_language = lang_code

    # Tarih filtresi yardımcısı)
    @staticmethod
    def is_date_in_range(target_date_str, start_date, end_date):
        # Verilen string tarihin, belirtilen aralıkta olup olmadığını kontrol eder
        try:
            t_date = datetime.strptime(target_date_str.split()[0], "%d-%m-%Y")
            return start_date <= t_date <= end_date
        except ValueError:
            return False

    # Haftalık, Aylık, Yıllık Gelir/Gider Hesabı (Kategori Bazlı)
    def analyze_by_period(self, period_type="month"):
        """
        period_type: 'week', 'month', 'year' olabilir.
        Dönüş: {'Gelir': {'Sponsor': 500}, 'Gider': {'Maaş': 1000}}
        """
        all_data = self.repo.load_all()
        now = datetime.now()
        
        # Tarih aralığını belirle
        if period_type == "week":
            start_date = now - timedelta(days=7)
        elif period_type == "month":
            start_date = now - timedelta(days=30)
        elif period_type == "year":
            start_date = now - timedelta(days=365)
        else:
            return {} # Geçersiz periyot

        # Sonuçları tutacak sözlük yapısı
        report = {
            TransactionType.INCOME.value: {},
            TransactionType.EXPENSE.value: {}
        }
        
        for item in all_data:
            # Tarih kontrolü 
            if self.is_date_in_range(item["tarih"], start_date, now):
                t_type = item["tip"]
                cat = item["kategori"]
                amount = item["tutar"]
                
                # İlgili kategorinin toplamını güncelle
                if cat in report[t_type]:
                    report[t_type][cat] += amount
                else:
                    report[t_type][cat] = amount
        
        self.__analysis_cache[f"period_{period_type}"] = report
        return report

    # Oyuncu Bazlı Toplam Maliyet Hesabı (ID ile Arama)
    def calculate_athlete_total_cost(self, athlete_id):
        """
        Belirli bir sporcuya (ID'sine göre) yapılan tüm harcamaları hesaplar.
        Not: Açıklama kısmında ID geçiyorsa o kişiye ait sayar.
        """
        all_data = self.repo.load_all()
        total_cost = 0.0
        details = []

        for item in all_data:
            # Sadece giderlere bakıyoruz
            if item["tip"] == TransactionType.EXPENSE.value:
                # Açıklama içinde ID geçiyor mu kontrolü (Arama mantığı)
                if athlete_id in item["aciklama"]:
                    total_cost += item["tutar"]
                    details.append(item)
        
        return {
            "athlete_id": athlete_id,
            "total_cost": total_cost,
            "transaction_count": len(details),
            "transactions": details
        }

    # Bütçe Açığı veya Kâr Durumu (Genel)
    def get_budget_status(self):
        summary = self._calculate_totals() # Private yardımcı metod
        balance = summary["balance"]
        
        status = "DENK"
        if balance > 0:
            status = "KÂR"
        elif balance < 0:
            status = "ZARAR (BÜTÇE AÇIĞI)"
            
        return {
            "durum": status,
            "net_bakiye": balance,
            "detay": summary
        }

    # ID veya Kriter ile Gelişmiş Arama (Genel Kullanım İçin)
    def search_transactions(self, search_term):
        all_data = self.repo.load_all()
        results = []
        
        for item in all_data:
            # ID'de, kategoride , tarihte veya açıklamada arama yapar
            if (search_term in item["id"] or 
                search_term in item["kategori"] or 
                search_term in item["tarih"] or
                search_term in item["aciklama"]):
                results.append(item)
                
        return results

    # Özel yardımcı metot (Kapsülleme örneği)
    def _calculate_totals(self):
        data = self.repo.load_all()
        inc = sum(t["tutar"] for t in data if t["tip"] == TransactionType.INCOME.value)
        exp = sum(t["tutar"] for t in data if t["tip"] == TransactionType.EXPENSE.value)
        return {"income": inc, "expense": exp, "balance": inc - exp}