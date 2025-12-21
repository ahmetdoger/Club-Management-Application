# =============================================================================
# MODULE 3 - CUSTOM EXCEPTION CLASSES
# Bu modül, Futbol Yönetim Sistemi'nde oluşabilecek özel hataları yönetir.
# Hata kodları ve detaylı hata mesajları burada tanımlanır.
# =============================================================================

class MatchSystemError(Exception):
    """
    Sistemin genel hata sınıfı.
    Diğer tüm hatalar bu sınıftan türetilir.
    """
    def __init__(self, message="Bilinmeyen bir sistem hatası oluştu.", code=500):
        self.message = message
        self.code = code
        super().__init__(self.message)

    def __str__(self):
        return f"[Hata Kodu: {self.code}] -> {self.message}"


# --- OYUN İÇİ MANTIK HATALARI (GAME LOGIC ERRORS) ---

class SameTeamError(MatchSystemError):
    """
    Bir maçta ev sahibi ve deplasman takımı aynı olduğunda fırlatılır.
    """
    def __init__(self, team_name):
        message = f"DİKKAT: '{team_name}' takımı kendi kendisiyle maç yapamaz!"
        super().__init__(message, code=101)


class MissingTeamError(MatchSystemError):
    """
    Takım seçimi yapılmadığında veya eksik olduğunda fırlatılır.
    """
    def __init__(self):
        super().__init__("Lütfen iki farklı takım seçtiğinizden emin olun.", code=102)


class InvalidScoreError(MatchSystemError):
    """
    Skor negatif veya geçersiz girildiğinde fırlatılır.
    """
    def __init__(self, score):
        super().__init__(f"Geçersiz skor girişi tespit edildi: {score}", code=103)


# --- TURNUVA HATALARI (TOURNAMENT ERRORS) ---

class TournamentRoundError(MatchSystemError):
    """
    Turnuva tur eşleşmelerinde hata olduğunda çalışır.
    """
    def __init__(self, round_name):
        super().__init__(f"Turnuva turu oluşturulurken hata: {round_name}", code=201)


# --- DOSYA VE VERİTABANI HATALARI (DATA ERRORS) ---

class DatabaseConnectionError(MatchSystemError):
    """
    Repository dosyasına erişilemediğinde fırlatılır.
    """
    def __init__(self, file_path):
        super().__init__(f"Veritabanı dosyasına ulaşılamadı: {file_path}", code=301)


class DataIntegrityError(MatchSystemError):
    """
    Veri bütünlüğü bozulduğunda (örn: ID çakışması) fırlatılır.
    """
    def __init__(self, data_id):
        super().__init__(f"Veri çakışması tespit edildi. ID: {data_id}", code=302)

# --- HATA MESAJLARI SÖZLÜĞÜ (EKSTRA SATIR İÇİN) ---
ERROR_DEFINITIONS = {
    101: "Same Team Selection",
    102: "Missing Team Object",
    103: "Invalid Score Value",
    201: "Tournament Round Mismatch",
    301: "File IO Error",
    302: "Duplicate Key Error"
}

