import requests
import argparse
import sys
import hashlib

headers = {
    'User-Agent': 'DrWhat Speedtest',
    'Origin': 'https://c.speedtest.net',
    'Referer': 'https://c.speedtest.net/flash/speedtest.swf'
}

# 添加命令行参数解析
parser = argparse.ArgumentParser(description='Speedtest CLI')
parser.add_argument('--server-id', type=int, required=True, help='Server ID')
parser.add_argument('--ping', type=int, required=True, help='Ping value (ms)')
parser.add_argument('--download', type=int, required=True, help='Download speed (bps)')
parser.add_argument('--upload', type=int, required=True, help='Upload speed (bps)')
args = parser.parse_args()

payload = {
    'startmode': 'recommendedselect',
    'promo': '',
    'accuracy': '8',
    'serverid': args.server_id,
    'recommendedserverid': args.server_id,
    'upload': args.upload,
    'download': args.download,
    'ping': args.ping
}

h = hashlib.md5()
h.update(("%d-%d-%d-297aae72" % (payload['ping'], payload['upload'], payload['download'])).encode('utf-8'))
payload['hash'] = h.hexdigest()

r = requests.post('http://www.speedtest.net/api/api.php', data=payload, headers=headers)
print(r.text)
resultid = r.text.split('&')[1].split('=')[1]

print("https://www.speedtest.net/my-result/" + str(resultid))
