#!/usr/bin/env python
"""

# push_wayback  -  
A python tool to check if a URL in the Wayback Machine is :seedling:fresh🥗, and recapture the URL if it is stale.

Use the Internet Archive's ia_plugin to check for recent captures (with a user specified number of days) before creating a new capture request.


Usage:
push_wayback.py [options] [URL]

Options:
  -h --help                 Show this help message and exit.
  -d --days=<factor>        Manually set days [default: 365].
  -v --version              Show version.
  -a --author               Show author.     #ERROR Note: This does not work
  -thx --thanks             Show gratitude.  #ERROR Note: This does not work



Run from bash with any of the following commands
--------

### Run on a single URL(!):
 *  `python3 push_wayback.py "URL"`

### Run on a single URL, do not recapture if fresher than: 7 days 
 *  `python3 -d 7 push_wayback.py "URL"`

### For a list of URLs(!):
 *  `cat "urls.txt" | while read -r line;  do python3 push_wayback.py $line; done`

### (!)Default recapture is "Do not recapture if fresher than: 365 days" 



Functional notes:

    1. This script will instruct the Internet Archive's Wayback Machine to capture a URL if either:
       A. the URL has not been captured
       B. the URL capture is stale (definition of fresh is specified by the user, by default fresh is within 365 days)

    2. This script does follow redirects.
       The final destination URL will be used to interact with the Wayback Machine
       *Future versions may support suppresion of this feature.

    3. If days is set to 0 via argument "-d 0" the URL will be submitted to the wayback.
       Based on observation the wayback may reject resubmissions if recently recaptured
       Perhaps the wayback has a limit on recaptures within a defined period



"""

import sys
from urllib.request import urlopen
import json
import datetime
import requests
from docopt import docopt

__version__ = '0.0.1'

#ERROR Note: These bellow do not work
__title__ = 'push/repush_wayback_plugin'
__url__ = 'https://github.com/'
__author__ = 'Antoine McGrath'
__all__ = ['push_wayback']
__email__ = 'Test@test.com'
__thanks__ = 'Thanks you to Johan van der Knijff!!! for: ia_plugin, and JJJake for posting ia_plugin to: https://github.com/jjjake/iawayback'
#ERROR Note: These above do not work



#### The following script will recapture a url if the most recent wayback capture is older than the specified days
#### Usage: push_wayback.py <url> <days>

def push_to_wayback(url):
    # Attempts to capture the website via the Wayback Machine
    # Alternative unexplored method available
    #    curl -X POST -H "Content-Type: application/json" -d '{"url": "URL"}' https://pragma.archivelab.org

    # Skip urls treated oddly by the wayback.api
    if url.find("/wp-json/oembed/1.0/embed") > 1:
        print("Page is wp-json formatting instructions, which is treated by the wayback/api differently: http://archive.org/help/wayback_api.php")
        sys.exit()
    else:
        # Push to wayback URL preface
        urlSAVE = "https://web.archive.org/save/"
        req = requests.get(urlSAVE + url)

        if req.status_code == 404:
            req.close()
            print("Page request is 404, page does not currently exist and cannot be archived")
            sys.exit()
        elif req.status_code == 400:
            req.close()
            print("Page request is 400, bad request")
            sys.exit()
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
    r = requests.get(url, allow_redirects=True)
    final_url = r.url
    r.close()

    print(submitted_url, " -> ", final_url)
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



def is_capture_recent_enough(days, timestamp):
    datetimeFormat = "%Y%m%d%H%M%S"
    current = datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S")
    timedelta = datetime.datetime.strptime(current, datetimeFormat) - datetime.datetime.strptime(str(timestamp), datetimeFormat)
    print("Most recent archive version is (Days Hours:Mins:Sec) ago:", timedelta)
    days = datetime.timedelta(days)

    if days < timedelta:
        print("Wayback capture is older than", str(days)[:6], "old. Generating a more recent wayback capture")
        recent_enough = False
    else:
        # return(available, urlWayback, status, timestamp)
        #print("Most recent capture is sufficient: ", urlWayback)
        #print("Recent enough")
        recent_enough = True

    return(recent_enough)

def executewill(arguments):

    url = (arguments['URL'])   # Set arg as value
    days = (int(arguments['--days']))  # Set arg as value

    url = follow_url_redirects(url)   # Follow (&reset) URL to/as final destination

    returns = fetch_wayback_captured_date(url)   # Fetch URLs most recent capture date
    timestamp = returns[0]

    if len(timestamp) == 0:   # URL not captured in wayback
        push_to_wayback(url)   # Capture URL
        returns = fetch_wayback_captured_date(url)   # Fetch URLs most recent capture date
        timestamp = returns[0]
    else:
        pass

    timestamp = returns[0]

    # Check if recent capture date is recent enough for user specified date (365 days if not specified)
    recent_enough = is_capture_recent_enough(days, timestamp)

    if recent_enough is True:
        urlWayback = returns[1]

    if recent_enough is False:

        #print("older timestamp: ", timestamp)
        push_to_wayback(url)
        urlWayback = fetch_wayback_captured_date(url)[1]
        #print("new capture: ", urlWayback)

    print(urlWayback)



def main():
    arguments = docopt(__doc__, version=__version__)

    if arguments['URL']:
        executewill(arguments)
    else:
        print(__doc__)



if __name__ == '__main__':
    main()


"""
#One way to create a list of URLs is to scrap links from urls that are already in the Wayback Machine.
#To capture URLS & relative URLs from a specified domain, execute the following in bash:

$wayback_machine_downloader "URL"
$cd /websites
$find ./websites -type f | grep .html | sort | uniq > file_list.txt
$cat file_list.txt | while read -r line; do lwp-request -m GET -o links $line >> links.txt; done
$cat links.txt | sort | uniq >> links_cleaner.txt
$cat links_cleaner.txt | grep -oh "\w*www.*" >> urls.txt
$cat "urls.txt" | while read -r line;  do python3 push_wayback.py $line; done

"""
