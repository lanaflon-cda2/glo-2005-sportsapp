from app.repositories.mysql_queries import MySQLQuery
from app.repositories.mysql_tables import MySQLPracticeCentersTable

all_fields_to_add = (MySQLPracticeCentersTable.name_col +
                     ', ' + MySQLPracticeCentersTable.email_col +
                     ', ' + MySQLPracticeCentersTable.web_site_col +
                     ', ' + MySQLPracticeCentersTable.phone_number_col)

all_fields = (MySQLPracticeCentersTable.id_col + ', ' + all_fields_to_add)

select_all_operation = ('SELECT ' + all_fields + ' FROM ' + MySQLPracticeCentersTable.table_name)


class MySQLPracticeCentersQuery(MySQLQuery):
    def get_all(self, form=None):
        inner_filtering = True

        if form is None:
            filters = None
        else:
            filters = []

            if form.all.data != '':
                inner_filtering = False
                filters.append(self.filter_like(MySQLPracticeCentersTable.name_col, form.all.data))
                filters.append(self.filter_like(MySQLPracticeCentersTable.email_col, form.all.data))
                filters.append(self.filter_like(MySQLPracticeCentersTable.web_site_col, form.all.data))
                filters.append(self.filter_like(MySQLPracticeCentersTable.phone_number_col, form.all.data))
            else:
                if form.name.data != '':
                    filters.append(self.filter_like(MySQLPracticeCentersTable.name_col, form.name.data))

                if form.email.data != '':
                    filters.append(self.filter_like(MySQLPracticeCentersTable.email_col, form.email.data))

                if form.web_site.data != '':
                    filters.append(self.filter_like(MySQLPracticeCentersTable.web_site_col, form.web_site.data))

                if form.phone_number.data != '':
                    filters.append(self.filter_like(MySQLPracticeCentersTable.phone_number_col, form.phone_number.data))

        orders = [MySQLPracticeCentersTable.name_col]

        return self.build_query(select_all_operation, filters, orders, inner_filtering)

    def get(self, practice_center_id):
        filters = [self.filter_equal(MySQLPracticeCentersTable.id_col, practice_center_id)]

        return self.build_query(select_all_operation, filters)

    def add(self):
        operation = ('INSERT INTO ' + MySQLPracticeCentersTable.table_name +
                     '(' + all_fields_to_add + ') VALUES (%s, %s, %s, %s)')

        return self.build_query(operation)
