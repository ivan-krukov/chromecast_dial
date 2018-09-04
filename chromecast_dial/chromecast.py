from urllib.request import Request, urlopen
from urllib.parse import urlparse, urlencode
from urllib.error import HTTPError
import xml.etree.ElementTree as ET

from .dial_protocol_defs import DIAL

def _xml_find(el, query, ns=DIAL.NS_UPNP_DEVICE):
    return el.find(ns+query)

class ChromeCast:

    def __init__(self, root):
        self.url_base = _xml_find(root, 'URLBase').text
        url = urlparse(self.url_base)
        self.addr = url.hostname
        self.port = url.port
        self.config_path = url.path

        spec_version = _xml_find(root, 'specVersion')
        self.spec = (_xml_find(spec_version, 'major').text,
                     _xml_find(spec_version, 'minor').text)

        device = _xml_find(root, 'device')
        self.friendly_name = _xml_find(device, 'friendlyName').text
        self.model_name = _xml_find(device, 'modelName').text
        self.udn = _xml_find(device, 'UDN').text

    def __repr__(self):
        return f'{self.model_name} ({self.friendly_name}) at {self.addr}:{self.port}'

    def app_url(self, app):
        return f'http://{self.addr}:{self.port}/apps/{app}'

    def _query_app(self, app, data = None, method = 'GET'):
        headers = {'Content-Lenght': 0} if data else {}

        req = Request(self.app_url(app),
                      headers = headers, data = data, method = method)
        resp_data = ''
        with urlopen(req) as resp:
            resp_data = resp.read()
        return (resp, resp_data)

    def app_status(self, app):
        status = 'Unknown'
        try:
            resp, data = self._query_app(app)
        except HTTPError:
            return 'App not found'

        if resp.status == 200:
            root = ET.fromstring(data)
            status = _xml_find(root, 'state', ns = DIAL.NS_DIAL).text

        return status

    def stop_app(self, app):
        try:
            resp, _ = self._query_app(app, method = 'DELETE')
        except HTTPError:
            return (404, 'No app running')
        return (resp.code, resp.reason)

    def post_youtube_video(self, video_id):
        data = urlencode({'v':video_id}).encode('utf-8')
        resp, _ = self._query_app('YouTube', data, 'POST')
        return (resp.code, resp.reason)

def get_chromecasts(urls):
    devices = []
    for url in urls:
        headers = {'Content-Length': 0}
        req = Request(url, headers = headers)
        with urlopen(req) as resp:
            if resp.status == 200:
                resp_str = resp.read()
                root = ET.fromstring(resp_str)
                devices.append(ChromeCast(root))
    return devices
