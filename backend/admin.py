import backend.table_names as tbn
from database_utility import database_sqlite3_utils as db


class AdminFunctionality:
    def __init__(self, admin_id):
        self.__admin_id = admin_id

    @staticmethod
    def get_unanswered_questions():
        table_name = tbn.QUESTION_ANSWER
        return_fields = ('question_id', 'student_id', 'question')
        conditions = dict(is_answered='false')
        result = db.fetch_record_by_condition(table_name, return_fields, conditions)
        return result

    def post_answer(self, question_id, answer):
        table_name = tbn.QUESTION_ANSWER
        id_field = 'question_id'
        id_field_value = question_id
        updates = dict(admin_id=self.__admin_id, answer=answer, is_answered='true')
        db.update_record_by_id(table_name, id_field, id_field_value, updates)

    @staticmethod
    def get_question_status_by_id(question_id):
        table_name = tbn.QUESTION_ANSWER
        return_fields = ('is_answered',)
        conditions = dict(question_id=question_id)
        result = db.fetch_record_by_condition(table_name, return_fields, conditions)

        if not result:
            return None
        elif result[0] == ('true',):
            return True
        elif result[0] == ('false',):
            return False

    @staticmethod
    def get_account_requests():
        table_name = tbn.STUDENT_ACCOUNT
        return_fields = ('student_id', 'name', 'branch', 'year')
        conditions = dict(approval_status='pending')
        result = db.fetch_record_by_condition(table_name, return_fields, conditions)
        return result

    def approve_student_account_request(self, student_id):
        status_value = 'approved'
        self.set_approval_status(student_id, status_value)

        password = AdminFunctionality.get_student_password(student_id)
        role = 'student'
        AdminFunctionality.set_account_credential(student_id, password, role)

    def set_approval_status(self, student_id, status_value):
        table_name = tbn.STUDENT_ACCOUNT
        id_field = 'student_id'
        id_field_value = student_id
        updates = dict(approval_status=status_value, approver_id=self.__admin_id)
        db.update_record_by_id(table_name, id_field, id_field_value, updates)

    @staticmethod
    def get_student_password(student_id):
        table_name = tbn.STUDENT_ACCOUNT
        return_field = ('password',)
        conditions = dict(student_id=student_id)
        result = db.fetch_record_by_condition(table_name, return_field, conditions)
        return result[0][0]

    @staticmethod
    def set_account_credential(account_id, password, role):
        table_name = tbn.CREDENTIALS
        record = dict(account_id=account_id, password=password, role=role)
        db.insert_record(table_name, record)

    @staticmethod
    def refuse_account_request(student_id):
        table_name = tbn.STUDENT_ACCOUNT
        id_field = 'student_id'
        conditions = dict()
        db.delete_record_by_id(table_name, id_field, student_id, conditions)

    @staticmethod
    def is_account_exist(student_id):
        table_name = tbn.STUDENT_ACCOUNT
        return_fields = ('student_id',)
        conditions = dict(student_id=student_id)
        result = db.fetch_record_by_condition(table_name, return_fields, conditions)

        if result:
            return True
        else:
            return False

    @staticmethod
    def is_account_approved(student_id):
        table_name = tbn.STUDENT_ACCOUNT
        return_field = ('approval_status',)
        conditions = dict(student_id=student_id)
        result = db.fetch_record_by_condition(table_name, return_field, conditions)
        if result[0][0] == 'approved':
            return True
        return False