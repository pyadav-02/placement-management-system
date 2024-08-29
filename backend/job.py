import backend.table_names as tbn
from utility import database_sqlite3_utils as db


class JobFunctionality:
    @staticmethod
    def create_job_posting(company_name,
                           job_description,
                           ctc,
                           applicable_branches: str,
                           total_round_count,
                           application_close_date):
        table_name = tbn.JOB_POSTING
        record = dict(company_name=company_name,
                      job_description=job_description,
                      ctc=ctc,
                      applicable_branches=applicable_branches,
                      total_round_count=total_round_count,
                      current_round='0',
                      application_close_date=application_close_date,
                      applicants_id='=')
        db.insert_record(table_name, record)

    @staticmethod
    def get_job_postings(admin_role=False):
        table_name = tbn.JOB_POSTING
        return_fields = ('job_id', 'company_name', 'job_description', 'ctc', 'applicable_branches',
                         'total_rounds_count', 'current_round', 'application_close_date')

        conditions = dict()
        if not admin_role:
            conditions['current_round'] = 0

        result = db.fetch_record_by_condition(table_name, return_fields, conditions)
        return result

    @staticmethod
    def apply_for_job(student_id, job_id):
        table_name = tbn.JOB_POSTING
        return_fields = ('applicants_id',)
        conditions = dict(job_id=job_id)
        applicants = db.fetch_record_by_condition(table_name, return_fields, conditions)

        applicants_string = applicants[0][0]
        new_applicants_string = applicants_string + ', ' + student_id

        records = dict(applicants_id=new_applicants_string)
        db.insert_record(table_name, records)

    @staticmethod
    def is_student_eligible(student_id, job_id):
        table_name = tbn.STUDENT_ACCOUNT
        return_fields = ('branch',)
        conditions = dict(student_id=student_id)
        branch = db.fetch_record_by_condition(table_name, return_fields, conditions)
        branch = branch[0][0]

        table_name = tbn.JOB_POSTING
        return_fields = ('applicable_branches',)
        conditions = dict(job_id=job_id)
        branches = db.fetch_record_by_condition(table_name, return_fields, conditions)

        branches = branches[0][0]
        branches = branches.split(', ')
        if branch in branches:
            return True
        return False

    @staticmethod
    def is_job_id_valid(job_id):
        table_name = tbn.JOB_POSTING
        return_fields = ('current_round',)
        conditions = dict(job_id=job_id)
        result = db.fetch_record_by_condition(table_name, return_fields, conditions)

        if not result:
            return False

        result = str(result[0][0])
        if result == 0:
            return True
        return False
