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
            curr = curr.execute(f"SELECT * FROM Admin INNER JOIN LoginCredentials ON Admin.UserID = LoginCredentials.UserID INNER JOIN Therapist ON Admin.ID = Therapist.AdminID INNER JOIN Booking ON Therapist.ID = Booking.TherapistID INNER JOIN Client ON Booking.ClientID = Client.ID WHERE LoginCredentials.UserID ='{userid}';")
            schedules = curr.fetchall()
            processed_schedules = []

            for schedule in schedules: 
                processed_schedules.append({
               "id": schedule[0],
                "name": schedule[1],
                "userid": schedule[2],
                "userid1": schedule[3],
                "username": schedule[4],
                "password": schedule[5],
                "usertype": schedule[6],
                "id1": schedule[7],
                "name": schedule[8],
                "phoneno": schedule[9],
                "teamleaderid": schedule[10],
                "nextofkinname": schedule[11],
                "extofkinnumber": schedule[12],
                "userid2": schedule[13],
                "adminid": schedule[14],
                "id2": schedule[15],
                "therapistid": schedule[16],
                "clientid": schedule[17],
                "latitude": schedule[18],
                "logitude": schedule[19],
                "address": schedule[20],
                "appointmentst": schedule[21],
                "appointmentet": schedule[22],
                "id3": schedule[23],
                "name": schedule[24],
                "phonenum": schedule[25],
                "flag": schedule[26],
                "reasonforflag": schedule[27],
                "userid4": schedule[28]
                
                })
        elif usertype == 'Therapist': 
            curr = curr.execute(f"SELECT * FROM(SELECT Therapist.ID AS TherapistID,Therapist.Name AS TherapistName,LoginCredentials.Username AS TherapistUsername FROM Therapist INNER JOIN LoginCredentials ON Therapist.UserID = LoginCredentials.UserID WHERE LoginCredentials.UserID = '{userid}') AS T INNER JOIN Booking ON T.TherapistID = Booking.TherapistID INNER JOIN Client AS C ON Booking.ClientID = C.ID;")
            schedules = curr.fetchall()
            processed_schedules = []

            for schedule in schedules: 
                processed_schedules.append({
               "therapistid": schedule[0],
                "therapistname": schedule[1],
                "therapistusername": schedule[2],
                "id": schedule[3],
                "therapistid": schedule[4],
                "clientid": schedule[5],
                "latitude": schedule[6],
                "logitude": schedule[7],
                "address": schedule[8],
                "appointmentst": schedule[9],
                "appointmentet": schedule[10],
                "id2": schedule[11],
                "name": schedule[12],
                "phonenum": schedule[13],
                "flag": schedule[14],
                "reasonforflag": schedule[15],
                "userid": schedule[16]
               })
        else:  
           
            curr = curr.execute(f"SELECT * FROM LoginCredentials AS LC INNER JOIN Client AS C ON LC.UserID = C.ID INNER JOIN Booking AS B ON C.ID = B.ClientID INNER JOIN Therapist AS T ON B.TherapistID = T.ID WHERE LC.UserID ='{userid}';")
            schedules = curr.fetchall()
            processed_schedules = []

            for schedule in schedules: 
                processed_schedules.append({
               "userid": schedule[0],
                "username": schedule[1],
                "password": schedule[2],
                "usertype": schedule[3],
                "id1": schedule[4],
                "name": schedule[5],
                "phoneno": schedule[6],
                "flag": schedule[7],
                "reasonforflag": schedule[8],
                "userid1": schedule[9],
                "id2": schedule[10],
                "therapistid": schedule[11],
                "clientid": schedule[12],
                "latitude": schedule[13],
                "longitude": schedule[14],
                "appointmentst": schedule[15],
                "appointmentet": schedule[16],
                "id3": schedule[17],
                "name": schedule[18],
                "phonenumber": schedule[19],
                "teamleaderid": schedule[20],
                "nextofkinname": schedule[21],
                "extofkinnumber": schedule[22],
                "userid2": schedule[23],
                "adminid": schedule[24]
                
                })
        

        return func.HttpResponse(
            json.dumps({"schedule": processed_schedules},default=str),
            mimetype="application/json"
        )
        
    except Exception as e:
        return func.HttpResponse(str(e), status_code=500)
    
    
def get_conn():
    conn = pyodbc.connect(connection_string)
    conn.setdecoding(pyodbc.SQL_WCHAR, encoding='utf-8')
    conn.setencoding(encoding='utf-8')
    return conn
