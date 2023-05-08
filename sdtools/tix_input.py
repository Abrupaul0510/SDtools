import gspread
import config
import datetime
from oauth2client.service_account import ServiceAccountCredentials
from requestcalls.getdata import get_task_order,get_tix_details,getmore_details_request

gsheet_path = config.gsheet_token_path





def addtix(tix):

    now = datetime.datetime.now()
    formatted_date = now.strftime("%d-%b-%y")
    res = get_tix_details(tix)
    tixarray = res['resultData']["rows"]

    for item in tixarray:

        ticketOFM = item['orderCode']

        if ticketOFM == tix:
            shardingKey = item['shardingKey']
            orderID = item['orderId']

            tasklist = get_task_order(str(orderID),str(shardingKey))
            firstele = tasklist['resultData'][0]
            recordID = firstele['operRecordId']



            reporter,tixtitle,flevel,subdomain,domain,tixdescription = getmore_details(recordID)

            cfile = gsheet_path
            scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
            creds = ServiceAccountCredentials.from_json_keyfile_name(cfile, scope)
            client = gspread.authorize(creds)


            sheet = client.open('dutypol').get_worksheet(1)
            sheet2 = client.open('dutypol').get_worksheet(2)
                     

            columnval = sheet.col_values(1)
            
            checker = False
            for itemsinexcel in columnval:
                if str(itemsinexcel) == str(tix):
                    checker = False
                else:
                    checker = True
            
            if checker == True:
                new_row = [tix,
                            '',
                            '', 
                            flevel,
                            '',
                            '',
                            '',
                            '',
                            '',
                            '',
                            'OFM',
                            reporter,
                            '',
                            'NCR',
                            domain,
                            subdomain,
                            '',
                            tixtitle,
                            tixdescription,
                            '',
                            '']

                new_exist = [tix,
                            'OFM Ticket Handling',
                            formatted_date,
                            '',
                            '',
                            '',
                            tixtitle,
                            '']
                

                sheet.append_row(new_row)
                sheet2.append_row(new_exist)
                


            
            
                



def getmore_details(recordID):

    res = getmore_details_request(recordID)

    detailspol = res['resultData']['jsonData']

    tixdescription = ""
    domain = ""
    subdomain = ""
    flevel = ""
    tixtitle = ""
    reporter = ""

    for items in detailspol:
        if items['eleCode'] == "eventDescription" or items['eleCode'] == "appleDesc":
            tixdescription += items['eleValue']

        if items['eleCode'] == "subordinateToTheSystemDomain" or items['eleCode'] == "ownSystemDomain":
            domain += items['eleValue']

        if items['eleCode'] == "subordinateToTheSystem" or items['eleCode'] == "PTO_OSS_EXTERNAL_SYSTEM":
            subdomain += items['eleValueName']

        if items['eleCode'] == "eventProcessingTimeMinutes" or items['eleCode'] == "responseValue":
            flevel += items['eleValue']

        if items['eleCode'] == "eventTitle" or items['eleCode'] == "orderTitle":
            tixtitle += items['eleValue']

        if items['eleCode'] == "requesterName" or items['eleCode'] == "applyName":
            reporter += items['eleValue']
    
    return reporter,tixtitle,flevel,subdomain,domain,tixdescription

