# tweetdeleter

A command line script to delete, and/or unlike tweets (and export them prior to that). Tweets can be "protected" from deletion by their IDs, or if they contains keywords, or by their age, or (for own tweets) by the number of retweets and likes. 


Original script by Mathew Inkson (http://www.mathewinkson.com/2015/03/delete-old-tweets-selectively-using-python-and-tweepy)
released unter the "Unlicense" (http://unlicense.org) as public domain. Fork of a modified version published on GitHub by Daniel Faulknor (also public domain under the "Unlicense").

Some of the things I've added/changed:

 - added command line arguments
 - added settings.ini for defaults and auth data
 - export tweets (as JSON)
 - wait after tweepy errors, then restart (e.g. work around rate limiting in a very simple way)
 - some exception handling / value validation  (incomplete) 

## Configuration file (settings.ini)

If a corresponding command line argument is provided, it will override the value specified in the configuration file.
```
[Authentication]
ConsumerKey = YOUR_CONSUMER_KEY_HERE
ConsumerSecret = YOUR_CONSUMER_SECRET_HERE
AccessToken = YOUR_ACCESS_TOKEN_HERE
AccessTokenSecret = YOUR_ACCESS_TOKEN_SECRET_HERE

[DefaultValues]
DaysToKeep = ONLY_DELETE_TWEETS_OLDER_THAN_DAYSTOKEEP_DAYS
LikedThreshold = NUMBER_OF_LIKES_TO_PROTECT_TWEET_OR_-1_TO_DISABLE
RetweetThreshold = NUMBER_OF_LIKES_TO_PROTECT_TWEET_OR_-1_TO_DISABLE

[DefaultPaths]
TweetIDsPath = PATH_TO_A_TEXT_FILE_WITH_ONE_TWEET_ID_PER_LINE
LikedIDsPath = PATH_TO_A_TEXT_FILE_WITH_ONE_TWEET_ID_PER_LINE
TweetKeywordsPath = PATH_TO_A_TEXT_FILE_WITH_ONE_KEYWORD_PER_LINE
LikedKeywordsPath = PATH_TO_A_TEXT_FILE_WITH_ONE_KEYWORD_PER_LINE
```

## Examples

A couple of example calls from the command line:

`python3 tweetdeleter.py --delete`

Delete all tweets. Load options from "settings.ini".

`python3 tweetdeleter.py --delete --config "another_settings_file.ini"`

Delete all tweets. Load other options from "another_settings_file.ini" instead of the default "settings.ini"

`python3 tweetdeleter.py --delete --days 10`

Delete all tweets that are more than 10 days old. Load other options from "settings.ini".

`python3 tweetdeleter.py --delete --likes 5`

Delete all tweets that have fewer than 5 likes.Load other options from "settings.ini".

`python3 tweetdeleter.py --delete --retweets 5`

Delete all tweets that have fewer than 5 retweets. Load other options from "settings.ini".

`python3 tweetdeleter.py --delete --days 30 --retweets 5`

Delete all tweets that are more than 30 days old, but only if they have fewer than 5 retweets. Load other options from "settings.ini".

`python3 tweetdeleter.py --unlike --tweetids "755877343051259906,755872834258337792"`

Delete all tweets, except the tweets with the ID 755877343051259906 and 755872834258337792. Load other options from "settings.ini"

`python3 tweetdeleter.py --unlike --likedkws "python,pandas,flask`

Unlike all tweets, except those containing either "python" or "pandas" or "flask" (case-insensitive). Load other default options from "settings.ini".

`python3 tweetdeleter.py --unlike --verbose`

Unlike all tweets, detailed output

`python3 tweetdeleter.py --export --delete`

Export and delete all tweets.

`python3 tweetdeleter.py --export --delete --unlike --verbose`

Export all tweets and liked tweets, delete all tweets, unlike all liked tweets, detailed output

## Requirements

- Python 3
- tweepy

## License
Apache License (2.0)
