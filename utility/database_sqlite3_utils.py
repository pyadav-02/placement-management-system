from utility.database_sqlite3_utils_helper import execute_query


def fetch_record_by_condition(table_name: str,
                              return_fields: tuple,
                              conditions: dict) -> list[tuple]:
    return_fields_str = ', '.join(return_fields)
    conditions_str = get_condition_query_string(conditions)

    query = ('SELECT ' + return_fields_str
             + ' FROM ' + table_name
             + ' WHERE ' + conditions_str + ';')
    result = execute_query(query, return_data=True)
    return result


def get_condition_query_string(conditions: dict):
    conditions_list = []
    for condition, value in conditions.items():
        condition_string = str(condition) + ' = ' + "'" + str(value) + "'"
        conditions_list.append(condition_string)
    conditions_list.append('1 = 1')
    conditions_string = ' AND '.join(conditions_list)
    return conditions_string


def update_record_by_id(table_name: str,
                        id_field: str,
                        id_field_value: str,
                        updates: dict) -> None:
    updates_string = get_updates_query_string(updates)
    query = ('UPDATE ' + table_name
             + ' SET ' + updates_string
             + ' WHERE ' + id_field + ' = ' + "'" + id_field_value + "'" + ';')
    execute_query(query)


def get_updates_query_string(updates: dict):
    updates_list = []
    for update, value in updates.items():
        update_string = str(update) + ' = ' + "'" + str(value) + "'"
        updates_list.append(update_string)
    updates_string = ', '.join(updates_list)
    return updates_string


def delete_record_by_id(tabel_name: str,
                        id_field: str,
                        id_field_value: str,
                        conditions: dict) -> None:
    conditions_string = get_condition_query_string(conditions)
    query = ('DELETE FROM ' + tabel_name
             + ' WHERE ' + id_field + ' = ' + "'" + id_field_value + "'" + ' AND '
             + conditions_string + ';')
    execute_query(query)


def insert_record(table_name: str,
                  record: dict) -> None:
    columns_string, values_string = get_column_value_string(record)
    query = ('INSERT INTO ' + table_name + columns_string
             + ' VALUES' + values_string + ';')
    execute_query(query)


def get_column_value_string(record):
    columns = record.keys()
    columns_string = '(' + ', '.join(columns) + ')'

    values = record.values()
    values = ["'" + str(value) + "'" for value in values]
    values_string = '(' + ', '.join(values) + ')'

    columns_values_string = (columns_string, values_string)
    return columns_values_string
