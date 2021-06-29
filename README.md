# Publix BOGO Beer
Publishes the Buy One Get One beers to the Twitter account of your choosing using AWS Lambda

## Requirements
- Python 3.7.x
- (Optional) Twitter API Credentials

## Installation and Setup
1. Clone the repository
1. Install the dependencies `pip install -r requirements.txt`
1. Copy file `config.template.ini` and save it as `config.ini`
1. Modify the relevant information in `config.ini`
1. Fill out the URL for parsing the Publix Ads (Go to the Publix Ads page and scroll to the bottom for "WEEKLY AD ACCESSIBILITY". One of the pages in that area is what is currently being used)
1. Test it out `python -c 'from BogoMain import *; lambda_handler("", "");'`
1. Zip the project files `zip -g ~/bogo.zip BogoMain.py bogos.py config.ini`
1. Add projects dependencies (`site-packages`). cd to `site-packages` and execute this command `zip -r9 ~/bogo.zip .`
