import socket
import selectors
import datetime as dt

from .dial_protocol_defs import DIAL

def discover(scan_timeout = 3, use_first = False, verbose = False):
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

