from injector import inject

from app.announces.repositories import AnnounceRepository
from app.equipments.exceptions import EquipmentNotFoundException
from app.equipments.models import Equipment
from app.equipments.repositories import EquipmentRepository
from app.equipments.infrastructure.queries import MySQLEquipmentQuery as Query
from app.equipments.infrastructure.tables import MySQLEquipmentTable as Equipments
from app.interfaces.database import Database
from app.sports.repositories import SportRepository


class MySQLEquipmentRepository(EquipmentRepository):
    @inject
    def __init__(self, database: Database,
                 sport_repository: SportRepository,
                 announce_repository: AnnounceRepository):
        self.database = database
        self.sport_repository = sport_repository
        self.announce_repository = announce_repository

    def get_all(self, form=None, offset=None, per_page=None):
        all_equipments = []

        try:
            with self.database.connect().cursor() as cur:
                query = Query().get_all(form, offset, per_page)
                cur.execute(query)

                for equipment_cur in cur.fetchall():
                    equipment = self.build_equipment(equipment_cur)
                    all_equipments.append(equipment)
        finally:
            cur.close()

        return all_equipments

    def get_count(self, form=None):
        try:
            with self.database.connect().cursor() as cur:
                query = Query().get_count(form)
                cur.execute(query)

                for equipment_cur in cur.fetchall():
                    return equipment_cur[Query.fake_count_col]
        finally:
            cur.close()

        return 0

    def get(self, equipment_id):
        try:
            with self.database.connect().cursor() as cur:
                query = Query().get(equipment_id)
                cur.execute(query)

            for equipment_cur in cur.fetchall():
                associated_sports = self.sport_repository.get_all_for_equipment_type(
                    equipment_cur[Equipments.type_id_col])
                announces = self.announce_repository.get_all_for_equipment(equipment_id)
                return self.build_equipment(equipment_cur, associated_sports, announces)
        finally:
            cur.close()

        raise EquipmentNotFoundException

    @staticmethod
    def build_equipment(cur, associated_sports=None, announces=None):
        return Equipment(cur[Equipments.id_col],
                         cur[Equipments.manufacturer_id_col],
                         cur[Query.fake_manufacturer_name_col],
                         cur[Equipments.type_id_col],
                         cur[Query.fake_type_name_col],
                         cur[Equipments.name_col],
                         cur[Equipments.description_col],
                         associated_sports,
                         announces)

    def get_by_name(self, name):
        try:
            with self.database.connect().cursor() as cur:
                query = Query().get_by_name(name)
                cur.execute(query)

            for equipment_cur in cur.fetchall():
                return self.build_simple_equipment(equipment_cur)
        finally:
            cur.close()

        raise EquipmentNotFoundException

    @staticmethod
    def build_simple_equipment(cur):
        return Equipment(cur[Equipments.id_col], None, None, None, None, cur[Equipments.name_col],
                         cur[Equipments.description_col])

    def add(self, equipment):
        try:
            with self.database.connect().cursor() as cur:
                query = Query().add()
                cur.execute(query, (equipment.manufacturer_id, equipment.type_id,
                                    equipment.name, equipment.description))

                self.database.connect().commit()

                equipment.id = cur.lastrowid

        finally:
            cur.close()
