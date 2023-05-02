import time
import pandas as pd
from requestcalls.getdata import get_task_order,check_ticket_count
from requestcalls.bot import send_ding,send_ding_error2
import datetime
import gspread
from sdtools.tix_input import addtix
from oauth2client.service_account import ServiceAccountCredentials
import pyfiglet
import config


gsheet_path = config.gsheet_token_path
bothost = config.bothost


cfile = gsheet_path  
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name(cfile, scope)
client = gspread.authorize(creds)


def checknget_owner(sdstaffid,filterstatus):

    gc = gspread.service_account(cfile)
    sh = gc.open('dutypol')
    worksheet = sh.get_worksheet(0)
    data = worksheet.get_all_records()
    df = pd.DataFrame(data)
    data = df[df['SD.Status'] == filterstatus]
    my_dict = data.to_dict(orient = 'records')


    sdid = [d['SD.Id'] for d in my_dict]
    sdname = [d['SD.Name'].strip() for d in my_dict]
    sdnumber = [d['SD.Number'] for d in my_dict]
    sdstatus = [d['SD.Status'].strip() for d in my_dict]
    
    dataSD = {}
    for i, (j, k, s) in zip(sdid, zip(sdname, sdnumber, sdstatus)):
        dataSD[i] = (j, k,s)  



    if sdstaffid in dataSD:
        name, number, status = dataSD[sdstaffid]
        return {'Status': status,
                'Name' : name,
                'Number' : number}

    else:
        return {'Status': "Not Available",
                'Name' : "",
                'Number' : ""}


def get_all_available(filterstatus):


    gc = gspread.service_account(cfile)
    
    sh = gc.open('dutypol')

    worksheet = sh.get_worksheet(0)
    data = worksheet.get_all_records()

    df = pd.DataFrame(data)


    data = df[df['SD.Status'] == filterstatus]

    my_dict = data.to_dict(orient = 'records')


    sdnumber = [d['SD.Number'] for d in my_dict]



    allavail = []
    for items in sdnumber:
        sdnum = "+63-"+str(items)
        allavail.append(str(sdnum))

    return allavail


