# Google Nomorobo phone number search

A Python script that uses the [Selenium](https://github.com/SeleniumHQ/selenium/) browser automation framework to extract phone numbers and possible descriptions of them, from the Google search results the query returns.

This is primarily meant to aid in the process of finding phone numbers to [scambait](https://en.wikipedia.org/wiki/Scam_baiting), and is *tuned* to extract last hour results from the website [Nomorobo](http://nomorobo.com/), but can of course be
modified to suit other purposes.

## A small warning

If you plan to use this script for finding phone numbers to scambait as well, please be cautious of who you reach when dialing phone numbers returned by this script.
If used for number extraction from websites like Nomorobo, RoboKiller, FindWhoCallsYou etc. (sites that deal with inbound, scammer -> victim, phone calls), you are very likely to come across many **spoofed** phone numbers. These phone numbers don't actually lead back to the scammer who originally made the outbound phone call, and were simply used as their outbound caller ID.
So upon calling it back, you are very likely to reach an innocent person.

## Usage

Upon opening up the main `nomorobo_search.py` file, near the top you'll see a data structure that looks like this:

```python
QUERIES = ['ssa site:nomorobo.com',
           'amazon site:nomorobo.com',
           'refund site:nomorobo.com',
           'subscription site:nomorobo.com',
           'computer site:nomorobo.com']
```

This is a Python list containg the search queries for the script to make in sequence, you can add or remove any that you like.
`site:<website_address>` is a Google search keyword that helps limit search results to a specific website only. In order for the script to successfully extract phone numbers, there must be 10 or 11 digit number present in the search result entries link name. For example, nomorobo.com is one of the sites that does this, findwhocallsyou.com does it as well.

##

This is optional, but can help avoid possible unwanted results. Each query you add to list mentioned above can have a corresponding list of 'bad' words to use
for avoiding certain search result entries in Google. If an entries preview text contains one of the words in the current queries blacklist, then it will be skipped over.

```python
WORD_BLACKLIST = {
 'ssa':[
  'disability',
  'advisor'],
 amazon':[
  'voice system',
  'households',
  'clients',
  'Alexa',
  'registered']
}
```


## Notes

This script unfortunately does not work when using the [geckodriver](https://github.com/mozilla/geckodriver) to interact
with a web browser, meaning it won't work with Firefox. So a Chromium based browser in combination with with [chromedriver](https://sites.google.com/a/chromium.org/chromedriver/downloads) is needed. I'm not 100% sure why currently,
but when using geckodriver, certain elements can't be interacted with via the click() and/or send_keys() methods.

Chrome is set to run in headless mode by default.


To be continued
