# Chromecast_DIAL

`Chromecast_DIAL` is a python library talking to a chromecast via the old `DIAL` protocol.

The protocol seems poorly supported on ChromeCasts, and only allows submitting YouTube videos.

The application supports a small command line interface for querying and posting to devices on the local netowrk.

For a more feature-complete library, see [pychromecast](https://github.com/balloob/pychromecast)
The source code benefits heavily form [`pydial`](https://github.com/claycollier/pydial).

## Comman line usage

### Discovery 

Discover devices on the local network:

```bash
python3 -m chromecast_dial --discover
```

### Using particular device

You can also interact with a single device if you know the IP:

```bash
python3 -m chromecast_dial --ip 127.0.0.2
```

Or work with the first device that responds:

```bash
python3 -m chromecast_dial --use-first
```


### Posting

Post a YouTube video request on all devices:

```bash
python3 -m chromecast_dial --video Dgxz0kZ2dp4
```

### Stoping

Stop the default app (`YouTube`):

```bash
python3 -m chromecast_dial --stop
```

Stop another app:

```bash
python3 -m chromecast_dial --stop --app Netflix
```

Since nothing else is supported, you will probably see `No app running`.

### Status

With no arguments, the program scan the status of the default app (`YouTube`) on all devices:

```bash
python3 -m chromecast_dial
```

You can change queried app with `--app`:

```bash
python3 -m chromecast_dial --app Netflix
```

But you will probably get a `App not found`.

A table of registered applications can be found on the [DIAL registry](http://www.dial-multiscreen.org/dial-registry/namespace-database)

### Fast scan

To only get configuration end-points, use `--fast-scan`. This will not query devices for names:

```bash
python3 -m chromecast_dial --fast-scan
```

## Module usage

Here is an example script to discover the first device and submit a video to it:

```python
from chromecast_dial import *

urls = discover(use_first=True)
cast = get_chromecasts(urls)[0]
cast.post_youtube_video('Dgxz0kZ2dp4')
```

# TODO

This code uses the `DIAL` protocol, which is not well supported, and not many feature can be provided with it.
There are a few other things that can be implemented:

* Setting video start time `&t=3m20s`, looping.
* Extra device info through `/setup/eureka_info`
* Restarting throught posting to `/setup/reboot -d ‘{“params”:”now”}’`

There appears to be no way to pause videos with the `DIAL` protocol.
