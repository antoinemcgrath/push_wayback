# wayback_refresh  -  A python tool to check if a URL in the Wayback Machine is fresh :seedling:, and recapture the URL if it is stale.

Use the Internet Archive's ia_plugin to check for recent captures (with a user specified number of days) before creating a new capture request.

Usage: `wayback_refresh.py [options] [URL]`
* -h --help                 Show this help message and exit.
* -d --days                 Manually set definition of fresh :seedling: (in days) [default: 365].
* -v --version              Show version.
* -a --author               Show author.     #ERROR Note: This does not work
* -thx --thanks             Show gratitude.  #ERROR Note: This does not work



Run from bash with any of the following commands
--------

### Run on a single URL(!):
 *  `python3 wayback_refresh.py "URL"`

### Run on a single URL, do not recapture if fresher than: 7 days 
 *  `python3 -d 7 wayback_refresh.py "URL"`

### For a list of URLs(!):
 *  `cat "urls.txt" | while read -r line;  do python3 wayback_refresh.py $line; done`

### (!) Default recapture is "Do not recapture if fresher than: 365 days" 



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
