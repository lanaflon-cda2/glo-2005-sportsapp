from app.equipments.infrastructure.filters import MySQLEquipmentFilter as Filter
from app.equipments.infrastructure.tables import MySQLEquipmentTable as Equipments
from app.interfaces.infrastructure.filters import MySQLFilter
from app.interfaces.infrastructure.queries import MySQLQuery
from app.manufacturers.infrastructure.tables import MySQLManufacturerTable as Manufacturers
from app.equipment_types.infrastructure.tables import MySQLEquipmentTypeTable as EquipmentTypes

all_fields_to_add = (f'{Equipments.manufacturer_id_col}'
                     f', {Equipments.type_id_col}'
                     f', {Equipments.name_col}'
                     f', {Equipments.description_col}')

select_all_simple_operation = (f"SELECT {Equipments.id_col},"
                               f" {Equipments.name_col},"
                               f" {Equipments.description_col}"
                               f" FROM {Equipments.table_name}")


class MySQLEquipmentQuery(MySQLQuery):
    fake_count_col = 'count'
    fake_manufacturer_name_col = 'manufacturer_name'
    fake_type_name_col = 'type_name'

    from_tables = (f' FROM {Equipments.table_name} E'
                   f' JOIN {Manufacturers.table_name} M ON M.{Manufacturers.id_col} ='
                   f' E.{Equipments.manufacturer_id_col}'
                   f' JOIN {EquipmentTypes.table_name} T ON T.{EquipmentTypes.id_col} ='
                   f' E.{Equipments.type_id_col}')

    select_all_operation = (f'SELECT E.{Equipments.id_col},'
                            f' E.{Equipments.manufacturer_id_col},'
                            f' {Filter.joined_manufacturer_name_col} AS'
                            f' {fake_manufacturer_name_col},'
                            f' E.{Equipments.type_id_col},'
                            f' {Filter.joined_type_name_col} AS {fake_type_name_col},'
                            f' E.{Equipments.name_col},'
                            f' E.{Equipments.description_col}'
                            f' {from_tables}')

    select_count_operation = f'SELECT COUNT(E.id) AS {fake_count_col} {from_tables}'

    def get_all(self, form=None, offset=None, per_page=None):
        filters, inner_filtering = Filter().build_filters(form)

        orders = [f'E.{Equipments.name_col}']

        return self.build_query(self.select_all_operation, filters, orders, inner_filtering, False,
                                offset, per_page)

    def get_count(self, form):
        filters, inner_filtering = Filter().build_filters(form)

        return self.build_query(self.select_count_operation, filters, None, inner_filtering)

    def get(self, equipment_id):
        filters = [MySQLFilter.filter_equal(f'E.{Equipments.id_col}', equipment_id)]

        return self.build_query(self.select_all_operation, filters)

    def get_by_name(self, name):
        filters = [MySQLFilter.filter_equal_string(f'{Equipments.name_col}', name)]

        return self.build_query(select_all_simple_operation, filters)

    def add(self):
        operation = (f'INSERT INTO {Equipments.table_name}'
                     f'({all_fields_to_add}) VALUES (%s, %s, %s, %s)')

        return self.build_query(operation)
