import requests
import re
import sys


def get_rss_url_from_channel_url(url, header):
    d = requests.get(url, headers=header)
    if d.status_code == 200:
        x = re.search('externalId":"([^\"]*)"', d.text)
        return "https://www.youtube.com/feeds/videos.xml?channel_id={}".format(x.group(1))
    return None

header = {
    "Cookie": sys.argv[2],  # Needs the CONSENT Cookie value else a cookie accept site is shown
}

for l in open(sys.argv[1]):
    if l:
        print(get_rss_url_from_channel_url(l.strip(), header))
