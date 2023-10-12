import datetime
import logging
import pyodbc
import azure.functions as func
import json

connection_string = "Driver={ODBC Driver 17 for SQL Server};Server=tcp:hackunamatata.database.windows.net,1433;Database=StaySafeDb;Uid=useradmin;Pwd=admin@123;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"

def main(mytimer: func.TimerRequest) -> str:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    if mytimer.past_due:
        logging.info('The timer is past due!')

    # current_time = datetime.tofday.date()        

    sql = "SELECT * FROM Booking WHERE CAST(AppointmentStartTime AS DATE) = CAST(GETDATE() AS DATE) AND AppointmentEndTime IS NULL AND DATEDIFF(MINUTE, AppointmentStartTime, GETDATE()) >= 5 AND (SELECT CheckIn FROM VisitSession WHERE BookingID = Booking.ID) IS NULL;"    

    curr = get_conn().cursor()
    curr = curr.execute(sql)

    logging.info('Python timer trigger function ran at %s', utc_timestamp)

    try:
        return func.HttpResponse(json.dumps(curr.fetchall()))
    except Exception as e:
        return func.HttpResponse(str(e), status_code=500)



def get_conn():
    conn = pyodbc.connect(connection_string)
    conn.setdecoding(pyodbc.SQL_WCHAR, encoding='utf-8')
    conn.setencoding(encoding='utf-8')
    return conn
