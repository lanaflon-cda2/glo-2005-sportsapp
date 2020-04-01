import unittest

from app.repositories.mysql_climate_repositories import MySQLClimatesRepository
from app.repositories.mysql_recommendation_repositories import MySQLRecommendationsRepository
from app.repositories.mysql_practice_center_repositories import MySQLPracticeCentersRepository
from app.repositories.mysql_sport_repositories import MySQLSportsRepository
from app.repositories.mysql_user_repositories import MySQLUsersRepository
from app.tests import test_basic
from app.tests.fakes import user2, \
    user1, user3, sport1, sport2, sport3, sport1_recommendation1_user1, sport2_recommendation1_user3, \
    sport2_recommendation2_user2, \
    sport3_recommendation1_user1, climate1, climate2, climate3, sport1_no_climates, sport2_no_climates, \
    sport3_no_climates, center1, center2, center3, center1_recommendation1_user1, center2_recommendation1_user1, \
    center2_recommendation2_user2, center3_recommendation1_user3, center3_recommendation2_user1
from app.users.exceptions import UserNotFoundException
from instance.db_create import db_create

sport_repository = MySQLSportsRepository()
practice_center_repository = MySQLPracticeCentersRepository()
climate_repository = MySQLClimatesRepository()
recommendation_repository = MySQLRecommendationsRepository()
user_repository = MySQLUsersRepository()


def reset_repositories():
    db_create()


def add_users():
    reset_repositories()
    user_repository.add(user1)
    user_repository.add(user2)
    user_repository.add(user3)


def add_climates():
    climate_repository.add(climate1)
    climate_repository.add(climate2)
    climate_repository.add(climate3)


def add_sports():
    sport_repository.add(sport1_no_climates)
    sport_repository.add(sport2_no_climates)
    sport_repository.add(sport3_no_climates)


def add_sports_recommendations():
    add_users()
    add_sports()
    recommendation_repository.add_for_sport(sport1_recommendation1_user1, sport1)
    recommendation_repository.add_for_sport(sport2_recommendation1_user3, sport2)
    recommendation_repository.add_for_sport(sport2_recommendation2_user2, sport2)
    recommendation_repository.add_for_sport(sport3_recommendation1_user1, sport3)


def add_practice_centers():
    add_users()
    add_climates()
    practice_center_repository.add(center1)
    practice_center_repository.add(center2)
    practice_center_repository.add(center3)


def add_practice_centers_recommendations():
    add_users()
    add_practice_centers()
    recommendation_repository.add_for_practice_center(center1_recommendation1_user1, center1)
    recommendation_repository.add_for_practice_center(center2_recommendation1_user1, center2)
    recommendation_repository.add_for_practice_center(center2_recommendation2_user2, center2)
    recommendation_repository.add_for_practice_center(center3_recommendation1_user3, center3)
    recommendation_repository.add_for_practice_center(center3_recommendation2_user1, center3)


class UsersRepositoryTests(test_basic.BasicTests):

    def test_get_with_no_user_should_raise_user_not_found_exception(self):
        reset_repositories()
        self.assertRaises(UserNotFoundException, user_repository.get, 1)

    def test_get_with_non_existent_user_should_raise_user_not_found_exception(self):
        add_users()
        self.assertRaises(UserNotFoundException, user_repository.get, -1)

    def test_get_should_get_user(self):
        add_users()
        user = user_repository.get(user1.username)
        self.assertEqual(user1, user)
        user = user_repository.get(user2.username)
        self.assertEqual(user2, user)
        user = user_repository.get(user3.username)
        self.assertEqual(user3, user)

    def test_get_should_get_sports_recommendations(self):
        add_sports_recommendations()
        user = user_repository.get(user1.username)
        self.assertCountEqual(user1.sport_recommendations, user.sport_recommendations)
        user = user_repository.get(user2.username)
        self.assertCountEqual(user2.sport_recommendations, user.sport_recommendations)
        user = user_repository.get(user3.username)
        self.assertCountEqual(user3.sport_recommendations, user.sport_recommendations)

    def test_get_should_get_practice_centers_recommendations(self):
        add_practice_centers_recommendations()
        user = user_repository.get(user1.username)
        self.assertCountEqual(user1.practice_center_recommendations, user.practice_center_recommendations)
        user = user_repository.get(user2.username)
        self.assertCountEqual(user2.practice_center_recommendations, user.practice_center_recommendations)
        user = user_repository.get(user3.username)
        self.assertCountEqual(user3.practice_center_recommendations, user.practice_center_recommendations)

    def test_get_all_with_no_user_center_get_no_user(self):
        reset_repositories()
        users = user_repository.get_all()
        self.assertEqual(0, len(users))

    def test_get_all_get_users(self):
        add_users()
        users = user_repository.get_all()
        self.assertIn(user1, users)
        self.assertIn(user2, users)
        self.assertIn(user3, users)


if __name__ == "__main__":
    unittest.main()
