from requestcalls.getdata import get_open_ticket
from requestcalls.getdata import get_tix_details
from requestcalls.getdata import tasklist,get_task_order
from datetime import datetime, timedelta
import datetime
import pyfiglet
import pandas as pd
import config

gsheet_path = config.gsheet_token_path



def handledtix(staffID,sd_handler):


    sd_handler = sd_handler

    staffID = staffID
    res = get_open_ticket(staffID)


    if res['resultData']["total"] <= 0:
        print("AgentID", staffID ,"Invalid or Not Found")
    else:
        print("Extracting Data for SD: ",sd_handler)
        print("")
        resobj = res['resultData']["rows"]

        handledtix = []

        for items in resobj:
            # pprint.pprint(items)
            ticketnum = items['orderCode']
            tickettype = items['packageName']
            ticketTitle = items['workOrderTitle']

            if tickettype == 'IT Service Request' or tickettype == "Incident Management":

                detailsobj = get_tix_details(ticketnum)
                # print(detailsobj)
                if detailsobj['resultData']["total"] <= 0:
                    print("Input Error!!! or No record found")
                else:
                    samp = detailsobj['resultData']["rows"]
                    for tix in samp:
                        
                        orderID = tix['orderId']
                        shardingKey = tix['shardingKey']
                        

                        res1 = tasklist(str(orderID))
                        task_orders = get_task_order(str(orderID),str(shardingKey))
                        filterfeedback = task_orders['resultData']
                        
                        for items in filterfeedback:
                            # pprint.pprint(items)

                            if items['operOrgName'] == 'Stratnet':
                                if str(items['operStaffId']) == str(staffID):
                                    if items['operTypeName'] == 'Remind' or items['operTypeName'] == 'Forward':

                                        oprtype = items['operTypeName']
                                        starttix = items['createDate']
                                        endtix = items['createDate']
                                        today = datetime.date.today()
                                        format_str = "%Y-%m-%d %H:%M:%S"
                                        date = datetime.datetime.strptime(starttix, format_str)
                                        year = date.year
                                        month = date.month
                                        day = date.day
                                        date_to_compare = datetime.date(year, month, day)
                                        if today == date_to_compare:
                                            checkouttime = starttix[11:]
                                            
                                            date = datetime.datetime.strptime(endtix, format_str)
                                            new_date = date + timedelta(minutes=10)
                                            endtixfor = new_date.strftime(format_str)
                                            endtime = endtixfor[11:]
                                            date = datetime.datetime.now()
                                            formatted_date = date.strftime("%d-%b-%y")

                                            add_new = {
                                            '1sdhandler': sd_handler,
                                            '2handlingtype': 'OFM Ticket Handling',
                                            '3curdate': formatted_date,
                                            '4checkout': checkouttime,
                                            '5endtime': endtime,
                                            '6ticketnum': ticketnum,
                                            '7tickettile': ticketTitle,
                                            '8actiontaken': oprtype
                                            }
                                            handledtix.append(add_new)
                                    

                        for task in res1:
                            if task['partyOrgName'] == 'Stratnet':
                                if str(task['partyStaffId']) == staffID:
                                    starttix = task['createDate']
                                    endtix = task['finishDate']
                                    today = datetime.date.today()
                                    format_str = "%Y-%m-%d %H:%M:%S"
                                    date = datetime.datetime.strptime(starttix, format_str)
                                    year = date.year
                                    month = date.month
                                    day = date.day
                                    date_to_compare = datetime.date(year, month, day)
                                    if today == date_to_compare:
                                        checkouttime = starttix[11:]
                                        if endtix is not None:
                                            endtime = endtix[11:]

                                            date = datetime.datetime.now()
                                            formatted_date = date.strftime("%d-%b-%y")

                                            add_new = {
                                                '1sdhandler': sd_handler,
                                                '2handlingtype': 'OFM Ticket Handling',
                                                '3curdate': formatted_date,
                                                '4checkout': checkouttime,
                                                '5endtime': endtime,
                                                '6ticketnum': ticketnum,
                                                '7tickettile': ticketTitle,
                                                '8actiontaken': 'ENTER!!'
                                            }
                                            handledtix.append(add_new)


        
        return handledtix                               

        

        



def getallworkorder():

    paul_art = pyfiglet.figlet_format("SDs-WorkOrder")
    print(paul_art)


    idArray = [
        {
            'sdID': '14738',
            'sdName': 'Claveria, Julius'
        },
        {
            'sdID': '21007',
            'sdName': 'Malinao, Rhenz'
        },
        {
            'sdID': '3309335',
            'sdName': 'Castillo, Timothy'
        },
        {
            'sdID': '3300201',
            'sdName': 'Uson, Christian Dave'
        },
        {
            'sdID': '14739',
            'sdName': 'De Leon, Alexandra'
        },
        {
            'sdID': '3311302',
            'sdName': 'Rivera,Rommel Nebreja'
        },
        {
            'sdID': '26009',
            'sdName': 'Abrugar, Paul Bryan'
        },
        {
            'sdID': '3311306',
            'sdName': 'Bagatnan, Patricia Ann'
        },
        {
            'sdID': '23010',
            'sdName': 'Claro, Carlito'
        },        
        {
            'sdID': '3309334',
            'sdName': 'Manalindo,Huzaima'
        },        
        {
            'sdID': '24013',
            'sdName': 'Sarmiento, John Leon Angelo'
        },
        {
            'sdID': '21027',
            'sdName': 'Mojica Van Angelo'
        }
        ]
    


    allhandledtix = []
    for item in idArray:
        staffID = item['sdID']
        sd_handler = item['sdName']
        res_handled_tix = handledtix(staffID,sd_handler)
        allhandledtix.extend(res_handled_tix)
        print(f"Done! SD work order total:",len(res_handled_tix))
        print(f"+++++++++++++++++++++++++++++++++")
        

    df = pd.DataFrame(allhandledtix)
    today = datetime.date.today()

    
    
    df.to_excel('ITSD-workorder'+str(today)+'.xlsx', index=False)
    print("Data Extracted, Please check root folder.")


