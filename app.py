import requests
import json
from flask import Flask, render_template, request, url_for, redirect
from helper import prettify_date, prettify_time


def accounts_query():
    related = {}
    url = "https://api.conviva.com/insights/2.4/accounts.json"
    headers = {
        'Authorization': "Basic Y2FnZGFzLmtheWFAc2t5LnVrOkhpTG9jay5NYXJrMDE=",
        'cache-control': "no-cache",
    }

    response = json.loads(requests.request("GET", url, headers=headers).text)['accounts']
    related['NowTV'] = response['c3.BSkyB-NowTV']
    related['SkyGo'] = response['c3.BSkyB']
    return related


def api_query(viewer_id):
    accounts = accounts_query()
    for k, v in accounts.items():
        url = "https://api.conviva.com/insights/2.4/viewer/views.json"
        querystring = {
            "viewer_id": viewer_id,
            "account": v
        }
        headers = {
            'Authorization': "Basic Y2FnZGFzLmtheWFAc2t5LnVrOkhpTG9jay5NYXJrMDE=",
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
    return render_template('index.jinja2')


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
    return render_template('sessions.jinja2', sessions=sessions, prettify_date=prettify_date, prettify_time=prettify_time, round=round,
                           viewer_id=viewer_id, len=len, acct=acct)


@app.route('/session/<int:session_id>')
def session_function(session_id):
    session = sessions.get(session_id)
    tags = session['tags']
    request_id = (session['streamUrl'].split('=')[1]) if len(session['streamUrl'].split('=')) > 1 else 'no c3.ri'
    start_time = prettify_date(session['startTimeMs'])
    end_time = prettify_date(session['startTimeMs'] + session['joinTimeMs'] + session['playTimeMs'] + session['buffTimeMs'])
    play_time = prettify_time(session['playTimeMs'])
    buff_ratio = (round(100 * (session['buffTimeMs'] / (session['playTimeMs'] + session['buffTimeMs'])), 2)) if (session['playTimeMs'] + session['buffTimeMs']) > 0 else 'no_play'
    abr = round(session['avgBitrateKbps'] / 1024, 2)
    vst = round(session['joinTimeMs'] / 1000, 2)
    if not session:
        return render_template('404.jinja2', message=f'A session with id {session_id} was not found.')
    return render_template('session.jinja2', session=session, request_id=request_id, start_time=start_time, end_time=end_time,
                           buff_ratio=buff_ratio, abr=abr, play_time=play_time, vst=vst, tags=tags)


if __name__ == '__main__':
    app.run(debug=True)

