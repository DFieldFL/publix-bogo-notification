from bogos import ScrapeBogos
import twitter

def lambda_handler(event, context):
  bogos = ScrapeBogos('https://accessibleweeklyad.publix.com/PublixAccessibility/BrowseByListing/ByCategory/?ListingSort=8&StoreID=2501049&CategoryID=5232521', '', '')
  bogos.initialize()
  tweetBogoBeers(bogos.getBeerList())

def tweetBogoBeers(beerList):
  api = twitter.Api(consumer_key='',
                    consumer_secret='',
                    access_token_key='',
                    access_token_secret='')
  if beerList:
    for beer in beerList:
      print(beer);
      api.PostUpdate(beer)
  else:
    print("nothing found");
    api.PostUpdate("Sorry no 🍺 this week 😞!")
