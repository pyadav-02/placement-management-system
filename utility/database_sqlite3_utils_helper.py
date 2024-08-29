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


def setup_tables():

    question_answer_table = """
    create table job_posting(
    job_id integer primary key autoincrement,
    company_name text not null,
    job_description text not null,
    ctc text not null,
    applicable_branches text not null,
    total_round_count integer not null,
    current_round integer not null,
    application_close_date text not null,
    applicants_id text
    );

        """
    execute_query(question_answer_table)
