import backend.table_names as tbn
from utility import database_sqlite3_utils as db
# import uuid


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
                      application_close_date=application_close_date)
        db.insert_record(table_name, record)

    @staticmethod
    def get_job_postings():
        table_name = tbn.JOB_POSTING
        return_fields = ('job_id', 'company_name', 'job_description', 'ctc', 'applicable_branches',
                         'total_rounds_count', 'current_round', 'application_close_date')
        conditions = dict()
        result = db.fetch_record_by_condition(table_name, return_fields, conditions)
        return result







