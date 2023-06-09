import requests
import config



gsheet_path = config.gsheet_token_path
dt_key = config.dingtalk_token
dt_key_checker = config.dt_token_for_wfc


def send_ding(tix,sdnames,sdwhatsya,sdnumber,sdlastouch,sdnameoff,sdlasttouch,status,tminutes,tseconds,domaindata,sdavail):
    title = domaindata['title']
    domain = domaindata['tdomain']
    system = domaindata['system']
    print(domaindata)

    ding_token = dt_key
    sdnumbr = '+63-'+str(sdnumber)
    sdwhat = sdwhatsya
    sdstatus = sdlastouch
    tixstatus = status

    if sdwhat == "New":
        tixnum = tix
        wut = sdwhat
        title = domaindata['title']
        domain = domaindata['tdomain']
        system = domaindata['system']
        


        headers = {
            'Content-Type': 'application/json',
        }

        params = {
            'access_token': ding_token,
        }
        json_data = {
                    "at": {
                "atMobiles": [
                    sdnumbr],
                "atUserIds":[
                    ""
                ],
                "isAtAll": bool(False)
            },
            'msgtype': 'text',
            'text': {
                'content': f'[{wut}] OFM Ticket \n\nTicket: {tixnum}\n\nTitle: {title}\n\nSystem Domain: {domain}\nSystem:{system}\n\nStatus: {tixstatus}\nOn Que: {tminutes}m {tseconds}s\nPlease get the ticket.\n\n\n\nPlease get the ticket:',
            },
        }
        response = requests.post('https://oapi.dingtalk.com/robot/send', params=params, headers=headers, json=json_data,timeout=200)
        return print(response)



    if sdwhat == "Existing":
        tixnum = tix
        title = title
        owners = sdnames
        wut = sdwhat
        
  

        if sdstatus == "Available":

            headers = {
            'Content-Type': 'application/json',
        }

            params = {
            'access_token': ding_token,
        }

            json_data = {
                    "at": {
                "atMobiles":[
                    sdnumbr
                ],
                "atUserIds":[
                    ""
                ],
                "isAtAll": bool(False)
            },
            'msgtype': 'text',
            'text': {
                'content': f'[{wut}] OFM Ticket \n\nTicket: {tixnum}\n\nTitle: {title}\n\nSystem Domain: {domain}\nSystem:{system}\n\nStatus: {tixstatus}\n\nOwner: {owners}\n\nOn Que: {tminutes}m {tseconds}s\n\nPlease get the ticket',
            },
            }
            response = requests.post('https://oapi.dingtalk.com/robot/send', params=params, headers=headers, json=json_data,timeout=5)
            return print(response)


        if sdstatus == "Not Available":

            headers = {
            'Content-Type': 'application/json',
        }

            params = {
            'access_token': ding_token,
        }

            json_data = {
                    "at": {
                "atMobiles":[
                    sdnumbr
                ],
                "atUserIds":[
                    ""
                ],
                "isAtAll": bool(False)
            },
            'msgtype': 'text',
            'text': {
                'content': f'[{wut}] OFM Ticket\n\nTicket: {tixnum}\n\nTitle: {title}\nSystem Domain: {domain}\nSystem: {system}\n\nStatus: {tixstatus}\n\nOwner: {sdnameoff} [NOT AVAILABLE]\nLast Handler: {sdnames}\n\nOn Que: {tminutes}m {tseconds}s\n\nPlease get the ticket',
            },
            }
            response = requests.post('https://oapi.dingtalk.com/robot/send', params=params, headers=headers, json=json_data,timeout=120)
            return print(response)



def send_ding_open_tix(stringdata,stringdata2,data):
    headers = {
            'Content-Type': 'application/json',
        }

    params = {
            'access_token': dt_key_checker,
        }

    json_data = {
                    "at": {
                "atMobiles":[
                    ""  
                ],
                "atUserIds":[
                    ""
                ],
                "isAtAll": bool(data['mention'])
            },
            'msgtype': 'text',
            'text': {
                'content': data['date']+'\n\n--TEST--\nAll Open Tickets OFM \n'+stringdata+'\n\n\nWrong Flow:\n'+stringdata2+'\n\n\n\nRuntime: '+str(data['runtime']),
            },
        }
    response = requests.post('https://oapi.dingtalk.com/robot/send', params=params, headers=headers, json=json_data,timeout=120)
    return print(response)



def send_ding_error(_error_):
    headers = {
            'Content-Type': 'application/json',
        }

    params = {
            'access_token': dt_key_checker,
        }

    json_data = {
                    "at": {
                "atMobiles":[
                
                ],
                "atUserIds":[
                    ""
                ],
                "isAtAll": bool(False)
            },
            'msgtype': 'text',
            'text': {
                'content':'OFM\n\n'+_error_,
            },
        }
    response = requests.post('https://oapi.dingtalk.com/robot/send', params=params, headers=headers, json=json_data,timeout=200)
    return print(response)



def send_ding_error2(_error_):
    headers = {
            'Content-Type': 'application/json',
        }

    params = {
            'access_token': dt_key,
        }

    json_data = {
                    "at": {
                "atMobiles":[
                    ""
                ],
                "atUserIds":[
                    ""
                ],
                "isAtAll": bool(False)
            },
            'msgtype': 'text',
            'text': {
                'content':'Host Problem:\nError @'+str(_error_)+"\n\nPlease connect to VPN",
            },
        }
    response = requests.post('https://oapi.dingtalk.com/robot/send', params=params, headers=headers, json=json_data,timeout=120)
    return print(response)


def wrongflowsend(stringdata2,sdnumbers):
    headers = {
            'Content-Type': 'application/json',
        }
    params = {
            'access_token': dt_key,
        }

    json_data = {
                    "at": {
                "atMobiles":[
                    sdnumbers
                ],
                "atUserIds":[
                    ""
                ],
                "isAtAll": bool(False)
            },
            'msgtype': 'text',
            'text': {
                'content': f'OFM Wrong Flow:\n{stringdata2}\n\nPlease check.',
            },
        }
    response = requests.post('https://oapi.dingtalk.com/robot/send', params=params, headers=headers, json=json_data,timeout=120)
    return print(response)



