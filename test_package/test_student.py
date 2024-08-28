import pytest
from unittest.mock import patch
from backend.student import StudentFunctionality
import backend.table_names as tbn


class TestStudentFunctionality:
    def setup_class(self):
        student_id = 'S574839475'
        password = 'fhyHua795#@haR'
        self.student_functionality = StudentFunctionality(student_id, password)

    @patch('utility.database_sqlite3_utils.insert_record')
    def test_create_account_request(self, mock_insert_record):
        name = 'Rishabh Yadav'
        branch = 'computer science'
        year = 2026
        cgpa = 9.2
        call_value = (name, branch, year, cgpa)
        self.student_functionality.create_account_request(*call_value)

        student_id = self.student_functionality.student_id
        password = self.student_functionality.password
        table_name = tbn.STUDENT_ACCOUNT
        field_names = ['student_id', 'password', 'name', 'branch', 'year', 'cgpa', 'approval_status']
        field_values = [student_id, password, name, branch, year, cgpa, 'pending']
        mock_insert_record.assert_called_once_with(table_name, field_names, field_values)

    @patch('utility.database_sqlite3_utils.fetch_record_by_condition')
    def is_account_approved_helper(self, mock_fetch_record_by_condition, expected_output, expected_return_value):
        mock_fetch_record_by_condition.return_value = expected_return_value
        result = self.student_functionality.is_account_approved()
        assert result == expected_output

        table_name = tbn.STUDENT_ACCOUNT
        return_field = ['approval_status']
        condition_field = ['student_id']
        condition_value = [self.student_functionality.student_id]
        expected_call = (table_name, return_field, condition_field, condition_value)
        mock_fetch_record_by_condition.assert_called_once_with(*expected_call)

    def test_is_account_approved_pending(self):
        self.is_account_approved_helper(expected_output='pending', expected_return_value=[('pending',)])

    def test_is_account_approved_approved(self):
        self.is_account_approved_helper(expected_output='approved', expected_return_value=[('approved',)])

    def test_is_account_approved_refused(self):
        self.is_account_approved_helper(expected_output='refused', expected_return_value=[])

    @patch('utility.database_sqlite3_utils.insert_record')
    def test_post_question(self, mock_insert_record):
        question = 'this question? is asked by student:)'
        self.student_functionality.post_question(question)

        table_name = tbn.QUESTION_ANSWER
        field_names = ['student_id', 'question', 'is_answered']
        student_id = self.student_functionality.student_id
        field_values = [student_id, question, 'False']
        mock_insert_record.assert_called_once_with(table_name, field_names, field_values)

    @patch('utility.database_sqlite3_utils.fetch_record_by_condition')
    def test_get_asked_questions(self, mock_fetch_record_by_condition):
        expected_output = [('what is it?', 'False'),
                           ('can i apply for job?', 'True')]
        mock_fetch_record_by_condition.return_value = expected_output
        result = self.student_functionality.get_asked_questions()
        assert result == expected_output

        table_name = tbn.QUESTION_ANSWER
        return_field = ['question']
        condition_field = ['student_id']
        condition_value = [self.student_functionality.student_id]
        expected_call = (table_name, return_field, condition_field, condition_value)
        mock_fetch_record_by_condition.assert_called_once_with(*expected_call)

    @patch('utility.database_sqlite3_utils.fetch_record_by_condition')
    def test_get_question_answer(self, mock_fetch_record_by_condition):
        expected_output = [('this is answer',)]
        mock_fetch_record_by_condition.return_value = expected_output
        question_id = 128
        result = self.student_functionality.get_question_answer(question_id)
        assert result == expected_output

        table_name = tbn.QUESTION_ANSWER
        return_field = ['question']
        condition_field = ['student_id', 'question_id']
        condition_value = [self.student_functionality.student_id, 'question_id']
        expected_call = (table_name, return_field, condition_field, condition_value)
        mock_fetch_record_by_condition.assert_called_once_with(*expected_call)

