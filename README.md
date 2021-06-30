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

### Config
#### BOGO
| Property | Description |
| --- | --- |
| url | URL for parsing the Publix Ads. Go to the Publix Ads page and scroll to the bottom for "WEEKLY AD ACCESSIBILITY". Choose one of the pages withing Accessibility to use the copy and paste the url into this property. |
| keywords | Keywords to use to match for notification. Seperate keywords by the comma |
| keywordMultiWord | If true the keyword match will span multiple words (ex. `hot dog,peanut butter`) |
| prefixText | Text to put at the beginning of the notification |
| postfixText | Text to put at the end of the notification |
| noBogoText | Text to use if there are no keyword matches |

#### TwitterApi (optional)
If the section does not exist the output will only be to the console. If you would like to post to twitter apply for a [developer account](https://developer.twitter.com/en/apply-for-access) and enter in required info in this section.
