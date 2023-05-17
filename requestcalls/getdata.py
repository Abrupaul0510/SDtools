import requests
import config

sd_id = config.sd_id


def get_tix_details(ticketn):
    tixnumstrim = ticketn
    ticketnumber = tixnumstrim.strip()
    cookies = {
}

    headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'https://portal.dito.ph',
    'Referer': 'https://portal.dito.ph/portal-web/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'X-CSRF-TOKEN': '30d7be0b-8a27-4a2c-a1bd-ecb3720da833',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

    data = {
    'serviceName': 'ptoOrderServiceBean',
    'methodName': 'queryOrderMonitorList',
    'moduleName': 'taskflow',
    'param': '{"serviceName":"ptoOrderServiceBean","method":"queryOrderMonitorList","p0":"{\\"orderState\\":\\"UNFINISHED\\",\\"orderCode\\":\\"\\",\\"orderCodeOrTitle\\":\\"'+ticketnumber+'\\",\\"packageId\\":null,\\"pageIndex\\":1,\\"pageSize\\":20,\\"resetPage\\":true,\\"qryOrgRegion\\":null,\\"notTicketType\\":[\\"PNAT\\"]}"}',
}

    response = requests.post(
    'https://portal.dito.ph/oss-eoms-taskflow/executeService/execute.do',
    cookies=cookies,
    headers=headers,
    data=data,
)
    res = response.json()

    return res


def get_closed(ticketn):
    tixnumstrim = ticketn
    ticketnumber = tixnumstrim.strip()
    cookies = {
}

    headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'https://portal.dito.ph',
    'Referer': 'https://portal.dito.ph/portal-web/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'X-CSRF-TOKEN': '40c6b1e1-9d1a-4377-b5f5-7b0dcb1ee385',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

    data = {
    'serviceName': 'ptoOrderServiceBean',
    'methodName': 'queryOrderMonitorList',
    'moduleName': 'taskflow',
    'param': '{"serviceName":"ptoOrderServiceBean","method":"queryOrderMonitorList","p0":"{\\"orderState\\":\\"-1\\",\\"orderCode\\":\\"\\",\\"orderCodeOrTitle\\":\\"'+ticketnumber+'\\",\\"packageId\\":null,\\"pageIndex\\":1,\\"pageSize\\":20,\\"resetPage\\":true,\\"qryOrgRegion\\":null,\\"notTicketType\\":[\\"PNAT\\"]}"}',
}

    response = requests.post(
    'https://portal.dito.ph/oss-eoms-taskflow/executeService/execute.do',
    cookies=cookies,
    headers=headers,
    data=data,
)
    res = response.json()
    return res


def get_open_ticket(staffID):


    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'https://portal.dito.ph',
        'Referer': 'https://portal.dito.ph/portal-web/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'X-CSRF-TOKEN': 'b633e246-ec67-4e6c-b7e4-40670c593034',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
    data = {
        'serviceName': 'ptoWorkOrderServiceBean',
        'methodName': 'queryOrderByParam',
        'moduleName': 'taskflow',
        'param': '{"serviceName":"ptoWorkOrderServiceBean","method":"queryOrderByParam","p0":"{\\"operationType\\":\\"mytask-processed\\",\\"workOrderState\\":\\"10F\\",\\"isFinished\\":false,\\"sortList\\":[],\\"pageIndex\\":1,\\"orderState\\":null,\\"pageSize\\":100,\\"siteRoomCable\\":\\"\\",\\"staffId\\":'+staffID+',\\"workOrderTitle\\":\\"\\",\\"notTicketType\\":[\\"PNAT\\"]}"}',
    }
    response = requests.post(
        'https://portal.dito.ph/oss-eoms-taskflow/executeService/execute.do',
        headers=headers,
        data=data,
        timeout=200
    )

    res = response.json()

    return res



