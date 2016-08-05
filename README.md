# tweetdelete

A command line script to export, delete, and/or unlike tweets. Tweets can be "protected" from deletion by their IDs if they contains keywords, their age, or (for own tweets) the number of retweets and likes. 


Original script by Mathew Inkson (http://www.mathewinkson.com/2015/03/delete-old-tweets-selectively-using-python-and-tweepy)
released unter the "Unlicense" (http://unlicense.org) as public domain. Fork of a modified version published on GitHub by Daniel Faulknor (also public domain under the "Unlicense").

Some of the things I've added/changed:

 - added command line arguments
 - added settings.ini for defaults and auth data
 - export tweets (as JSON)
 - wait after tweepy errors, then restart (e.g. work around rate limiting in a very simple way)
 - some exception handling / value validation  (incomplete) 


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

`python3 tweetdeleter.py --unlike --tweetids "755877343051259906,755872834258337792"`

Delete all tweets, except the tweets with the ID 755877343051259906 and 755872834258337792

`python3 tweetdeleter.py --unlike --likedkws "python,pandas,flask`

Unlike all tweets, except those containing either "python" or "pandas" or "flask" (case-insensitive)

`python3 tweetdeleter.py --unlike --verbose`

Unlike all tweets, detailed output

`python3 tweetdeleter.py --export --delete`

Export and delete all tweets.

`python3 tweetdeleter.py --export --delete --unlike --verbose`

Export all tweets and liked tweets, delete all tweets, unlike all liked tweets, detailed output
