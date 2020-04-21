# CRM Data Generator

This Readme describes how to execute the Python code and upload the data to an Azure SQL Server.

### Tools Used
1. Python3 and Pip3 environment (Python 3.6.8 used here)
2. Local or Remote SQL Server that you have admin authority on
3. SQL Server Management Server 18 (used to upload the CSV to the Server)

### Getting Started
1. Clone the repo to your local machine
2. `cd` to the top level of the project

### Python Setup 
1. Create or activate a Python virtual environment if you plan to use one
2. Run `pip install -r requirements.txt` to install the pip packages required by the project
3. Make sure the `output` directory exists at the top level. If not, create it with `mkdir output`

### Generate the Data
1. Double check `./config/config.py` and `./config/ml_model.py` to confirm the data generation parameters
    - in `config.py`, the seccess rate determines how many opportunities from the list advance to the next stage
    - in `config.py`, the start/end dates determines the random range that the opportunities will pick a start date from
    - in `config.py`, the delta tuples determine how many days pass between stages
2. Double check the `./parter_list.py` file to add/remove/edit the list of partners
3. WARNING: Running the program will overwrite the existing CSV files. Back them up if you need them
4. From the root project level, run `python run.py` to generate the CSVs. These files will be in the `./output/` directory

### Setup SQL Server for Import
The following will create DB User Reader who can only read from the DB. 
1. Open a query tab in SSMS and login with an admin account
2. Open the `./user_init.sql` file in a text editor and change:
    - the password string to a memorable password. Strong passwords are enforced by the server, so make sure it contains a letter, number, and symbol or the query will fail
    - if you don't want to call the databases "Leads", change both instances of the name to desired value
3. Copy/paste the entire query text into the SSMS query editor
4. In the upper left side of the window on last row of of the toolbar is the database dropdown. Select `master` from this dropdown
5. Click the execute button in the toolbar to run the query
6. In the database dropdown from step 4, now select the new 'Leads' database
7. Comment out or delete the lines in the query window that were just run, then uncomment the last line. Click execute to run that line
8. Back in the object explorer, right click on the 'Leads' object and click Properties
9. On the left hand pane, select the permissions page. You should see the 'Contrib' user in the Users and Roles list
10. In the permission list at the bottom, scroll way down to the SELECT permission and check the GRANT box. Click OK

### Import the CSVs into SQL Server
1. Launch SQL Server Management Studio
2. Open the Object Explorer if it is not present (View -> Object Explorer)
3. Click 'Connect' at the top of the Object Explorer, to a Database Engine
4. Type in the login details for the ADMIN account. The Reader cannot create tables
5. When connected, expand the 'Databases' in the explorer and find the 'Leads' object (or whatever you called your database instead of leads)
    - Right-click on the 'Leads' object and click 'Tasks -> Import Flat File'. 
    - In 'Specify Input File', click Browse, and find the CSV output folder from the project
    - In 'New Table Name', specify what to call the Table. (Accounts for accounts.csv for example) then click Next
    - Click Next on 'Preview Data'
    - In 'Modify Columns', change the data type dropdown of columns that are clearly numbers from `nvarchar` to `int`
    - If one of the numerical columns is a Primary Key, go ahead and check the relevant 'Primary Key` box
    - Click Next, and Next one last time to begin the import
    - If successful, click the refresh icon at the top of the object explorer to refresh the list. Expand the 'Leads' object, then the 'Tables' group and you should see the table you just created
    - Right-click on the new Table and click "Select top 1000 rows..." to query the table. If you see all the data pop up, the import was successful
    - Repeat these bullets again with the next CSV file until all files are imported
    
    
### Setup Azure ML
In order for a Jupyter Notebook to get SQL Server data, it needs the ODBC drivers.
See the [Microsoft Docs](https://docs.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server?view=sql-server-ver15) for more.

1. Start or create an Azure ML Compute instance
2. When the instance is running, click JupyterLab, and open a Terminal
3. With the provided `./get-drivers.sh` file, copy/paste the entire contents into terminal or run each line one by one
    - Note: DO NOT elevate to root with `sudo su` when running these commands
4. Optional: After all the commands run, stop and restart your VM


