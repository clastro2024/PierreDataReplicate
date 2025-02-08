
#^###############################  mainPOC.py  ####################################
# ^ Author: Sukhendu Sain
# ^ Description: Main Code File
# ^ Data: 30-Jan-2025
#^###############################################################################
from config import *
from itertools import islice
import utils, os, time, xmlrpc.client, threading, csv



#try:
uid = utils.authenticateOdoo(ODOO_URL, DB_NAME, USERNAME, API_SECRET)
print("Successfully authenticated!")

models = xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/object")

bucket = utils.authenticateB2(ACCOUNT_ID, APPLICATION_KEY, bucket_name)
# bucket.upload_bytes(bucket


with open('accessModels.csv') as modelsList:
    file = modelsList.readlines()
    for j in range(47):
        # print(j, file[(9*j)+1:(9*(j+1))+1])
        thread = threading.Thread(target=utils.replicateModels, args=(bucket, file[(3*j)+1:(3*(j+1))+1], DB_NAME, API_SECRET, ODOO_URL, USERNAME))
        thread.daemon = True
        thread.start()


while True:
    time.sleep(1)

# with open('stdout.txt') as stdout:
#     i = 0
#     for line in stdout.readlines():
#         #print(line)
#         if ("All Models" in line):
#             i += 1
# print(i)
# def get_all_tables(models):
#     return models.execute_kw(DB_NAME, uid, API_SECRET, 'ir.model', 'search_read', [
#         [('model', '!=', 'ir.model')],  # Exclude the 'ir.model' table itself
#         {'fields': ['model']}
#     ], {'order_by': 'model'})

# try:
#     # 1. Connect to Odoo
#     common = xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/common")
#     uid = common.authenticate(DB_NAME, USERNAME, API_SECRET, {})

#     if uid:
#         print("Successfully authenticated!")

#         # 2. Access Odoo Objects (Example: Get a list of partners)
#         models = xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/object")
#         print("Done 0")
#         # Modify this line
#         result = models.execute_kw(DB_NAME, uid, API_SECRET, 'ir.attachment', 'search', [[]])
#         print("Done 1")

#         # Check if the result is a dictionary
#         if isinstance(result, dict):
#             attQ = result.get('result', [])
#         elif isinstance(result, list):
#             attQ = result
#         else:
#             raise ValueError(f"Unexpected result type: {type(result)}")

#         model_ids = models.execute_kw(DB_NAME, uid, API_SECRET, 'ir.model', 'search', [[]])
#         models_data = models.execute_kw(DB_NAME, uid, API_SECRET, 'ir.model', 'read', [model_ids], {'fields': ['name', 'model']})
#         #print(model_ids)
#         #print(models_data)      
#         print("Done 2")    
#     else:
#         print("Authentication failed.")

# except Exception as e:
#     print(f"An error occurred: {e}")


# def check_accessibility(models):
#     accessible_tables = []
#     inaccessible_tables = []

#     for i, table in enumerate(models_data, start=1):
#         print(i)
#         model = table['model']
#         # if i == 20:  
#         #     break
#         try:
#             # Attempt to read a record from the model
#             result = models.execute_kw(DB_NAME, uid, API_SECRET, model, 'read', [1], {'fields': ['name']})
#             if result:
#                 accessible_tables.append(list(table.values()))
# #                print(f"{i}. Table OK: {model}")
#             else:
#                 inaccessible_tables.append(model)
# #                print(f"{i}. NOT Accessible: {model}")
#         except Exception as e:
#             inaccessible_tables.append(model)
#             #print(f"{i}. EXCEPTION: accessing {model}: {str(e)}")

#     return accessible_tables, inaccessible_tables

# accessible, inaccessible = check_accessibility(models)
# #print(models_data)
# #print(accessible)
# print(len(accessible))

# #utils.writeCSV(accessible, "id, name, model", 'accessModels.csv')
# with open('accessModels.csv', 'w', newline='', encoding='utf-8') as csvfile:
#             writer = csv.writer(csvfile)
#             writer.writerow("id, name, model")
#             for d in accessible:
#                 writer.writerow(d)


#modelList = utils.fetchOdooModel('ir.model', models, uid, DB_NAME, API_SECRET, ['name', 'model'])  
# utils.writeCSV(modelList, modelList[0].keys(), 'models.csv')


# acctList = utils.fetchOdooModel('account.account', models, uid, DB_NAME, API_SECRET)   
# utils.writeCSV(acctList, acctList[0].keys(), 'accounts.csv')

# rows = []
# j = 0
# with open('models.csv') as modelsList:
#     for lines in modelsList.readlines():
#         print(lines.split(",")[2].split("\n")[0])
#         if j > 50: break
#         try: modList = utils.fetchOdooModel(lines.split(",")[2].split("\n")[0], models, uid, DB_NAME, API_SECRET) 
#         except Exception as e: continue
#         if len(modList) == 0: continue  
#         rows.append([lines.split(",")[0], lines.split(",")[1], lines.split(",")[2].split("\n")[0]])
#         j = j + 1

# utils.writeCSV(rows, "id, name, model", "filteredModels.csv")


# while True:
#     start = time.time()
#     i = i + 1

#     filePaths = []
#     with open('filteredModels.csv') as modelsList:
#         for lines in modelsList.readlines()[1:tN+1]:
#             print(lines.split(",")[2].split("\n")[0], i)
#             try: modList = utils.fetchOdooModel(lines.split(",")[2].split("\n")[0], models, uid, DB_NAME, API_SECRET) 
#             except Exception as e: print(f"Error Fetching Model {lines.split(",")[2].split("\n")[0]} for {i} iteration: {e}"); continue
#             if len(modList) == 0: continue  
#             utils.writeCSV(modList, modList[0].keys(), f'files\{lines.split(",")[2].split('.')[1].split("\n")[0]}.csv')
#             filePaths.append(f'files\\{lines.split(",")[2].split('.')[1].split("\n")[0]}.csv')
#     print(f'Top {tN} Fetched for {i} iterations; {time.time()-start} seconds')




#     for file_path in filePaths:
#         file_name = os.path.basename(file_path)   ## Extract filename from path
#         try: 
#             uploaded_file = bucket.upload_local_file(local_file=file_path, file_name=file_name) 
#         except Exception as e:
#             print(f"Error uploading file {file_path} for {i} iteration: {e}")

#     print(f'Models Data Uploaded for {i} iterations; Total Iteration {i} took {time.time()-start} seconds')


    #print(f"File uploaded successfully: {uploaded_file}")
    

# except Exception as e:
#     print(f"An error occurred: {e}")













# & acct_ids = models.execute_kw(DB_NAME, uid, API_SECRET, 'account.account', 'search', [[]])
# & acctList = models.execute_kw(DB_NAME, uid, API_SECRET, 'account.account', 'read', [model_ids])
 
# & model_ids = models.execute_kw(DB_NAME, uid, API_SECRET, 'ir.model', 'search', [[]])
# & modelList = models.execute_kw(DB_NAME, uid, API_SECRET, 'ir.model', 'read', [model_ids], {'fields': ['name', 'model']})