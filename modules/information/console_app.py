import os
import sys
import time

# --- DOSYA YOLU AYARLAMALARI ---
# Python'un modülleri bulabilmesi için gerekli yol ayarları
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)
project_root = os.path.abspath(os.path.join(script_dir, '..', '..'))
sys.path.append(project_root)

from modules.information.repository import AthleteRepository
from modules.information.services import AthleteService
from modules.information.errors import ClubManagerError

# Global Servis Değişkeni (Sezon modu ile değişebilir)
current_service = None

def clear_screen():
    """Terminal ekranını temizler."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    clear_screen()
    print("================================================================")
    print("        SPOR KULÜBÜ YÖNETİM SİSTEMİ - TERMİNAL ARAYÜZÜ")
    print("================================================================")

def get_input(prompt, type_func=str, required=True):
    """Kullanıcıdan güvenli veri alma fonksiyonu."""
    while True:
        try:
            value = input(prompt).strip()
            if required and not value:
                print("   [!] Bu alan boş bırakılamaz.")
                continue
            if not required and not value:
                return None
            return type_func(value)
        except ValueError:
            print(f"   [!] Hatalı veri tipi. Lütfen geçerli bir {type_func.__name__} giriniz.")

def show_athlete_details(athlete):
    """Sporcu bilgilerini formatlı yazdırır."""
    print("-" * 60)
    print(f"ID: {athlete.get('athlete_id')} | {athlete.get('name')} {athlete.get('surname').upper()}")
    print(f"Branş: {athlete.get('sport_branch')} | Kategori: {athlete.get('type')}")
    print(f"Yaş: {athlete.get('age')} | Boy/Kilo: {athlete.get('height')}/{athlete.get('weight')}")
    print(f"Statü: {athlete.get('status')} | Güçlü Taraf: {athlete.get('strong_side')}")
    
    # Kategoriye özel alanlar
    if athlete.get('type') == 'ProfessionalAthlete':
        print(f"Maaş: {athlete.get('salary'):,.2f} TL | Sözleşme: {athlete.get('contract_end_date')}")
        print(f"Toplam Maliyet (Vergiler Dahil): {athlete.get('total_cost'):,.2f} TL")
    elif athlete.get('type') == 'AmateurAthlete':
        print(f"Lisans No: {athlete.get('licence_number')}")
    elif athlete.get('type') == 'YouthAthlete':
        print(f"Veli: {athlete.get('guardian_name')} | Burs: {athlete.get('scholarship_amount')} TL")
    print("-" * 60)

# --- MENÜ FONKSİYONLARI ---

def menu_register_athlete():
    print("\n--- YENİ SPORCU KAYDI ---")
    try:
        name = get_input("İsim: ")
        surname = get_input("Soyisim: ")
        age = get_input("Yaş: ", int)
        gender = get_input("Cinsiyet (Male/Female): ")
        height = get_input("Boy (cm): ", int)
        weight = get_input("Kilo (kg): ", int)
        branch = get_input("Branş (Football/Basketball/Volleyball vb.): ")
        strong_side = get_input("Güçlü Taraf (Right/Left): ")

        print("\nKategori Seçiniz:")
        print("1. Profesyonel (Maaşlı)")
        print("2. Amatör (Lisanslı)")
        print("3. Altyapı (Burslu)")
        cat_choice = get_input("Seçiminiz (1-3): ", int)

        kwargs = {}
        category = ""

        if cat_choice == 1:
            category = "Professional"
            kwargs['salary'] = get_input("Maaş Beklentisi: ", float)
            kwargs['contract_end_date'] = get_input("Sözleşme Bitiş Tarihi (YYYY-AA-GG): ", required=False)
        elif cat_choice == 2:
            category = "Amateur"
            kwargs['licence_number'] = get_input("Lisans Numarası (Varsayılan için Enter): ", required=False)
        elif cat_choice == 3:
            category = "Youth"
            kwargs['guardian_name'] = get_input("Veli Adı Soyadı: ")
            # Burs hesaplama simülasyonu
            exam_score = get_input("Sınav Puanı (0-100): ", int)
            kwargs['scholarship_amount'] = 10000 if exam_score > 90 else 5000
            print(f"   -> Sınav puanına göre burs atandı: {kwargs['scholarship_amount']} TL")
        else:
            print("   [!] Geçersiz kategori.")
            return

        # Servis çağrısı
        result = current_service.register_athlete(
            name, surname, age, gender, height, weight, branch, category, strong_side, **kwargs
        )
        print(f"\n   [BAŞARILI] {result}")

    except ClubManagerError as e:
        print(f"\n   [HATA - {e.error_type}] {e.message}")
        print(f"   (Hata Kodu: {e.error_code})")
    except Exception as e:
        print(f"\n   [BEKLENMEYEN HATA] {str(e)}")
    
    input("\nDevam etmek için Enter'a basınız...")

def menu_search_athlete():
    print("\n--- SPORCU ARAMA ---")
    keyword = get_input("Arama Terimi (ID veya İsim): ")
    results = current_service.search_athlete(keyword)
    
    if results:
        print(f"\n{len(results)} kayıt bulundu:\n")
        for athlete in results:
            show_athlete_details(athlete)
    else:
        print("\n   [!] Kayıt bulunamadı.")
    input("\nDevam etmek için Enter'a basınız...")

def menu_list_filter():
    print("\n--- LİSTELEME VE FİLTRELEME ---")
    print("1. Tümünü Listele")
    print("2. Branşa Göre Listele")
    print("3. Detaylı Filtre (Yaş, Statü, Cinsiyet)")
    choice = get_input("Seçiminiz: ", int)

    results = []
    if choice == 1:
        results = current_service.repository.get_all()
    elif choice == 2:
        branch = get_input("Hangi Branş?: ")
        results = current_service.list_athletes_by_branch(branch)
    elif choice == 3:
        min_age = get_input("Minimum Yaş (Yoksa 0): ", int)
        status = get_input("Statü (Active/Injured vb. - Yoksa Enter): ", required=False)
        gender = get_input("Cinsiyet (Yoksa Enter): ", required=False)
        results = current_service.filter_athletes_by_criteria(min_age, status if status else None, gender if gender else None)
    
    if results:
        print(f"\n{len(results)} kayıt listeleniyor:\n")
        for athlete in results:
            show_athlete_details(athlete)
    else:
        print("\n   [!] Kriterlere uygun kayıt yok.")
    input("\nDevam etmek için Enter'a basınız...")

def menu_update_status():
    print("\n--- STATÜ GÜNCELLEME ---")
    athlete_id = get_input("Sporcu ID: ", int)
    
    # Önce sporcuyu bulup gösterelim
    athlete = current_service.repository.get_by_id(athlete_id)
    if not athlete:
        print("   [!] Sporcu bulunamadı.")
        time.sleep(1.5)
        return

    print(f"Seçilen Sporcu: {athlete['name']} {athlete['surname']} (Mevcut Durum: {athlete['status']})")
    new_status = get_input("Yeni Statü (Active, Injured, Suspended, Retired): ")

    try:
        success = current_service.update_athlete_status(athlete_id, new_status)
        if success:
            print("\n   [BAŞARILI] Statü güncellendi.")
        else:
            print("\n   [HATA] Güncelleme başarısız.")
    except ClubManagerError as e:
        print(f"\n   [İŞ KURALI HATASI] {e.message}")
        print("   -> Örneğin: Cezalı oyuncu doğrudan sakat statüsüne geçemez.")
    
    input("\nDevam etmek için Enter'a basınız...")

def menu_season_mode():
    print("\n--- SEZON MODU (CLASS METHOD DEMO) ---")
    print("Bu özellik, 'start_season_mode' class metodunu kullanarak")
    print("sistemi farklı bir yıl için (farklı bir veritabanı dosyasıyla) yeniden başlatır.")
    
    year = get_input("Hangi sezonu yönetmek istersiniz? (Örn: 2025, 2026): ", int)
    
    global current_service
    # Class method kullanımı
    current_service = AthleteService.start_season_mode(year)
    
    print(f"\n   [BİLGİ] Sistem {year} sezonuna geçiş yaptı.")
    print(f"   Veritabanı Dosyası: athletes_{year}.json")
    input("\nDevam etmek için Enter'a basınız...")

# --- ANA DÖNGÜ ---

def main():
    global current_service
    # Başlangıçta varsayılan repository ve servisi yükle
    repo = AthleteRepository()
    current_service = AthleteService(repo)

    while True:
        print_header()
        print(f"Aktif Veritabanı Modu: {current_service.repository.get_database_info()}")
        print("-" * 64)
        print("1. Yeni Sporcu Ekle (Register)")
        print("2. Sporcu Ara (Search)")
        print("3. Listele / Filtrele")
        print("4. Statü Güncelle (Update - İş Kuralları)")
        print("5. Sezon Değiştir (Class Method Demo)")
        print("6. Çıkış")
        print("-" * 64)
        
        choice = get_input("Seçiminiz: ", int)

        if choice == 1:
            menu_register_athlete()
        elif choice == 2:
            menu_search_athlete()
        elif choice == 3:
            menu_list_filter()
        elif choice == 4:
            menu_update_status()
        elif choice == 5:
            menu_season_mode()
        elif choice == 6:
            print("\nÇıkış yapılıyor... Güle güle!")
            break
        else:
            print("Geçersiz seçim!")
            time.sleep(1)

if __name__ == "__main__":
    main()