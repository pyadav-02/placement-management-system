import utility.database_sqlite3_utils_helper as dbh
from frontend import main_menu

# import utility.database_sqlite3_utils as db
# from backend.authentication import AuthenticationFunctionality
#
# a = dict(role='admin')
# db.update_record_by_id('credentials', 'account_id', 'A962820126', a)


# account_id = input('id: ')
# password = input('password: ')
#
# result = AuthenticationFunctionality.is_valid(account_id, password, 'admin')


main_menu.start_menu()


dbh.disconnect()

print('Program ended')
