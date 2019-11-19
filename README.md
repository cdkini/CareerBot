
# <img src="images/logo.png" width="37.5" height="37.5">CareerBot 
A Discord bot aimed to help aspiring developers (or any job seekers in any industry) identify available job postings based on user criteria and save them for future use. All scraped job data comes from Indeed.com. 

Feel free to play around with it in a test server: https://discord.gg/eGWQJqU (Requires a Discord account to actually use but one can view with just the link.)

# Installation
### Dependencies
* <b>bs4</b> (<i>0.0.1</i>): Used to scrape motivational quotes / job postings.
* <b>discord</b> (<i>1.3.0a</i>): Used to access [Discord's API](https://discordpy.readthedocs.io/en/latest/index.html).
* <b>pandas</b> (<i>0.25.2</i>): Used to store/organize scraped data.

Python 3.8.0 was used to write this bot but 3.6.0 and newer should be compatible due to usage of f-strings.

### Other
Create your own credentials file for the bot's token and save it in the main directory (I've used a file named secrets.py, which is noted in the .gitignore). Tokens can be generated from the developer tools within Discord. 

# Usage
![CareerBot Functions](images/all_functions.PNG)
CareerBot functions are split into three primary categories: 
* <b>General</b>: Basic commands to talk to CareerBot.
* <b>Query</b>: Commands regarding the generation of job results based on given criteria.
* <b>Database</b>: Commands used to access and/or delete saved job results from prior queries.

Functions are called using "-function."

<i>For example</i>: <b>-hello</b> --> Returns a greeting. 


For functions that have {brackets} in their description, ensure that you enter a valid argument after calling the function. 

<i>For example</i>: <b>-generate "software developer/new york/entry"</b> --> Returns job postings that meet the given criteria.

Use -help to reveal all available functions and their parameters.

# License
MIT

This project is meant purely as a means of developing my programming abilities and is not intended to be monetized in any way. If you would like to collaborate or suggest revisions, please fork/pull accordingly!
