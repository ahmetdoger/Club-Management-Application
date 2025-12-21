import random
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
