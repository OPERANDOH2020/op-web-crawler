#OPERANDO Web Crawler

Web Crawler gets a list of OSPs URLs and the according credentials to log in, to fetch the privacy settings of the OSPs so that the WatchDog can determine whether new settings have been introduced.

Similarly, Web Crawler browses the pages where OSPs share their privacy policy and sends them to WatchDog to determine whether the OSP introduced new terms.

Web Crawler runs on Python 2.7 and uses:
* [flask](http://flask.pocoo.org/)
* [selenium](http://www.seleniumhq.org/)
* [phantomjs](http://phantomjs.org/)

The credentials for each dummy account are stored in a configuration file (credentials.ini), so make the according changes to have this up and running.
