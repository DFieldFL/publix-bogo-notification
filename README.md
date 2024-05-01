# Publix BOGO Beer
Publishes the Buy One Get One beers to the Twitter account of your choosing using AWS Lambda

## Requirements
- Python 3.10.x
- (Optional) Twitter API Credentials

## Installation and Setup
1. Clone the repository
2. Install the dependencies `pip install -r requirements.txt`
3. Copy file `config.template.ini` and save it as `config.ini`
4. Modify the relevant information in `config.ini`
5. Fill out the URL for parsing the Publix Ads (Go to the Publix Ads page and scroll to the bottom for "WEEKLY AD ACCESSIBILITY". One of the pages in that area is what is currently being used)
6. Test it out `python -c 'from BogoMain import *; lambda_handler("", "");'`
7. Zip the project files `zip -g ~/bogo.zip BogoMain.py bogos.py config.ini`
8. Add projects dependencies (`site-packages`). cd to `site-packages` and execute this command `zip -r9 ~/bogo.zip .`

## Updating Dependencies
1. `pip install -r requirements-minimum.txt`
2. run tests
3. execute program to use the Console Producer
4. `pip freeze > requirements.txt`

### Config
#### BOGO
| Property | Description |
| :--- | :--- |
| url | URL for parsing the Publix Ads. Go to the Publix Ads page and scroll to the bottom for "WEEKLY AD ACCESSIBILITY". Choose one of the pages withing Accessibility to use the copy and paste the url into this property. |
| keywords | Keywords to use to match for notification. Seperate keywords by the comma |
| keywordMultiWord | If true the keyword match will span multiple words (ex. `hot dog,peanut butter`) |
| prefixText | Text to put at the beginning of the notification |
| postfixText | Text to put at the end of the notification |
| noBogoText | Text to use if there are no keyword matches |

#### TwitterApi (optional)
If the section does not exist the output will only be to the console. If you would like to post to twitter apply for a [developer account](https://developer.twitter.com/en/apply-for-access) and enter in required info in this section.
