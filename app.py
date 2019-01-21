import requests
import json
import datetime
from flask import Flask, render_template, request, url_for, redirect

url = "https://api.conviva.com/insights/2.4/viewer/views.json"
querystring = {"viewer_id": "4f18f7b5e8e6bcc8fbed5448002ea0ee5c70dc0d"}
headers = {
    'Authorization': "Basic Y2FnZGFzLmtheWFAc2t5LnVrOkhpTG9jay5NYXJrMDE=",
    'cache-control': "no-cache",
}

response = requests.request("GET", url, headers=headers, params=querystring)
sessions = json.loads(response.text)['sessions']  # list
sessions = {n: s for n, s in enumerate(sessions)}  # dict

app = Flask(__name__)

# '''
#test

@app.route('/')
def home():
    return render_template('home.jinja2', sessions=sessions)


@app.route('/session/<int:session_id>')
def session_function(session_id):
    session = sessions.get(session_id)
    request_id = session['streamUrl'].split('=')[1]
    start_time = datetime.datetime.fromtimestamp(session['startTimeMs'] / 1000, datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S %Z")
    end_time = datetime.datetime.fromtimestamp((session['startTimeMs'] + session['joinTimeMs'] + session['playTimeMs'] + session['buffTimeMs']) / 1000,
                                               datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S %Z")
    buff_ratio = round(100 * (session['buffTimeMs'] / (session['playTimeMs'] + session['buffTimeMs'])), 2)
    abr = round(session['avgBitrateKbps'] / 1024, 2)
    if not session:
        return render_template('404.jinja2', message=f'A session with id {session_id} was not found.')
    return render_template('session.jinja2', session=session, request_id=request_id, start_time=start_time, end_time=end_time, buff_ratio=buff_ratio, abr=abr)


if __name__ == '__main__':
    app.run(debug=True)
# '''
