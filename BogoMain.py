from bogos import ScrapeBogos

import configparser
import twitter


def lambda_handler(event, context):
    config = configparser.ConfigParser()
    config.read("config.ini")
    keywords = ""
    keywordMultiWord = False
    url = ""
    prefixText = ""
    postfixText = ""
    noBogoText = ""

    print("Config values:")
    if "BOGO" not in config:
        print("No BOGO config found")
        return
    else:
        bogoConfig = config["BOGO"]
        if "keywords" not in bogoConfig or "url" not in bogoConfig:
            print("'keywords' or 'url' was provided in the config")
            return
        else:
            keywords = bogoConfig["keywords"].split(",")
            print("keywords: " + str(keywords))
            url = bogoConfig["url"]
            print("url: " + url)

    if "keywordMultiWord" in bogoConfig:
        keywordMultiWord = bogoConfig["keywordMultiWord"].lower() == "true"
        print("keywordMultiWord: " + str(keywordMultiWord))

    if "prefixText" in bogoConfig:
        prefixText = bogoConfig["prefixText"]
        print("prefixText: " + prefixText)

    if "postfixText" in bogoConfig:
        postfixText = bogoConfig["postfixText"]
        print("postfixText: " + postfixText)

    if "noBogoText" in bogoConfig:
        noBogoText = bogoConfig["noBogoText"]
        print("noBogoText: " + noBogoText)

    consumer_key = ""
    consumer_secret = ""
    access_token_key = ""
    access_token_secret = ""
    if "TwitterApi" in config:
        twitterConfig = config["TwitterApi"]
        consumer_key = twitterConfig["consumer_key"]
        consumer_secret = twitterConfig["consumer_secret"]
        access_token_key = twitterConfig["access_token_key"]
        access_token_secret = twitterConfig["access_token_secret"]

    print("End of config values")
    print("====================\n")

    bogos = ScrapeBogos(url, keywords, keywordMultiWord, prefixText, postfixText)
    bogos.initialize()
    tweetBogo(
        bogos.getItemsFound(),
        noBogoText,
        consumer_key,
        consumer_secret,
        access_token_key,
        access_token_secret,
    )


def tweetBogo(
    itemsFound,
    noBogoText,
    consumer_key,
    consumer_secret,
    access_token_key,
    access_token_secret,
):
    twitterApi = None
    if consumer_key and consumer_secret and access_token_key and access_token_secret:
        twitterApi = twitter.Api(
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            access_token_key=access_token_key,
            access_token_secret=access_token_secret,
        )
    if itemsFound:
        for item in itemsFound:
            print(item)
            if twitterApi:
                print("posting to twitter: " + item)
                twitterApi.PostUpdate(item)
    elif noBogoText:
        print(noBogoText)
        if twitterApi:
            print("posting to twitter: " + noBogoText)
            twitterApi.PostUpdate(noBogoText)
    else:
        print("nothing found")
