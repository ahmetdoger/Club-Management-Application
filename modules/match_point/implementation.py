import random
from datetime import datetime

# Yan dosyalardaki sınıfları çağırıyoruz
# (.) nokta kullanımı aynı klasördeki dosyalara erişim sağlar
from base import MatchBase
from entities import Team, Stadium, Referee


# 1. FriendlyMatch (Dostluk Maçı)
# Özellik: Puan verilmez, kurallar daha esnektir.
class FriendlyMatch(MatchBase):
    """
    Dostluk maçlarını temsil eden sınıf.
    Lig puan tablosuna etkisi yoktur, hazırlık amaçlıdır.
    """
    def __init__(self, match_id, home_team, away_team, date_time, location):
        super().__init__(match_id, home_team, away_team, "Friendly", date_time)
        
        # Bu sınıfa özgü özellikler (Kapsüllenmiş)
        self.__location = location  # Stadium nesnesi
        self.__charity_event = False # Yardım maçı mı?
        self.__ticket_price = 0.0    # Bilet fiyatı

    def simulate_match(self):
        """
        Dostluk maçı simülasyonu. (Override)
        Daha rastgele ve bol gollü geçer.
        """
        print(f"\n--- Hazırlık Maçı Başlıyor: {self.get_home_team().get_name()} vs {self.get_away_team().get_name()} ---")
        
        home_score = random.randint(0, 5)
        away_score = random.randint(0, 5)
        
        self.set_score(f"{home_score}-{away_score}")
        self._set_status_internal("Finished")
        
        # İstatistikleri güncelle (Puan verilmez)
        self.get_home_team().update_stats(home_score, away_score)
        self.get_away_team().update_stats(away_score, home_score)
        
        print(f"Maç Sonucu: {self.get_score()}")

    def calculate_points(self):
        # Polimorfizm: Puan yok
        return "Dostluk maçında puan verilmez."

    def get_match_info(self):
        loc_name = self.__location.get_name() if self.__location else "Bilinmiyor"
        return f"[Hazırlık] {self.get_home_team().get_short_code()} vs {self.get_away_team().get_short_code()} @ {loc_name}"

    def update_status(self, new_status):
        self._set_status_internal(new_status)

    # --- Getter & Setter Metotları 

    def get_ticket_price(self):
        return self.__ticket_price

    def set_ticket_price(self, price):
        if price >= 0:
            self.__ticket_price = price
        else:
            print("Hata: Bilet fiyatı negatif olamaz.")

    def is_charity_event(self):
        return self.__charity_event

    def set_charity_event(self, status):
        if isinstance(status, bool):
            self.__charity_event = status

    def get_location(self):
        return self.__location
# 2. LeagueMatch (Lig Maçı)
# Özellik: Galibiyet 3 puan, Beraberlik 1 puan. Hakem zorunludur.
class LeagueMatch(MatchBase):
    """
    Resmi lig müsabakalarını temsil eder.
    """
    def __init__(self, match_id, home_team, away_team, date_time, week_number, referee):
        super().__init__(match_id, home_team, away_team, "League", date_time)
        
        self.__week_number = week_number
        self.__referee = referee # Referee nesnesi
        self.__weather_condition = "Sunny"

    def simulate_match(self):
        """
        Lig maçı simülasyonu. (Override)
        Ev sahibi avantajı vardır.
        """
        print(f"\n--- Lig Maçı ({self.__week_number}. Hafta) ---")
        print(f"Hakem: {self.__referee.get_full_name()}")
        
        # Ev sahibi avantajı mantığı
        h_power = random.randint(1, 10) + 2
        a_power = random.randint(1, 10)
        
        h_goals = 0
        a_goals = 0
        
        if h_power > a_power:
            h_goals = random.randint(1, 4)
            a_goals = random.randint(0, h_goals - 1) if h_goals > 0 else 0
        elif a_power > h_power:
            a_goals = random.randint(1, 4)
            h_goals = random.randint(0, a_goals - 1) if a_goals > 0 else 0
        else:
            h_goals = random.randint(0, 2)
            a_goals = h_goals
            
        self.set_score(f"{h_goals}-{a_goals}")
        self._set_status_internal("Finished")
        
        if self.__referee:
            self.__referee.increment_match_count()
            
        # Puanlar Team sınıfında otomatik hesaplanır
        self.get_home_team().update_stats(h_goals, a_goals)
        self.get_away_team().update_stats(a_goals, h_goals)

    def calculate_points(self):
        if self.get_status() != "Finished":
            return "Maç bitmedi."
        
        score = self.get_score().split("-")
        h, a = int(score[0]), int(score[1])
        
        if h > a: return f"{self.get_home_team().get_name()} (3 Puan)"
        elif a > h: return f"{self.get_away_team().get_name()} (3 Puan)"
        else: return "Beraberlik (1 Puan)"

    def get_match_info(self):
        return f"[Lig - Hft {self.__week_number}] {self.get_home_team().get_name()} vs {self.get_away_team().get_name()} | Skor: {self.get_score()}"

    def update_status(self, new_status):
        self._set_status_internal(new_status)



