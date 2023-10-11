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
            curr = curr.execute(f"SELECT A.TherapistName,C.Name AS ClientName,A.AppointmentStartTime,A.AppointmentEndTime FROM(SELECT Admin.ID AS AdminID,Admin.Name AS AdminName,Therapist.ID AS TherapistID,Therapist.Name AS TherapistName,Booking.ID AS BookingID,Booking.ClientID,Booking.AppointmentStartTime,Booking.AppointmentEndTime,LoginCredentials.Username AS AdminUsername,LoginCredentials.Password AS AdminPasswordFROM Admin INNER JOIN LoginCredentials ON Admin.UserID = LoginCredentials.UserID INNER JOIN Therapist ON Admin.ID = Therapist.AdminID INNER JOIN Booking ON Therapist.ID = Booking.TherapistID WHERE LoginCredentials.UserID = '{userid}') AS INNER JOIN Client AS C ON A.ClientID = C.ID;")
            schedules = curr.fetchall()
            processed_schedules = []

            for schedule in schedules: 
                processed_schedules.append({
               "therapistname": user[0],
                "clientname": user[1],
                "appointmentst": user[2],
                "appointmentet": user[3]
                })
        elif usertype == 'Therapist': 
            curr = curr.execute(f"T.TherapistName,T.TherapistUsername,SELECT T.TherapistID,,C.Name AS ClientName FROM(SELECT Therapist.ID AS TherapistID,Therapist.Name AS TherapistName,LoginCredentials.Username AS TherapistUsername FROM Therapist INNER JOIN LoginCredentials ON Therapist.UserID = LoginCredentials.UserID WHERE LoginCredentials.UserID = '{userid}') AS T INNER JOIN Booking ON T.TherapistID = Booking.TherapistID INNER JOIN Client AS C ON Booking.ClientID = C.ID;")
            schedules = curr.fetchall()
            processed_schedules = []

            for schedule in schedules: 
                processed_schedules.append({
               "therapistname": user[0],
                "therapistid": user[1],
                "clientname": user[2]})
        else:  
           
            curr = curr.execute(f"SELECT T.Name AS TherapistName,T.PhoneNumber AS TherapistPhoneNumber,B.AppointmentStartTime,B.AppointmentEndTime FROM LoginCredentials AS LC INNER JOIN Client AS C ON LC.UserID = C.ID INNER JOIN Booking AS B ON C.ID = B.ClientID INNER JOIN Therapist AS T ON B.TherapistID = T.ID WHERE LC.UserID ='{userid}';")
            schedules = curr.fetchall()
            processed_schedules = []

            for schedule in schedules: 
                processed_schedules.append({
               "therapistname": user[0],
                "therapistph": user[1],
                "appointmentst": user[2],
                "appointmentet": user[3]})
        

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
