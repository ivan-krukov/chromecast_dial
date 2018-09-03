from chromecast_dial import *

if __name__ == '__main__':
    import sys
    from argparse import ArgumentParser
    parser = ArgumentParser(description = 'Send YouTube videos to ChromeCast')

    parser.add_argument('--video',     type=str,  help='YouTube video id')
    parser.add_argument('--ip',        type=str,  help='IP address of the device')
    parser.add_argument('--app',       type=str,  default='YouTube', help='App to use (only YouTube is supported)')
    parser.add_argument('--stop',      action='store_const', const=True, help='Stop currently running app')
    parser.add_argument('--discover',  action='store_const', const=True, help='Scan for devices')
    parser.add_argument('--fast-scan', action='store_const', const=True, help='Only scan config URLs')
    parser.add_argument('--use-first', action='store_const', const=True, help='Use first device')
    parser.add_argument('--verbose',   action='store_const', const=True, help='Verbose output')

    args = parser.parse_args()

    if not args.ip:
        urls = discover(scan_timeout = 3, use_first = args.use_first, verbose = args.verbose)
    else:
        urls = [f'http://{args.ip}:8008/ssdp/device-desc.xml']

    if len(urls) == 0:
        print('No devices found. Exiting.')
        sys.exit(1)

    elif args.fast_scan:
        print('Found URLs:')
        for u in urls:
            print("\t", u)
        sys.exit(0)

    devs = get_chromecasts(urls)

    if args.discover:
        print('Found devices:')
        for d in devs:
            print("\t", d)
        sys.exit(0)


    elif args.video is not None:
        for d in devs:
            status, reason = d.post_youtube_video(args.video)
            print(f"{d.friendly_name}\t{reason}")

    elif args.stop:
        for d in devs:
            status, reason = d.stop_app(args.app)
            print(f"{d.friendly_name}\t{reason}")

    # show status
    else:
        for d in devs:
            st = d.app_status(args.app)
            print(f"{d.friendly_name}\t{st}")
