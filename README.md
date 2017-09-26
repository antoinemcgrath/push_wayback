# wayback_refresh:seedling: 

-  A python tool to refresh stale URLs in the Wayback Machine


Specify a URL & how fresh (# of days) you want the Wayback capture to be. 

This script will use the Internet Archive's ia_plugin to update the capture if it is stale. 


______
Usage: `wayback_refresh.py [options] [URL]`


* -d --days                 Manually set definition of fresh :seedling: (in days) [default: 365].



Run from bash with any of the following commands
--------

### Run on a single URL:
 *  `python3 wayback_refresh.py "URL"`

### Run on a single URL, do not recapture if fresher than: 7 days 
 *  `python3 -d 7 wayback_refresh.py "URL"`

### For a list of URLs:
 *  `cat "urls.txt" | while read -r line;  do python3 wayback_refresh.py $line; done`



Functional notes:

    1. This script will instruct the Internet Archive's Wayback Machine to capture a URL if either:
       A. the URL has not been captured
       B. the URL capture is stale (by default fresh is within 365 days, to overide use -d #)

    2. This script does follow redirects.
       The final destination URL will be used to interact with the Wayback Machine
       *Future versions may support suppresion of this feature.

    3. If days is set to 0 via argument "-d 0" the URL will be submitted to the wayback.


Comments, criqitues, compliments? -> [![alt text][1.2]][1] Twitter: @AGreenDCBike    


<!-- Please don't remove this: Grab your social icons from https://github.com/carlsednaoui/gitsocial -->
[1.2]: http://i.imgur.com/wWzX9uB.png (twitter icon without padding)
[1]: http://www.twitter.com/AGreenDCBike
