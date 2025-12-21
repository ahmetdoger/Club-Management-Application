
 #Bu modül, Maç ve Turnuva Yönetim Sistemi için gerekli olan temel varlık sınıflarını (Entities) içerir.1. Stadium Class (Stadyum Varlığı)
class Stadium:
    # Statik sayaç 
    _total_stadiums = 0

    def __init__(self, stadium_id, name, city, capacity, surface_type="Grass"):
        self.__stadium_id = stadium_id
        self.__name = name
        self.__city = city
        self.__capacity = capacity
        self.__surface_type = surface_type  # Grass, Artificial, Hybrid
        self.__is_under_maintenance = False # Bakımda mı?
        
        Stadium.increment_count()

    # --- Static Methods 
    @staticmethod
    def validate_capacity(cap):
        """Kapasitenin geçerli olup olmadığını kontrol eder."""
        if cap < 0:
            return False
        return True

    @classmethod
    def increment_count(cls):
        cls._total_stadiums += 1

    # Getter & Setter Methods 

    def get_stadium_id(self):
        return self.__stadium_id

    def set_stadium_id(self, s_id):
        self.__stadium_id = s_id

    def get_name(self):
        return self.__name

    def set_name(self, name):
        if len(name) > 2:
            self.__name = name
        else:
            print("Hata: İsim çok kısa.")

    def get_city(self):
        return self.__city

    def set_city(self, city):
        self.__city = city

    def get_capacity(self):
        return self.__capacity

    def set_capacity(self, capacity):
        if self.validate_capacity(capacity):
            self.__capacity = capacity

    def get_surface_type(self):
        return self.__surface_type

    def set_surface_type(self, surface):
        self.__surface_type = surface

    def is_under_maintenance(self):
        return self.__is_under_maintenance

    def set_maintenance_status(self, status):
        """Stadyumu bakıma alır veya bakımdan çıkarır."""
        if isinstance(status, bool):
            self.__is_under_maintenance = status

    def get_full_info(self):
        return f"{self.__name} ({self.__city}) - {self.__capacity} Kişilik"



# 2. Referee Class (Hakem Varlığı)

class Referee:
    
    # yönetecek hakem bilgilerini tutar.
    
    def __init__(self, referee_id, first_name, last_name, license_level, experience_year):
        self.__referee_id = referee_id
        self.__first_name = first_name
        self.__last_name = last_name
        self.__license_level = license_level # FIFA, National, Regional
        self.__experience_year = experience_year
        self.__matches_officiated = 0 # Yönettiği maç sayısı

    # --- Getter & Setter Methods 

    def get_referee_id(self):
        return self.__referee_id

    def get_full_name(self):
        return f"{self.__first_name} {self.__last_name}"

    def set_first_name(self, name):
        self.__first_name = name

    def set_last_name(self, name):
        self.__last_name = name

    def get_license_level(self):
        return self.__license_level

    def set_license_level(self, level):
        valid_levels = ["FIFA", "National", "Regional", "Amateur"]
        if level in valid_levels:
            self.__license_level = level
        else:
            print(f"Uyarı: {level} geçerli bir lisans değil.")

    def get_experience_year(self):
        return self.__experience_year

    def increment_match_count(self):
        self.__matches_officiated += 1

    def get_match_count(self):
        return self.__matches_officiated



# 3. Team Class (Takım Varlığı)
class Team:

    #Lig veya turnuvada yer alan takımı temsil eder.  Maçlarda 'home' ve 'away' parametresi olarak bu sınıf kullanılır.
    def __init__(self, team_id, name, short_code, founding_year, colors):
        self.__team_id = team_id
        self.__name = name
        self.__short_code = short_code 
        self.__founding_year = founding_year
        self.__colors = colors 
        
        # Takım İstatistikleri
        self.__played = 0
        self.__won = 0
        self.__drawn = 0
        self.__lost = 0
        self.__goals_scored = 0
        self.__goals_conceded = 0
        self.__points = 0

    # --- İstatistik Metotları ---
    def update_stats(self, goals_for, goals_against):
        """Maç sonucuna göre istatistikleri günceller."""
        self.__played += 1
        self.__goals_scored += goals_for
        self.__goals_conceded += goals_against
        
        if goals_for > goals_against:
            self.__won += 1
            self.__points += 3
        elif goals_for == goals_against:
            self.__drawn += 1
            self.__points += 1
        else:
            self.__lost += 1
            # Mağlubiyette puan artmaz

    def get_goal_difference(self):
        """Averajı hesaplar."""
        return self.__goals_scored - self.__goals_conceded

    # --- Getter & Setter Methods ---
    def get_team_id(self):
        return self.__team_id

    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name

    def get_short_code(self):
        return self.__short_code

    def get_colors(self):
        return ", ".join(self.__colors)

    def get_points(self):
        return self.__points

    def get_stats_string(self):
        """Puan tablosu için özet string döner."""
        return (f"{self.__short_code:<5} | P: {self.__played} W: {self.__won} "
                f"D: {self.__drawn} L: {self.__lost} | Pts: {self.__points}")

