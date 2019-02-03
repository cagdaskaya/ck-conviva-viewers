import requests
import json
from flask import Flask, render_template, request, url_for, redirect
from helper import prettify_date, prettify_time


def accounts_query():
    related = {}
    url = "https://api.conviva.com/insights/2.4/accounts.json"
    headers = {
        'Authorization': "Basic ***REMOVED***",
        'cache-control': "no-cache",
    }

    response = json.loads(requests.request("GET", url, headers=headers).text)['accounts']
    related['NowTV'] = response['c3.BSkyB-NowTV']
    related['SkyGo'] = response['c3.BSkyB']
    return related


def api_query(viewer_id):
    global accounts
    # accounts = accounts_query()
    for k, v in accounts.items():
        url = "https://api.conviva.com/insights/2.4/viewer/views.json"
        querystring = {
            "viewer_id": viewer_id,
            "account": v
        }
        headers = {
            'Authorization': "Basic ***REMOVED***",
            'cache-control': "no-cache",
        }

        response = requests.request("GET", url, headers=headers, params=querystring)
        sessions_list = json.loads(response.text)['sessions']  # list
        if sessions_list:
            sessions_dict = {n: s for n, s in enumerate(sessions_list)}  # dict
            return sessions_dict, k
    else:
        return {}, 'no'


app = Flask(__name__)


@app.route('/')
def index_func():
    return render_template('index.html')


# This route will be arrived at looking like this:
# 127.0.0.1:5000/sessions
# It will also have some inner data as part of the payload (which is hidden), containing the data in the form.
@app.route('/sessions', methods=['POST'])
def create():
    viewer_id = request.form.get('viewer_id')
    return redirect(url_for('sessions_func', viewer_id=viewer_id))


@app.route('/sessions/<string:viewer_id>')
def sessions_func(viewer_id):
    global sessions
    sessions, acct = api_query(viewer_id)
    asset_set = {d['asset'] for d in sessions.values()}
    vsfs = [d['isPlayStartFail'] for d in sessions.values() if d['isPlayStartFail']]
    ebvs = [d['joinTimeMs'] for d in sessions.values() if (d['joinTimeMs'] < 0 and d['playTimeMs'] == 0 and not d['isPlayStartFail'])]
    play_d = prettify_time(sum([d['playTimeMs'] for d in sessions.values()]))
    # os_list = [d['os'] for d in sessions.values()]
    # os_set = {d['os'] for d in sessions.values()}
    os_p = [(round((100 * [d['os'] for d in sessions.values()].count(i) / len([d['os'] for d in sessions.values()]))), i) for i in {d['os'] for d in sessions.values()}]
    loc_p = [(round((100 * [d['city'] for d in sessions.values()].count(i) / len([d['city'] for d in sessions.values()]))), i) for i in {d['city'] for d in sessions.values()}]
    isp_p = [(round((100 * [d['isp'] for d in sessions.values()].count(i) / len([d['isp'] for d in sessions.values()]))), i) for i in {d['isp'] for d in sessions.values()}]
    return render_template('sessions.html', sessions=sessions, prettify_date=prettify_date, os_p=os_p, loc_p=loc_p,
                           prettify_time=prettify_time, round=round, viewer_id=viewer_id, ebvs=ebvs, isp_p=isp_p,
                           len=len, acct=acct, list=list, asset_set=asset_set, vsfs=vsfs, play_d=play_d)


@app.route('/session/<int:session_id>')
def session_function(session_id):
    session = sessions.get(session_id)
    tags = session['tags']
    request_id = (session['streamUrl'].split('c3.ri=')[1]) if len(session['streamUrl'].split('c3.ri=')) > 1 else 'no c3.ri'
    start_time = prettify_date(session['startTimeMs'])
    end_time = prettify_date(session['startTimeMs'] + session['joinTimeMs'] + session['playTimeMs'] + session['buffTimeMs'])
    play_time = prettify_time(session['playTimeMs'])
    buff_ratio = (round(100 * (session['buffTimeMs'] / (session['playTimeMs'] + session['buffTimeMs'])), 2)) if (session['playTimeMs'] + session['buffTimeMs']) > 0 else 'no_play'
    abr = round(session['avgBitrateKbps'] / 1024, 2)
    vst = round(session['joinTimeMs'] / 1000, 2)
    if not session:
        return render_template('404.html', message=f'A session with id {session_id} was not found.')
    return render_template('session.html', session=session, request_id=request_id, start_time=start_time, end_time=end_time,
                           buff_ratio=buff_ratio, abr=abr, play_time=play_time, vst=vst, tags=tags)


accounts = accounts_query()

if __name__ == '__main__':
    app.run(debug=True)
