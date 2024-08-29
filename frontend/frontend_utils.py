
def get_choice(choices):
    choice = input('Enter input: ')
    try:
        choice = int(choice)
    except ValueError:
        pass

    while choice not in choices:
        print('Invalid input please enter valid input')

        choice = input('Enter input: ')
        try:
            choice = int(choice)
        except ValueError:
            pass

    return choice
