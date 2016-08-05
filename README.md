# TweetDeleter




Original script by Mathew Inkson (http://www.mathewinkson.com/2015/03/delete-old-tweets-selectively-using-python-and-tweepy)
released unter the "Unlicense" (http://unlicense.org) as public domain. Fork of a modified version published on GitHub by Daniel Faulknor (also public domain under the "Unlicense").


## Examples

A couple of example calls from the command line:

`python3 tweetdeleter.py --delete`

Delete all tweets.

`python3 tweetdeleter.py --delete --days 10`

Delete all tweets that are more than 10 days old

`python3 tweetdeleter.py --delete --likes 5`

Delete all tweets that have fewer than 5 likes

`python3 tweetdeleter.py --delete --retweets 5`

Delete all tweets that have fewer than 5 retweets

`python3 tweetdeleter.py --delete --days 30 --retweets 5`

Delete all tweets that are more than 30 days old, but only if they have fewer than 5 retweets


`python3 tweetdeleter.py --unlike --verbose`

Unlike all tweets, detailed output

`python3 tweetdeleter.py --export --delete`

Export and delete all tweets.



`python3 tweetdeleter.py --export --delete --unlike --verbose`

Export all tweets and liked tweets, delete all tweets, unlike all liked tweets, detailed output
