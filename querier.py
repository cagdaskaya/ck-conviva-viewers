import base64
import requests
import json

# username = input('Conviva username: ')
# password = input('Conviva password: ')
# credentials = username + ':' + password
# credentials = input('Conviva username: ') + ':' + input('Conviva password: ')
# encoded = base64.b64encode(bytes(credentials, 'utf-8')).decode('ascii')
encoded = 'WExCZkVpUm9IRDg3ZlF1a3ExTFVLUDo4YVZ2aFFHZkV1N3VqZFNkbVV6b0pNMm16RjNTMVBoN3NXZU1xQXdLNFRXVA=='
headers = {'Cache-Control': 'no-cache', 'Authorization': f'Basic {encoded}'}
encoded_go = 'NU1YcWRrY2ZoaUQzSDhnTnBzUk1HMjoza2pTQWJNR2pyemEzRnUxOUdyTFU5a2FLaTRQaHMyZXNwTVNpdG5BQlk0Vw==' # fix later
headers_go = {'Cache-Control': 'no-cache', 'Authorization': f'Basic {encoded_go}'} # fix later


def accounts_query():
    """
    Sends an https request for NowTV and SkyGo account IDs.
    :return:    dictionary of platform names as key and account ids as values
    """
    related = {}
    url = "https://api.conviva.com/insights/2.4/accounts.json"
    response = json.loads(requests.request("GET", url, headers=headers).text)['accounts']
    response_go = json.loads(requests.request("GET", url, headers=headers_go).text)['accounts'] # fix later
    related['NowTV'] = response['c3.BSkyB-NowTV']
    related['SkyGo'] = response_go['c3.BSkyB'] # fix later
    return related


accounts = accounts_query()


def api_query(viewer_id):
    """
    Sends an https request with viewer ID as a search item. Uses accounts dictionary to search as a loop.
    Feature update: take login parameters and generate auth header with Base64.
    :param viewer_id: string
    :return:    2 item tuple with dictionary of sessions and platform name as string.
                if there are no sessions empty dictionary and no as string
    """
    # accounts = accounts_query()
    global accounts
    for k, v in accounts.items():
        url = 'https://api.conviva.com/insights/2.1/viewer/views.json'
        querystring = {
            'viewer_id': viewer_id,
            'account': v
        }
        response = requests.request('GET', url, headers=headers, params=querystring)
        if k == 'NowTV': # fix later
            response = requests.request('GET', url, headers=headers, params=querystring) # fix later
        elif k == 'SkyGo': # fix later
            response = requests.request('GET', url, headers=headers_go, params=querystring) # fix later
        sessions_list = json.loads(response.text)['sessions']  # list
        if sessions_list:
            sessions_dict = {n: s for n, s in enumerate(sessions_list)}  # dict
            return sessions_dict, k
    else:
        return {}, 'no'

