from urllib.request import Request, urlopen
from urllib.parse import urlparse, urlencode
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
        req = Request(self.app_url(app), data = data, method = method)
        with urlopen(req) as resp:
            pass
        return resp

    def app_status(self, app):
        status = 'Unknown'
        resp = self._query_app(app)

        if resp.status == 200:
            resp_str = resp.read()
            root = ET.fromstring(resp_str)
            status = _xml_find(root, DIAL.NS_DIAL, 'state')

        return status

    def start_app(self, app):
        resp = self._get_app(app)
        return (resp.code, resp.reason)

    def stop_app(self, app):
        resp = self._query_app(app, method = 'DELETE')
        return (resp.code, resp.reason)

    def post_youtube_video(self, video_id):
        data = urlencode({'v':video_id}).encode('utf-8')
        resp = self._query_app('YouTube', data, 'POST')
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
