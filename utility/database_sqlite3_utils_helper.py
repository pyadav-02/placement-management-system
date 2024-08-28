import sqlite3
import os
project_directory = os.path.dirname(os.path.abspath(__file__))
ADDRESS = os.path.join(project_directory, 'database.db')

connection = sqlite3.connect(ADDRESS)
cursor = connection.cursor()
print('connected')


def execute_query(query, return_data=False):
    print("*" * 10)
    print(query)
    print("*" * 10)

    global cursor
    cursor.execute(query)

    if return_data:
        return cursor.fetchall()
    else:
        connection.commit()


def disconnect():
    global connection
    connection.close()


# def setup_tables():
#
#     question_answer_table = """
#         insert into credentials
#         (account_id, password, role)
#         values ('A962820126', 'R00tP@@s', 'role');
#         """
#     execute_query(question_answer_table)
