import unittest
from unittest.mock import patch
from backend.admin import AdminFunctionality
import backend.table_names as tbn


class TestAdminFunctionality:
    def setup_class(self):
        self.admin_id = 'A962820126'
        self.admin_functionality = AdminFunctionality(self.admin_id)

    @patch('utility.database_sqlite3_utils.fetch_record_by_condition')
    def test_get_unanswered_questions(self, mock_fetch_record_by_condition):
        expected_result = [('S219301502', 'a random question?'),
                           ('S219301087', 'something students ask')]
        mock_fetch_record_by_condition.return_value = expected_result

        result = AdminFunctionality.get_unanswered_questions()
        assert result == expected_result

        table_name = tbn.QUESTION_ANSWER
        return_field = ['student_id', 'question']
        condition_field = ['is_answered']
        condition_value = ['False']
        expected_call = (table_name, return_field, condition_field, condition_value)
        mock_fetch_record_by_condition.assert_called_once_with(*expected_call)

    @patch('utility.database_sqlite3_utils.update_record_by_id')
    def test_post_answer(self, mock_update_record_by_id):
        question_id = 2315
        answer = 'answer given by the admin'

        self.admin_functionality.post_answer(question_id, answer)

        table_name = tbn.QUESTION_ANSWER
        id_field = 'question_id'
        id_field_value = question_id
        fields_to_update = ['admin_id', 'answer', 'is_answered']
        update_values = [self.admin_id, answer, 'True']
        expected_call = (table_name, id_field, id_field_value, fields_to_update, update_values)
        mock_update_record_by_id.assert_called_once_with(*expected_call)

    @patch('utility.database_sqlite3_utils.fetch_record_by_condition')
    def test_get_account_requests(self, mock_fetch_record_by_condition):
        expected_output = [('S219301502', 'Piyush Yadav', 'Btech', 'CSE', 4),
                           ('S219301087', 'Manav Kumar', 'Btech', 'CSE-AI', 3)]
        mock_fetch_record_by_condition.return_value = expected_output

        result = AdminFunctionality.get_account_requests()
        assert result == expected_output

        table_name = tbn.STUDENT_ACCOUNT
        return_field = ['student_id', 'name', 'program', 'branch', 'year']
        condition_field = ['is_approved']
        condition_value = ['Pending']
        expected_call = (table_name, return_field, condition_field, condition_value)
        mock_fetch_record_by_condition.assert_called_once_with(*expected_call)

    @patch('backend.admin.AdminFunctionality.get_student_password')
    @patch('backend.admin.AdminFunctionality.set_account_credential')
    @patch('backend.admin.AdminFunctionality.set_approval_status')
    def test_approve_student_account_request(self,
                                             mock_set_approval_status,
                                             mock_set_account_credential,
                                             mock_get_student_password):
        status_value = 'approved'
        student_id = 'S857485168'
        password = 'fkahUGi59f@#K'
        role = 'student'
        mock_get_student_password.return_value = password
        self.admin_functionality.approve_student_account_request(student_id)

        mock_set_approval_status.assert_called_once_with(student_id, status_value)
        mock_get_student_password.assert_called_once_with(student_id)
        mock_set_account_credential.assert_called_once_with(student_id, password, role)

    @patch('utility.database_sqlite3_utils.update_record_by_id')
    def test_set_approval_status(self, mock_update_record_by_id):
        status_value = 'approved'
        student_id = 'S219301502'
        self.admin_functionality.set_approval_status(student_id, status_value)

        table_name = tbn.STUDENT_ACCOUNT
        id_field = 'student_id'
        id_field_value = student_id
        fields_to_update = ['approval_status', 'approver_id']
        update_values = [status_value, self.admin_id]
        expected_call = (table_name, id_field, id_field_value, fields_to_update, update_values)
        mock_update_record_by_id.assert_called_once_with(*expected_call)

    @patch('utility.database_sqlite3_utils.fetch_record_by_condition')
    def test_get_student_password(self, mock_fetch_record_by_condition):
        expected_result = [('dkdf*&931dYaH',), ('HYafh71924&4+a',)]
        student_id = 'S184718291'
        mock_fetch_record_by_condition.return_value = expected_result

        result = AdminFunctionality.get_student_password(student_id)
        assert result == expected_result

        table_name = tbn.STUDENT_ACCOUNT
        return_field = ['password']
        condition_field = ['student_id']
        condition_value = [student_id]
        expected_call = (table_name, return_field, condition_field, condition_value)
        mock_fetch_record_by_condition.assert_called_once_with(*expected_call)

    @patch('utility.database_sqlite3_utils.insert_record')
    def test_set_account_credential(self, mock_insert_record):
        student_id = 'S184018391'
        password = 'euH8*+fh&211h'
        role = 'student'
        AdminFunctionality.set_account_credential(student_id, password, role)

        table_name = tbn.CREDENTIALS
        field_names = ['account_id', 'password', 'role']
        field_values = [student_id, password, role]
        mock_insert_record.assert_called_once_with(table_name, field_names, field_values)

    @patch('utility.database_sqlite3_utils.delete_record_by_id')
    def test_refuse_account_request(self, mock_delete_record_by_id):
        student_id = 'S184018391'
        AdminFunctionality.refuse_account_request(student_id)

        table_name = tbn.STUDENT_ACCOUNT
        id_field = 'student_id'
        condition_field = []
        condition_value = []
        expected_call = (table_name, id_field, student_id, condition_field, condition_value)
        mock_delete_record_by_id.assert_called_once_with(*expected_call)
