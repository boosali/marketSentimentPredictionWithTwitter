import Controller.twitter as twc
import Models.tweet as tw
from flask import Flask
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Store/KwakKwak.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True

twitter_api_bearer_token = 'AAAAAAAAAAAAAAAAAAAAAOcJGAEAAAAAV49HukMG3MWpW0TJ6TsKerTIwxI%3DXi0jJje4RZAzQUei3D36ZK7rH9aaXzV5JdvUv5u1i2ig8Uo8U5'
to_search_in_twitter = 'NASDAQ'


def main():

    twitter = twc.TweeterController(OauthToken=twitter_api_bearer_token)
    next_page = ''
    counter = 0
    while True:
        relevant_tweets = twitter.search_tweets_post(to_search_in_twitter, next=next_page)
        if relevant_tweets.status_code == 200:
            json_of_tweets = relevant_tweets.json()

            for tweet in json_of_tweets['results']:
                symbols = ''
                companies = ''
                for tweet_symbol in tweet['entities']['symbols']:
                    symbols = str(symbols) + str(tweet_symbol['text']) + ","

                for tweet_compeny in tweet['entities']['user_mentions']:
                    companies = companies + tweet_compeny['name'] + ","

                if len(tweet['entities']['urls']) > 0:
                    url = tweet['entities']['urls'][0]['url']
                else:
                    url = 'No URL SUPPLIED'

                format_timestamp = datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S %z %Y')

                new_tweet = tw.Tweet(text=tweet['text'],
                                     timestamp=format_timestamp,
                                     source=tweet['user']['screen_name'],
                                     symbols=symbols,
                                     company_names=companies,
                                     url=url,
                                     verified=tweet['user']['verified'],
                                     followers=tweet['user']['followers_count']
                                     )
                new_tweet.save_to_db()

            counter += 1
            print("Imported 100 Results: " + str(counter) + "th time")

        else:
            if relevant_tweets.status_code == 429:
                print("Exceeded Allowed API activation within 15 minute window")
                break
            else:
                print("Error with Tweets request: " + str(relevant_tweets.status_code) + " With Message: " + relevant_tweets.content)


        if json_of_tweets['next'] and relevant_tweets.status_code != 429:
            next_page = json_of_tweets['next']
        else:
            print("Done Collecting Data")
            break

    print("Finished Execution")


if __name__ == "__main__":
    from db import db
    db.init_app(app)
    db.create_all()
    main()
