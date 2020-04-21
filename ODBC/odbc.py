import pyodbc
import csv
from config import sql_config


def create_schemas(username, password, server, database):
    driver = sql_config.driver
    try:
        conx = pyodbc.connect(
            "DRIVER=" + driver + ";SERVER=" + server + ";UID=" + username + ";PWD=" + password + ";DATABASE=" + database)
        try:
            cursor = conx.cursor()
            conx.autocommit = False
            cursor.execute("CREATE TABLE Accounts(" +
                           "acc_id INT IDENTITY(1, 1) NOT NULL, " +
                           "name NVARCHAR(50) NOT NULL, " +
                           "size NVARCHAR(20) NOT NULL, " +
                           "location INT NOT NULL, " +
                           "PRIMARY KEY(acc_id)" +
                           ");"
                           )
            print("Accounts created")

            cursor.execute("CREATE TABLE Facts(" +
                           "fact_id INT IDENTITY(1, 1) NOT NULL, " +
                           "pid INT NOT NULL, " +
                           "acc_id INT NOT NULL, " +
                           "opp_id INT NOT NULL, " +
                           "stage_id INT NOT NULL, " +
                           "timestamp datetime2 NOT NULL, " +
                           "PRIMARY KEY(fact_id)" +
                           ");"
                           )
            print("Facts created")

            cursor.execute("CREATE TABLE Opportunities(" +
                           "opp_id INT IDENTITY(1, 1) NOT NULL, " +
                           "pid INT NOT NULL, " +
                           "acc_id INT NOT NULL, " +
                           "opp_size FLOAT NOT NULL, " +
                           "PRIMARY KEY(opp_id)" +
                           ");"
                           )
            print("Opportunities created")

            cursor.execute("CREATE TABLE Partners(" +
                           "pid INT IDENTITY(1, 1) NOT NULL, " +
                           "p1_devs INT NOT NULL, " +
                           "p2_devs INT NOT NULL, " +
                           "alignment FLOAT NOT NULL, " +
                           "partner_driven BIT NOT NULL, " +
                           "name NVARCHAR(255) NOT NULL, " +
                           "size NVARCHAR(50) NOT NULL, " +
                           "location INT NOT NULL, " +
                           "PRIMARY KEY(pid)" +
                           ");"
                           )
            print("Partners created")

            cursor.execute("CREATE TABLE Regions(" +
                           "region_id INT IDENTITY(1, 1) NOT NULL, " +
                           "region NVARCHAR(50) NOT NULL, " +
                           "PRIMARY KEY(region_id)" +
                           ");"
                           )
            print("Regions created")

            cursor.execute("CREATE TABLE Sales_Stages(" +
                           "stage_id INT IDENTITY(1, 1) NOT NULL, " +
                           "sales_stage NVARCHAR(50) NOT NULL, " +
                           "PRIMARY KEY(stage_id)" +
                           ");"
                           )
            print("Sales Stages created")

        except pyodbc.DatabaseError as err:
            print(err)
            conx.rollback()
        else:
            conx.commit()
        finally:
            conx.autocommit = True

    except ConnectionError as e:
        raise ConnectionError(e)


def seed_tables(username, password, server, database):
    driver = sql_config.driver
    try:
        conx = pyodbc.connect(
            "DRIVER=" + driver + ";SERVER=" + server + ";UID=" + username + ";PWD=" + password + ";DATABASE=" + database)

        try:
            cursor = conx.cursor()
            conx.autocommit = False
            with open('./output/accounts.csv', newline='') as f:
                contents = []
                reader = csv.DictReader(f)
                for row in reader:
                    contents.append((row['name'], row['size'], row['location']))
                cursor.executemany("INSERT INTO Accounts(name, size, location) VALUES (?, ?, ?)", contents)
                print("Seeded Accounts")
                f.close()

            with open('./output/facts.csv', newline='') as f:
                contents = []
                reader = csv.DictReader(f)
                for row in reader:
                    contents.append((row['pid'], row['acc_id'], row['opp_id'], row['stage_id'], row['timestamp']))
                cursor.executemany("INSERT INTO Facts(pid, acc_id, opp_id, stage_id, timestamp) VALUES (?, ?, ?, ?, ?)", contents)
                print("Seeded Facts")
                f.close()

            with open('./output/opportunities.csv', newline='') as f:
                contents = []
                reader = csv.DictReader(f)
                for row in reader:
                    contents.append((row['pid'], row['acc_id'], row['opp_size']))
                cursor.executemany("INSERT INTO Opportunities(pid, acc_id, opp_size) VALUES (?, ?, ?)", contents)
                print("Seeded Opportunities")
                f.close()

            with open('./output/partners.csv', newline='') as f:
                contents = []
                reader = csv.DictReader(f)
                for row in reader:
                    contents.append((row['name'], row['size'], row['location'], row['p1_devs'], row['p2_devs'], row['alignment'], row['partner_driven']))
                cursor.executemany("INSERT INTO Partners(name, size, location, p1_devs, p2_devs, alignment, partner_driven) VALUES (?, ?, ?, ?, ?, ?, ?)", contents)
                print("Seeded Partners")
                f.close()

            with open('./output/regions.csv', newline='') as f:
                contents = []
                reader = csv.DictReader(f)
                for row in reader:
                    contents.append((row['region'],))
                cursor.executemany("INSERT INTO Regions(region) VALUES (?)", contents)
                print("Seeded Regions")
                f.close()

            with open('./output/stages.csv', newline='') as f:
                contents = []
                reader = csv.DictReader(f)
                for row in reader:
                    contents.append((row['sales_stage'],))
                cursor.executemany("INSERT INTO Sales_Stages(sales_stage) VALUES (?)", contents)
                print("Seeded Sales Stages")
                f.close()
        except pyodbc.DatabaseError as err:
            print(err)
            conx.rollback()
        else:
            conx.commit()
        finally:
            conx.autocommit = True

    except ConnectionError as e:
        raise ConnectionError(e)
