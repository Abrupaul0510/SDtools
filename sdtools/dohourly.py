import calendar
import datetime
import pandas as pd
from requestcalls.getdata import get_tix_details
import pyfiglet
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import config


gsheet_path = config.gsheet_token_path
bothost = config.bothost

cfile = gsheet_path
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name(cfile, scope)
client = gspread.authorize(creds)


def input_gsheet(tixarray):

    sheet = client.open('dutypol').get_worksheet(4)

    sheet.append_rows(tixarray)

    print('Gsheet already updated!')


def checkticket(tixnumclean,dataobj):

    res = get_tix_details(tixnumclean)
    second_line_status = ["Second-line Handle", "Handle for Technical Support", "Second-line Operate", "IT Confirm"]
    confirmstatus = ['Applicant Confirm', 'Confirm(Creator)','Callback','Confirm(Service Desk),Suspend Confirm']
    suspend = ['Confirm(Service Desk),Suspend Confirm','Suspend']
    tixarray = res['resultData']["rows"]
    if len(tixarray) >= 0:


        for tixcheck in tixarray:
            
            tixnumber = tixcheck['orderCode']
            if tixnumber == tixnumclean and tixcheck['tacheName'] in second_line_status:
                print("Done checking: ",tixnumclean)
                tix = tixcheck['orderCode'] 
                tixtitle = tixcheck['orderTitle']
                handler = tixcheck['partyStaffNames'] 
                orgName = tixcheck['partyRoleNames'] 
                handlerorg = tixcheck['partyOrgNames'] 


            

                monthday = tix[7:11] 
                month = monthday[0:2]
                int_month = int(month)
                day = monthday[2:4]
                int_day = int(day)
                date = datetime.datetime(2022,int_month,int_day)
                month_name = get_word_of_month(date)
                monthwithday = month_name+' '+day

                #check if monthandday exist in dataobj
                if monthwithday in [month["month"] for month in dataobj]:
                        for month in dataobj:
                            if month["month"] == monthwithday:
                                if handlerorg != "Stratnet" or orgName != "OSS_IT_SERVICE_DESK":
                                    monthwithday = month
                                    new_ticket = {"Ticket": tix,"Title": tixtitle, "handler": handler, "orgName": orgName, "handlerorg" : handlerorg}
                                    monthwithday["tickets"].append(new_ticket)
                                    
                                    return
                else:
                        if handlerorg != "Stratnet":
                            dateadd = {
                                    "month": monthwithday,
                                    "tickets": 
                                    [{  "Ticket": tix, 
                                        "Title": tixtitle,
                                        "handler": handler, 
                                        "orgName": orgName, 
                                        "handlerorg" : handlerorg
                                    }]
                                    }
                            dataobj.append(dateadd)
                        return
            elif tixnumber == tixnumclean and tixcheck['tacheName'] in confirmstatus:
                print(tixnumclean,"ALREADY FOR CONFIRMATION [PLEASE UPDATE STATUS ON TICKET TRACKER]")

            elif tixnumber == tixnumclean and tixcheck['tacheName'] in suspend:
                print(tixnumclean,"Status is on Apply Suspend [PLEASE CHECK]")

            elif tixnumber == tixnumclean:
                print(tixnumclean," CLOSED")

    else:
        print("No Found, please check manually ")


def get_word_of_month(date):
    month_name = calendar.month_name[date.month]
    return month_name


def hourlymain():

    paul_art = pyfiglet.figlet_format("HOURLY", font = "5lineoblique" )
    print(paul_art,"v2\n")

    print("Extracing data from excel...")
    df = pd.read_excel('rawdata.xlsx', sheet_name="2023 Ticket Tracker")
    dataall = df['Case No.'].notnull().sum()


    data = df[df['Status'] == 'Second-line handle']
    dataclosed = df[df['Status'] == 'Closed']
    dataconfirm = df[df['Status'] == 'Pending-customer confirm']
    dataaction = df[df['Status'] == 'Pending-customer action']

    secondlinet = len(data)
    actiont = len(dataaction)
    closedt = len(dataclosed)
    confirm = len(dataconfirm)

    #GETTING ALL DATA ===Second line in records format
    my_dict = data.to_dict(orient = 'records')



    #Extracting only ticket number with SL status
    tixnum_ar = [d['Case No.'].strip() for d in my_dict]
    print("Checking status in OFM...")
    dataobj=[]
    for tixnum in tixnum_ar:
        tixnumstrim = tixnum
        tixnumclean = tixnumstrim.strip()
        checkticket(tixnumclean,dataobj)


    now = datetime.datetime.now()

    propdate = now.strftime("%B %d, %H")
    #OUTPUTING ALL DATA

    print("")
    print("")
    print("IT Service Desk Hourly Update:")
    print(str(propdate)+":00 Number of Tickets:"+str(dataall)+" , Resolved: "+str(closedt)+" , Escalated: "+str(secondlinet)+" , Pending customer confirmation: "+str(confirm)+" , Pending customer action: "+str(actiont))
    #Generating for report
    for month in dataobj:
        print("")
        print("*"+month["month"] + "")
        for ticket in month["tickets"]:
            if not ticket["handler"]:
                print(ticket["Ticket"] + " - " + ticket["orgName"])
            else:
                print(ticket["Ticket"] + " - " + ticket["handlerorg"] +" | "+ ticket["handler"])


    #INSERT TO GSHEET
    tixarray = []
    now = datetime.datetime.now()
    formatted_date = now.strftime("%d-%b-%y")
    hourstart = now.strftime("%H")
    strstart = hourstart
    intstart = int(strstart)
    initial_time = now.replace(hour=intstart, minute=0, second=0, microsecond=0)
    checktimepertix = 60/secondlinet

    print("CheckTime Per Ticket:",checktimepertix)

    for item in dataobj:
        tickets = item['tickets']
        for ticket in tickets:
            end_time = initial_time + datetime.timedelta(minutes=checktimepertix)
            ticket_number = ticket['Ticket']
            title = ticket['Title']
            ticket_data = [bothost, formatted_date, initial_time.strftime("%H:%M:%S"),end_time.strftime("%H:%M:%S"),ticket_number,title,'Update / Check the updated handler']
            tixarray.append(ticket_data)
            initial_time = end_time

    input_gsheet(tixarray)






