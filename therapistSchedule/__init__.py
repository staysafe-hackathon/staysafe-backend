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
        userid = body['userid']
        usertype= body['usertype']

        if usertype== 'Admin': 
            curr = curr.execute(f"SELECT Admin.ID AS AdminID,Admin.Name AS AdminName,Therapist.ID AS TherapistID,Therapist.Name AS TherapistName,Booking.ID AS BookingID,Booking.ClientID,Booking.AppointmentStartTime,Booking.AppointmentEndTime,LoginCredentials.Username AS AdminUsername,LoginCredentials.Password AS AdminPassword FROM Admin INNER JOIN LoginCredentials ON Admin.UserID = LoginCredentials.UserID INNER JOIN Therapist ON Admin.ID = Therapist.AdminID INNER JOIN Booking ON Therapist.ID = Booking.TherapistID Where LoginCredentials.UserID= '{userid}';")
         
        elif usertype == 'Therapist': 
            curr = curr.execute(f"SELECT Therapist.ID AS TherapistID,Therapist.Name AS TherapistName,LoginCredentials.Username AS TherapistUsername FROM Therapist INNER JOIN LoginCredentials ON Therapist.UserID = LoginCredentials.UserID Where LoginCredentials.UserID= '{userid}';")
        else:  
           
            curr = curr.execute(f"SELECT LoginCredentials.UserID, Client.Name AS ClientName,Booking.ID AS BookingID,Booking.AppointmentStartTime,Booking.AppointmentEndTime FROM LoginCredentials INNER JOIN Client ON LoginCredentials.UserID = Client.ID INNER JOIN Booking ON Client.ID = Booking.ClientID WHERE LoginCredentials.UserID = '{userid}';")
        
        schedules = curr.fetchall()
        

        processed_schedules = []

        for schedule in schedules: 
            processed_schedules.append({
                ""
            })

        return func.HttpResponse(
            json.dumps({"schedule": processed_schedules}),
            mimetype="application/json"
        )
        
    except Exception as e:
        return func.HttpResponse(str(e), status_code=500)
    
    
def get_conn():
    conn = pyodbc.connect(connection_string)
    conn.setdecoding(pyodbc.SQL_WCHAR, encoding='utf-8')
    conn.setencoding(encoding='utf-8')
    return conn
