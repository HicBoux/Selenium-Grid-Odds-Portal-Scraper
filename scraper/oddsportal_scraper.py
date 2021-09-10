# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options

import random
from random import random, randint, seed
import re
import pandas as pd
from datetime import datetime, timedelta
import time
import locale
import os
from dateutil.parser import parse as parse_dt
import json

def import_config_parameters(file_path):
	"""Import the parameters set in the JSON configuration file."""
	with open(file_path) as f:
	    config = json.load(f)
	selected_sports = config["sport"] # List of sports to scrape
	wt = float(config["waiting_time_multiplicator"]) # Constant multiplier to manage script pauses in order to avoid "overwhelming" web scraping
	return selected_sports, wt

def launch_webdriver():
	"""Set the parameters of the webdriver and launch it."""
	chrome_options = webdriver.ChromeOptions()
	chrome_options.add_argument("--headless")
	chrome_options.add_argument("--disable-gpu")
	chrome_options.add_argument("window-size=1024,768")
	chrome_options.add_argument("--no-sandbox")
	chrome_options.add_argument('--disable-dev-shm-usage')        
	driver = webdriver.Remote("http://selenium:4444/wd/hub", desired_capabilities=DesiredCapabilities.CHROME)
	return driver

def visit_back_with_random_moves(yesterday_url):
    rd_action = randint(0,2)
    if rd_action == 2:
    	driver.get(yesterday_url)
    elif rd_action == 1:
    	driver.back()
    else:
    	driver.get("http://google.com")
    	time.sleep(wt*random())
    	driver.get(yesterday_url)