def open_ticket_closed(staffID,reqDate):

    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'https://portal.dito.ph',
        'Referer': 'https://portal.dito.ph/portal-web/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
        'X-CSRF-TOKEN': 'b0e0eace-1913-46f9-99ce-d4bd36e0ac7b',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    data = {
        'serviceName': 'ptoWorkOrderServiceBean',
        'methodName': 'queryOrderByParam',
        'moduleName': 'taskflow',                                                                                                                                                                   #2023-05-16
        'param': '{"serviceName":"ptoWorkOrderServiceBean","method":"queryOrderByParam","p0":"{\\"operationType\\":\\"mytask-processed\\",\\"workOrderState\\":\\"10F\\",\\"startCreateTime\\":\\"'+reqDate+' 00:00:00\\",\\"endCreateTime\\":\\"'+reqDate+' 23:59:59\\",\\"isFinished\\":true,\\"sortList\\":[],\\"pageIndex\\":1,\\"orderState\\":null,\\"pageSize\\":100,\\"siteRoomCable\\":\\"\\",\\"staffId\\":'+staffID+',\\"workOrderTitle\\":\\"\\",\\"notTicketType\\":[\\"PNAT\\"]}"}',
    }

    response = requests.post(
        'https://portal.dito.ph/oss-eoms-taskflow/executeService/execute.do',
        headers=headers,
        data=data,
        timeout=200
    )

    res = response.json()

    return res



def get_task_order(orderIDs,shardingKey):


    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'https://portal.dito.ph',
        'Referer': 'https://portal.dito.ph/portal-web/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'X-CSRF-TOKEN': '97f3e7e3-c9a2-4a57-b613-19fea5339bd5',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    data = {
        'serviceName': 'ossOperRecordServiceBean',
        'methodName': 'selectOssOperRecordByMap',
        'moduleName': 'taskflow',
        'param': '{"serviceName":"ossOperRecordServiceBean","method":"selectOssOperRecordByMap","p0":"{\\"orderId\\":'+orderIDs+',\\"shardingKey\\":'+shardingKey+'}"}',
    }

    response = requests.post(
        'https://portal.dito.ph/oss-eoms-taskflow/executeService/execute.do',
        headers=headers,
        data=data,
    timeout=200)
    res = response.json()

    return res


def check_ticket_count():

    cookies =  {}
 
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'https://portal.dito.ph',
        'Referer': 'https://portal.dito.ph/portal-web/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        'X-CSRF-TOKEN': '669fc550-0ba9-4d60-ad2b-f18e0498a038',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    data = {
        'serviceName': 'ptoWorkOrderServiceBean',
        'methodName': 'queryOrderByParam',
        'operator': '',
        'moduleName': 'taskflow',
        'param': '{"serviceName":"ptoWorkOrderServiceBean","method":"queryOrderByParam","p0":"{\\"operationType\\":\\"mytask-todo\\",\\"sortList\\":[],\\"staffId\\":'+sd_id+',\\"partyId\\":'+sd_id+',\\"partyOrgId\\":12012,\\"workOrderTitle\\":\\"\\",\\"timeoutFlag\\":\\"01\\",\\"pageIndex\\":1,\\"pageSize\\":20,\\"notTicketType\\":[\\"PNAT\\"]}"}',
    }

    response = requests.post(
        'https://portal.dito.ph/oss-eoms-taskflow/executeService/execute.do',
        cookies=cookies,
        headers=headers,
        data=data,
    )
    rawdata = response.json()

    resultdata = rawdata

    return resultdata['resultData']


def getmore_details_request(recordID):
    cookies = {
       
    }

    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Referer': 'https://portal.dito.ph/portal-web/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
        'X-CSRF-TOKEN': 'eddc1774-87d2-4d3f-908d-218f37854eb8',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    data = {
        'serviceName': 'dynamicFormServiceBean',
        'methodName': 'qryFormEleInstByOperRecordId',
        'operator': '',
        'moduleName': 'taskflow',
        'param': '{"serviceName":"dynamicFormServiceBean","method":"qryFormEleInstByOperRecordId","p0":"'+str(recordID)+'"}',
    }

    response = requests.post(
        'https://portal.dito.ph/oss-eoms-taskflow/executeService/execute.do',
        cookies=cookies,
        headers=headers,
        data=data,
    )


    
    res = response.json()

    return res

def tasklist(orderIDs):

    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'https://portal.dito.ph',
        'Referer': 'https://portal.dito.ph/portal-web/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
        'X-CSRF-TOKEN': '226cc00c-09ee-4732-9815-9ae2c30414b2',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    data = {
        'serviceName': 'ptoWorkOrderServiceBean',
        'methodName': 'queryWoWorkOrderList',
        'moduleName': 'taskflow',
        'param': '{"serviceName":"ptoWorkOrderServiceBean","method":"queryWoWorkOrderList","p0":"{\\"orderId\\":'+orderIDs+'}"}',
    }

    response = requests.post(
        'https://portal.dito.ph/oss-eoms-taskflow/executeService/execute.do',
        headers=headers,
        data=data,
    )

    rawdata = response.json()

    resultdata = rawdata

    return resultdata['resultData']
