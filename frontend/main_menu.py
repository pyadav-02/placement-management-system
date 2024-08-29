from frontend.authenticate_interface import AuthInterface
from frontend import frontend_utils as utils
from frontend.student_interface import StudentInterface
from frontend.admin_interface import AdminInterface

def start_menu():
    menu = """
    press 0 to exit
    press 1 for login
    press 2 for creating account
    """

    print(menu)
    choices = [0, 1, 2]
    choice = utils.get_choice(choices)

    while choice != 0:
        if choice == 1:
            result = AuthInterface.do_authentication()

            if result is not None and result['role'] == 'student':
                student_interface = StudentInterface(result['account_object'])
                student_interface.do_student_function()

            if result is not None and result['role'] == 'admin':
                student_interface = AdminInterface(result['account_object'])
                student_interface.do_admin_function()

        elif choice == 2:
            StudentInterface.student_create_account()

        print(menu)
        choice = utils.get_choice(choices)




