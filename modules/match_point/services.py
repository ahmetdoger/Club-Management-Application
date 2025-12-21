import random
import os
from exceptions import SameTeamError
from exceptions import MissingTeamError

from implementation import FriendlyMatch
from implementation import TournamentMatch
from implementation import LeagueMatch



# SERVICES KATMANI (İş Mantığı ve Yöneticiler)  , Maç oluşturma, Fikstür ve Puan Tablosu servisleri
class MatchManager:  

    #bellekteki maç listesi (Repository yerine geçici)
    def __init__(self):
        self.__matches = []  

    def create_match(self, match_type, home_team, away_team, date_time, **kwargs):
       
       # Takım nesneleri gelmediyse veya None ise bu hatayı fırlat
        if home_team is None or away_team is None:
            raise MissingTeamError() 

        # AYNI TAKIM KONTROLÜ 
        if home_team.get_name() == away_team.get_name():
            raise SameTeamError(home_team.get_name())
        
    
        match_id = random.randint(10000, 99999)
        new_match = None

        # Gerekli validasyonlar
        if not home_team or not away_team:
            print("Hata: Takımlar eksik.")
            return None
        #bellekteki maç listesi (Repository yerine geçici
        if match_type == "Friendly":
            location = kwargs.get("location", None)
         
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
        #Belirli durumdaki (örn: Scheduled) maçları döner.
    def get_matches_by_status(self, status):
        return [m for m in self.__matches if m.get_status() == status]
     #Planlanmış tüm maçları sırayla oynatır.
    def simulate_all_scheduled(self):
        print("\n TÜM MAÇLAR OYNATILIYOR ")
        count = 0
        for match in self.__matches:
            if match.get_status() == "Scheduled":
                match.simulate_match()
                count += 1
        print(f" {count} maç tamamlandı. \n")


   # Takıma göre maç geçmişi listeleme.
    def get_matches_of_team(self, team_name):
        
        team_matches = []
        for match in self.__matches:
            h_name = match.get_home_team().get_name()
            a_name = match.get_away_team().get_name()
            
            # Eğer takım ev sahibi veya deplasmandaysa listeye ekle
            if team_name.lower() in h_name.lower() or team_name.lower() in a_name.lower():
                team_matches.append(match)
        return team_matches


    # Verilen maç nesnesini manuel skorla oynatır.
    def play_match_manually(self, match, home_score, away_score):
        match.set_score(f"{home_score}-{away_score}")
        match.update_status("Finished")
        
        # Eğer LİG maçıysa puanları da işle (Turnuvada işleme)
        # MatchBase içinde type 'League' olarak tutuluyor
        if getattr(match, "_MatchBase__match_type") == "League":
            match.get_home_team().update_stats(home_score, away_score)
            match.get_away_team().update_stats(away_score, home_score)
            
        print(f"✅ Manuel Giriş Başarılı: {match.get_match_info()}")

    # ID ve skor ile manuel oynatma (Test dosyasının çağırdığı yer burası)
    def enter_manual_score(self, match_id, home_score, away_score):
        found_match = None
        for m in self.__matches:
            # ID kontrolü (String çevirip karşılaştırıyoruz garanti olsun)
            if str(getattr(m, "_MatchBase__match_id")) == str(match_id):
                found_match = m
                break
        
        if found_match:
            self.play_match_manually(found_match, home_score, away_score)
            return True
            
        print("❌ Hata: Bu ID ile eşleşen maç bulunamadı.")
        return False
    


    def play_match_manually(self, match, home_score, away_score):
        """
        Maçı verilen skorla oynatır ve bitirir.
        Lig maçıysa puan tablosunu günceller.
        """
        # Skoru yaz ve bitir
        match.set_score(f"{home_score}-{away_score}")
        match.update_status("Finished")
        
        # Eğer LİG maçıysa puanları da işle (Turnuvada işleme)
        if getattr(match, "_MatchBase__match_type") == "League":
            match.get_home_team().update_stats(home_score, away_score)
            match.get_away_team().update_stats(away_score, home_score)
            
        print(f"✅ Manuel Giriş Başarılı: {match.get_match_info()}")


    # Puan durumu tablosunu oluşturan yardımcı servis.
