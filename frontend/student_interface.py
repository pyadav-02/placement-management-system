from backend.student import StudentFunctionality
from backend.job import JobFunctionality
from frontend.student_admin_comman_interface import ComanInterface
from frontend import frontend_utils


class StudentInterface:
    MENU = """
    press 0 to logout
    press 1 to ask question
    press 2 to see asked questions
    press 3 to see answer of the question
    press 4 to see job postings
    press 5 to apply for job
    """

    def __init__(self, student_object: StudentFunctionality):
        self.student = student_object

    @staticmethod
    def student_create_account():
        student_id = input('Enter Student id: ')
        password = input('Enter your password: ')
        name = input('Enter name: ')
        branch = input('Enter branch: ')
        year = input('Enter Year: ')
        cgpa = input('Enter CGPA: ')

        call_value = (student_id, password, name, branch, year, cgpa)
        StudentFunctionality.create_account_request(*call_value)

    def do_student_function(self):
        print(StudentInterface.MENU)
        choices = (0, 1, 2, 3, 4)
        choice = frontend_utils.get_choice(choices)

        while choice != 0:
            if choice == 1:
                self.ask_question_interface()
            elif choice == 2:
                self.view_asked_questions()
            elif choice == 3:
                self.view_answer_of_question()
            elif choice == 4:
                ComanInterface.view_job_postings('student')

            print(StudentInterface.MENU)
            choice = frontend_utils.get_choice(choices)

    def ask_question_interface(self):
        question = input('Enter your question: ')
        self.student.post_question(question)

    def view_asked_questions(self):
        questions = self.student.get_asked_questions()
        for question in questions:
            print(*question, sep=' -> ')

    def view_answer_of_question(self):
        question_id = input('Enter question id: ')

        question_status = self.student.is_question_answered(question_id)
        if question_status is None:
            print('-----invalid question id-----')
            return
        if not question_status:
            print('-----question is not answered yet-----')
            return

        answer = self.student.get_question_answer(question_id)
        print('question id:', answer[0])
        print('question:', answer[1])
        print('answer:', answer[2])

    def apply_for_job(self):
        job_id = input('Enter job id: ')

        if not JobFunctionality.is_job_id_valid(job_id):
            print('-----invalid job id-----')
            return

        if not JobFunctionality.is_student_eligible(self.student.student_id, job_id):
            print('-----you are not eligible-----')
