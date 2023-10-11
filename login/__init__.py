import logging

import azure.functions as func
import pyodbc
import os

connection_string = "Driver={ODBC Driver 18 for SQL Server};Server=tcp:hackunamatata.database.windows.net,1433;Database=StaySafeDb;Uid=useradmin;Pwd=admin@123;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        curr = get_conn().cursor()
        curr = curr.execute("SELECT * from LoginCredentials;")
        
        return func.HttpResponse(str(curr.fetchall()))
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "{connection_string}",
             status_code=200
        )
    
def get_conn():
    conn = pyodbc.connect(connection_string)
    conn.setdecoding(pyodbc.SQL_WCHAR, encoding='utf-8')
    conn.setencoding(encoding='utf-8')
    return conn
