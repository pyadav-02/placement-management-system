from backend.authentication import AuthenticationFunctionality
from backend.admin import AdminFunctionality
from backend.student import StudentFunctionality
from frontend import frontend_utils


class AuthInterface:
    MENU = """
    press 1 to login as admin
    press 2 to login as student
    press 3 to go back
    """
    __account_object = None

    @staticmethod
    def do_authentication():
        print(AuthInterface.MENU)
        choices = [1, 2, 3]
        choice = frontend_utils.get_choice(choices)

        while choice != 3:
            role = ''
            if choice == 1:
                role = 'admin'
            elif choice == 2:
                role = 'student'

            validation_status = AuthInterface.account_validator(role)
            if validation_status:
                account_object = AuthInterface.__account_object
                AuthInterface.__account_object = None
                return dict(account_object=account_object, role=role)

            print(AuthInterface.MENU)
            choice = frontend_utils.get_choice(choices)

        return None

    @staticmethod
    def account_validator(role) -> bool:
        account_id = input("\nEnter account id: ")

        if role == 'student':
            student_status = AuthInterface.get_student_account_status(account_id)
            if student_status == 'pending':
                print('----account request is not approved yet-----')
                return False

        password = input("Enter password: ")
        check = AuthenticationFunctionality.is_valid(account_id, password, role)
        if check:
            print('-----login successful-----')
            AuthInterface.set_account_object(account_id, role)
            return True
        else:
            print('-----invalid account or password-----')
            return False

    @staticmethod
    def get_student_account_status(account_id):
        student = StudentFunctionality(account_id)
        return student.is_account_approved()

    @staticmethod
    def set_account_object(account_id, role):
        if role == 'admin':
            AuthInterface.__account_object = AdminFunctionality(account_id)
        elif role == 'student':
            AuthInterface.__account_object = StudentFunctionality(account_id)
