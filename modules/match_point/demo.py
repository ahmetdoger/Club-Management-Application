# Gerekli modülleri içe aktarıyoruz. 
from entities import Team
from entities import Referee
from entities import Stadium
from services import MatchManager
from services import LeagueTable
from repository import MatchRepository
 
 # Projenin ana senaryosunu çalıştıran fonksiyon. Hocanın istediği tüm özelliklerin (Maç türleri, Kayıt, Tablo) çalıştığını gösterir.
def run_demo():
    print("\n" + "="*60)
    print("DEMO SENARYOSU BAŞLATILIYOR: FUTBOL YÖNETİM SİSTEMİ")
    print("="*60 + "\n")

    # 1. HAZIRLIK: Repository ve Manager Başlatma
    repo = MatchRepository()
    manager = MatchManager()
    
    # Önceki verileri temizle (Demo her seferinde temiz başlasın)
    repo.clear_database()
    print(">> Veritabanı temizlendi ve kullanıma hazır.\n")

    # 2. VARLIKLARIN OLUŞTURULMASI (Entities)
    print("1. TAKIMLAR, HAKEMLER VE STATLAR OLUŞTURULUYOR ")
    
    
    t1 = Team(1, "Galatasaray", "GS", 1905, ["Sarı", "Kırmızı"])
    t2 = Team(2, "Fenerbahçe", "FB", 1907, ["Sarı", "Lacivert"])
    t3 = Team(3, "Beşiktaş", "BJK", 1903, ["Siyah", "Beyaz"])
    t4 = Team(4, "Trabzonspor", "TS", 1967, ["Bordo", "Mavi"])
    
    
    ref1 = Referee(10,"Kerem","Aran","FIFA",3)
    
    stadium = Stadium(55, "Olimpiyat Stadı", "İstanbul", 76000)
    
    print(f"✅ {t1.get_name()} ve diğer takımlar lige katıldı.")
    print(f"✅ Hakem {ref1.get_full_name()} atandı.\n")

    # 3. MAÇLARIN OLUŞTURULMASI (Factory Pattern)
    print("--- 2. MAÇ FİKSTÜRÜ OLUŞTURULUYOR (Factory Pattern) ---")
    
    # A) Dostluk Maçı
    manager.create_match("Friendly", t1, t4, "2025-08-01 19:00", location=stadium)
    
    # B) Lig Maçları (Puanlı)
    manager.create_match("League", t1, t2, "2025-08-10 20:00", week=1, referee=ref1)
    # BJK vs TS
    manager.create_match("League", t3, t4, "2025-08-10 20:00", week=1, referee=ref1)
    # FB vs BJK
    manager.create_match("League", t2, t3, "2025-08-17 20:00", week=2, referee=ref1)

    # C) Kupa Maçı (Penaltılı)
    
    manager.create_match("Tournament", t1, t3, "2025-09-01 21:00", round_name="Süper Kupa Finali")
    
    print(">> Tüm maçlar sisteme planlandı (Scheduled).\n")

    # 4. SİMÜLASYON (Maçların Oynatılması)
    print("--- 3. MAÇLAR OYNATILIYOR (Simülasyon) ")
    manager.simulate_all_scheduled()
    
    # 5. RAPORLAMA VE KAYIT
    print("--- 4. SONUÇLAR VE KAYIT ---")
    
    # Puan Tablosunu Göster
    all_teams = [t1, t2, t3, t4]
    print("\n[GÜNCEL PUAN DURUMU]")
    LeagueTable.print_table(all_teams)
    
    # Verileri JSON'a kaydet
    matches = manager.get_all_matches()
    if repo.save_matches_to_json(matches):
        print("✅ Tüm maç verileri 'matches_data.json' dosyasına başarıyla kaydedildi.")
    else:
        print("❌ Kayıt sırasında hata oluştu.")

    print("\n" + "="*60)
    print("DEMO BAŞARIYLA TAMAMLANDI")
    print("="*60 + "\n")

# Eğer bu dosya doğrudan çalıştırılırsa demoyu başlat
if __name__ == "__main__":
    run_demo()
