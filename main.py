import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QMessageBox
from PyQt5 import uic

# --- 1. UBUNTU EKRAN AYARI (Hata almamak için şart) ---
os.environ["QT_QPA_PLATFORM"] = "xcb"

# --- 2. SENİN VERDİĞİN İMPORTLAR ---
try:
    from modules.information.PlayerInformationPage import PlayerInfoPage
<<<<<<< HEAD
    from modules.finance.FinancialManagementPage import FinancialPage
=======
    from modules.finance.ui.FinanceModule import FinancialPage
>>>>>>> Financial-Management-Module
    from modules.matches.MatchPointManagementPage import MatchPointPage
    print("✅ Modüller başarıyla yüklendi.")
except ImportError as e:
    print(f"❌ İMPORT HATASI: {e}")
    print("Lütfen dosya adlarının ve içindeki Class adlarının birebir tuttuğundan emin olun.")
    sys.exit(1)

class AnaUygulama(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # --- 3. ARAYÜZÜ YÜKLE ---
        ui_dosyasi = 'ui/main_window.ui'
        if os.path.exists(ui_dosyasi):
            try:
                uic.loadUi(ui_dosyasi, self)
                print("✅ Arayüz (.ui) yüklendi.")
            except Exception as e:
                print(f"❌ UI Dosyası bozuk veya hatalı: {e}")
        else:
            print(f"❌ '{ui_dosyasi}' bulunamadı! Klasör yapısını kontrol et.")

        # --- 4. SAYFALARI OLUŞTUR ---
        # Burada modülleri hafızaya alıyoruz
        self.sayfa_player = PlayerInfoPage()
        self.sayfa_finance = FinancialPage()
        self.sayfa_match = MatchPointPage()

        # --- 5. STACKED WIDGET (DEĞİŞEN ALAN) ---
        # Qt Designer'da objectName kısmına 'stackedWidget' yazdığını varsayıyoruz.
        self.ana_ekran = self.findChild(QWidget, 'stackedWidget')
        
        if self.ana_ekran:
            # Sayfaları içine ekle
            self.ana_ekran.addWidget(self.sayfa_player)   # İndeks 0 (veya mevcutun sonuna eklenir)
            self.ana_ekran.addWidget(self.sayfa_finance)  # İndeks 1
            self.ana_ekran.addWidget(self.sayfa_match)    # İndeks 2
        else:
            print("❌ HATA: 'stackedWidget' bulunamadı! Designer'daki ismi kontrol et.")

        # --- 6. BUTONLARI BAĞLA ---
        # Designer'daki buton isimlerini (objectName) buraya yaz:
        # (Eğer Designer'da farklı isim verdiysen aşağıdaki parantez içlerini değiştir)
        self.btn_oyuncu = self.findChild(QWidget, 'btn_player')
        self.btn_finans = self.findChild(QWidget, 'btn_finance')
        self.btn_mac = self.findChild(QWidget, 'btn_match')

        # Tıklama olaylarını tanımla
        if self.btn_oyuncu:
            self.btn_oyuncu.clicked.connect(lambda: self.sayfa_degistir(self.sayfa_player))
        else:
            print("⚠️ UYARI: 'btn_player' bulunamadı.")

        if self.btn_finans:
            self.btn_finans.clicked.connect(lambda: self.sayfa_degistir(self.sayfa_finance))
        else:
            print("⚠️ UYARI: 'btn_finance' bulunamadı.")

        if self.btn_mac:
            self.btn_mac.clicked.connect(lambda: self.sayfa_degistir(self.sayfa_match))
        else:
            print("⚠️ UYARI: 'btn_match' bulunamadı.")

    def sayfa_degistir(self, sayfa_objesi):
        if self.ana_ekran:
            self.ana_ekran.setCurrentWidget(sayfa_objesi)

if __name__ == '__main__':
    print("🚀 Uygulama başlatılıyor...")
    app = QApplication(sys.argv)
    window = AnaUygulama()
    window.show()
    print("✅ Pencere açıldı.")
    sys.exit(app.exec_())