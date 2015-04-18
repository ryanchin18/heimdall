# From : http://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask
from common import REDIS_POOL, config, redis_key_template
from common.records import SeverityRecord
from common.graphs import SessionGraph
from flask import Flask, jsonify
from modeller.factors import *
import cPickle as pickle
import redis

r_db = redis.Redis(connection_pool=REDIS_POOL)
app = Flask(__name__)

# get traffic summary
@app.route('/orion/api/v1.0/traffic_summary', methods=['GET'])
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
@app.route('/orion/api/v1.0/ip_summary/<string:ip>', methods=['GET'])
def get_ip_summary(ip):
    sg = SessionGraph(ip)
    sr = SeverityRecord(ip)

    factors = {}
    for Factor in BaseFactor.__subclasses__():
        factor = Factor(None, None, None)
        key = factor._FACTOR_KEY
        factors[key] = sg.get_graph_property(key)
        pass

    sr['factors'] = factors
    sr['request_graph'] = "generated/{0}_c_g.png".format(ip)

    return jsonify({
        'status': 'success',
        'code': 200,
        'data': sr
    }), 200


# ban IP
@app.route('/todo/api/v1.0/ban_ip/<string:ip>', methods=['PUT'])
def ban_ip(ip):
    sr = SeverityRecord(ip)
    sr.ban()
    return jsonify({
        'status': 'success',
        'code': 200,
    }), 200


# un ban IP
@app.route('/todo/api/v1.0/unban_ip/<string:ip>', methods=['PUT'])
def unban_ip(ip):
    sr = SeverityRecord(ip)
    sr.unban()
    return jsonify({
        'status': 'success',
        'code': 200,
    }), 200


# get request graph
@app.route('/todo/api/v1.0/request_graph/<string:ip>', methods=['GET'])
def get_request_graph(ip):
    return jsonify({
        'status': 'success',
        'code': 200,
        # 'data': sessions
    }), 200


if __name__ == '__main__':
    app.run(
        host=config.dashboard.get('host', '127.0.0.1'),
        port=config.dashboard.get('port', '9090'),
        debug=True
    )