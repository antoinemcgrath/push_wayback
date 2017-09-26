#!/usr/bin/env python
"""

-  A python tool to refresh🌱 stale URLs in the Wayback Machine

Specify a URL & how fresh (# of days) you want the Wayback capture to be. 
This script will use the Internet Archive's ia_plugin to update the capture if it is stale. 


Usage:
wayback_refresh.py [options] [URL]

Options:
  -d --days=<factor>        Set days still fresh🌱 [default: 365].
  -h --help                 Show this help message and exit.
  -v --version              Show version.  
  -s --suppress             Suppress all responses. #ERROR Note: This does not work
  -l --less_text            Allow fresh URL responses only. #ERROR Note: This does not work
  -a --author               Show author.     #ERROR Note: This does not work
  -thx --thanks             Show gratitude.  #ERROR Note: This does not work


### Run on a single URL:
 *  `python3 wayback_refresh.py "URL"`

### Run on a single URL, do not recapture if fresher than: 7 days 
 *  `python3 -d 7 wayback_refresh.py "URL"`

### Run on a list of URLs:
 *  `cat "urls.txt" | while read -r line;  do python3 wayback_refresh.py $line; done`



Functional notes:

    1. This script will instruct the Internet Archive's Wayback Machine to capture a URL if either:
       A. the URL has not been captured
       B. the URL capture is stale (by default fresh is within 365 days, to overide use -d #)

    2. This script does follow redirects.
       The final destination URL will be used to interact with the Wayback Machine
       *Future versions may support suppression of this feature.

    3. If days is set to 0 via argument "-d 0" the URL will be submitted to the Wayback.


Comments, critiques? Contact me -> @AGreenDCBike (https://www.twitter.com/AGreenDCBike)  

Like the Internet Archive as much as I do? Thank them for hosting the Wayback & much more! -> https://archive.org/donate/


"""

import sys
from urllib.request import urlopen
import json
import datetime
import requests
from docopt import docopt

__version__ = '0.0.1'

#ERROR Note: These bellow do not work
__title__ = 'wayback_refresh_plugin'
__url__ = 'https://github.com/'
__author__ = 'Antoine McGrath'
__all__ = ['wayback_refresh']
__email__ = 'Test@test.com'
__thanks__ = 'Thanks you to Johan van der Knijff!!! for: ia_plugin, and JJJake for posting ia_plugin to: https://github.com/jjjake/iawayback'
#ERROR Note: These above do not work



#### The following script will recapture a url if it is stale (the wayback capture is older than the user specified days)
#### Usage: wayback_refresh.py <url> <days>

def wayback_refresh(url):
    # Attempts to capture the website via the Wayback Machine
    # Alternative unexplored method available
    #    curl -X POST -H "Content-Type: application/json" -d '{"url": "URL"}' https://pragma.archivelab.org

    # Skip urls treated oddly by the wayback.api
    if url.find("/wp-json/oembed/1.0/embed") > 1:
        print(chr(9940), "Page is wp-json formatting instructions, which are rejected by the wayback/api: http://archive.org/help/wayback_api.php")
        sys.exit()  # Stale ending: No fresh capture exists, and no refresh was possible
    else:
        # Push URL to refresh wayback
        urlSAVE = "https://web.archive.org/save/"
        req = requests.get(urlSAVE + url)

        if req.status_code == 404:
            req.close()
            print(chr(9940), "ERROR: Page request is 404, page does not currently exist and cannot be archived")
            sys.exit()  # Stale ending: No fresh capture exists, and no refresh was possible
        elif req.status_code == 400:
            req.close()  # Stale ending: No fresh capture exists, and no refresh was possible
            print(chr(9940), "ERROR: Page request is 400, bad request, Wayback refresh did not complete")
            sys.exit()  # Stale ending: No fresh capture exists, and no refresh was possible
        elif req.status_code == 502:
            req.close()
            print(chr(9940), "ERROR: Page request is 502, bad gateway, Wayback refresh did not complete")
            sys.exit()  # Stale ending: No fresh capture exists, and no refresh was possible
        pass
        #if req.status_code == 200:
        #    print("Page request is 200, good request")



def follow_url_redirects(url):

    # URL of interest
    submitted_url = url
    if url.startswith("https://"):
        url = url[8:]
        # print("URL started with https://")
    if url.startswith("http://"):
        url = url[7:]
        # print("URL started with http://")
    # else:
    #    pass
    url = "http://" + url

    # Get the desination url
    try:
        r = requests.get(url, allow_redirects=True)
        final_url = r.url
        r.close()
        print(submitted_url, " -> ", final_url)

    except requests.exceptions.RequestException as e:  # This is the correct syntax
        print(chr(9889), "ALERT: URL does not currently result in an online site. "
              "Checking Wayback to see if URL previously hosted content.")
        final_url = url
    return(final_url)


