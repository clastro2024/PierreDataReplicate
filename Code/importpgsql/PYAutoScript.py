import psycopg2, csv
from configImport import SERVER, DATABASE, USERNAME, PASSWORD, table_names, export_name, export_path, file_dir, file_names, insert_print_per_rows, logs, commitPer, continueIfError, BatchInsertSize, filter_rows, ret_queries
from PYAutoScriptUtils import open_data_file, import_data, import_data2, export_csv, run_query, delete_tables, column_counter, remCols, batchRemCols, log
# Connect to the database
cnxn = psycopg2.connect(database=DATABASE, user=USERNAME, password=PASSWORD, host=SERVER)
print("Connected")

if len(table_names) != len(file_names):
    raise ValueError("The number of table names and file names should be the same.")

for table_name, file_name in zip(table_names, file_names):
    # Open the Data File and Unpack it
    data, headers = open_data_file(file_dir, file_name[0], file_name[1], continueIfError, filter_rows, 0)
    print(data)

    # Delete the existing table if it exists
    delete_tables(cnxn, [table_name])
    
    # Remove specified columns from all rows
    # data_new = batchRemCols(data, 20, 12)

    # Log the size of the original and modified data
    # log(["Size of Data: ", "Size of Data after BatchRemCols: "], [len(data), len(data_new)])

    # Insert the data into the table
    exeTime = import_data2(data[0], data[1:], table_name, cnxn, logs, insert_print_per_rows, BatchInsertSize)
    print("Time taken to insert: ", exeTime, " . Running Queries..")

    # Run SQL queries on the newly created table
    # run_query(cnxn, ret_queries(table_name))
    # log([f"TABLE {table_name} DONE! STARTING NEXT TABLE..."])

#export_csv(cnxn, table_name, export_name, export_path)


cnxn.close()


def lol():
    with open(r"D:\Sohan Sain\Programming\DataBase\DELTA_ShopifyPiesExport.txt", 'r', encoding='utf-8') as csvfile: # Open the CSV file in read mode
        csv_reader = csv.reader(csvfile, delimiter='|') # For text file
        headers = next(csv_reader) # Get the headers/column names from the first row of the CSV

        wrongRows = []
        for c in csv_reader:
            if len(c) < len(headers): 
                wrongRows.append(c)

    with open(r"ghoh.txt", 'w', encoding='utf-8') as hmmm:
        for row in wrongRows:
            hmmm.write("|".join(row) + "\n")

