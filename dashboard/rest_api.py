# From : http://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask
from common import REDIS_POOL, config, root_dir, redis_key_template
from common.records import SeverityRecord
from common.graphs import SessionGraph
from flask import Flask, jsonify, send_file, render_template, make_response
from functools import update_wrapper
import cPickle as pickle
import redis
import os
import re

r_db = redis.Redis(connection_pool=REDIS_POOL)
app = Flask('OrionDashboard')


def nocache(f):
    def new_func(*args, **kwargs):
        resp = make_response(f(*args, **kwargs))
        resp.cache_control.no_cache = True
        return resp
    return update_wrapper(new_func, f)


# index page
@app.route('/')
def index():
    return render_template('index.html')
    pass


# get traffic summary
@app.route('/heimdall/api/v1.0/traffic_summary', methods=['GET'])
@nocache
def get_traffic_summary():
    try:
        keys = r_db.keys('*type::severity*')
        sessions = [pickle.loads(record) for record in r_db.mget(keys)]
    except Exception, e:
        sessions = []
    return jsonify({
        'status': 'success',
        'code': 200,
        'data': sessions
    }), 200


# get activity of a ip
@app.route('/heimdall/api/v1.0/ip_summary/<ip>', methods=['GET'])
@nocache
def get_ip_summary(ip):
    sr = SeverityRecord(ip)
    record = r_db.get(redis_key_template.format(ip, "factors", None))
    if record:
        fv_map = pickle.loads(record)
    else:
        fv_map = {"No Values": "No Values"}

    factors = []
    for f_key, f_val in fv_map.items():
        factors.append({
            'key': " ".join([a for a in re.split(r'([A-Z]+[a-z]*)', f_key) if a]),
            'value': f_val
        })
        pass

    sr['factors'] = factors
    sr['request_graph'] = "/heimdall/api/v1.0/request_graph/{0}".format(ip)

    return jsonify({
        'status': 'success',
        'code': 200,
        'data': sr
    }), 200


# ban IP
@app.route('/heimdall/api/v1.0/ban_ip/<ip>', methods=['PUT'])
@nocache
def ban_ip(ip):
    sr = SeverityRecord(ip)
    sr.ban()
    return jsonify({
        'status': 'success',
        'code': 200,
    }), 200


# un ban IP
@app.route('/heimdall/api/v1.0/unban_ip/<ip>', methods=['PUT'])
@nocache
def unban_ip(ip):
    sr = SeverityRecord(ip)
    sr.unban()
    return jsonify({
        'status': 'success',
        'code': 200,
    }), 200


# get request graph
@app.route('/heimdall/api/v1.0/request_graph/<ip>', methods=['GET'])
@nocache
def get_request_graph(ip):
    sg = SessionGraph(ip)
    sg.print_graph()
    path = os.path.join(root_dir, "generated", "graphs", "{0}_c_g.png".format(ip))
    return send_file(path, mimetype='image/png')


if __name__ == '__main__':
    app.run(
        host=config.dashboard.get('host', '127.0.0.1'),
        port=config.dashboard.get('port', '9090'),
        debug=True
    )