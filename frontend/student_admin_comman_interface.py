from backend.job import JobFunctionality


class ComanInterface:
    @staticmethod
    def view_job_postings(role):
        if role == 'admin':
            job_postings = JobFunctionality.get_job_postings(admin_role=True)
        else:
            job_postings = JobFunctionality.get_job_postings()

        attributes = ('job id:', 'company name:', 'job description: ', 'ctc:', 'applicable branches:',
                      'total rounds:', 'current round:', 'closing date of application(dd-mm-yyyy):')
        print('-' * 10)
        for job_posting in job_postings:
            for attribute, value in zip(attributes, job_posting):
                print(attribute, value)
            print('-' * 10)
