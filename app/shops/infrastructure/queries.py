from app.interfaces.infrastructure.filters import MySQLFilter
from app.interfaces.infrastructure.queries import MySQLQuery
from app.shops.infrastructure.filters import MySQLShopFilter as Filter
from app.shops.infrastructure.tables import MySQLShopTable as Shops

all_fields_to_add = (f'{Shops.name_col}'
                     f', {Shops.email_col}'
                     f', {Shops.phone_number_col}'
                     f', {Shops.web_site_col}')

all_fields = f'{Shops.id_col}, {all_fields_to_add}'

select_all_operation = f'SELECT {all_fields} FROM {Shops.table_name}'


class MySQLShopQuery(MySQLQuery):
    fake_count_col = 'count'

    select_count_operation = f'SELECT COUNT(*) AS {fake_count_col} FROM {Shops.table_name}'

    def get_all(self, form=None, offset=None, per_page=None):
        filters, inner_filtering = Filter().build_filters(form)

        orders = [Shops.name_col]

        return self.build_query(select_all_operation, filters, orders, inner_filtering, False,
                                offset, per_page)

    def get_count(self, form=None):
        filters, inner_filtering = Filter().build_filters(form)

        return self.build_query(self.select_count_operation, filters, None, inner_filtering)

    def get(self, shop_id):
        filters = [MySQLFilter.filter_equal(Shops.id_col, shop_id)]

        return self.build_query(select_all_operation, filters)

    def get_by_name(self, name):
        filters = [MySQLFilter.filter_equal_string(Shops.name_col, name)]

        return self.build_query(select_all_operation, filters)

    def add(self):
        operation = (f'INSERT INTO {Shops.table_name}'
                     f'({all_fields_to_add}) VALUES (%s, %s, %s, %s)')

        return self.build_query(operation)
