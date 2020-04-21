from ODBC.seed_sv import generate_csv
from ODBC.odbc import create_schemas, seed_tables

if __name__ == '__main__':
    db_user = ''
    db_pass = ''
    db_server = ''
    db_database = ''

    generate_csv()
    create_schemas(db_user, db_pass, db_server, db_database)
    seed_tables(db_user, db_pass, db_server, db_database)