# 3. TournamentMatch (Turnuva/Kupa Maçı)
# Özellik: Beraberlik olmaz. Uzatmalar ve Penaltılar vardır.

class TournamentMatch(MatchBase):
    """
    Eleme usulü turnuva maçlarını temsil eder.
    Kazanan mutlaka belirlenmelidir.
    """
    def __init__(self, match_id, home_team, away_team, date_time, round_name, knockout=True):
        super().__init__(match_id, home_team, away_team, "Tournament", date_time)
        
        self.__round_name = round_name # Çeyrek Final, Yarı Final vb.
        self.__knockout = knockout     # Tek maç eleme mi?
        self.__extra_time_played = False
        self.__penalties_played = False

    def simulate_match(self):
        """
        Turnuva maçı simülasyonu. (Override)
        Beraberlik durumunda uzatmalar ve penaltılar devreye girer.
        """
        print(f"\n--- Kupa Maçı ({self.__round_name}) ---")
        
        # 1. Normal Süre
        h_goals = random.randint(0, 3)
        a_goals = random.randint(0, 3)
        print(f"Normal Süre: {h_goals}-{a_goals}")
        
        # 2. Uzatmalar (Eğer eleme maçıysa ve berabereyse)
        if self.__knockout and h_goals == a_goals:
            print(">> Eşitlik bozulmadı! Uzatmalara gidiliyor...")
            self.__extra_time_played = True
            
            # Uzatmada gol olma ihtimali
            h_goals += random.randint(0, 1)
            a_goals += random.randint(0, 1)
            print(f"Uzatma Sonucu: {h_goals}-{a_goals}")
            
            # 3. Penaltılar (Hala berabereyse)
            if h_goals == a_goals:
                print(">> Eşitlik bozulmadı! Penaltı atışları başlıyor...")
                self.__penalties_played = True
                
                # Penaltı simülasyonu (Kazanan çıkana kadar)
                p_h, p_a = 0, 0
                while p_h == p_a:
                    p_h = random.randint(3, 5)
                    p_a = random.randint(3, 5)
                
                winner = self.get_home_team().get_name() if p_h > p_a else self.get_away_team().get_name()
                print(f"Penaltılar Sonucu: {p_h}-{p_a} ({winner} kazandı)")
                
                # Penaltı galibini belirlemek için skora sembolik ekleme yapmıyoruz,
                # skor tabloda berabere görünür ama tur atlayan bellidir.

        self.set_score(f"{h_goals}-{a_goals}")
        self._set_status_internal("Finished")
        
        # Turnuva maçında lig puanı verilmez ama istatistik (goller) işlenebilir
        self.get_home_team().update_stats(h_goals, a_goals)
        self.get_away_team().update_stats(a_goals, h_goals)

    def calculate_points(self):
        return f"Tur atlayan belirlendi. ({self.__round_name})"

    def get_match_info(self):
        info = f"[Kupa - {self.__round_name}] {self.get_home_team().get_name()} vs {self.get_away_team().get_name()}"
        if self.__extra_time_played: info += " (UZ)"
        if self.__penalties_played: info += " (PEN)"
        return info

    def update_status(self, new_status):
        self._set_status_internal(new_status)



