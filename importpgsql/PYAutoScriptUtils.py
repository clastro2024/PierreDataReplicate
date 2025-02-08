import csv
import time
import os
import sys
import math
import pandas as pd
import numpy as np
# sys.tracebacklimit = 0

def open_data_file(filepath, filename=None, delim=',', continueIfError=True, filter=True, sheet_name=0):
    """
    Open and extract data from a CSV, TXT or Excel file.

    Args:
        filepath (str): Path to the directory containing the CSV file.
        filename (str, optional): Name of the CSV file. Defaults to None.
        delim (str, optional): Delimiter character for the CSV file. Defaults to ','.
        continueIfError (bool, optional): Whether to continue processing if errors occur. Defaults to True.
        sheet_name (str | int, optional): Name or Index of Sheet of Excel File to Import. Only if the File is Excel. Defaults to 0

    Returns:
        data, array: Array of Data Extracted from the CSV file.
        unique_headers, array: Array of Unique Headers/Columns.
    """
    if (filename.split('.')[-1] == 'csv') or (filename.split('.')[-1] == 'CSV') or (filename.split('.')[-1] == 'txt') or (filename.split('.')[-1] == 'TXT'): data, unique_headers = _open_csv_or_txt(filepath, filename, delim, continueIfError, filter)
    if (filename.split('.')[-1] == 'xlsx') or (filename.split('.')[-1] == 'XLSX'): data, unique_headers = _open_excel(filepath, filename, sheet_name)
    return data, unique_headers  

def import_data(headers, data, table_name, cnxn, logs=True, insprintper=5, commitPer=0):
    """
    Import data from a CSV file into a SQL Server database table.

    Args:
        headers (list): Column headers for the table.
        data (list): List of rows to insert into the table.
        table_name (str): Name of the target table in the database.
        cnxn (pyodbc connection object): Connection to the SQL Server database.
        logs (bool, optional): Whether to log progress. Defaults to True.
        insprintper (int, optional): Interval for printing progress. Defaults to 5.
        commitPer (int, optional): Interval for committing transactions. Defaults to 0.

    Returns:
        exeTime, float: Execution time of the import operation.
    """
    exeTime = _import_data(headers, data, table_name, cnxn, logs, insprintper, commitPer)
    return exeTime

def import_data2(headers, data, table_name, cnxn, logs=True, insprintper=5, biSize=5):
    """
    Alternative method to import data from a CSV file into a SQL Server database table.

    Args:
        headers (list): Column headers for the table.
        data (list): List of rows to insert into the table.
        table_name (str): Name of the target table in the database.
        cnxn (pyodbc connection object): Connection to the SQL Server database.
        logs (bool, optional): Whether to log progress. Defaults to True.

    Returns:
        None
    """
    exeTime = _import_data2(headers, data, table_name, cnxn, logs, insprintper, biSize)

    return exeTime

def export_csv(cnxn, export_table_name, export_name, export_path):
    """
    Export data from a SQL Server table to a CSV file.

    Args:
        cnxn (pyodbc connection object): Connection to the SQL Server database.
        export_table_name (str): Name of the table to export from.
        export_name (str): Name of the CSV file to save the exported data.
        export_path (str): Path where the CSV file will be saved.

    Returns:
        None
    """
    _export_csv(cnxn, export_table_name, export_name, export_path)

def run_query(cnxn, queries, run_all=False, detailed=True, printRowCount=10):
    """
    Execute an array of SQL queries against the database.

    Args:
        cnxn (pyodbc connection object): Connection to the SQL Server database.
        queries (list): List of SQL queries to execute.
        run_all (bool, optional): Whether to run all queries. Defaults to True.
        detailed (bool, optional): Whether to print detailed execution information. Defaults to True.

    Returns:
        None
    """
    _run_query(cnxn, queries, run_all, detailed, printRowCount)

