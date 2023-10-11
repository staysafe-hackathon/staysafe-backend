import logging

import azure.functions as func
import pyodbc
import os

connection_string = "Driver={ODBC Driver 17 for SQL Server};Server=tcp:hackunamatata.database.windows.net,1433;Database=StaySafeDb;Uid=useradmin;Pwd=admin@123;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    curr = get_conn().cursor()
    curr = curr.execute("SELECT * from Booking ;")
    try:
        return func.HttpResponse(str(curr.fetchall()))
    except Exception as e:
        return func.HttpResponse(str(e), status_code=500)
    
    
def get_conn():
    conn = pyodbc.connect(connection_string)
    conn.setdecoding(pyodbc.SQL_WCHAR, encoding='utf-8')
    conn.setencoding(encoding='utf-8')
    return conn