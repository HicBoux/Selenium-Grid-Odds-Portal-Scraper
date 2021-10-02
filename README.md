<h1>Selenium-Grid-Odds-Portal-Scraper</h1>

A simple dockerized web scraper of sport odds and results for the odds monitoring website oddsportal.com. Built in Python with Selenium Grid.

<h2>Type of data scraped :</h2>

<ul>
    <li>URL</li>
    <li>Teams playing</li>
    <li>Country & Competition</li>
    <li>Date & Time</li>
    <li>Final & Half time scores</li>
    <li>Final result</li>
    <li>Average odds of all bookmakers</li>
    <li>Maximum odds found among all bookmakers</li>
    <li>Scraping datetime</li>
</ul>

<h2>How to set it :</h2>

1) Set the config files as wished:</br>
-Feel free to add or remove sports to scrape so that there is a valid URL like "https://www.oddsportal.com/matches/soccer"</br>
-You can change the "waiting_time_multiplicator" value which modifies the time to wait a page is loaded.</br>
```json
{
	"sport":["handball","rugby","hockey","soccer","basketball","baseball","volleyball","pesapallo"],
	"waiting_time_multiplicator":0.05
}
```

2) Open a terminal and change your current directory to the repository's root one and execute :</br>
-Simply with the makefile: ```make```</br>
-Or with docker-compose: ```docker-compose up```

3) Wait a few minutes and check the results appended to the CSV file "./scraper/scraped_data/all_scraped_data.csv" or which have been created as a CSV with date and time of execution into "./scraper/scraped_data/batch_results".

4) If necessary, it is possible to remove/uninstall the whole app/docker image from the disk with the following command : ```make uninstall```
<h2>Credits :</h2>

Copyright (c) 2021, HicBoux. Work released under MIT License. 

(Please contact me if you wish to use my work in specific conditions not allowed automatically by the MIT License.)

<h2>Disclaimer :</h2>

This solution has been made available for informational and educational purposes only. I hereby disclaim any and all 
liability to any party for any direct, indirect, implied, punitive, special, incidental or other consequential 
damages arising directly or indirectly from any use of this content, which is provided as is, and without warranties.
I also disclaim all responsibility for web scraping at a disruptive rate and eventual damages caused by a such use.