def delete_tables(cnxn, table_names, logs=False):
    """
    Delete multiple tables from the SQL Server database.

    Args:
        cnxn (pyodbc connection object): Connection to the SQL Server database.
        table_names (list): List of table names to delete.
        logs (bool, optional): Whether to log deletion operations. Defaults to False.

    Returns:
        None
    """
    _delete_tables(cnxn, table_names, logs)

def column_counter(headers, data, filePath=None, writeFile=False):
    """
    Count columns in each row of CSV data and save the results to a file.

    Args:
        headers (list): Column headers for the CSV data.
        data (list): List of rows containing the actual data.
        filePath (str): Path where the output CSV file will be saved.

    Returns:
        None
    """
    cC = _column_counter(headers, data, filePath, writeFile)
    return cC

def remCols(row, col1, col2): 
    """
    Remove columns from a row based on indices.

    Args:
        row (list): Input row.
        col1 (int): Starting index of columns to remove.
        col2 (int): Ending index of columns to remove.

    Returns:
        list: Modified row with specified columns removed.
    """
    final_row = _remCols(row, col1, col2)
    return final_row

def batchRemCols(rows, col1, col2):
    """
    Remove specified columns from multiple rows and save the results to a CSV file.

    Args:
        rows (list): List of input rows.
        col1 (int): Starting index of columns to remove.
        col2 (int): Ending index of columns to remove.
        filepath (str): Path where the output CSV file will be saved.
        filename (str, optional): Name of the output CSV file. Defaults to 'BatchRemCols.csv'.
        delim (str, optional): Delimiter character for the output CSV file. Defaults to ','.

    Returns:
        list: Modified rows with specified columns removed.
    """
    final_rows = _batchRemCols(rows, col1, col2)
    return final_rows

def log(print_statements, print_data=[]):
    """
        Log each of Print statements and print data together.

        Args: 
            print_statements (array): Array of Print Statments, each would be with the corresponding print_data value
            print_data (array): Array of Print data, each would be with the corresponding print_statements value

        Returns:
            None
    """
    _log(print_statements, print_data)


### FUNCTIONS INIT ----------------------------------------------------------------


# Open and extract data of a CSV
def _open_csv_or_txt(filepath, filename=None, delim=',', continueIfError=True, filter=True):   
    data = []
    if os.path.getsize(os.path.join(filepath, filename)) == 0: return [], []
    with open(os.path.join(filepath, filename), 'r', encoding='utf-8') as csvfile: # Open the CSV file in read mode
        csv_reader = csv.reader(csvfile, delimiter=delim) # For text file
        headers = next(csv_reader) # Get the headers/column names from the first row of the CSV

        # Identify unique columns
        unique_headers = list(dict.fromkeys(headers))  # Removes duplicates by converting to dict and back to list
        unique_indices = [headers.index(header) for header in unique_headers] # Determine indices of unique columns
                
        # headers = unique_headers # Filter out duplicate columns from headers
        data.append(unique_headers)  # Store headers if needed later

        for n, row in enumerate(csv_reader): # Iterate through the remaining rows in the CSV file and Filter out duplicate columns from data rows
            if not filter: data.append(str(row)); continue
            if len(headers) > len(row): 
                if continueIfError: 
                    print("WARNING: Data Row " + str(n+1) + " has " + str(len(headers)-len(row)) + " less columns " + str(len(row)) + " than Header (" + str(len(headers)) + "columns). Ignoring Row and Continuing...") 
                    continue
                else: 
                    raise Exception("EXCEPTION: Data Row " + str(n+1) + " has " + str(len(headers)-len(row)) + " less columns " + str(len(row)) + " than Header (" + str(len(headers)) + "columns). Closing Program...") 
            try: 
                filtered_row = [row[index] for index in unique_indices]
            except: 
                if continueIfError: 
                    print("EXCEPTION: Occured in the data row: " + str(n+1) + " (file row of " + str(n+2) + ")(Possibly not enough Columns). Ignoring and Continuing...")
                    continue
                else: 
                    raise Exception("EXCEPTION: Occured in the data row: " + str(n+1) + " (file row of " + str(n+2) + ")(Possibly not enough Columns). Closing Program...") from None 

            data.append(filtered_row)

        for row in data[1:]:
            # Check each value in the row and replace empty strings with None. It Inserts NULL in DataBase.
            #row = list(row)
            for i, val in enumerate(row):
                if not val.strip():
                    row[i] = None    

        return data, unique_headers  

