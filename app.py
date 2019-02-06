from flask import Flask, render_template, request, url_for, redirect
from helper import prettify_date, prettify_time, v_lister, v_setter, v_adder, calc_percentages
from querier import api_query

app = Flask(__name__)


@app.route('/')
def index_func():
    """
    This page should have login capability.
    :return:  renders homepage of flask template
    """
    return render_template('index.html')


@app.route('/sessions', methods=['POST'])
def create():
    """
    get viewer id string with post method from the search button and redirects to the sessions page.
    This route will be arrived at looking like this: 127.0.0.1:5000/sessions
    It will also have some inner data as part of the payload (which is hidden), containing the data in the form.
    :return:    redirects to the sessions page of flask template
    """
    viewer_id = request.form.get('viewer_id')
    return redirect(url_for('sessions_func', viewer_id=viewer_id))


@app.route('/sessions/<string:viewer_id>')
def sessions_func(viewer_id):
    """
    uses viewer id string to get all the related sessions data.
    uses the data to generate summary cards, a table with expendable rows for details.
    :param viewer_id: string
    :return:    renders sessions page of flask template
    """
    global sessions
    find_by = request.args.get('find_by')
    find = request.args.get('find')
    sessions, acct = api_query(viewer_id)
    session_list = sessions.values()
    asset_set = v_setter(session_list, 'asset')
    vsfs = [i for i in v_lister(session_list, 'isPlayStartFail') if i]
    ebvs = [d['asn'] for d in session_list if (d['playTimeMs'] == 0 and not d['isPlayStartFail'])]
    play_d = prettify_time(v_adder(session_list, 'playTimeMs'))
    os_p = calc_percentages(session_list, 'os')
    cdn_p = calc_percentages(session_list, 'cdn')
    loc_p = calc_percentages(session_list, 'city')
    isp_p = calc_percentages(session_list, 'isp')
    return render_template('sessions.html', sessions=sessions, prettify_date=prettify_date, os_p=os_p, loc_p=loc_p, find=find,
                           prettify_time=prettify_time, round=round, viewer_id=viewer_id, ebvs=ebvs, isp_p=isp_p, find_by=find_by,
                           len=len, acct=acct, list=list, asset_set=asset_set, vsfs=vsfs, play_d=play_d, cdn_p=cdn_p)


@app.route('/session/<string:viewer_id>/<int:session_id>')
def session_function(viewer_id, session_id):
    """
    a separate page for each session with same details.
    :param viewer_id: string
    :param session_id: integer
    :return:    renders per session details page of flask template
    """
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
                           buff_ratio=buff_ratio, abr=abr, play_time=play_time, vst=vst, tags=tags, viewer_id=viewer_id)


# @app.route('/test/<string:viewer_id>')
# def test_func(viewer_id):
#     """
#     test
#     :param viewer_id: string
#     :return:    renders sessions page of flask template
#     """
#     global sessions
#     find_by = request.args.get('find_by')
#     find = request.args.get('find')
#     sessions, acct = api_query(viewer_id)
#     session_list = sessions.values()
#     asset_set = v_setter(session_list, 'asset')
#     vsfs = [i for i in v_lister(session_list, 'isPlayStartFail') if i]
#     ebvs = [d['asn'] for d in session_list if (d['playTimeMs'] == 0 and not d['isPlayStartFail'])]
#     play_d = prettify_time(v_adder(session_list, 'playTimeMs'))
#     os_p = calc_percentages(session_list, 'os')
#     cdn_p = calc_percentages(session_list, 'cdn')
#     loc_p = calc_percentages(session_list, 'city')
#     isp_p = calc_percentages(session_list, 'isp')
#     return render_template('test.html', sessions=sessions, prettify_date=prettify_date, os_p=os_p, loc_p=loc_p, find_by=find_by,
#                            prettify_time=prettify_time, round=round, viewer_id=viewer_id, ebvs=ebvs, isp_p=isp_p, type=type,
#                            len=len, acct=acct, list=list, asset_set=asset_set, vsfs=vsfs, play_d=play_d, cdn_p=cdn_p, find=find)
#
#
if __name__ == '__main__':
    app.run(debug=True)
