import database_utility.database_sqlite3_utils_helper as dbh
from frontend import main_menu


# dbh.setup_tables()
main_menu.start_menu()


dbh.disconnect()

print('Program ended')