# SERVICES KATMANI (İş Mantığı ve Yöneticiler)
# PDF Madde 192: Maç oluşturma, Fikstür ve Puan Tablosu servisleri

class MatchManager:
    """
    Tüm maç süreçlerini yöneten ana servis sınıfı.
    Maç oluşturma, listeleme ve oynatma işlemlerini yapar.
    """
    def __init__(self):
        self.__matches = [] # Bellekteki maç listesi (Repository yerine geçici)

    def create_match(self, match_type, home_team, away_team, date_time, **kwargs):
        """
        Factory Pattern: İstenen türe göre doğru sınıfı üretir.
        """
        match_id = random.randint(10000, 99999)
        new_match = None

        # Gerekli validasyonlar
        if not home_team or not away_team:
            print("Hata: Takımlar eksik.")
            return None

        if match_type == "Friendly":
            location = kwargs.get("location", None)
            # Eğer lokasyon yoksa ev sahibi takımın şehri olsun (basit mantık)
            new_match = FriendlyMatch(match_id, home_team, away_team, date_time, location)

        elif match_type == "League":
            week = kwargs.get("week", 1)
            referee = kwargs.get("referee", None)
            if referee:
                new_match = LeagueMatch(match_id, home_team, away_team, date_time, week, referee)
            else:
                print("Hata: Lig maçı için hakem zorunludur!")

        elif match_type == "Tournament":
            round_name = kwargs.get("round_name", "Eleme")
            new_match = TournamentMatch(match_id, home_team, away_team, date_time, round_name)

        if new_match:
            self.__matches.append(new_match)
            print(f"✅ Maç Planlandı: {new_match.get_match_info()}")
            return new_match
        
        return None

    def get_all_matches(self):
        return self.__matches

    def get_matches_by_status(self, status):
        """Belirli durumdaki (örn: Scheduled) maçları döner."""
        return [m for m in self.__matches if m.get_status() == status]

    def simulate_all_scheduled(self):
        """Planlanmış tüm maçları sırayla oynatır."""
        print("\n TÜM MAÇLAR OYNATILIYOR ")
        count = 0
        for match in self.__matches:
            if match.get_status() == "Scheduled":
                match.simulate_match()
                count += 1
        print(f" {count} maç tamamlandı. \n")


class LeagueTable:
    """
    Puan durumu tablosunu oluşturan yardımcı servis.
    """
    @staticmethod
    def print_table(team_list):
        """
        Takımları puanlarına göre sıralayıp tablo halinde basar.
        Sıralama Kriteri: Puan (Çoktan aza) -> Averaj (Çoktan aza)
        """
        # Python'un sort fonksiyonu ile çoklu kriterli sıralama
        sorted_teams = sorted(
            team_list, 
            key=lambda t: (t.get_points(), t.get_goal_difference()), 
            reverse=True
        )

        print("\n" + "="*55)
        print(f"{'SIRA':<5} {'TAKIM (KOD)':<20} {'P':<3} {'G':<3} {'B':<3} {'M':<3} {'AV':<4} {'PUAN':<5}")
        print("="*55)

        for i, team in enumerate(sorted_teams, 1):
            stats = team.get_stats_string() # Entities içindeki formatlı string
            # Örnek stats çıktısı: "GS    | P: 5 W: 3 D: 1 L: 1 | Pts: 10"
            # Burada daha temiz bir format için elle yazdırabiliriz:
            print(f"{i:<5} {team.get_name()[:15]:<20} {team.get_points():<5}") 
            # Not: Detaylı tabloyu entities içindeki verilere göre burada güzelleştirebilirsin.
            # Şimdilik basit basıyoruz.
            print(f"      └── {stats}")

        print("="*55 + "\n")

















