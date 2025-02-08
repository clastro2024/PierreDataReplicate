import os

# Database Connection Credentials
# SERVER = 'ec2-35-182-148-237.ca-central-1.compute.amazonaws.com'
# DATABASE = 'Shopify_Image_Prep'
# USERNAME = 'Sukhendu'
# PASSWORD = 's734dSfhn*ndu'
# connectionString = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD};TrustServerCertificate=yes'

SERVER = 'localhost'
DATABASE = 'Odoo Test'
USERNAME = 'postgres'
PASSWORD = 'postgres'
#connectionString = f"host='{SERVER}' dbname='{DATABASE}' user='{USERNAME}'"
connectionString = "host=localhost port=5432 dbname='Odoo Test' user=postgres sslmode=prefer connect_timeout=10"

# Naming
file_dir = r"D:\Sohan Sain\Programming\Project&Jobs\PierreDataCreate\allCsv"
importAllInDir = True
ImportExtensions = ['.csv'] # If importAllInDir == True
ImportDelim = ',' # if importAllInDir == True
if importAllInDir:
    file_names = [[f, ImportDelim] for f in os.listdir(file_dir) if f.endswith(tuple(ImportExtensions))]
else:
    file_names = [
        ["Ledgers in Default Template.xlsx", '|'], 
    ]  # If importAllInDir == false


table_names = [
    fn[0].split('.')[0] for fn in file_names
]

export_path = "exports"
export_name = 'TableName.csv'

insert_print_per_rows = 50
logs = True
commitPer = 20
continueIfError = True
BatchInsertSize = 9999
filter_rows = False

# Queries
def ret_queries(table_name):
    return [
    "USE Testing",
    f"UPDATE  [dbo].[{table_name}] SET [Additional Image] = NULL Where  [Additional Image]  like '%Prop65%.jpg'",
    f"UPDATE  [dbo].[{table_name}] SET [Additional Image] = NULL Where  [Additional Image]  like '%Prop65%.tif'",
    f"UPDATE  [dbo].[{table_name}] SET [Additional Image] = NULL Where  [Additional Image]  like '%Warning%.jpg'",
    f"UPDATE  [dbo].[{table_name}] SET [Additional Image] = NULL Where  [Additional Image]  like '%Warning%.tif'"
    ]