class LeagueTable:

   # Takımları puanlarına göre sıralayıp PRO FORMATTA basar.
    @staticmethod
    def print_table(team_list):
        
        # Sıralama Kriteri: Puan (Çoktan aza) -> Averaj (Çoktan aza)
        sorted_teams = sorted(
            team_list, 
            key=lambda t: (t.get_points(), t.get_goal_difference()), 
            reverse=True
        )
        # Başlıklar: O=Oynanan, G=Galibiyet, B=Beraberlik, M=Mağlubiyet, AV=Averaj, P=Puan
        print("\n" + "="*75)
        print(f"{'SIRA':<5} {'TAKIM':<20} {'O':<4} {'G':<4} {'B':<4} {'M':<4} {'AV':<5} {'PUAN':<5}")
        print("-" * 75)

        # Python'ın 'getattr' fonksiyonunu kullanıyoruz. 
        for i, team in enumerate(sorted_teams, 1):
            
            w = getattr(team, "_Team__won", getattr(team, "_Team__wins", 0))
            d = getattr(team, "_Team__drawn", getattr(team, "_Team__draws", 0))
            l = getattr(team, "_Team__lost", getattr(team, "_Team__losses", 0))
            
            played = w + d + l
            avg = team.get_goal_difference()
            points = team.get_points()
            name = team.get_name()

            # Tek satırda, hizalı ve temiz çıktı
            print(f"{i:<5} {name[:19]:<20} {played:<4} {w:<4} {d:<4} {l:<4} {avg:<5} {points:<5}")

        print("="*75 + "\n")



# YARDIMCI SERVİSLER (UTILITIES) . Sistem güvenliği, loglama ve veri doğrulama işlemlerini yapan sınıflar.
class SystemLogger:
   # Log dosyasını bu python dosyasının olduğu yere kaydeder.
    def __init__(self, filename="system_events.log"):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        
        self.__log_file = os.path.join(base_dir, filename)
        
        self.__enabled = True

    # Loglama sistemini aktif veya pasif hale getirir.
    def set_enabled(self, status):
        if isinstance(status, bool):
            self.__enabled = status

    # Bilgilendirme mesajı kaydeder (INFO).
    def log_info(self, message):
        if self.__enabled:
            self.__write_to_file(f"[INFO] {message}")

    # Hata mesajı kaydeder (ERROR).
    def log_error(self, message):
        if self.__enabled:
            self.__write_to_file(f"[ERROR] !!! {message} !!!")

    # Uyarı mesajı kaydeder (WARNING).
    def log_warning(self, message):
        if self.__enabled:
            self.__write_to_file(f"[WARNING] {message}")

    # Maç sonucu girişlerini özel formatta kaydeder.
    def log_match_result(self, match_info, score):
        self.log_info(f"Maç Sonuçlandı: {match_info} -> Skor: {score}")

    # Mesajı dosyaya zaman damgasıyla birlikte yazar (Private Metot).
    def __write_to_file(self, content):
        try:
            with open(self.__log_file, "a", encoding="utf-8") as f:
                f.write(f"{content}\n")
        except:
        
            pass


# Kullanıcı girişlerini kontrol eden doğrulama sınıfı.
class InputValidator:
    
    # Skor girişinin mantıklı olup olmadığını kontrol eder.
    @staticmethod
    def validate_score(score):
        if isinstance(score, int) and 0 <= score <= 30:
            return True
        return False

    # Girilen tarihin formatını basitçe kontrol eder.
    @staticmethod
    def validate_date_format(date_string):
        if isinstance(date_string, str) and len(date_string) == 10:
            if "-" in date_string:
                return True
        return False

    # Takım seçiminde aynı takımın seçilip seçilmediğini kontrol eder.
    @staticmethod
    def validate_team_selection(team1, team2):
        if team1 is None or team2 is None:
            return False
        if team1.get_name() == team2.get_name():
            return False
        return True

    # Lig haftasının geçerli olup olmadığını kontrol eder.
    @staticmethod
    def validate_league_week(week):
        if 1 <= week <= 38:
            return True
        return False


# Maç istatistiklerini hesaplayan yardımcı analiz sınıfı.
class MatchAnalytics:
    
    # Verilen maç listesindeki toplam gol sayısını hesaplar.
    @staticmethod
    def calculate_total_goals(match_list):
        total = 0
        for match in match_list:
            if match.get_status() == "Finished":
                parts = match.get_score().split("-")
                total += int(parts[0]) + int(parts[1])
        return total

    # En gollü maçı bulur ve döner.
    @staticmethod
    def find_highest_scoring_match(match_list):
        max_goals = -1
        target_match = None
        
        for match in match_list:
            if match.get_status() == "Finished":
                parts = match.get_score().split("-")
                goals = int(parts[0]) + int(parts[1])
                if goals > max_goals:
                    max_goals = goals
                    target_match = match
        return target_match

    # Galibiyet yüzdesini hesaplar (Sadece bitmiş maçlar).
    @staticmethod
    def calculate_win_rate(match_list, team_name):
        played = 0
        won = 0
        for match in match_list:
            if match.get_status() == "Finished":
                h = match.get_home_team().get_name()
                a = match.get_away_team().get_name()
                s = match.get_score().split("-")
                h_s, a_s = int(s[0]), int(s[1])
                
                if team_name == h:
                    played += 1
                    if h_s > a_s: won += 1
                elif team_name == a:
                    played += 1
                    if a_s > h_s: won += 1
                    
        if played == 0: return 0.0
        return (won / played) * 100




