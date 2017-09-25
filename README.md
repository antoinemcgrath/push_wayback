# push_wayback - Push URLs to the Wayback Machine 

using the Internet Archive's ia_plugin

Usage:

push_wayback.py [options] [URL]

Options:

-h --help                 Show this help message and exit.

-d --days=<factor>        Manually set days [default: 365].

-v --version              Show version.

-a --author               Show author.     #ERROR Note: This does not work

-thx --thanks             Show gratitude.  #ERROR Note: This does not work



Executing
--------

**Run from bash with any of the following commands**

###Run on a single URL:
python3 push_wayback.py "URL"

###Run on a single URL and recapture if older than 7 days:
python3 -d 7 push_wayback.py "URL"

###For a list of URLs:
cat "urls.txt" | while read -r line;  do python3 push_wayback.py $line; done




Functional notes:

    1. This script will instruct the Internet Archive's Wayback Machine to capture a URL if either:
       A. the URL has not been captured
       B. the URL capture is older than the days sepcified by the user (defaults to 365 days)

    2. This script does follow redirects.
       The final destination URL will be used to interact with the Wayback Machine
       *Future versions may support suppresion of this feature.

    3. If days is set to 0 via argument "-d 0" the URL will be submitted to the wayback.
       Based on observation the wayback may reject resubmissions if recently recaptured
       Perhaps the wayback has a limit on recaptures within a defined period
