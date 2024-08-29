import backend.table_names as tbn
from database_utility import database_sqlite3_utils as db


class JobFunctionality:
    @staticmethod
    def create_job_posting(company_name,
                           job_description,
                           ctc,
                           applicable_branches: str,
                           total_rounds_count,
                           application_close_date):
        table_name = tbn.JOB_POSTING
        record = dict(company_name=company_name,
                      job_description=job_description,
                      ctc=ctc,
                      applicable_branches=applicable_branches,
                      total_rounds_count=total_rounds_count,
                      current_round='0',
                      application_close_date=application_close_date,
                      applicants_id='0')
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

        id_field = 'job_id'
        records = dict(applicants_id=new_applicants_string)
        db.update_record_by_id(table_name, id_field, job_id, records)

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
        print(result)
        if not result:
            return False

        result = str(result[0][0])
        if result == '0':
            return True
        return False

    @staticmethod
    def job_next_round(job_id, new_students_id: tuple[str]):
        table_name = tbn.JOB_POSTING
        return_fields = ('total_rounds_count', 'current_round', 'applicants_id', 'company_name')
        conditions = dict(job_id=job_id)
        records = db.fetch_record_by_condition(table_name, return_fields, conditions)

        record = records[0]
        total_round_count = int(record[0])
        current_round = int(record[1])
        applicants_id = record[2]
        company_name = record[3]

        if current_round == total_round_count:
            JobFunctionality.set_students_job_status(company_name, new_students_id)

            id_field = 'job_id'
            id_field_value = job_id
            conditions = dict()
            db.delete_record_by_id(table_name, id_field, id_field_value, conditions)






        applicants_id = applicants_id.split(', ')

    @staticmethod
    def set_students_job_status(company_name, students_id: tuple):
        table_name = tbn.STUDENT_ACCOUNT
        updates = dict(company_name=company_name, placement_status='placed')

        conditions = dict()
        for student_id in students_id:
            conditions['student_id'] = student_id

        db.update_record_by_condition(table_name, updates, conditions)



