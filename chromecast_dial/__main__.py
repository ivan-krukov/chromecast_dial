from chromecast_dial import *

if __name__ == '__main__':
    discovered_urls = discover(scan_timeout = 3, use_first = True)
    print(discovered_urls)
    if len(discovered_urls) == 0:
        print('No devices found. Exiting')
        sys.exit(1)
    else:
        devs = get_chromecasts(discovered_urls)
        print(devs)
        st = devs[0].post_youtube_video('3ZdSDUyxFmc')
        print(st)
