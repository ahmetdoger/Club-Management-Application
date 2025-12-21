import unittest
from datetime import datetime
from entities import Team
from services import MatchManager
from exceptions import SameTeamError
from entities import Referee
from entities import Stadium
from services import MatchAnalytics
from exceptions import MissingTeamError
# Sistemin tüm parçalarının hatasız çalıştığını doğrulayan test senaryoları.

class TestTeamEntity(unittest.TestCase): 
    def setUp(self):
        # Her testten önce sıfır bir takım oluşturur.
        self.team = Team(1, "Test SK", "TST", 1900, ["Siyah", "Beyaz"])

    def test_initial_values(self):
        self.assertEqual(self.team.get_points(), 0)
        self.assertEqual(self.team.get_goal_difference(), 0)

    def test_victory_points(self):
        self.team.update_stats(3, 0)
        self.assertEqual(self.team.get_points(), 3)
        self.assertEqual(self.team.get_goal_difference(), 3)

    def test_draw_points(self):
        self.team.update_stats(1, 1)
        self.assertEqual(self.team.get_points(), 1)

    def test_loss_points(self):
        self.team.update_stats(0, 2)
        self.assertEqual(self.team.get_points(), 0)
        self.assertEqual(self.team.get_goal_difference(), -2)


class TestMatchManager(unittest.TestCase):
    
    #MatchManager (Maç Yönetimi) sınıfının testleri. Maç oluşturma, hata yakalama ve listeleme testleri.
    def setUp(self):
        self.manager = MatchManager()
        self.home = Team(1, "Home FC", "HOM", 2000, ["Red"])
        self.away = Team(2, "Away FC", "AWY", 2000, ["Blue"])
        self.stadium = Stadium(1, "Test Arena", "City", 1000)

    def test_create_friendly_match(self):
        match = self.manager.create_match("Friendly", self.home, self.away, "2025-01-01", location=self.stadium)
        self.assertIsNotNone(match)
        self.assertEqual(len(self.manager.get_all_matches()), 1)

    def test_create_match_same_team_error(self):
        # Aynı takımı seçince hata veriyor mu?
        with self.assertRaises(SameTeamError):
            self.manager.create_match("Friendly", self.home, self.home, "2025-01-01")

    def test_create_match_missing_team_error(self):
        # Takım eksikse hata veriyor mu?
        with self.assertRaises(MissingTeamError):
            self.manager.create_match("Friendly", None, self.away, "2025-01-01")

    def test_manual_score_entry(self):
        
        ref = Referee(99, "Test", "Hakem", "FIFA", 5)
        
        
        match = self.manager.create_match("League", self.home, self.away, "2025-01-01", week=1, referee=ref)
        
        m_id = getattr(match, "_MatchBase__match_id")
        
        result = self.manager.enter_manual_score(m_id, 3, 1)
    
        self.assertTrue(result)
        self.assertEqual(match.get_score(), "3-1")
        self.assertEqual(match.get_status(), "Finished")


class TestMatchAnalytics(unittest.TestCase):
    
   # İstatistik ve Analiz modülünün testleri.
    
    def setUp(self):
        self.manager = MatchManager()
        self.t1 = Team(1, "A", "A", 2000, [])
        self.t2 = Team(2, "B", "B", 2000, [])
        
        m1 = self.manager.create_match("Friendly", self.t1, self.t2, "2025-01-01", location=None)
        m2 = self.manager.create_match("Friendly", self.t2, self.t1, "2025-01-02", location=None)
        
        # services.py'ye eklediğimiz fonksiyonu kullanıyoruz
        self.manager.play_match_manually(m1, 2, 1) 
        self.manager.play_match_manually(m2, 1, 1) 

    def test_total_goals(self):
        matches = self.manager.get_all_matches()
        total = MatchAnalytics.calculate_total_goals(matches)
        self.assertEqual(total, 5)

    def test_highest_scoring_match(self):
        matches = self.manager.get_all_matches()
        best_match = MatchAnalytics.find_highest_scoring_match(matches)
        self.assertEqual(best_match.get_score(), "2-1")


class TestIntegration(unittest.TestCase):
    #Sistemin genel akışını test eder.
    def test_full_flow(self):
        gs = Team(1, "Galatasaray", "GS", 1905, ["Sarı", "Kırmızı"])
        fb = Team(2, "Fenerbahçe", "FB", 1907, ["Sarı", "Lacivert"])
        
    
        mgr = MatchManager()
        ref = Referee(1, "Hakem", "Bey", "FIFA", 5)
        match = mgr.create_match("League", gs, fb, "2025-05-20", week=30, referee=ref)
        
        mgr.play_match_manually(match, 2, 1)
        
        self.assertEqual(gs.get_points(), 3)
        self.assertEqual(fb.get_points(), 0)
        self.assertEqual(gs.get_goal_difference(), 1)


if __name__ == "__main__":
    print("\n--- TESTLER BAŞLATILIYOR ---\n")
    unittest.main()