## api.py

from flask import Flask, request, jsonify
from datetime import datetime
import os
from dotenv import load_dotenv
from requests import get, post, put, delete, patch

# Load environment variables
env_path = os.path.join(os.path.dirname(__file__), 'Keys', 'keys.env')
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)

# --- Helper functions (Honeygain API wrappers) ---
def create_user(email: str, password: str, coupon: str = ''):
    resp = post(
        'https://dashboard.honeygain.com/api/v1/users',
        json={'email': email, 'password': password, 'coupon': coupon}
    )
    return resp.json().get('data', {})


def gen_authcode(email: str, password: str):
    resp = post(
        'https://dashboard.honeygain.com/api/v1/users/tokens',
        json={'email': email, 'password': password}
    )
    return resp.json().get('data', {})


def fetch_aboutme(token: str):
    resp = get(
        'https://dashboard.honeygain.com/api/v1/users/me',
        headers={'Authorization': f'Bearer {token}'}
    )
    data = resp.json().get('data', {})
    # parse created_at
    data['created_at'] = datetime.strptime(
        data.get('created_at').replace('+00:00', 'Z'),
        '%Y-%m-%dT%H:%M:%SZ'
    )
    return data


def fetch_tosstatus(token: str):
    resp = get(
        'https://dashboard.honeygain.com/api/v1/users/tos',
        headers={'Authorization': f'Bearer {token}'}
    )
    return resp.json().get('data', {})


def fetch_trafficstats(token: str):
    resp = get(
        'https://dashboard.honeygain.com/api/v1/dashboards/traffic_stats',
        headers={'Authorization': f'Bearer {token}'}
    )
    data = resp.json().get('data', {})
    for entry in data.get('traffic_stats', []):
        entry['date'] = datetime.strptime(entry['date'], '%Y-%m-%d')
    return data


def fetch_balances(token: str):
    resp = get(
        'https://dashboard.honeygain.com/api/v1/users/balances',
        headers={'Authorization': f'Bearer {token}'}
    )
    return resp.json().get('data', {})


def fetch_devices(token: str, deleted: bool = False):
    appendix = '?deleted=true' if deleted else ''
    devices = []
    page = 1
    while True:
        resp = get(
            f'https://dashboard.honeygain.com/api/v1/devices{appendix}&page={page}',
            headers={'Authorization': f'Bearer {token}'}
        ).json()
        data = resp.get('data', [])
        devices.extend(data)
        meta = resp.get('meta', {}).get('pagination', {})
        if page >= meta.get('total_pages', 0):
            break
        page += 1
    return devices


def fetch_referrals(token: str):
    referrals, page = [], 1
    while True:
        resp = get(
            f'https://dashboard.honeygain.com/api/v1/referrals?page={page}',
            headers={'Authorization': f'Bearer {token}'}
        ).json()
        referrals.extend(resp.get('data', []))
        meta = resp.get('meta', {}).get('pagination', {})
        if page >= meta.get('total_pages', 0):
            break
        page += 1
    return referrals


def fetch_transactions(token: str):
    txs, page = [], 1
    while True:
        resp = get(
            f'https://dashboard.honeygain.com/api/v1/transactions?page={page}',
            headers={'Authorization': f'Bearer {token}'}
        ).json()
        for t in resp.get('data', []):
            t['booked_at'] = datetime.strptime(t['booked_at'], '%Y-%m-%d %H:%M:%S')
            t['created_at'] = datetime.strptime(t['created_at'], '%Y-%m-%d %H:%M:%S')
            txs.append(t)
        meta = resp.get('meta', {}).get('pagination', {})
        if page >= meta.get('total_pages', 0):
            break
        page += 1
    return txs


def chg_password(token: str, current: str, new: str):
    resp = put(
        'https://dashboard.honeygain.com/api/v1/users/passwords',
        headers={'Authorization': f'Bearer {token}'},
        json={'current_password': current, 'new_password': new}
    )
    return resp.status_code


def chg_devicename(token: str, device_id: str, title: str):
    resp = put(
        f'https://dashboard.honeygain.com/api/v1/devices/{device_id}/titles',
        headers={'Authorization': f'Bearer {token}'},
        json={'title': title}
    )
    return resp.status_code


def del_device(token: str, device_id: str):
    resp = delete(
        f'https://dashboard.honeygain.com/api/v1/devices/{device_id}',
        headers={'Authorization': f'Bearer {token}'}
    )
    return resp.status_code


def res_device(token: str, device_id: str):
    resp = patch(
        f'https://dashboard.honeygain.com/api/v1/devices/{device_id}',
        headers={'Authorization': f'Bearer {token}'},
        json={'deleted': False}
    )
    return resp.status_code

# --- Route definitions ---
@app.route('/auth/register', methods=['POST'])
def route_create_user():
    data = request.json or {}
    user = create_user(data.get('email'), data.get('password'), data.get('coupon', ''))
    return jsonify(user), 201

@app.route('/auth/token', methods=['POST'])
def route_gen_token():
    data = request.json or {}
    token = gen_authcode(data.get('email'), data.get('password'))
    return jsonify(token)

@app.route('/users/me', methods=['GET'])
def route_aboutme():
    token = request.headers.get('Authorization', '').split('Bearer ')[-1]
    return jsonify(fetch_aboutme(token))

@app.route('/users/tos', methods=['GET'])

def route_tos():
    token = request.headers.get('Authorization', '').split('Bearer ')[-1]
    return jsonify(fetch_tosstatus(token))

@app.route('/stats/traffic', methods=['GET'])
def route_traffic():
    token = request.headers.get('Authorization', '').split('Bearer ')[-1]
    return jsonify(fetch_trafficstats(token))

@app.route('/users/balances', methods=['GET'])
def route_balances():
    token = request.headers.get('Authorization', '').split('Bearer ')[-1]
    return jsonify(fetch_balances(token))

@app.route('/devices', methods=['GET'])
def route_devices():
    token = request.headers.get('Authorization', '').split('Bearer ')[-1]
    deleted = request.args.get('deleted', 'false').lower() == 'true'
    return jsonify(fetch_devices(token, deleted))

@app.route('/referrals', methods=['GET'])
def route_referrals():
    token = request.headers.get('Authorization', '').split('Bearer ')[-1]
    return jsonify(fetch_referrals(token))

@app.route('/transactions', methods=['GET'])
def route_transactions():
    token = request.headers.get('Authorization', '').split('Bearer ')[-1]
    return jsonify(fetch_transactions(token))

@app.route('/users/password', methods=['PUT'])
def route_change_password():
    token = request.headers.get('Authorization', '').split('Bearer ')[-1]
    data = request.json or {}
    status = chg_password(token, data.get('current_password'), data.get('new_password'))
    return '', status

@app.route('/devices/<string:device_id>/title', methods=['PUT'])
def route_change_devicename(device_id):
    token = request.headers.get('Authorization', '').split('Bearer ')[-1]
    data = request.json or {}
    status = chg_devicename(token, device_id, data.get('title'))
    return '', status

@app.route('/devices/<string:device_id>', methods=['DELETE'])
def route_delete_device(device_id):
    token = request.headers.get('Authorization', '').split('Bearer ')[-1]
    status = del_device(token, device_id)
    return '', status

@app.route('/devices/<string:device_id>/restore', methods=['PATCH'])
def route_restore_device(device_id):
    token = request.headers.get('Authorization', '').split('Bearer ')[-1]
    status = res_device(token, device_id)
    return '', status

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.getenv('PORT', 5320), debug=True)

