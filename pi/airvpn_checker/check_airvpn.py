import argparse
import requests
import warnings


def get_airvpn_status(vpn_api_token, expected_session_count):
    url = 'https://airvpn.org/api/'
    exit_code = 0

    resp = requests.get(url, params={'service': 'userinfo',
                                     'format': 'json',
                                     'key': vpn_api_token})
    try:
        resp.raise_for_status()
    except requests.HTTPError as e:
        message_text = 'Exception when getting status: {}'.format(e)
        exit_code = 2
        return message_text, exit_code

    data = resp.json()
    message_text = 'Sessions currently connected: ' + ",".join([d['device_name'] for d in data['sessions']])
    if len(data['sessions']) < expected_session_count:
        exit_code = 2
    return message_text, exit_code

def submit_check(vpn_api_token, expected_session_count, passive_check_endpoint, token, hostname):
    status_text, exit_code = get_airvpn_status(vpn_api_token, expected_session_count)
    submit_cmd = "PROCESS_SERVICE_CHECK_RESULT;{};AirVPN Status;{};{}".format(hostname, exit_code, status_text)

    with warnings.catch_warnings():
        # ignore the SSL related warning as this is internal
        warnings.simplefilter("ignore")
        _ = requests.get(passive_check_endpoint, verify=False, params={'token': token,
                                                                       'cmd': 'submitcmd',
                                                                       'command': submit_cmd})

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--vpn-api-token', type=str, help="VPN API token")
    parser.add_argument('--expected-session-count', type=int, default=2, help="number of sessions to expect")
    parser.add_argument('--submit-check-url', type=str, help="Nagios passive check url")
    parser.add_argument('--token', type=str, help="Nagios passive check token")
    parser.add_argument('--hostname', type=str, help="Nagios passive check url")
    args = parser.parse_args()

    submit_check(args.vpn_api_token, args.expected_session_count, args.submit_check_url, args.token, args.hostname)
