import types

DIAL = types.SimpleNamespace(

    SSDP_ADDR = '239.255.255.250',
    SSDP_PORT = 1900,
    # TODO: should this be parameter-controlled?
    SSDP_MAX  = 2,

    SSDP_TARG = 'urn:dial-multiscreen-org:service:dial:1',


    NS_UPNP_DEVICE = '{urn:schemas-upnp-org:device-1-0}',
    NS_DIAL = '{urn:dial-multiscreen-org:schemas:dial}',
    NS_CAST = '{urn:chrome.google.com:cast}')

DIAL.SSDP_REQ  = \
f"""M-SEARCH * HTTP/1.1
HOST: {DIAL.SSDP_ADDR}:{DIAL.SSDP_PORT}
MAN: "ssdp:discover"
MX: {DIAL.SSDP_MAX}
ST: {DIAL.SSDP_TARG}

"""
