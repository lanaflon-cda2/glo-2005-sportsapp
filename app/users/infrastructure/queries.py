from app.interfaces.infrastructure.filters import MySQLFilter
from app.interfaces.infrastructure.queries import MySQLQuery
from app.users.infrastructure.filters import MySQLUserFilter as Filter
from app.users.infrastructure.tables import MySQLUserTable as Users
from app.users.infrastructure.tables import MySQLPasswordTable as Passwords


all_fields_to_add = (f'{Users.username_col}'
                     f', {Users.email_col}'
                     f', {Users.first_name_col}'
                     f', {Users.last_name_col}'
                     f', {Users.phone_number_col}'
                     f', {Users.creation_date_col}')

all_fields = f'{all_fields_to_add}, {Users.last_login_date_col}'

password_fields_to_add = (f'{Passwords.username_col}'
                          f', {Passwords.password_col}')

select_all_operation = f'SELECT {all_fields} FROM {Users.table_name}'


class MySQLUserQuery(MySQLQuery):
    def get(self, username):
        filters = [MySQLFilter.filter_equal_string(Users.username_col, username)]

        return self.build_query(select_all_operation, filters)

    def get_all(self, form=None):
        filters, inner_filtering = Filter().build_filters(form)

        orders = [Users.username_col]

        return self.build_query(select_all_operation, filters, orders, inner_filtering)

    def add_password(self):
        operation = (f'INSERT INTO {Passwords.table_name}'
                     f' ({password_fields_to_add})'
                     f' VALUES (%s, %s)')

        return self.build_query(operation)

    def add(self):
        operation = (f'INSERT INTO {Users.table_name}'
                     f' ({all_fields_to_add})'
                     f' VALUES (%s, %s, %s, %s, %s, %s)')

        return self.build_query(operation)

    def get_password(self, username):
        operation = (f'SELECT {Passwords.password_col} FROM {Passwords.table_name} P '
                     f"WHERE P.{Passwords.username_col} = '{username}' ")
        return self.build_query(operation)
