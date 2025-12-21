import sys
import time
# Noktasız import
from entities import Team
from entities import Referee
from entities import Stadium
from services import MatchManager
from services import LeagueTable
from repository import MatchRepository
from exceptions import SameTeamError
from exceptions import MissingTeamError
from services import MatchAnalytics
from services import SystemLogger

# Terminal tabanlı kullanıcı arayüzünü yöneten ana sınıf.
class ConsoleUI:
    # Sınıf başlatılırken manager, repo ve varsayılan verileri yükler.
    def __init__(self):
        self.manager = MatchManager()
        self.repo = MatchRepository()
        self.logger = SystemLogger() # Loglayıcıyı başlat
        self.logger.log_info("Program başlatıldı.") # İlk logu at
        self.teams = [] 
        self.referee = Referee(999, "Sistem", "Hakemi", "FIFA", 10)
        self.stadium = Stadium(1, "Olimpiyat", "İst", 70000)
        self.load_initial_data()

    # Test amaçlı varsayılan takımları sisteme ekler.
    def load_initial_data(self):
        self.teams.append(Team(1, "Galatasaray", "GS", 1905, ["Sarı", "Kırmızı"]))
        self.teams.append(Team(2, "Fenerbahçe", "FB", 1907, ["Sarı", "Lacivert"]))
        self.teams.append(Team(3, "Beşiktaş", "BJK", 1903, ["Siyah", "Beyaz"]))
        self.teams.append(Team(4, "Trabzonspor", "TS", 1967, ["Bordo", "Mavi"]))

    # Kullanıcıya işlem seçeneklerini içeren ana menüyü basar.
    def display_menu(self):
        print("\n" + "="*50)
        print(" FUTBOL YÖNETİM SİSTEMİ (FULL ÖZELLİK) ")
        print("="*50)
        print("--- İŞLEMLER ---")
        print("1. Dostluk Maçı Oluştur")
        print("2. Lig Maçı Oluştur")
        print("3. Kupa Maçı Oluştur")
        print("4. MAÇLARI OYNAT (Simülasyon)")
        print("5. Puan Durumunu Göster")
        print("6. Verileri Dosyaya KAYDET")
        print("-" * 30)
        print("--- RAPORLAMA VE FİLTRELEME (PDF İSTEKLERİ) ---")
        print("7. Takıma Göre Maç Geçmişi (Service)")
        print("8. ID'ye Göre Maç Ara (Repository)")
        print("9. Tarihe Göre Filtrele (Repository)")
        print("10. Turnuva Tipine Göre Filtrele (Repository)")
        print("11. DETAYLI SİSTEM ANALİZİ (New)")
        print("0. ÇIKIŞ")
        print("="*50)

    # Uygulamanın ana döngüsünü başlatır ve kullanıcı seçimlerini yönetir.
    def run(self):
        while True:
            self.display_menu()
            choice = input("Seçiminiz: ")

            if choice == '1': self.create_friendly_ui()
            elif choice == '2': self.create_league_ui()
            elif choice == '3': self.create_cup_ui()
            elif choice == '4': self.simulate_matches_ui()
            elif choice == '5': self.show_standings_ui()
            elif choice == '6': self.save_data_ui()
            
            # --- YENİ EKLENEN FİLTRE ÖZELLİKLERİ ---
            elif choice == '7': self.filter_by_team_ui()
            elif choice == '8': self.search_by_id_ui()
            elif choice == '9': self.filter_by_date_ui()
            elif choice == '10': self.filter_by_type_ui()
            elif choice == '11': self.show_analytics_ui()
            elif choice == '0': 
                print("Çıkış yapılıyor..."); break
            else: print("Geçersiz seçim.")


    # Kullanıcıdan listeden iki farklı takım seçmesini ister.
    def select_teams(self):
        print("\n--- Takım Listesi ---")
        for i, team in enumerate(self.teams):
            print(f"{i+1}. {team.get_name()}")
        try:
            h = int(input("Ev Sahibi No: ")) - 1
            a = int(input("Deplasman No: ")) - 1
            return self.teams[h], self.teams[a]
        except: return None, None

    # Kullanıcı arayüzü üzerinden dostluk maçı oluşturur.
    def create_friendly_ui(self):
        print("\n[YENİ DOSTLUK MAÇI]")
        try:
            home, away = self.select_teams()
            self.manager.create_match("Friendly", home, away, "2025-05-20", location=self.stadium)

        # Çoklu Hata Yakalama (Parantez içine alıyoruz)
        except (SameTeamError, MissingTeamError) as e:
            print(f"\n❌ HATA: {e}")

    # Kullanıcı arayüzü üzerinden lig maçı oluşturur.
    def create_league_ui(self):
        print("\n[YENİ LİG MAÇI]")
        try:
            home, away = self.select_teams()
            self.manager.create_match("League", home, away, "2025-05-21", week=10, referee=self.referee)
        except (SameTeamError, MissingTeamError) as e:
            print(f"\n❌ HATA: {e}")

    # Kullanıcı arayüzü üzerinden kupa (turnuva) maçı oluşturur.
    def create_cup_ui(self):
        print("\n[YENİ KUPA MAÇI]")
        try:
            home, away = self.select_teams()
            self.manager.create_match("Tournament", home, away, "2025-06-01", round_name="Final")
        except (SameTeamError, MissingTeamError) as e:
            print(f"\n❌ HATA: {e}")
    
    # Bekleyen maçların simülasyonunu başlatır.
    def simulate_matches_ui(self):
        print("\n>>> MAÇ SİMÜLASYONU BAŞLIYOR...")
        
        # Oynanmamış (Scheduled) maçları çek
        all_matches = self.manager.get_all_matches()
        pending_matches = [m for m in all_matches if m.get_status() == "Scheduled"]
        
        if not pending_matches:
            print("❌ Oynanacak bekleyen maç yok.")
            return

        print(f"Sırada {len(pending_matches)} maç var.\n")

        # Her maç için tek tek sor
        for match in pending_matches:
            h_name = match.get_home_team().get_name()
            a_name = match.get_away_team().get_name()
            
            print("-" * 40)
            print(f"SIRADAKİ MAÇ: {h_name} vs {a_name}")
            print("-" * 40)
            print("1. Manuel Skor Gir")
            print("2. Otomatik Oynat (Rastgele)")
            
            choice = input("Seçiminiz (1 veya 2): ")
            
            if choice == '1':
                # --- MANUEL GİRİŞ ---
                try:
                    h = int(input(f"{h_name} Golü: "))
                    a = int(input(f"{a_name} Golü: "))
                    if h < 0 or a < 0:
                        print("Hata: Eksi değer giremezsin! Otomatik oynatılıyor...")
                        match.simulate_match()
                    else:
                        # Az önce services.py'ye eklediğimiz fonksiyonu çağırıyoruz
                        self.manager.play_match_manually(match, h, a)
                except:
                    print("Hata: Sayı girmedin! Otomatik oynatılıyor...")
                    match.simulate_match()
            else:
                print(">> Sistem oynatıyor...")
                match.simulate_match()
                time.sleep(1) # 1 saniye bekle (Heyecan olsun)
        
        print("\n✅ TÜM MAÇLAR TAMAMLANDI!")
    # Güncel puan durumunu ekrana tablo olarak basar.
    def show_standings_ui(self):
        LeagueTable.print_table(self.teams)

    # Mevcut maç verilerini JSON dosyasına kaydeder.
    def save_data_ui(self):
        matches = self.manager.get_all_matches()
        if self.repo.save_matches_to_json(matches):
            print("✅ KAYIT BAŞARILI (JSON güncellendi)")
        else: print("❌ Hata oluştu.")


    # Takım ismine göre o takımın maç geçmişini filtreler.
    def filter_by_team_ui(self):
        name = input("Aranacak Takım Adı (örn: Galatasaray): ")
        matches = self.manager.get_matches_of_team(name)
        print(f"\n--- {name} MAÇ GEÇMİŞİ ---")
        for m in matches:
            print(m.get_match_info())
        input("Devam etmek için Enter...")

    # Maç ID'sine göre veritabanında arama yapar.
    def search_by_id_ui(self):
        print("Not: ID'leri görmek için önce verileri kaydedip JSON dosyasına bakabilirsin.")
        mid = input("Aranacak Maç ID: ")
        result = self.repo.find_match_by_id(mid)
        if result:
            print(f"✅ BULUNDU: {result['home']} vs {result['away']} | Skor: {result['score']}")
        else:
            print("❌ Maç bulunamadı (Önce '6' ile kaydettiğinden emin ol).")
        input("Devam...")

    # Kullanıcının girdiği tarihe göre maçları filtreler.
    def filter_by_date_ui(self):
        date = input("Tarih girin (YYYY-MM-DD): ") 
        results = self.repo.filter_matches_by_date(date)
        print(f"\n--- {date} Tarihli Maçlar ---")
        for m in results:
            print(f"{m['home']} vs {m['away']} ({m['type']})")
        if not results: print("Kayıt bulunamadı.")
        input("Devam...")

    # Maç türüne (Lig, Dostluk vb.) göre filtreleme yapar.
    def filter_by_type_ui(self):
        mtype = input("Maç Tipi (League / Friendly / Tournament): ")
        results = self.repo.filter_matches_by_type(mtype)
        print(f"\n--- {mtype} Tipi Maçlar ---")
        for m in results:
            print(f"{m['home']} vs {m['away']} | Skor: {m['score']}")
        if not results: print("Kayıt bulunamadı.")
        input("Devam...")


    #  analiz metodu services.py içindeki MatchAnalytics sınıfını kullanarak istatistik gösterir.
    def show_analytics_ui(self):
        print("\n📊 --- SİSTEM ANALİZ RAPORU --- 📊")
        
        matches = self.manager.get_all_matches()
        
        # 1. Toplam Gol Sayısı
        total_goals = MatchAnalytics.calculate_total_goals(matches)
        print(f"⚽ Ligde Atılan Toplam Gol: {total_goals}")
        
        # 2. En Gollü Maç
        highest_match = MatchAnalytics.find_highest_scoring_match(matches)
        if highest_match:
            print(f"🔥 En Heyecanlı Maç: {highest_match.get_score()} ({highest_match.get_home_team().get_name()} vs {highest_match.get_away_team().get_name()})")
        else:
            print("🔥 En Heyecanlı Maç: Veri Yok")

        # 3. Şampiyonluk Adaylarının Galibiyet Oranı
        print("\n--- Galibiyet Oranları ---")
        for team in self.teams:
            win_rate = MatchAnalytics.calculate_win_rate(matches, team.get_name())
            print(f"- {team.get_name()}: %{win_rate:.1f}")
            
        # Log kaydı atalım
        self.logger.log_info("Kullanıcı analiz raporunu görüntüledi.")
        input("\nDevam etmek için Enter...")
if __name__ == "__main__":
    app = ConsoleUI()
    app.run()

