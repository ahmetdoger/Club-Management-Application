import random
from datetime import datetime
from exceptions import SameTeamError
from exceptions import MissingTeamError

# Yan dosyalardaki sınıfları çağırıyoruz  
from base import MatchBase
from entities import Team, Stadium, Referee

# 1. FriendlyMatch (Dostluk Maçı). Özellik: Puan verilmez, LİG TABLOSUNA ETKİ ETMEZ.
class FriendlyMatch(MatchBase):
    
    #Dostluk maçlarını temsil eden sınıf.Lig puan tablosuna etkisi yoktur, hazırlık amaçlıdır.
    def __init__(self, match_id, home_team, away_team, date_time, location):
        super().__init__(match_id, home_team, away_team, "Friendly", date_time)
        
        self.__location = location  # Stadium nesnesi
        self.__charity_event = False 
        self.__ticket_price = 0.0    
       #Dostluk maçı simülasyonu. Daha rastgele ve bol gollü geçer.
    def simulate_match(self):

        print(f"\n--- Hazırlık Maçı Başlıyor: {self.get_home_team().get_name()} vs {self.get_away_team().get_name()} ---")
        
        home_score = random.randint(0, 5)
        away_score = random.randint(0, 5)
        
        self.set_score(f"{home_score}-{away_score}")
        self._set_status_internal("Finished")
         # Lig maçlarında puanları 'update_stats' ile işliyoruz.

        
        print(f"Maç Sonucu: {self.get_score()} (Dostluk maçı olduğu için puana etki etmedi)")

    def calculate_points(self):
        return "Dostluk maçında puan verilmez."

    def get_match_info(self):
        loc_name = self.__location.get_name() if self.__location else "Bilinmiyor"
        return f"[Hazırlık] {self.get_home_team().get_short_code()} vs {self.get_away_team().get_short_code()} @ {loc_name}"

    def update_status(self, new_status):
        self._set_status_internal(new_status)

    #  Getter & Setter Metotları 
    def get_ticket_price(self): return self.__ticket_price
    def set_ticket_price(self, price): 
        if price >= 0: self.__ticket_price = price
    def is_charity_event(self): return self.__charity_event
    def set_charity_event(self, status): 
        if isinstance(status, bool): self.__charity_event = status
    def get_location(self): return self.__location
    # 2. LeagueMatch (Lig Maçı). Özellik: Galibiyet 3 puan, Beraberlik 1 puan. Hakem zorunludur.
class LeagueMatch(MatchBase):
    
    #Resmi lig müsabakalarını temsil eder.
    def __init__(self, match_id, home_team, away_team, date_time, week_number, referee):
        super().__init__(match_id, home_team, away_team, "League", date_time)
        
        self.__week_number = week_number
        self.__referee = referee # Referee nesnesi
        self.__weather_condition = "Sunny"

    def simulate_match(self):
        
       # Lig maçı simülasyonu. (Override) Ev sahibi avantajı vardır.
        print(f"\n--- Lig Maçı ({self.__week_number}. Hafta) ---")
        print(f"Hakem: {self.__referee.get_full_name()}")
        
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



# 3. TournamentMatch (Turnuva/Kupa Maçı) Özellik: Beraberlik olmaz. Uzatmalar ve Penaltılar vardır.
class TournamentMatch(MatchBase):
    
   # Eleme usulü turnuva maçlarını temsil eder. mutlaka belirlenmelidir.
    def __init__(self, match_id, home_team, away_team, date_time, round_name, knockout=True):
        super().__init__(match_id, home_team, away_team, "Tournament", date_time)
        
        self.__round_name = round_name # Çeyrek Final, Yarı Final vb.
        self.__knockout = knockout     # Tek maç eleme mi?
        self.__extra_time_played = False
        self.__penalties_played = False

    def simulate_match(self):
        #Turnuva maçı simülasyonu. (Override) Beraberlik durumunda uzatmalar ve penaltılar devreye girer.
        
        print(f"\n--- Kupa Maçı ({self.__round_name}) ---")
        
        h_goals = random.randint(0, 3)
        a_goals = random.randint(0, 3)
        print(f"Normal Süre: {h_goals}-{a_goals}")
        
        # 2. Uzatmalar (Eğer eleme maçıysa ve berabereyse)
        if self.__knockout and h_goals == a_goals:
            print(">> Eşitlik bozulmadı! Uzatmalara gidiliyor...")
            self.__extra_time_played = True
            
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
                # Penaltı galibini belirlemek için skora sembolik ekleme yapmıyoruz  skor tabloda berabere görünür ama tur atlayan bellidir.

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



















