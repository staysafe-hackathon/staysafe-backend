import logging

import azure.functions as func
import pyodbc
import json 

connection_string = "Driver={ODBC Driver 17 for SQL Server};Server=tcp:hackunamatata.database.windows.net,1433;Database=StaySafeDb;Uid=useradmin;Pwd=admin@123;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    curr = get_conn().cursor()
    body = req.get_json()

    try:
        username = body['username']
        pw = body['password']
        curr = curr.execute(f"SELECT UserID, UserType from LoginCredentials where Username = '{username}' and Password='{pw}';")
        
        user = curr.fetchone()
        
        if user is not None:
        
            return func.HttpResponse(
                json.dumps({
                "user_id": user[0],
                "client_type": user[1],
                "hash": "verysecurehash"
                }),

            mimetype="application/json")
        
        return func.HttpResponse("Not authorized", status_code=401)
    except Exception as e:
        return func.HttpResponse(str(e), status_code=500)
    
    
def get_conn():
    conn = pyodbc.connect(connection_string)
    conn.setdecoding(pyodbc.SQL_WCHAR, encoding='utf-8')
    conn.setencoding(encoding='utf-8')
    return conn