if __name__ == "__main__":

	start = time.time()
	print("--------- START ---------")
	time.sleep(10) # Script pause until all the docker containers are running well
	os.system("locale")

	# Set random seed
	rd_seed = randint(0,99999)
	seed(rd_seed) 

	# Set current directory path, import configuration parameters and launch the webdriver
	cwd = os.path.dirname(os.path.realpath(__file__)) + "/"

	selected_sports, wt = import_config_parameters(cwd + "config/config.json")

	driver = launch_webdriver()

	# Initialize the dataframe of scraped data to fill out
	header = ["ID","URL","Sport","Country","Competition",
		                              "Home_Team","Away_Team","Date","Time",
		                              "Home_Score","Away_Score","FTR",
		                              "Home_Score_1st_Halftime","Away_Score_1st_Halftime",
		                              "Home_Score_2nd_Halftime","Away_Score_2nd_Halftime",
		                              "AVG_Home_Odd","AVG_Draw_Odd","AVG_Away_Odd",
		                              "MAX_Home_Odd","MAX_Draw_Odd","MAX_Away_Odd",
		                              "Scraping_Date","Scraping_Time"
		                              ]
	bets_df = pd.DataFrame([], columns=header)

	# Get yesterday's date in order to check all the matches which occured this day 
	yesterday = datetime.today() - timedelta(days=1)
	
	# For each sport input in the config file
	for selected_sport in selected_sports:

		print("----", selected_sport)

		# Visit the web page summarizing all previous matches
		yesterday_url = "https://www.oddsportal.com/matches/" + selected_sport + "/" + yesterday.strftime('%Y%m%d')
		driver.get(yesterday_url)

		time.sleep(3+wt*random())

		# Visit the web page summarizing all previous matches
		all_match_urls = driver.find_elements_by_xpath('//*[@class="name table-participant"]/a')
		nb_match_urls = len(all_match_urls)

		# For each match found on the summary web page
		for i in range(nb_match_urls):

			# Retrieve the ID and URL of the match in order to visit it
		    all_match_urls = driver.find_elements_by_xpath('//*[@class="name table-participant"]/a')
		    match_url = all_match_urls[i].get_attribute("href")
		    match_id = match_url[-9:-1]
		    driver.get(match_url)

		    # Record the actual date and time 
		    scraping_date = datetime.now().strftime('%H:%M:%S')
		    scraping_time = datetime.today().strftime('%d/%m/%Y')
		    
		    # Retrieve metadata of the match : sport, country, competition, teams
		    metadata = driver.find_elements_by_xpath('//*[@id="breadcrumb"]')[0].text.split("»")
		    sport = metadata[1].strip()
		    country = metadata[2].strip()
		    competition = metadata[3].strip()
		    home_team = metadata[4].split(" - ")[0].strip()
		    away_team = metadata[4].split(" - ")[1].strip()
		    match_full_date = driver.find_elements_by_xpath('//*[@id="col-content"]/p[1]')[0].text
		    match_date = datetime.strptime(match_full_date.split(", ")[1], "%d %b %Y").strftime('%d/%m/%Y')
		    start_time = datetime.strptime(match_full_date.split(", ")[2], "%H:%M").strftime('%H:%M')
		    print(i, match_url, home_team, away_team, match_full_date)
		    
		    # Retrieve the half-time and final score of the match
		    	# Put 9999 if unidentified
		    try:
		    	score = driver.find_elements_by_xpath('//*[@id="event-status"]/p/strong')[0].text
		    	home_score = int(score.split(":")[0])
		    	away_score = int(score.split(":")[1])
		    except:
		    	home_score = 9999
		    	away_score = 9999

		    # Deduce match result from score
		    if home_score == 9999 or away_score == 9999: ftr =9999
		    elif home_score > away_score: ftr = "H"
		    elif home_score < away_score: ftr = "A"
		    elif home_score == away_score: ftr = "D"
		    else: ftr = 9999
		    
		    # Scrape half-time scores if they're found on the web page
		    	# Put 9999 if unidentified
		    try:
		    	halftime_scores = re.search("\((.*?)\)", driver.find_elements_by_xpath('//*[@id="event-status"]/p')[0].text).group(1)
		    	home_score_1st_halftime = int(halftime_scores.split(", ")[0].split(":")[0])
		    	home_score_2nd_halftime = int(halftime_scores.split(", ")[1].split(":")[0])
		    	away_score_1st_halftime = int(halftime_scores.split(", ")[0].split(":")[1])
		    	away_score_2nd_halftime = int(halftime_scores.split(", ")[1].split(":")[1])
		    except:
		    	home_score_1st_halftime = 9999
		    	home_score_2nd_halftime = 9999
		    	away_score_1st_halftime = 9999
		    	away_score_2nd_halftime= 9999
		    
		    # Extract average odds of the match
		    	# Put 9999 if unidentified
		    try:
		    	avg_odds = driver.find_elements_by_xpath('//*[@class="aver"]')[0].text
		    	avg_home_odd = float(avg_odds.split(" ")[1])
		    	avg_draw_odd = float(avg_odds.split(" ")[2])
		    	avg_away_odd = float(avg_odds.split(" ")[3])
		    except:
		    	avg_home_odd = 9999
		    	avg_draw_odd = 9999
		    	avg_away_odd = 9999

		   	# Extract maximum odds of the match
		    	# Put 9999 if unidentified
		    try:
		    	max_odds = driver.find_elements_by_xpath('//*[@class="highest"]')[0].text
		    	max_home_odd = float(max_odds.split(" ")[1])
		    	max_draw_odd = float(max_odds.split(" ")[2])
		    	max_away_odd = float(max_odds.split(" ")[3])
		    except:
		    	max_home_odd = 9999
		    	max_draw_odd = 9999
		    	max_away_odd = 9999
		    
		    # Add the data into a dataframe
		    actual_df = pd.DataFrame([[match_id, match_url, sport, country, competition, 
			          home_team, away_team, match_date, start_time,
			          home_score, away_score, ftr, 
			          home_score_1st_halftime,away_score_1st_halftime,
			          home_score_2nd_halftime,away_score_2nd_halftime,
			          avg_home_odd,avg_draw_odd,avg_away_odd,
			          max_home_odd,max_draw_odd,max_away_odd,
			          scraping_date, scraping_time
			         ]], columns = header)
		    bets_df = bets_df.append(actual_df)

		    # Add them to the global CSV file of scraped data
		    actual_df.to_csv(cwd + "scraped_data/all_scraped_data.csv", header=False, index=False, mode="a")
		    
		    time.sleep(wt*random()) #Ensure the embbeded text generated by javascript is loaded

		    visit_back_with_random_moves(yesterday_url)

		    time.sleep(wt*random())

	# Record the actual date and time
	now_time = datetime.now().strftime('%Hh%Mmin%Ss')
	now_date = datetime.today().strftime('%Y%m%d')

	# Export all the scraped data by the script into a CSV file 
	bets_df.to_csv(cwd + "scraped_data/batch_results/" + now_date + "_" + now_time + "_scraped_data.csv", header=True, index=False)

	print("--------- END ---------")
	driver.quit()
	end = time.time()
	print(end - start)
