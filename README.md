# Publix BOGO Beer
Parses Publix BOGO items based on search terms and publishes them to producers like Twitter and console.

# Requirements
- Python 3.10.x
- (Optional) Twitter API Credentials

# Development Setup
1. Clone the repository
2. Install the dependencies `pip install -r requirements-dev.txt`
3. Copy file `config.template.ini` and save it as `src/config.ini`
4. Modify the relevant information in `config.ini`
5. Fill out the URL for parsing the Publix Ads (Go to the Publix Ads page and scroll to the bottom for "WEEKLY AD ACCESSIBILITY". One of the pages in that area is what is currently being used)
6. Execute `main.py`

## Updating Dependencies
1. `pip install -r requirements-minimum.txt`
2. run tests
3. execute program to use the Console Producer
4. `pip freeze > requirements.txt`

# AWS Lambda Setup
1. Clone the repository
2. Install the dependencies `pip install -r requirements.txt`
3. Copy file `config.template.ini` and save it as `src/config.ini`
4. Modify the relevant information in `config.ini`
5. Fill out the URL for parsing the Publix Ads (Go to the Publix Ads page and scroll to the bottom for "WEEKLY AD ACCESSIBILITY". One of the pages in that area is what is currently being used)
6. Test it out `cd src` and execute `python -c 'from publix_bogos.main import *; lambda_handler("", "");'`
7. Zip the project files `cd src` and `zip -r ~/bogo.zip publix_bogos config.ini -x "*__pycache__*"`
8. Add projects dependencies (`site-packages`). cd to `site-packages` (`python -m site`) and execute this command `zip -r ~/bogo.zip .`

# Config
## Logging
| Property | Description |
| :--- | :--- |
| level | Set logging level. ex. DEBUG, INFO, WARN, or ERROR |

## BOGO
| Property | Description |
| :--- | :--- |
| url | URL for parsing the Publix Ads. Go to the Publix Ads page and scroll to the bottom for "WEEKLY AD ACCESSIBILITY". Choose one of the pages withing Accessibility to use the copy and paste the url into this property. |
| keywords | Keywords to use to match for notification. Separate keywords with a comma (ex `beer,lager,ale,pilsner,ipa`). |
| prefix_text | Text to put at the beginning of the notification |
| postfix_text | Text to put at the end of the notification |
| no_bogo_text | Text to use if there are no keyword matches |
| producers | Names of producers to enable. Choose from: 'twitter_producer', 'logging_producer', etc. |

## Twitter Producer (optional)
If the section does not exist the output will only be to the console. If you would like to post to twitter apply for a [developer account](https://developer.twitter.com/en/apply-for-access) and enter in required info in this section.
