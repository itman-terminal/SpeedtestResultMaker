import json
import datetime
from hashlib import md5
from urllib.parse import parse_qs
from requests import Request, Session
import requests
url = "https://www.speedtest.net/api/js/servers"
response = requests.get(url)
data = json.loads(response.text)

class SpeedtestResults(object):
    def __init__(self, download=0, upload=0, ping=0, jitter=0, server=None, client=None,
                 secure=False):
        self.download = download
        self.upload = upload
        self.ping = ping
        self.jitter = jitter
        if server is None:
            self.server = {}
        else:
            self.server = server
        self.client = client or {}

        self._share = None
        self.timestamp = '%sZ' % datetime.datetime.utcnow().isoformat()
        self.bytes_received = 0
        self.bytes_sent = 0

        self._secure = secure
        self._session = Session()

    def share(self):
        if self._share:
            return self._share

        download = int(round(self.download / 1000.0, 0))
        ping = int(round(self.ping, 0))
        upload = int(round(self.upload / 1000.0, 0))
        jitter = int(round(self.jitter, 0))

        api_data = [
            ('recommendedserverid', self.server['id']),
            ('ping', ping),
            ('jitter', jitter),
            ('screenresolution', ''),
            ('promo', ''),
            ('download', download),
            ('screendpi', ''),
            ('upload', upload),
            ('testmethod', 'http'),
            ('hash', md5(('%s-%s-%s-%s' %
                         (ping, upload, download, '297aae72'))
                        .encode()).hexdigest()),
            ('touchscreen', 'none'),
            ('startmode', 'pingselect'),
            ('accuracy', '1'),
            ('bytesreceived', self.bytes_received),
            ('bytessent', self.bytes_sent),
            ('serverid', self.server['id']),
        ]

        headers = {'Referer': 'http://c.speedtest.net/flash/speedtest.swf'}
        url = 'http://www.speedtest.net/api/api.php' if not self._secure else 'https://www.speedtest.net/api/api.php'
        req = Request('POST', url, data=api_data, headers=headers)
        prepped = self._session.prepare_request(req)
        resp = self._session.send(prepped)

        if resp.status_code == 200:
            qsargs = parse_qs(resp.text)
            resultid = qsargs.get('resultid')
            if resultid and len(resultid) == 1:
                self._share = 'http://www.speedtest.net/result/%s.png' % resultid[0]
                return self._share
        return None

def submit_custom_results():

    server_id = int(input("Enter server ID: "))
    download_speed = float(input("Enter download speed (Mbps): "))
    upload_speed = float(input("Enter upload speed (Mbps): "))
    ping_latency = float(input("Enter ping latency (ms): "))
    jitter = float(input("Enter jitter (ms): "))

    results = SpeedtestResults(
        download=download_speed * 1000000,
        upload=upload_speed * 1000000,
        ping=ping_latency,
        jitter=jitter,
        server={
            "id": server_id,
            "sponsor": "Example Sponsor",
            "name": "Example Server"
        },
        client={
            "ip": "185.206.249.178"
        }
    )

    share_link = results.share()
    if share_link:
        print(f"Speedtest results shared: {share_link}")
    else:
        print(f"Failed to submit results to speedtest.net:{e}")

if __name__ == "__main__":
    for server in data:
        print(f"URL: {server['url']}")
        print(f"Latitude: {server['lat']}")
        print(f"Longitude: {server['lon']}")
        print(f"Distance: {server['distance']}")
        print(f"Name: {server['name']}")
        print(f"Country: {server['country']}")
        print(f"Country Code: {server['cc']}")
        print(f"Sponsor: {server['sponsor']}")
        print(f"ID: {server['id']}")
        print(f"Preferred: {server['preferred']}")
        print(f"HTTPS Functional: {server['https_functional']}")
        print(f"Host: {server['host']}")
        print()

    submit_custom_results()
