import calendar
import datetime
from dateutil import parser
import pprint
import pandas as pd
import pyfiglet
import config
from requestcalls.getdata import get_closed


##checking ticket thru OFM
def checkticket(tixnumclean,dataobj):

    res = get_closed(tixnumclean)

    tixarray = res['resultData']["rows"]
    if len(tixarray) >= 0:


        for tixcheck in tixarray:

            tixnumber = tixcheck['orderCode']
            if tixnumber == tixnumclean:
                # samp = res['resultData']["rows"][i]

                status = tixcheck['tacheName']

                if not status :
                    date_string = tixcheck['finishDate']

     
                    print(tixnumclean," CLOSED @ ",date_string)
                    return
    else:
        print("")


def pen_ac22():

    rawdata = config.excel_path
    paul_art = pyfiglet.figlet_format("Closed Tickets")
    print(paul_art)
    print("Checking for closed tickets")
    df = pd.read_excel(rawdata, sheet_name="2023 Ticket Tracker")
    data = df[df['Status'] == 'Pending-customer confirm']
    my_dict = data.to_dict(orient = 'records')


    df1 = pd.read_excel(rawdata, sheet_name="2023 Ticket Tracker")
    data1 = df1[df1['Status'] == 'Pending-customer action']
    my_dict1 = data1.to_dict(orient = 'records')


    df2 = pd.read_excel(rawdata, sheet_name="2023 Ticket Tracker")
    data2 = df2[df2['Status'] == 'Second-line handle']
    my_dict2 = data2.to_dict(orient = 'records')




    my_dict.extend(my_dict1)
    my_dict.extend(my_dict2)


    tixnum_ar = [d['CaseNo.'].strip() for d in my_dict]
    dataobj=[]

    for tixnum in tixnum_ar:
        
        tixnumstrim = tixnum
        tixnumclean = tixnumstrim.strip()
        checkticket(tixnumclean,dataobj)