def fetch_wayback_captured_date(url):
    # Queries the Wayback Machine's most recent capture date (if available)
    # Returns new archived version is (Days Hours:Mins:Sec) ago: 0:01:47
    # Returns URL of the most recent capture

    urlAPI = "https://archive.org/wayback/available?url="
    # API url (see: http://archive.org/help/wayback_api.php)
    req = requests.get(urlAPI + url)
    data = req.json()
    req.close()

    # Decode json object
    snapshots = data['archived_snapshots']

    if len(snapshots) == 0:
        # No snapshots found, no capture is available in the Wayback
        urlWayback = ""
        timestamp = ""

    else:
        # Snapshot(s) available
        # For now API only returns 1 snaphot, which is the most recent one.
        closest = snapshots['closest']
        urlWayback = closest['url']
        timestamp = closest['timestamp']

    return(timestamp, urlWayback)



def is_capture_fresh_enough(days, timestamp):
    datetimeFormat = "%Y%m%d%H%M%S"
    current = datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S")
    timedelta = datetime.datetime.strptime(current, datetimeFormat) - datetime.datetime.strptime(str(timestamp), datetimeFormat)
    print("Most recent archive version is (Days Hours:Mins:Sec) ago:", timedelta)
    days = datetime.timedelta(days)

    if days < timedelta:
        fresh_enough = False
    else:
        # return(available, urlWayback, status, timestamp)
        #print("Most recent capture is fresh: ", urlWayback)
        fresh_enough = True

    return(fresh_enough)

def executewill(arguments):
    # Set arguement values
    url = (arguments['URL'])
    days = (int(arguments['--days']))

    url = follow_url_redirects(url)   # Follow (&reset) URL to/as final destination

    returns = fetch_wayback_captured_date(url)   # Fetch URLs most recent capture date
    timestamp = returns[0]
    urlWayback = returns[1]

    if len(timestamp) != 0:   # Timestamp exists URL captured in wayback
        # Check if recent capture date is fresh enough for user specified date
        fresh_enough = is_capture_fresh_enough(days, timestamp)

    else: # No timestamp, URL is not captured in wayback
        print("Wayback has no record of this URL. Requesting Wayback capture", chr(127793))
        wayback_refresh(url)
        returns_2 = fetch_wayback_captured_date(url)
        timestamp = returns_2[0]
        urlWayback = returns_2[1]

        if len(timestamp) == 0: # Still no timestamp, despite a refresh attempt
            print(chr(9940), "ALERT: No wayback record exists and no Wayback refresh was possible")
            sys.exit()  # Stale ending: No capture exists, and no refresh was possible

        else: # New timestamp, refresh attempt worked
            print("Wayback refresh complete. A first capture of the URL", chr(127793))
            print(urlWayback)
            sys.exit()  # Fresh ending with a first time capture of the URL


    if fresh_enough is False: # A capture existed but was not fresh
        # Refresh the Wayback's capture
        print("Wayback capture is stale (more than", str(days)[:6], "old). Requesting Wayback refresh", chr(127793))
        wayback_refresh(url)
        # Fetch new capture date if available
        returns_3 = fetch_wayback_captured_date(url)
        timestamp = returns_3[0]
        urlWayback = returns_3[1]

        if len(timestamp) == 0:
            print(chr(9940), "ALERT: Most recent capture remains stale, a Wayback refresh did not complete:")
            print("STALE:", urlWayback)
            sys.exit()  # Stale ending: Capture exists but a refresh was not possible

        else:  # Fresh enough is True
            print(urlWayback)
            sys.exit()  # Fresh ending: With a fresh capture

    else:  # Fresh enough is True
        print(urlWayback)
        sys.exit()  # Fresh ending: No new capture was needed


def main():
    arguments = docopt(__doc__, version=__version__)

    if arguments['URL']:
        executewill(arguments)
    else:
        print(__doc__)



if __name__ == '__main__':
    main()


"""
One way to create a list of URLs is to scrape links from urls that are already in the Wayback Machine.
To capture URLS & relative URLs from a specified domain: 
 -Utilize https://github.com/hartator/wayback-machine-downloader 
 -And execute the following in bash:

$wayback_machine_downloader "URL"
$cd /websites
$find ./websites -type f | grep .html | sort | uniq > file_list.txt
$cat file_list.txt | while read -r line; do lwp-request -m GET -o links $line >> links.txt; done
$cat links.txt | sort | uniq >> links_cleaner.txt
$cat links_cleaner.txt | grep -oh "\w*www.*" >> urls.txt
$cat "urls.txt" | while read -r line;  do python3 wayback_refresh.py $line; done

"""
