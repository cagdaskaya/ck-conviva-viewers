import base64
import requests
import json
from decouple import config

'''
Create a `.env` file on app root directory and add your API Client Credentials per Conviva account:
ACCOUNT=<ClientID>:<ClientSecret>
e.g. NOWTV=your-now-api-id:your-now-secret
Then, decide whether to comment/uncomment api_secrets dictionary key-value pairs accordingly. 
'''
api_secrets = {
    'c3.BSkyB': config('SKYGO'),
    'c3.BSkyB-NowTV': config('NOWTV'),
    'c3.BSkyB-OTTI': config('NOWIE'),
    'c3.SkyIP-T01': config('SOIP_UK'),
    'c3.SkyIP-T02': config('SOIP_DE'),
    'c3.SkyIP-T03': config('SOIP_IT'),
    # 'c3.BSkyB-Test': config('SKYGO_TEST'),
    # 'c3.BSkyB-NowTV-Test': config('NOWTV_TEST'),
    # 'c3.SkyIP-T01-Test': config('SOIP_UK_TEST'),
    # 'c3.SkyIP-T02-Test': config('SOIP_DE_TEST'),
    # 'c3.SkyIP-T03-Test': config('SOIP_IT_TEST'),
    'c3.BSkyB-SkyStore': config('SKYSTORE')
}

def api_query(viewer_id):
    """
    Sends an https request with viewer ID as a search item.
    Feature update: take login parameters and generate auth header with Base64.
    :param viewer_id: string
    :return:    2 item tuple with dictionary of sessions and platform name as string.
                if there are no sessions empty dictionary and no as string
    """
    global api_secrets
    for account, secret in api_secrets.items():
        accounts_url = 'https://api.conviva.com/insights/2.4/accounts.json'
        views_url = 'https://api.conviva.com/insights/2.1/viewer/views.json'
        basic_auth = base64.b64encode(bytes(secret, 'utf-8')).decode('ascii')
        headers = {
            'Cache-Control': 'no-cache',
            'Authorization': f'Basic {basic_auth}'
        }
        account_id = list(
            json.loads(
                requests.request('GET', accounts_url, headers=headers).text
            )['accounts'].values()
        )[0]
        querystring = {
            'viewer_id': viewer_id,
            'account': account_id
        }
        response = requests.request('GET', views_url, headers=headers, params=querystring)
        try:
            sessions_list = json.loads(response.text)['sessions']  # list
        except Exception:
            sessions_list = []
        if sessions_list:
            sessions_dict = {n: s for n, s in enumerate(sessions_list)}  # dict
            return sessions_dict, account
    else:
        return {}, 'no'