def _open_excel(filepath, filename=None, sheet_name=0):
    excel_file_path = os.path.join(filepath, filename)

    # Read Excel file using pandas
    df = pd.read_excel(excel_file_path, sheet_name=sheet_name)

    # Extract unique column names
    unique_headers = df.columns.tolist()

    # Convert the DataFrame to a numpy array and add the headers
    data = df.to_numpy(na_value=None)
    data = np.vstack((unique_headers, data))

    for r, row in enumerate(data):
        for c, col in enumerate(row):
            data[r, c] = str(col) if col != None else None

    return data, unique_headers

# Import a CSV into a Table
def _import_data(headers, data, table_name, cnxn, logs=True, insprintper=5, commitPer=0):
    cursor = cnxn.cursor()

    create_table_query = f"CREATE TABLE {table_name} ({', '.join([f'[{header}] NVARCHAR(MAX)' for header in headers])})" 

    start = time.time()
    try: 
        cursor.execute(create_table_query) # Execute the query to create the table
    except Exception as e:
            raise Exception("EXCEPTION: Error creating table. Error: " + str(e) + " Create Query: " + create_table_query[:75] + "...") from None
    cnxn.commit()  # Commit the transaction to finalize the table creation

    if logs: print("Table created successfully.")

    # Insert data into the newly created table
    sTime = time.time()
    for n, row in enumerate(data[1:]):  # Skip the headers when inserting data
        insert_query = f"INSERT INTO {table_name} VALUES ({', '.join(['?' for _ in row])})"
        
        try: cursor.execute(insert_query, row)
        except: raise Exception("Error occured while inserting filtered data Row: " + str(n+1), "Row Data: ", row) from None

        if n%insprintper == 0 & logs: 
            print(f"Row {n} inserted; {(n/(len(data)-1))*100}%, Time: {time.time()-sTime}") 
            sTime = time.time()
        if commitPer and n%commitPer == 0: cnxn.commit()  # Commit the transaction after a certain number of rows

    cnxn.commit()  # Commit the transaction after inserting data
    if logs: print("Data Inserted successfully")

    end = time.time()
    exeTime = end - start

    return exeTime

# Import a CSV into a Table in a Alternative Method
def _import_data2(headers, data, table_name, cnxn, logs=True, insprintper=5, biSize=10):
    start = time.time()

    cursor = cnxn.cursor()

    create_table_query = f"CREATE TABLE {table_name} ({', '.join([f'{header} TEXT' for header in headers])});" 

    start = time.time()
    try: 
        cursor.execute(create_table_query) # Execute the query to create the table
    except Exception as e:
            raise Exception("EXCEPTION: Error creating table. Error: " + str(e) + " Create Query: " + create_table_query[:75] + "...") from None
    cnxn.commit()  # Commit the transaction to finalize the table creation

    if logs: print("Table created successfully:", table_name)

    il = 0
    lastPrintIndex = 0

    for _ in range(math.ceil(len(data)/biSize)):
        values = []
        batchTimeStart = time.time()
        for row in data[biSize*il:biSize*(il+1)]: 
            # row = row.replace(',,', ', ,').replace('\'', '').replace('[', '').replace(']', '').replace('{', '')
            # row = row.split(',')
            fRow = []
            for col in row:
                #print(col, type(col))
                if col != None: fRow.append("'" + str(col.replace("'", "")) + "'"); continue
                fRow.append('NULL')
            values.append('(' + ', '.join(fRow) + ')')
        insert_query = f"INSERT INTO {table_name} VALUES " +  (", ".join(values)) + ";"

        try: cursor.execute(insert_query)
        except Exception as e: 
            with open(r"hmm.txt", "w", encoding='utf-16') as hmmm: 
                hmmm.write(insert_query)
            raise Exception("Error occured while inserting", e, " query: ", insert_query[:100]) from None

        if ((biSize*(il+1)-lastPrintIndex) > insprintper) & (logs==True): print(f"Row {min(len(data), biSize*(il+1))} inserted; {min((biSize*(il+1)/(len(data)-1))*100, 100)}%, Total Time: {time.time()-start}, Batch Time: {time.time()-batchTimeStart}"); lastPrintIndex = biSize*(il+1)
        il+=1

    cnxn.commit()  # Commit the transaction after inserting data
    if logs: print("Data Inserted successfully")

    end = time.time()
    exeTime = end - start

    return exeTime

