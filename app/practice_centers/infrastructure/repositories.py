from injector import inject

from app.climates.repositories import ClimateRepository
from app.interfaces.database import Database
from app.practice_centers.exceptions import PracticeCenterNotFoundException
from app.practice_centers.infrastructure.queries import MySQLPracticeCenterQuery as Query
from app.practice_centers.infrastructure.tables import MySQLPracticeCenterTable as PracticeCenters
from app.practice_centers.models import PracticeCenter
from app.practice_centers.repositories import PracticeCenterRepository
from app.recommendations.repositories import RecommendationRepository


class MySQLPracticeCenterRepository(PracticeCenterRepository):
    @inject
    def __init__(self, database: Database, climate_repository: ClimateRepository,
                 recommendation_repository: RecommendationRepository):
        self.database = database
        self.climates_repository = climate_repository
        self.recommendation_repository = recommendation_repository

    def get_all(self, form=None, offset=None, per_page=None):
        all_practice_centers = []

        try:
            with self.database.connect().cursor() as cur:
                query = Query().get_all(form, offset, per_page)
                cur.execute(query)

                for practice_center_cur in cur.fetchall():
                    practice_center = self.build_practice_center_with_note(practice_center_cur)
                    all_practice_centers.append(practice_center)
        finally:
            cur.close()

        return all_practice_centers

    def get_count(self, form=None):
        try:
            with self.database.connect().cursor() as cur:
                query = Query().get_count(form)
                cur.execute(query)

                for practice_center_cur in cur.fetchall():
                    return practice_center_cur[Query.fake_count_col]
        finally:
            cur.close()

        return 0

    def get(self, practice_center_id):
        try:
            with self.database.connect().cursor() as cur:
                query = Query().get(practice_center_id)
                cur.execute(query)

                for practice_center_cur in cur.fetchall():
                    climates = self.climates_repository\
                        .get_all_for_practice_center(practice_center_id)
                    recommendations = self.recommendation_repository\
                        .get_all_for_practice_center(practice_center_id)
                    return self.build_practice_center_with_note(practice_center_cur, climates,
                                                                recommendations)
        finally:
            cur.close()

        raise PracticeCenterNotFoundException

    @staticmethod
    def build_practice_center_with_note(cur, climates=None, recommendations=None):
        return PracticeCenter(cur[PracticeCenters.id_col],
                              cur[PracticeCenters.name_col],
                              cur[PracticeCenters.email_col],
                              cur[PracticeCenters.web_site_col],
                              cur[PracticeCenters.phone_number_col],
                              climates,
                              recommendations,
                              cur[Query.fake_average_note_col])

    def get_by_name(self, name):
        try:
            with self.database.connect().cursor() as cur:
                query = Query().get_by_name(name)
                cur.execute(query)

                for practice_center_cur in cur.fetchall():
                    return self.build_practice_center(practice_center_cur)
        finally:
            cur.close()

        raise PracticeCenterNotFoundException

    @staticmethod
    def build_practice_center(cur):
        return PracticeCenter(cur[PracticeCenters.id_col],
                              cur[PracticeCenters.name_col],
                              cur[PracticeCenters.email_col],
                              cur[PracticeCenters.web_site_col],
                              cur[PracticeCenters.phone_number_col])

    def add(self, practice_center):
        try:
            with self.database.connect().cursor() as cur:
                query = Query().add()
                cur.execute(query, (practice_center.name, practice_center.email,
                                    practice_center.web_site, practice_center.phone_number))

                self.database.connect().commit()

                practice_center.id = cur.lastrowid

                for climate in practice_center.climates:
                    self.climates_repository.add_to_practice_center(climate, practice_center)
        finally:
            cur.close()
