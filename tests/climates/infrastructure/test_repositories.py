from app.climates.infrastructure.repositories import MySQLClimateRepository
from tests.interfaces.infrastructure.database import test_database
from tests.interfaces.infrastructure.test_repositories import RepositoryTests
from tests.practice_centers.fakes import center1, center2, center3
from tests.sports.fakes import sport1, sport2, sport3


class ClimateRepositoryTests(RepositoryTests):

    def setUp(self):
        super().setUp()
        self.repository = MySQLClimateRepository(test_database)

    def test_get_all_for_sport_without_sport_get_get_no_climate(self):
        self.recreate_database()
        climates = self.repository.get_all_for_sport(sport1.id)
        self.assertEqual(0, len(climates))
        climates = self.repository.get_all_for_sport(sport2.id)
        self.assertEqual(0, len(climates))
        climates = self.repository.get_all_for_sport(sport3.id)
        self.assertEqual(0, len(climates))

    def test_get_all_for_sport_should_get_sport_climates(self):
        climates = self.repository.get_all_for_sport(sport1.id)
        self.assertCountEqual(sport1.climates, climates)
        climates = self.repository.get_all_for_sport(sport2.id)
        self.assertCountEqual(sport2.climates, climates)
        climates = self.repository.get_all_for_sport(sport3.id)
        self.assertCountEqual(sport3.climates, climates)

    def test_get_all_for_practice_center_should_without_practice_center_get_no_climate(self):
        self.recreate_database()
        climates = self.repository.get_all_for_practice_center(center1.id)
        self.assertEqual(0, len(climates))
        climates = self.repository.get_all_for_practice_center(center2.id)
        self.assertEqual(0, len(climates))
        climates = self.repository.get_all_for_practice_center(center3.id)
        self.assertEqual(0, len(climates))

    def test_get_all_for_practice_center_should_get_practice_center_climates(self):
        climates = self.repository.get_all_for_practice_center(center1.id)
        self.assertCountEqual(center1.climates, climates)
        climates = self.repository.get_all_for_practice_center(center2.id)
        self.assertCountEqual(center2.climates, climates)
        climates = self.repository.get_all_for_practice_center(center3.id)
        self.assertCountEqual(center3.climates, climates)