### Run Arrays of queries
def _run_query(cnxn, queries, run_all=False, detailed=True, printRowCount=1):
    cursor = cnxn.cursor()
    
    for n, q in enumerate(queries):
        if detailed and not run_all: 
            inp = input(f"Run Query: {q}? Y/n: ")
            while inp.lower() not in ['y', 'yes']:
                print('Not recognized character. Please enter Y or N.')
                inp = input(f"Run Query: {q}? Y/n: ")
            if inp.lower() in ['n', 'no']:
                continue
        
        cursor.execute(q)
        
        if 'Select' in q or 'Update' in q:
            result = cursor.fetchall()
            print(f"Query executed. Result length: {len(result)},,  {printRowCount}")
            if detailed:
                print(f"Query {n+1} executed, Rows affected: {cursor.rowcount}")
                
                if result:
                    print(f"First {printRowCount} Rows:")
                    for row in result[:printRowCount]:
                        print(row)
                else:
                    print("No rows returned.")
        else:
            if detailed:
                print(f"Query {n+1} executed, Rows affected: {cursor.rowcount}")

        cursor.commit()
        print("\nExecuting Next Query...\n")
    
    
# Export Data from Table in a CSV
def _export_csv(cnxn, export_table_name, export_name, export_path):
    cursor = cnxn.cursor()
    cursor.execute(f"SELECT * FROM {export_table_name}")
    
    col_names = [column[0] for column in cursor.description] # Fetch the column names
        
    rows = cursor.fetchall() # Fetch all rows from the last executed statement
    
    # Write the data to a CSV file
    with open(os.path.join(export_path, export_name), 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(col_names)  # Write the column names as the first row
        writer.writerows(rows)  # Write the rows
    
    print(f"Data exported successfully to '{os.path.join(export_path, export_name)}'")

### Delete a Array of Table
def _delete_tables(cnxn, table_names, logs=False):
    for table in table_names:   
        print(f"DROP TABLE IF EXISTS {table};")
        cnxn.cursor().execute(f"DROP TABLE IF EXISTS {table};")
        if logs: print(f"Table '{table}' deleted successfully.")

#Count Number of Columns each Row
def _column_counter(headers, data, filePath, writeFile=False):
    len_headers = len(headers)
    column_count = []
    for n, row in enumerate(data):
        column_count.append([n+1, len(row), len(row)-len_headers])
    if writeFile:  # Write the column count to a CSV file
        with open(filePath, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["File Row Num (include headers)", "Row Columns", "Row Offset"])  # Write the column names as the first row
            writer.writerows(column_count)  # Write the rows
        return
    return column_count

def _remCols(row, col1, col2): 
    final_row = row[:col1] + row[-col2:]
    return final_row

def _batchRemCols(rows, col1, col2):
    final_rows = []
    for n, row in enumerate(rows):
        if (len(row) < col1+col2): print("Row ", n, "has ", len(row), " columns. Ignoring and Continuing..."); continue
        #if (len(row) > 2000): continue
        final_row = _remCols(row, col1, col2)
        final_rows.append(final_row)

    return final_rows

def _log(print_statement, print_data):
    for ps, pd in zip(print_statement, print_data):
        print(ps, pd)