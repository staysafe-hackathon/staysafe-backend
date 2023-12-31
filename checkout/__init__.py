import logging

import azure.functions as func
import pyodbc
import os
import datetime

connection_string = "Driver={ODBC Driver 17 for SQL Server};Server=tcp:hackunamatata.database.windows.net,1433;Database=StaySafeDb;Uid=useradmin;Pwd=admin@123;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"

#app = func.FunctionApp()

#@app.route(route="checkin")
def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    body = req.get_json()

    booking_id = body["bookingId"]
    feedback_flag = body["feedbackFlag"]
    request_extension_minutes = body["requestExtensionMinutes"]
    date = datetime.datetime.now()

    print("booking id is: ", booking_id)

    sql = "UPDATE VisitSession SET CheckOut = ?, FeedbackFlag = ?, RequestExtensionMinutes = ? WHERE BookingID = ?"

    curr = get_conn().cursor()
    curr = curr.execute(sql, (date, feedback_flag, request_extension_minutes, booking_id))

    curr.commit()

    try:
        return func.HttpResponse(str(curr.fetchall()))
    except Exception as e:
        return func.HttpResponse(str(e), status_code=500)
    
    
def concatenate_geocoords(lat: float, long: float) -> str:
    concatenated = str(lat) + " " + str(long)
    return concatenated

def get_conn():
    conn = pyodbc.connect(connection_string)
    conn.setdecoding(pyodbc.SQL_WCHAR, encoding='utf-8')
    conn.setencoding(encoding='utf-8')
    return conn
