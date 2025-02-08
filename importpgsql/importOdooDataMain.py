import psycopg2
import math
import os
import csv; csv.field_size_limit(10000000)


def connect(dbName, dbUser, passw, host):
    cnxn = psycopg2.connect(database=dbName, user=dbUser, password=passw, host=host)
    return cnxn

def read_csv(filePath):
    if os.path.getsize(filePath) == 0: return []
    with open(filePath, 'r', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)  # Skip header row
        fData = []
        for i, row in enumerate(csvreader):
            row = str(row)
            #if type(row) == str:
            #if i < 2: print(row)
            row = row.replace('\'\'', 'NULL').replace('[', '').replace(']', '')#.replace('{', '\'{').replace('}', '}\'')
            #if i < 2: print(row)
            row = row.split(',')
            fData.append(list(row))

        return fData
    
def getCreateQuery(filePath):
    with open(filePath, 'r') as defFile:
        defin = defFile.read()
        mainTable = "|".join(defin.split('|')[:-1]).split('-')[-1].strip().replace('  ', '')
        #for lol in mainTable.strip().replace(' ', '').split('\n'): print(lol)
        createQuery = f"CREATE TABLE {filePath.split('/')[-1].split('.')[0]} ({"".join([f"{col.split('|')[0].strip()} {col.split('|')[1]}," for col in mainTable.split('\n')]).strip(',')});"
        #print("filepath: ", filePath)
        #print("create query: ", createQuery)
        return createQuery
    
def checkTableExistance(cnxn, tableName):
    try:
        cursor = cnxn.cursor()
        cursor.execute(f"""
                SELECT EXISTS (
                    SELECT 1 
                    FROM information_schema.tables 
                    WHERE table_name = '{tableName}' AND table_schema = 'public'
                );
            """)
        # print(f"""
        #         SELECT EXISTS (
        #             SELECT 1 
        #             FROM information_schema.tables 
        #             WHERE table_name = '{tableName}' AND table_schema = 'public'
        #         );
        #     """)
        result = cursor.fetchone()
        return result
    except Exception as e:
        print(f"An error occurred while checking table existence: {str(e)}")
        return False
    

def importData(cnxn, data, tableName, biSize):
    cursor = cnxn.cursor()

    il = 0
    for _ in range(math.ceil(len(data)/biSize)):
        #values = []
        insert_query = f"INSERT INTO {tableName} VALUES {",".join([f"({",".join(row).strip(',')})" for row in data[biSize*il:biSize*(il+1)]]).strip(',')};"
        # for row in data[biSize*il:biSize*(il+1)]: 
        #     fRow = []
        #     for col in row:
        #         #print(col, type(col))
        #         if col != None: fRow.append("'" + str(col.replace("'", "")) + "'"); continue
        #         fRow.append('NULL')
        #     values.append('(' + ', '.join(fRow) + ')')
        # insert_query = f"INSERT INTO {table_name} VALUES " +  (", ".join(values)) + ";"
        cursor.execute(insert_query)
        il+=1

    cnxn.commit()  # Commit the transaction after inserting data





    

def main():
    with connect("Odoo Test", "postgres", "postgres", "localhost") as cnxn:
        with cnxn.cursor() as cursor:
            i = 0
            for fileName in os.listdir(r"D:\Sohan Sain\Programming\Project&Jobs\PierreDataCreate\allCsv"):
                #if i == 1: break
                i += 1
                #fData = read_csv(f'allCsv/{fileName}')
                print(fileName)
                #print(f'allTxt/{fileName.split('.')[0]}.txt')
                try:
                    cursor.execute(f"DROP TABLE IF EXISTS {fileName.split('.')[0]};")
                    #with open('hmm.txt', 'a') as query:
                    #    query.write(getCreateQuery(f'allTxt/{fileName.split('.')[0]}.txt')+'\n')
                    cursor.execute(getCreateQuery(f'allTxt/{fileName.split('.')[0]}.txt'))
                    #cursor.
                    #importData(cnxn, fData, fileName.split('.')[0], 1000)
                    #print(checkTableExistance(cnxn, fileName.split('.')[0]))
                    #if checkTableExistance(cnxn, fileName.split('.')[0]):
                    os.remove(f'allCsv/{fileName}')
                    cnxn.commit()
                        
                except Exception as e:
                    print(f'Error Inserting Data for {fileName.split('.')[0]}: {e}')
                    cnxn.rollback()
                
            #cnxn.commit()



main()