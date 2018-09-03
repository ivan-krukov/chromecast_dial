import socket
import selectors
import datetime as dt
import ipdb
import sys
from urllib.request import Request, urlopen
from urllib.parse import urlparse, urlencode
import xml.etree.ElementTree as ET

from dial import DIAL

def _xml_find(el, query, ns=DIAL.NS_UPNP_DEVICE):
    return el.find(ns+query)

class Device:

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

    def app_url(self, app='YouTube'):
        return f'http://{self.addr}:{self.port}/apps/{app}'

    def stop_youtube(self):
        req = Request(self.app_url(), method = 'DELETE')
        with urlopen(req) as resp:
            pass
        return (resp.code, resp.reason)

    def post_video(self, video_id):
        data = urlencode({'v':video_id}).encode('utf-8')
        req = Request(self.app_url(), data, method = 'POST')
        with urlopen(req) as resp:
            pass
        return (resp.code, resp.reason)

def discover_urls(scan_timeout = 3, use_first = False, verbose = False):
    sel = selectors.DefaultSelector()

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(bytes(DIAL.SSDP_REQ, 'utf-8'), (DIAL.SSDP_ADDR, DIAL.SSDP_PORT))
    sock.setblocking(False)
    sel.register(sock, selectors.EVENT_READ, data=None)

    start_t = dt.datetime.now()
    discovered = []
    done_scanning = False

    while not done_scanning:
        elapsed = dt.datetime.now() - start_t

        if elapsed.seconds < scan_timeout:
            events = sel.select(timeout = 1)
            if events:
                for sel_key, mask in events:
                    resp = str(sel_key.fileobj.recv(1024), 'utf-8')
                    resp_lines = resp.split("\r\n")
                    proto, status, _ = resp_lines.pop(0).split()
                    if int(status) == 200:

                        if verbose:
                            print("\n".join(resp_lines))

                        entries = (l.split(': ') for l in resp_lines)
                        populated = (e for e in entries if len(e) == 2)

                        for key, value in populated:
                            if key == 'LOCATION':
                                discovered.append(value)

                        if use_first and len(discovered) == 1:
                            done_scanning = True

        else:
            done_scanning = True

    return discovered

def create_devices(urls):
    devices = []
    for url in urls:
        headers = {'Content-Length': 0}
        req = Request(url, headers = headers)
        with urlopen(req) as resp:
            if resp.status == 200:
                resp_str = resp.read()
                root = ET.fromstring(resp_str)
                #ipdb.set_trace()
                devices.append(Device(root))
    return devices

if __name__ == '__main__':
    discovered_urls = discover_urls(scan_timeout = 3)
    print(discovered_urls)
    if len(discovered_urls) == 0:
        print('No devices found. Exiting')
        sys.exit(1)
    else:
        devs = create_devices(discovered_urls)
        st = devs[0].post_video('3ZdSDUyxFmc')
        print(st)
