import backend.table_names as tbn
from utility import database_sqlite3_utils as db
import uuid


class JobFunctionality:
    @staticmethod
    def create_job_posting(company_name,
                           duration,
                           ctc,
                           job_description,
                           total_round_count,
                           application_close_date,
                           applicable_branches):
        table_name = tbn.JOB_POSTING
        job_id = str(uuid.uuid1())
        record = dict(job_id=job_id,
                      company_name=company_name,
                      duration=duration,
                      ctc=ctc,
                      job_description=job_description,
                      total_round_count=total_round_count,
                      current_round=0,
                      application_close_date=application_close_date)
        db.insert_record(table_name, record)

        table_name = tbn.APPLICABLE_BRANCHES
        record = dict()
        for branch in applicable_branches:
            record[job_id] = branch
        db.insert_record(table_name, record)

    @staticmethod
    def get_job_postings():
        table_name = tbn.JOB_POSTING
        return_fields = ('company_name',
                         'duration',
                         'ctc',
                         'job_description',
                         'total_round_count',
                         'process_start_date')
        conditions = dict(current_round=0)
        result = db.fetch_record_by_condition(table_name, return_fields, conditions)
        return result

    @staticmethod
    def apply_job_application(student_id, job_id):
        requirement = JobFunctionality.is_applicable_for_job(student_id, job_id)
        if not requirement:
            return False

        table_name = tbn.JOB_APPLICATION
        records = dict(student_id=student_id, job_id=job_id, progress_round=0)

    @staticmethod
    def is_applicable_for_job(student_id, job_id):
        table_name = tbn.STUDENT_ACCOUNT
        return_fields = ('branch',)
        conditions = dict(student_id=student_id)
        student_branch = db.fetch_record_by_condition(table_name, return_fields, conditions)
        student_branch = student_branch[0]

        table_name = tbn.APPLICABLE_BRANCHES
        return_fields = ('branch',)
        conditions = dict(job_id=job_id)
        applicable_branches = db.fetch_record_by_condition(table_name, return_fields, conditions)

        if student_branch in applicable_branches:
            return True
        return False




