# Standard Python modules
from time import strftime
from re import findall, sub
from os import getcwd

# Selenium module (handles brower automation)
# Can be installed with: "pip install selenium"
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

# The Chrome web driver is needed as well
# You can find it here: https://sites.google.com/a/chromium.org/chromedriver/downloads


"""
NOTES:

- This script unfortunately does not work when using geckodriver to interact
with a web browser, meaning it won't work with Firefox. I'm not 100% sure why currently,
but when using geckodriver, certain elements won't work with click() and can't
be interacted with via send_keys() either.

- Chrome runs in headless mode by default

"""


# Constants to be used throughout script
SEARCH_ENGINE = 'https://google.com'

# ---> ADD YOUR SEARCH QUERIES TO THIS LIST <---
QUERIES = ['ssa site:nomorobo.com',
           'amazon site:nomorobo.com',
           'refund site:nomorobo.com',
           'subscription site:nomorobo.com',
           'computer site:nomorobo.com']

# This is optional, but can help avoid possible unwanted results.
Each query above can have a corresponding list of 'bad' words to use
for avoiding certain search result entries in Google, if an entries
preview text contains one of the words in the current queries blacklist,
then it will be skipped over.

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

RUN_DIR = getcwd()

START_TIME = strftime('%F_%T_%Z')


# Create an instance of the Chrome browser driver,
# set it to run in headless mode (no window)
browser_options = Options()
browser_options.headless = True  # This can be changed to False to see what the browser is actually doing
browser_options.add_argument('--window-size=1280,1280')
browser = webdriver.Chrome(options=browser_options)


# Returns results from the last hour for the provided search query
def get_last_hour(query):
  # Navigate to the initial search page
  browser.get(SEARCH_ENGINE)

  # Make sure the browser reached the correct page, this is set staticlly to Google right now
  if not "Google" in browser.title:
    print('[ERROR] Selenium was unable to reach google.com, exiting...')
    exit(1)

  # Change focus to the Google search box
  search = browser.find_element_by_name('q')
  search.clear()
  search.send_keys(query)
  search.send_keys(Keys.RETURN)

  # Locate the direct link to the "Past hour" results
  past_hour_element = browser.find_element_by_id('qdr_h')
  past_hour_element = past_hour_element.find_element_by_tag_name('a')
  past_hour_link = past_hour_element.get_attribute('href')

  # Then navigate to it
  browser.get(past_hour_link)

  if "did not match any documents." in browser.page_source:
    return f'[FAILURE] No results found for the query {query}', False

  else:
    search_results = browser.find_elements_by_class_name('rc')
    return f'[SUCCESS] Found {len(search_results)} results for the query {query}', search_results




# Loops through and filters the provided search results
def parse_results(search_results, category):
  results = {}
  result_num = 0
  bad_words = []

  # If the current search query has an entry in WORD_BLACKLIST,
  # then exclude search results which contain any of those words
  if category in WORD_BLACKLIST:
    print(f'[NOTICE] Category {category} found in WORD_BLACKLIST' + \
    ' , excluding results that contain any of the following:', \
    WORD_BLACKLIST[category], '\n')
    bad_words = WORD_BLACKLIST[category]
    
  # Loop through the provided search results
  for result in search_results:
    # Get the link name and preview of each result
    title = result.find_element_by_tag_name('h3')
    preview = result.find_element_by_class_name('st')

    # Performs the actual search result exclusion for the word blacklist
    # Simply skips the current interation of the for loop if a bad word 
    # was found in the preview text for the result
    if any(word in preview.text for word in bad_words):
      print(f'[NOTICE] Result {result_num} for query' + \
      f'{category} contained a blacklisted word, skipping...\n')
      continue

    # Filter the phone number out of the link name
    number = findall('\d{10}', title.text)
    if number:
      number = number[0]
    else:
      # If the first pattern fails to find a match, try a different one,
      # as Nomorobo seems to use two different number formats in their URLs
      number = sub('\D', '', title.text)
      if len(number) == 10:
        number = number
      else:
        number = 'no_phone_number_found'

    # Replace link previews which don't contain the word "Transcript"
    has_transcript = findall('Transcript\\b', preview.text)
    if has_transcript:
      preview = preview.text
    else:
      preview = 'no_transcript_found'
  
    # Add each result into a new dictionary and increment the result number
    results[f'result{result_num}'] = {'number':number, 'preview':preview}
    result_num += 1

  # After parsing each result on the page, return the dictionary
  return results




# Starting point for script, loops through earch search
# query provided in the QUERIES list and filters the data it
# returns, organizing it into a dictionary.


query_num = 0
results_file = open(f'{RUN_DIR}/results_{START_TIME}.txt', 'wt')

for query in QUERIES:
  # Find the scam category from the query
  category = findall('^\w+', query)
  
  # Search by last hour using the query
  message, search_results = get_last_hour(query)
  print(message)
  query_num += 1

  # Write the query name to the results file
  results_file.write(f'[Results for: {query}]\n')

  # If data from the query was returned, it can be sent off somewhere below
  if search_results:
    results_dict = parse_results(search_results, category[0])

  # If data from the query was not returned, try the next query
  # until we reach the end of the QUERIES list
  else:
    print('Trying next query...\n')
    results_file.write('No results found\n\n\n\n')
    results_dict = None
    continue

  for result_num in results_dict:
    result = results_dict[result_num]
    print(f'{result_num}: {result}\n')

    results_file.write(f'\n---- {result_num} ----\n' + \
    f'Number: {result["number"]}\n' + \
    f'Transcript: {result["preview"]}\n')

  results_file.write('\n\n\n')
  print('\n\n')



# After the above for loop has completed,
# close the Chrome browser process
print(f'[NOTICE] Finished, total searches made: {query_num}\n')
results_file.close()
browser.quit()
exit(0)
