# import libraries 
import time # wait commands (space out)
import re # regular expressions (text parser)
import urllib # Internet connection (socket connections, https)
import csv

date = time.time()

# ---------------------------------------------------------------------------# 
# For the CSV of character names + URLs
top_columns = ['season', 'episode', 'stuff']

filename = str(date) + 'character-name-url.csv'

# /Users/jessiewillms/Dropbox/terry_loves/...py

directory = '/Users/jessiewillms/Dropbox/terry_loves/csv/'
CharacterNameAndURL = csv.writer(file(directory + filename, 'a'),dialect='excel')
CharacterNameAndURL.writerow(top_columns)

# -------------------------------------------------------------------------- # # Loop over every page #
# -------------------------------------------------------------------------- # 
def scrape_character_pages(ep_array):
	counter = 0
	# ---------------------------------------------------------------------- # 
	# Loop over every URL in the URL array #
	# ---------------------------------------------------------------------- #
	terry_loves_this = []
	terry_hates_this = []
	for ep in ep_array:
		# print 'ep', ep

		# Open each page and get the contents
		ep_page = urllib.urlopen(ep).read()
		# print ep_page
		print ' ------------------------------------------------------'

		# ---------------------------------------------------------------------- #
		if ep_page is not None:

			# ---------------------------------------------------------------------- #
			# Get season number #
			# ---------------------------------------------------------------------- #
			ep_season_episode = re.search('<h1>(.+?)</h1>', ep_page, re.S|re.DOTALL)
			if ep_season_episode.group(1) is not None:
				ep_season_episode = ep_season_episode.group(1)
				print 'ep_season_episode', ep_season_episode
			
			# ---------------------------------------------------------------------- #
			# Get episode title #
			# ---------------------------------------------------------------------- #
			ep_title = re.search('<h3>(.+?)</h3>', ep_page, re.S|re.DOTALL)
			if ep_title is not None:
				# ep_title = ep_title.group(1)
				print 'ep_title', ep_title.group(1)

			# ---------------------------------------------------------------------- #
			# Go get the script content and search for stuff Terry loves #
			# ---------------------------------------------------------------------- #
			script_content = re.search('<div class="scrolling-script-container">(.+?)</div>', ep_page, re.S|re.DOTALL)
			
			if script_content is not None:
				# print script_content.group(0)

				for single_loves in re.finditer('Terry loves(.+?)<br>', script_content.group(0), re.S|re.DOTALL):
					print 'single_loves', single_loves.group(0)
					terry_loves_this.append(single_loves.group(0))
				
				for single_likes in re.finditer('Terry likes(.+?)<br>', script_content.group(0), re.S|re.DOTALL):
					print 'single_likes', single_likes.group(0)
					terry_loves_this.append(single_likes.group(0))

				for single_hates in re.finditer('Terry hates(.+?)<br>', script_content.group(0), re.S|re.DOTALL):
					print 'single_hates', single_hates.group(0)
					terry_hates_this.append(single_hates.group(0))

			# print character_data
			CharacterNameAndURL.writerow([terry_loves_this, terry_hates_this])

		# ------------------------------------------------------------------- #
		# Increment the number in the counter #
		counter = counter + 1
		# ------------------------------------------------------------------- #

		# Reduce calls to the site to every one (1) second
		time.sleep(1)
		# ------------------------------------------------------------------- #

# -------------------------------------------------------------------------- # 
# Get initial page - get all names
# -------------------------------------------------------------------------- # 

def scrape_page(html_page):

	for single in re.finditer('<div class="season-episodes">(.+?)</div>', html_page, re.S|re.DOTALL):

		get_seasons_nums = re.search('<h3 id="season(.+?)">(.+?)</h3>', single.group(0), re.S|re.DOTALL)

		if get_seasons_nums.group(1) is not None:
			season_number = get_seasons_nums.group(1)
	
	# ------------------------------------------------------
	ep_array = []
	for single_ep in re.finditer('<a href="(.+?)" class="season-episode-title">(.+?). (.+?)</a>', html_page, re.S|re.DOTALL):
		
		if single_ep is not None:
			
			ep_url = 'https://www.springfieldspringfield.co.uk/' + single_ep.group(1)
			ep_array.append(ep_url)

			ep_season = ep_url.split('&episode=')
			season_number = ep_season[1].split('s')[1].split('e')[0]
			episode_number = ep_season[1].split('s')[1].split('e')[1]
			
			ep_title = single_ep.group(3)
			# print 'ep_title', ep_title

	# print 'ep_array', ep_array
	scrape_character_pages(ep_array)

# URLs to access
base_url = 'https://www.springfieldspringfield.co.uk/episode_scripts.php?tv-show=brooklyn-nine-nine'
# full_url = base_url

html_page = urllib.urlopen(base_url).read() # .urlopen() takes one value, the URL to open # .read() as a method to read returns
scrape_page(html_page)

