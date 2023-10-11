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
    user_id = body["userId"]
    lat = body["latitude"]
    long = body["longitude"]
    date = datetime.datetime.now()

    print("booking id is: ", booking_id)
    print("user id is: ", user_id)
    print("date is: ", date)

    sql = "INSERT INTO VisitSession (BookingID, CheckIn, CheckOut, FeedbackFlag, RequestExtensionMinutes, Latitude, Longitude) VALUES (?, ?, ?, ?, ?, ?, ?)"

    curr = get_conn().cursor()
    curr = curr.execute(sql, (booking_id, date, None, None, None, lat, long))

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
