import backend.table_names as tbn
from database_utility import database_sqlite3_utils as db


class StudentFunctionality:
    def __init__(self, student_id):
        self.student_id = student_id

    @staticmethod
    def create_account_request(student_id, password, name, branch, year, cgpa):
        table_name = tbn.STUDENT_ACCOUNT
        record = dict(student_id=student_id,
                      password=password,
                      name=name,
                      branch=branch,
                      year=year,
                      cgpa=cgpa,
                      approval_status='pending',
                      placement_status='unplaced')
        db.insert_record(table_name, record)

    def is_account_approved(self):
        table_name = tbn.STUDENT_ACCOUNT
        return_field = ('approval_status',)
        conditions = dict(student_id=self.student_id)
        result = db.fetch_record_by_condition(table_name, return_field, conditions)
        if not result:
            return 'refused'
        return result[0][0]

    def post_question(self, question):
        table_name = tbn.QUESTION_ANSWER
        record = dict(student_id=self.student_id,
                      question=question,
                      is_answered='false')
        db.insert_record(table_name, record)

    def get_asked_questions(self):
        table_name = tbn.QUESTION_ANSWER
        return_field = ('question_id', 'question',)
        conditions = dict(student_id=self.student_id)
        result = db.fetch_record_by_condition(table_name, return_field, conditions)
        return result

    def get_question_answer(self, question_id):
        table_name = tbn.QUESTION_ANSWER
        return_field = ('question_id', 'question', 'answer')
        conditions = dict(student_id=self.student_id, question_id=question_id)
        result = db.fetch_record_by_condition(table_name, return_field, conditions)
        return result

    def is_question_answered(self, question_id):
        table_name = tbn.QUESTION_ANSWER
        return_field = ('is_answered',)
        conditions = dict(student_id=self.student_id, question_id=question_id)
        result = db.fetch_record_by_condition(table_name, return_field, conditions)

        if not result:
            return None
        elif result[0] == ('true',):
            return True
        elif result[0] == ('false',):
            return False

