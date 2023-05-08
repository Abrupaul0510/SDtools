from requestcalls.getdata import get_open_ticket
from requestcalls.getdata import get_tix_details
from requestcalls.getdata import tasklist
import datetime
import pyfiglet

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import config

sd_handler = config.log_sheet
gsheet_path = config.gsheet_token_path

def handledtix():

    cfile = gsheet_path  
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(cfile, scope)
    client = gspread.authorize(creds)


    sheet = client.open('dutypol').get_worksheet(7)


    paul_art = esult = pyfiglet.figlet_format("HANDLED-TIX")
    print(paul_art)
    print("Extracting Data...")

    staffID = config.sd_id
    res = get_open_ticket(staffID)


    if res['resultData']["total"] <= 0:
        print("AgentID", staffID ,"Invalid or Not Found")
    else:
        print("StaffID: ",staffID)
        print("")
        resobj = res['resultData']["rows"]
        all_secondline_status = []
        all_confirm_status = []

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
                        for task in res1:
                            if task['partyOrgName'] == 'Stratnet':
                                if str(task['partyStaffId']) == staffID:
                                    stafIDs = task['partyStaffId']
                                    stafName = task['partyName']
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
                                        

        for row in handledtix:
            sheet.insert_row([row['1sdhandler'], row['2handlingtype'], row['3curdate'], row['4checkout'], row['5endtime'], row['6ticketnum'], row['7tickettile'], row['8actiontaken']], 2)

        print("Extraction complete Please check Gsheets")
