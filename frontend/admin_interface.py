from backend.admin import AdminFunctionality
from backend.job import JobFunctionality
from frontend.student_admin_comman_interface import ComanInterface
from frontend import frontend_utils


class AdminInterface:
    MENU = """
    press 0 to go back and logout
    press 1 to view account requests
    press 2 to approve account request
    press 3 to view all unanswered questions
    press 4 to answer any question
    press 5 to post job
    press 6 to view all job postings
    """

    def __init__(self, admin_object: AdminFunctionality):
        self.admin = admin_object

    def do_admin_function(self):
        print(AdminInterface.MENU)
        choices = (0, 1, 2, 3, 4, 5, 6)
        choice = frontend_utils.get_choice(choices)

        while choice != 0:
            if choice == 1:
                self.view_account_requests()
            elif choice == 2:
                self.approve_account_request()
            elif choice == 3:
                AdminInterface.view_unanswered_questions()
            elif choice == 4:
                self.answer_question()
            elif choice == 5:
                AdminInterface.post_job()
            elif choice == 6:
                ComanInterface.view_job_postings('admin')

            print(AdminInterface.MENU)
            choice = frontend_utils.get_choice(choices)

    def view_account_requests(self):
        account_requests = self.admin.get_account_requests()
        print('-' * 10)
        for account_request in account_requests:
            print('student id:', account_request[0])
            print('student name:', account_request[1])
            print('branch:', account_request[2])
            print('year:', account_request[3])
            print('-' * 10)

    def approve_account_request(self):
        account_id = input('Enter account id: ')

        if AdminFunctionality.is_account_exist(account_id):
            self.admin.approve_student_account_request(account_id)
            print('-----account approved-----')
            return

        print("-----account don't exist-----")

    @staticmethod
    def view_unanswered_questions():
        questions = AdminFunctionality.get_unanswered_questions()

        for question in questions:
            print('-' * 10)
            print('question_id:', question[0])
            print('student_id:', question[1])
            print('question:', question[2])
        print('-' * 10)

    def answer_question(self):
        question_id = input('Enter question id: ')
        question_status = AdminFunctionality.get_question_status_by_id(question_id)
        if question_status is None:
            print('-----invalid question id-----')
            return
        elif question_status:
            print('-----question already answered-----')
            return

        answer = input('Enter answer: ')
        self.admin.post_answer(question_id, answer)

    @staticmethod
    def post_job():
        company_name = input('Enter company name: ')
        job_description = input('Enter job description: ')
        ctc = input('Enter ctc(lpa): ')
        applicable_branches = input('Enter applicable branches(branch, branch, ...): ')
        total_rounds_count = input('Enter total number of rounds: ')
        application_close_date = input('Enter application close date(dd-mm-yyyy): ')
        JobFunctionality.create_job_posting(company_name,
                                            job_description,
                                            ctc,
                                            applicable_branches,
                                            total_rounds_count,
                                            application_close_date)
