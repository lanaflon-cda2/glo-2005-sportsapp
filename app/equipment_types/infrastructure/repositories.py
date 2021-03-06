from injector import inject

from app.equipment_types.models import EquipmentType
from app.equipment_types.repositories import EquipmentTypeRepository
from app.equipment_types.infrastructure.queries import MySQLEquipmentTypeQuery as Query
from app.equipment_types.infrastructure.tables import MySQLEquipmentTypeTable as EquipmentTypes
from app.interfaces.database import Database


class MySQLEquipmentTypeRepository(EquipmentTypeRepository):
    @inject
    def __init__(self, database: Database):
        self.database = database

    def get_all_for_sport(self, sport_id):
        equipment_types = []

        try:
            with self.database.connect().cursor() as cur:
                query = Query().get_all_for_sport(sport_id)
                cur.execute(query)

                for type_cur in cur.fetchall():
                    equipment_types.append(self.build_equipment_type(type_cur))
        finally:
            cur.close()

        return equipment_types

    def get_by_name(self, name):
        try:
            with self.database.connect().cursor() as cur:
                query = Query().get_by_name(name)
                cur.execute(query)

                for type_cur in cur.fetchall():
                    return self.build_equipment_type(type_cur)
        finally:
            cur.close()

    @staticmethod
    def build_equipment_type(cur):
        return EquipmentType(cur[EquipmentTypes.id_col], cur[EquipmentTypes.name_col])

    def add(self, equipment_type):
        try:
            with self.database.connect().cursor() as cur:
                query = Query().add()
                cur.execute(query, equipment_type.name)

                self.database.connect().commit()

                equipment_type.id = cur.lastrowid
        finally:
            cur.close()

    def add_to_sport(self, equipment_type, sport):
        try:
            with self.database.connect().cursor() as cur:
                query = Query().add_to_sport()
                cur.execute(query, (equipment_type.id, sport.id))

                self.database.connect().commit()
        finally:
            cur.close()
