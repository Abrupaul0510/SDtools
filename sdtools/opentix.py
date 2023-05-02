from requestcalls.getdata import get_open_ticket
from requestcalls.getdata import get_tix_details
from requestcalls.getdata import get_task_order
import datetime
import pyfiglet
import config

def opentix():

    paul_art = pyfiglet.figlet_format("OPENTIX")
    print(paul_art)
    # staffID = sys.argv[1]

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
        for items in resobj:
            ticketnum = items['orderCode']
            tickettype = items['packageName']

            if tickettype == 'IT Service Request' or tickettype == "Incident Management":

                detailsobj = get_tix_details(ticketnum)
                # print(detailsobj)
                if detailsobj['resultData']["total"] <= 0:
                    print("Input Error!!! or No record found")
                else:
                    samp = detailsobj['resultData']["rows"][0]
                    tix = samp['orderCode']
                    prio = samp['orderPriority']
                    status = samp['tacheName']
                    lastDate = samp['taskCreateDate']
                    orderID = samp['orderId']
                    shardingKey = samp['shardingKey']

                    second_line_status = ["Second-line Handle", "Handle for Technical Support", "Second-line Operate", "IT Confirm"]
                    confirmstatus = ['Applicant Confirm', 'Confirm(Creator)','Callback','Confirm(Service Desk),Suspend Confirm']

                    orderIDtrim = orderID
                    orderIDs = str(orderIDtrim)
                    objremind = []
                    res1 = get_task_order(orderIDs,str(shardingKey))
                    
                    indx = len(res1['resultData'])
                    
                    indxlast = indx-2
                    taskdata = res1['resultData'][-indxlast]
                    taskdatalast = res1['resultData'][-1]

                    filterfeedback = res1['resultData']

                    lastDate = taskdatalast['createDate']
                    date_str = lastDate

                    format_str = "%Y-%m-%d %H:%M:%S"

                    date = datetime.datetime.strptime(date_str, format_str)

                    year = date.year
                    month = date.month
                    day = date.day
                    hour = date.hour
                    minute = date.minute
                    second = date.second

                    date1 = datetime.datetime(year, month, day, hour, minute, second)
                    date2 = datetime.datetime.now()
                    difference = date2 - date1
                    days = difference.days
                    hours = difference.seconds / 3600

                    tixfeedbacks = []
                    for feed in filterfeedback:
                        if feed['operTypeName'] == 'Feedback':

                            fcreator = feed['operStaffName']
                            fdate = feed['createDate']
                            fremarks = feed['handleResult']

                            feed_add = {'fcreator':fcreator,
                                        'fdate': fdate,
                                        'fremarks': fremarks }
                            
                            tixfeedbacks.append(feed_add)






                    if str(taskdata.get('operStaffId')) == str(staffID):  
    
                        if status in second_line_status:
                                # {
                                #    "month": monthwithday,
                                #    "tickets": 
                                #             [{  "Ticket": tix, 
                                #                 "handler": handler, 
                                #                 "orgName": orgName, 
                                #                 "handlerorg" : handlerorg
                                #             }]
                                #             }

                            add_sl = {
                                'ticket':tix,
                                'feedback': tixfeedbacks,
                                'status':status,
                                'days':days,
                                'hours':hour
                                }
                            all_secondline_status.append(add_sl)




                        elif status in confirmstatus:
                            add_co = {
                                'ticket':tix,
                                'feedback': tixfeedbacks,
                                'status':status,
                                'days':days,
                                'hours':hour
                                }
                            all_confirm_status.append(add_co)


            else:
                print("")


        print('All Second Line:')
        for item in all_secondline_status:
            print(item['ticket'],"-",str(item['days'])+"d "+str(item['hours'])+"h since LAST activity/follow-up on ticket")
            if len(item['feedback']) > 0:
                lastfeed = item['feedback'][-1]
                remarks = lastfeed['fremarks'][17::]
                print("*******>>",lastfeed['fdate'],"-[",lastfeed['fcreator'],"]-",remarks)
                print("")


        print("")
        print("")
        print("")
        print('All Pending:')
        for item in all_confirm_status:
            print(item['ticket'],"-",str(item['days'])+"d "+str(item['hours'])+"h since LAST activity/follow-up on ticket")
            if len(item['feedback']) > 0:
                lastfeed = item['feedback'][-1]
                remarks = lastfeed['fremarks'][17::]
                print("*******>>",lastfeed['fdate'],"-",lastfeed['fcreator'],"-",remarks)
                print("")

            

        


        
