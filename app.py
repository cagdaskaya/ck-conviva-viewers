import requests
import json
# import datetime
from flask import Flask, render_template, request, url_for, redirect
from helper import prettify_date, prettify_time


# '''

def api_query(viewer_id="4f18f7b5e8e6bcc8fbed5448002ea0ee5c70dc0d"):
    url = "https://api.conviva.com/insights/2.4/viewer/views.json"
    querystring = {
        "viewer_id": viewer_id,
        "account": "f5095ff483b5a703a5f6247daf180f9a9f93aa1b"
    }
    headers = {
        'Authorization': "Basic ***REMOVED***",
        'cache-control': "no-cache",
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    sessions_list = json.loads(response.text)['sessions']  # list
    sessions_dict = {n: s for n, s in enumerate(sessions_list)}  # dict
    return sessions_dict


app = Flask(__name__)


@app.route('/')
def form():
    return render_template('create.jinja2')


# This route will be arrived at looking like this:
# 127.0.0.1:5000/sessions
# It will also have some inner data as part of the payload (which is hidden), containing the data in the form.
@app.route('/sessions', methods=['POST'])
def create():
    viewer_id = request.form.get('viewer_id')
    # print(viewer_id)
    return redirect(url_for('home', viewer_id=viewer_id))


@app.route('/sessions/<string:viewer_id>')
def home(viewer_id="4f18f7b5e8e6bcc8fbed5448002ea0ee5c70dc0d"):
    global sessions
    sessions = api_query(viewer_id)
    return render_template('home.jinja2', sessions=sessions, prettify_date=prettify_date, prettify_time=prettify_time, round=round,
                           viewer_id=viewer_id, len=len)


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
# '''
