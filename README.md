# Publix BOGO Beer
Publishes the Buy One Get One beers to the Twitter account of your choosing using AWS Lambda

## Requirements
Python 3.7.x
Twitter API Credentials

## Installation and Setup
1. Clone the repository
1. Install the dependencies `pip install -r requirements.txt`
1. Fill out the Twitter API Credentials in BogoMain.py
1. Fill out the URL for parsing the Publix Ads (Go to the Publix Ads page and scroll to the bottom for "WEEKLY AD ACCESSIBILITY". One of the pages in that area is what is currently being used)
1. Test it out `python -c 'from BogoMain import *; lambda_handler("", "");'`