def tixmonitor():

    count = False
    while True:

        tixcountres = check_ticket_count()
        tixcount = tixcountres['rows']

        if len(tixcount) == 0:
            __ignore_ = "None"

        else:
            count = True

        if count == True:
    
            for item in tixcountres['rows']:
                tix = item['orderCode']
                tixstart = item['publicDate']          
                date_str = tixstart
                format_str = "%Y-%m-%d %H:%M:%S"
                date = datetime.datetime.strptime(date_str, format_str)
                now = datetime.datetime.now()
                difference = now - date
                tminutes = int(difference.total_seconds() // 60)
                tseconds = int(difference.total_seconds() % 60)
                tixnum = tix

                bothostcheck = item['partyName'].strip()
                if bothostcheck == bothost:
                    tixnum = tix
                    if tminutes >= 1:
                        print("Current Task:")
                        duration = str(tminutes)+"Minutes "+str(tseconds)+"Seconds"
                        print(tixnum+" - "+duration)
                    
                else:
                    tixnum = tix
 
                    print(tixnum)
           
                    date_str = tixstart
                    
                    format_str = "%Y-%m-%d %H:%M:%S"

                    date = datetime.datetime.strptime(date_str, format_str)
                    now = datetime.datetime.now()

                    
                    difference = now - date

                    tminutes = int(difference.total_seconds() // 60)
                    tseconds = int(difference.total_seconds() % 60)


                    
                    domain = item['systemDomain']
                    system = item['system']
                    title = str(item['orderTitle'])
                    domaindata = {
                            'tdomain' : domain,
                            'system' : system,
                            'title' : str(title),
                        }
                    status = item['tacheName'] 
                    orderId = item['orderId'] 
                    shardingKey = item['shardingKey']
                    title = item['orderTitle']
                        

                    detailed = get_task_order(str(orderId),str(shardingKey))
                    taskdata = detailed['resultData']





                    pos = -1
                    for i,item in enumerate(taskdata):
                        if item.get('operOrgName') == 'Stratnet' and item.get('operTypeName') == 'Check Out':
                                pos = i
                                break
                        
                    if pos >= 0:
                        sdwhat = "Existing" 
                        sdnameoff = ""
                        sdlasttouch = ""
                        sdstaffid = taskdata[pos]['operStaffId']
                        owner_excel = checknget_owner(sdstaffid,filterstatus='Available')
                        sdstatusowner = owner_excel.get('Status')
                        sdname = owner_excel.get('Name')

                        allavail = ""
                        
                        currentrotation = getcurrentrot()
                        sd_status_owner = ""
                        sd_number_available = ""
                        for sublist in currentrotation:
                            if str(sublist[0]) == str(sdstaffid) and sublist[2] == 'Available':
                                sd_number_available += sublist[2]
                                sd_status_owner += sublist[2]
                                break
                            else:
                                sd_number_available += sublist[2]
                                sd_status_owner += "Not Available"
                                break

                        

                        
                        if sd_status_owner == "Available":
                            sdnumbr = sd_number_available
                            send_ding(tix,sdname,sdwhat,sdnumbr,sd_status_owner,sdnameoff,sdlasttouch,status,tminutes,tseconds,domaindata,allavail)

                        elif sd_status_owner == "Not Available":
                                
                                sdtouch = []
                                newtats = []
                                for i,item in enumerate(taskdata):
                                    if item.get('operOrgName') == 'Stratnet' and item.get('operTypeName') == 'Check Out':

                                        staffID = item.get('operStaffId')
                                        
                                        dataSD = checknget_owner(staffID,filterstatus='Available')
                                        
                                        if dataSD.get('Name') != '':
                                            SDcnumber = dataSD.get('Number')
                                            SDname = dataSD.get('Name')

                                            

                                            newdata = SDname
                                            sorting = str(i)

                                            dataappend =   { 
                                                "id": sorting,        
                                                "name": SDname,        
                                                "number": SDcnumber}

                                            newtats.append(dataappend)

                                        sdtouchtrim = item.get('operStaffName').strip()
                                        sdtouch.append(sdtouchtrim)

                                

                                unique_names = {d['name']: d for d in newtats}
                                sorted_names = sorted(unique_names.values(), key=lambda x: x['id'])
                                names_and_numbers = [(d['name'], d['number']) for d in sorted_names]

                                if len(names_and_numbers) == 0:
                                    name = "[NONE]"
                                    number = ""
                                    allavail = ""
                                    mintix = min(currentrotation, key=lambda x: int(x[5]))
                                    
                                    sd_number = mintix[2]
                                    number = sd_number

                                else: 
                                    name, number = names_and_numbers[-1]
 
                                result = checknget_owner(sdstaffid,filterstatus='Not Available')
                                sdnameoff = result.get('Name')

                                sdnames = ""
                                send_ding(tix,name,sdwhat,number,sdstatusowner,sdnameoff,sdlasttouch,status,tminutes,tseconds,domaindata,allavail)

                    else:
                        
                        sdwhat = "New"
                        sdnames = ""
                        sdnumber= ""
                        sdstatusowner=" "
                        sdnameoff = ""
                        sdlasttouch = ""
                        addtix(tix)
                        
                        currentrotation = getcurrentrot()
                        allavail = ""
                        mintix = min(currentrotation, key=lambda x: int(x[5]))
                        sd_number = mintix[2]
                        send_ding(tix,sdnames,sdwhat,sd_number,sdstatusowner,sdnameoff,sdlasttouch,status,tminutes,tseconds,domaindata,allavail)

                            
                        
            
            
            time.sleep(30)
            count = False
        time.sleep(1)


def startMonitoring():
    intro_at = pyfiglet.figlet_format('MONITORING...')
    print("MONITORING STARTS....")
    while True:
        try:
            
            print(intro_at)
            
            tixmonitor()
        except Exception as err:
            print(err)
            send_ding_error2(err)
            time.sleep(30)


def getcurrentrot():
    sheet = client.open('dutypol').get_worksheet(0)

    
    data = sheet.get_all_values()

    
    results = []
    for row in data[1:]: 
        if row[3] == "Available":
            results.append([ row[0],row[1],row[2], row[3], row[4], row[5]])

    return results