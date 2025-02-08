
#^###############################  utils.py  ####################################
# ^ Author: Sukhendu Sain
# ^ Description: Utils File
# ^ Data: 30-Jan-2025
#^###############################################################################
import xmlrpc.client
import csv, time, io
from b2sdk.v2 import B2Api, InMemoryAccountInfo

def authenticateOdoo(odooURL, dbName, user, apiKey):
    try:
        common = xmlrpc.client.ServerProxy(f"{odooURL}/xmlrpc/2/common")
        uid = common.authenticate(dbName, user, apiKey, {})

        if uid: return uid
        else: raise Exception(f"Odoo Authentication Failed: No UID Returned")
    except Exception as e:
        raise Exception(f"Odoo Authentication Failed: Error {e}")
    

def authenticateB2(keyID, appKey, bucketName):
    try:
        info = InMemoryAccountInfo() 
        b2_api = B2Api(info) 
        b2_api.authorize_account("production", keyID, appKey) 
        bucket = b2_api.get_bucket_by_name(bucketName)

        return bucket
    except Exception as e:
        raise Exception(f"BBB2 Authentication Failed: Error {e}")
    

def fetchOdooModel(modelName, models, uid, dbName, apiKey, fields=None):
    try:
        modelIds = models.execute_kw(dbName, uid, apiKey, modelName, 'search', [[]])
        if fields:
            modelList = models.execute_kw(dbName, uid, apiKey, modelName, 'read', [modelIds], {'fields': fields})
        else:
            modelList = models.execute_kw(dbName, uid, apiKey, modelName, 'read', [modelIds])

        return modelList
    except Exception as e:
        raise Exception(f"Odoo Model '{modelName}' Fetch Failed: Error {e}")
    

def writeCSV(data, headers, filename='data.csv'):
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(headers)
            for d in data:
                writer.writerow(list(d.values()))
    except Exception as e:
        raise Exception(f"CSV Write Failed: Error {e}")


def replicateModel(bucket, modelName, dbName, apiKey, odooUrl, user):
    uid = authenticateOdoo(odooUrl, dbName, user, apiKey)
    models = xmlrpc.client.ServerProxy(f"{odooUrl}/xmlrpc/2/object")
    i = 0
    while True:
        i += 1
        try: 
            start = time.time()
            modelList = fetchOdooModel(modelName, models, uid, dbName, apiKey)   
            #print(modelName, modelList)
            writeCSV(modelList, modelList[0].keys(), f'files\{modelName.split(".")[1]}.csv')

            bucket.upload_local_file(local_file=f"files\{modelName.split(".")[1]}.csv", file_name=f"{modelName.split(".")[1]}.csv") 
            print(f"Replication of Model {modelName} done of Iteration {i}; Took {time.time()-start} Seconds")
        except Exception as e:
            print(f"Replication of Model {modelName} Failed of Iteration {i}: Error {e}")


def replicateModels(bucket, modelNames, dbName, apiKey, odooUrl, user):
    i = 0
    tStart = time.time()
    while True:
        if i == 5: break
        iStart = time.time()
        time.sleep(2)
        i += 1
        for modelName in modelNames:
            try: 
                start = time.time()
                uid = authenticateOdoo(odooUrl, dbName, user, apiKey)
                models = xmlrpc.client.ServerProxy(f"{odooUrl}/xmlrpc/2/object")
                modelName = modelName.split(",")[2].split("\n")[0]
                
                modelList = fetchOdooModel(modelName, models, uid, dbName, apiKey)  

                tempSringIO = io.StringIO() 
                # writer = csv.writer(tempSringIO)
                # writer.writerow(modelList[0].keys())
                # for row in modelList:
                #     writer.writerow(row.values())
                writeCSV(modelList, modelList[0].keys(), tempSringIO)#f'files\{modelName.split(".")[1]}.csv')
                
                bucket.upload_local_file(local_file=f"files\{modelName.split(".")[1]}.csv", file_name=f"{modelName.split(".")[1]}.csv")
                # bucket.upload_bytes(data_bytes=bytes(tempSringIO), file_name=f"{modelName.split(".")[1]}.csv")  
                # print(f"Replication of Model {modelName} done of Iteration {i}; Took {time.time()-start} Seconds")
            except Exception as e:
                #print(f"Replication of Model {modelName} Failed of Iteration {i}: Error {e}")
                continue
        # print(f"All Tables {modelNames[:][2]} for iter {i}; took {time.time()-iStart} Seconds")
        print(f"All Tables for iter {i}; took {time.time()-iStart} Seconds; total {time.time()-tStart} Seconds")