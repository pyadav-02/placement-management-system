from backend.admin import AdminFunctionality
from frontend import frontend_utils


class AdminInterface:
    MENU = """
    press 0 to go back and logout
    press 1 to view account requests
    press 2 to approve account request
    """

    def __init__(self, admin_object: AdminFunctionality):
        self.admin = admin_object

    def do_admin_function(self):
        print(AdminInterface.MENU)
        choices = (0, 1, 2)
        choice = frontend_utils.get_choice(choices)

        while choice != 0:
            if choice == 1:
                self.view_account_requests()
            if choice == 2:
                self.approve_account_request()

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


