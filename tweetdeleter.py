#!/usr/bin/env python
 
import os
import sys
import argparse
import datetime 
import configparser
import time
import tweepy

class TweetDeleter():
    def __init__(self, days_to_keep=0, simulate=False, verbose=True):
        self.simulate = simulate
        self.verbose = verbose
        self.script_dir = os.path.dirname(os.path.realpath(sys.argv[0]))
        self.tweet_ids_to_keep = []
        self.fav_ids_to_keep = []
        self.tweet_strings_to_keep = []
        self.fav_strings_to_keep = []
        self.tweet_fav_threshold = -1
        self.tweet_retweet_threshold = -1
        try: 
            days_to_keep = int(days_to_keep)
        except TypeError:
            print("Please provide a number of days to keep, set to 0 to delete all:\n{}".format(e))
        else:
            self.cutoff_date = datetime.datetime.utcnow() - datetime.timedelta(days=days_to_keep)
            print("Keeping tweets from the last {} days. Cutoff date: {} (UTC)".format(days_to_keep, self.cutoff_date))      

    def list_loader(self, list_path, target, list_type):
        try:
            with open(list_path) as h:
                target = [l.strip("\n").strip() for l in h.readlines()]
        except IOError:
            print("Could not read {} file.".format(list_type))                

    def load_tweets_ids_to_keep_from_file(self, id_path):
        self.list_loader(id_path, self.tweet_ids_to_keep, "tweet ID")

    def load_tweets_strings_to_keep_from_file(self, str_path):
        self.list_loader(str_path, self.tweet_strings_to_keep, "tweet strings")

    def load_fav_ids_to_keep_from_file(self, id_path):
        self.list_loader(id_path, self.fav_ids_to_keep, "liked tweet ID")

    def load_fav_strings_to_keep_from_file(self, str_path):
        self.list_loader(str_path, self.fav_strings_to_keep, "liked tweet strings")

    def set_days_to_keep(self, days_to_keep):
        try: 
            days_to_keep = int(days_to_keep)
        except TypeError:
            print("Please provide a number of days to keep, set to 0 to delete all:\n{}".format(e))
        else:
            self.cutoff_date = datetime.datetime.utcnow() - datetime.timedelta(days=days_to_keep)
            print("Keeping tweets from the last {} days. Set cutoff date to {} (UTC)".format(days_to_keep, self.cutoff_date))        

    def set_cutoff_date(self, cutoff_date):
        try:
            self.cutoff_date = datetime.datetime.strptime(cutoff_date, '%Y-%m-%d')
        except (TypeError, ValueError, NameError) as e:
            print("Could not set a cutoff date. Please provide a date as a YYYY-MM-DD string:\n{}".format(e))
        else:
            self.cutoff_date = datetime.datetime.strptime(cutoff_date, '%Y-%m-%d')
            print("Set cutoff date to {} (UTC)".format(self.cutoff_date))

    def authenticate_from_config(self, config_path=None):
        if not config_path:
            config_path = os.path.join(self.script_dir, "settings.ini")
        config = configparser.SafeConfigParser()
        try:
            with open(config_path) as h:
                config.read_file(h)
        except IOError:
            print("Please specify a valid config file or use command line arguments to authenticate. An empty template has been created as settings.ini")
            self.create_config_template()
        else:
            try:
                ck = config.get('Authentication', 'ConsumerKey')
                cs = config.get('Authentication', 'ConsumerSecret')
                at = config.get('Authentication', 'AccessToken')
                ats = config.get('Authentication', 'AccessTokenSecret')
            except (configparser.NoSectionError,):
                print("Please check the authentication information in your configuration file.")
            else:
                if all([ck, cs, at, ats]):
                    self.authenticate(ck, cs, at, ats)
                else:
                    print("Please check the authentication information in your configuration file.")

    def authenticate(self, consumer_key, consumer_secret, access_token, access_token_secret):
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(auth)
        try: 
            self.me = self.api.me()
        except tweepy.error.TweepError as e:
            print("Please check the authentication information:\n{}".format(e))
            self.api = None
            self.me = None
 
    def create_config_template(self):
        config = configparser.SafeConfigParser()
        config.optionxform = str
        config.add_section("Authentication")
        config.set("Authentication", "ConsumerKey", "")
        config.set("Authentication", "ConsumerSecret", "")
        config.set("Authentication", "AccessToken", "")
        config.set("Authentication", "AccessTokenSecret", "")
        config.add_section("DefaultValues")
        config.set("DefaultValues", "DaysToKeep", "")
        config.set("DefaultValues", "TweetFavThreshold", "")
        config.set("DefaultValues", "TweetRetweetThreshold", "")
        config.add_section("DefaultPaths")
        config.set("DefaultPaths", "TweetIDsToKeepPath", "")
        config.set("DefaultPaths", "FavIDsToKeepPath", "")
        config.set("DefaultPaths", "StringsToKeepPath", "")

        with open(os.path.join(self.script_dir, "settings.ini"), "w") as h:
            config.write(h)

    def contains_strings_to_keep(self, tweet, fav=False):
        if fav:
            protected = any([True for s in self.fav_strings_to_keep if s.lower() in tweet.text.lower()])
        else:
            protected = any([True for s in self.tweet_strings_to_keep if s.lower() in tweet.text.lower()])
        return protected

    def is_protected_tweet(self, tweet):
        protected = False
        if tweet.id in self.tweet_ids_to_keep:
            protected = True
        elif tweet.created_at >= self.cutoff_date:
            protected = True
        elif self.contains_strings_to_keep(tweet):
            protected = True
        elif self.tweet_fav_threshold != -1 and tweet.favorite_count >= self.tweet_fav_threshold:
            protected = True
        elif self.tweet_retweet_threshold != -1 and tweet.retweet_count >= self.tweet_retweet_threshold:
            protected = True
        return protected

    def is_protected_like(self, tweet):
        protected = False
        if tweet.id in self.fav_ids_to_keep:
            protected = True
        elif tweet.created_at >= self.cutoff_date:
            protected = True
        elif self.contains_strings_to_keep(tweet, fav=True):
            protected = True
        elif self.tweet_fav_threshold != -1 and tweet.favorite_count >= self.tweet_fav_threshold:
            protected = True
        elif self.tweet_retweet_threshold != -1 and tweet.retweet_count >= self.tweet_retweet_threshold:
            protected = True
        return protected

    def delete_tweets(self):
        if not self.api:
            return
        # rate limit appears to be 350 request / hour
        print("Deleting tweets older than {}".format(self.cutoff_date))
        if self.tweet_ids_to_keep:
            print("Keeping tweets with the following ids: {}".format(self.tweet_ids_to_keep))
        if self.tweet_strings_to_keep:
            print("Keeping tweets containing the following strings (case-insensitive): {}".format(self.tweet_strings_to_keep))
        if self.tweet_retweet_threshold > -1:
            print("Keeping tweets with at least {} retweets".format(self.tweet_retweet_threshold))
        if self.tweet_fav_threshold > -1:
            print("Keeping tweets with at least {} likes".format(self.tweet_fav_threshold))
        timeline_tweets = tweepy.Cursor(self.api.user_timeline).items()
        deletion_count = 0
        ignored_count = 0
        try:
            for ind, tweet in enumerate(timeline_tweets):
                if not self.is_protected_tweet(tweet) and not self.simulate:
                    try:
                        self.api.destroy_status(tweet.id) 
                    except tweepy.error.TweepError as e:
                        print("\t#{}\tCOULD NOT DELETE {} ({})".format(ind, tweet.id, tweet.created_at))
                        print("\t", e)
                    else:
                        deletion_count += 1
                        if self.verbose:
                            print("\t#{}\tDELETED {} ({})".format(ind, tweet.id, tweet.created_at))
                else:                    
                    ignored_count += 1
                    if self.verbose:
                        print("\t#{}\tKEEPING {} ({})".format(ind, tweet.id, tweet.created_at))
        except tweepy.error.TweepError as e:
            print(e)
            print("Waiting 10 minutes, then starting over ({})".format(datetime.datetime.now()))
            time.sleep(600)
            self.delete_tweets()
        print("{} tweets were deleted. {} tweets were protected.".format(deletion_count, ignored_count))

    def unlike_tweets(self):
        if not self.api:
            return
        likes = tweepy.Cursor(api.favorites).items()
        unliked_count = 0
        ignored_count = 0
        for ind, tweet in enumerate(likes):
            # Where tweets are not in save list and older than cutoff date
            if not is_protected_like(tweet) and not self.simulate:
                try:
                    api.destroy_favorite(tweet.id)
                except tweepy.error.TweepError as e:
                    print("\t#{}\tCOULD NOT UNLIKE {} ({})".format(ind, tweet.id, tweet.created_at))
                    print(e)
                else:
                    unliked_count += 1
                    if self.verbose:
                        print("\t#{}\tUNLIKED {} ({})".format(ind, tweet.id, tweet.created_at))
            else:
                ignored_count += 1
                if self.verbose:
                    print("\t#{}\tKEEPING {} ({})".format(ind, tweet.id, tweet.created_at))
        print("{} tweets were unliked. {} liked tweets were protected.".format(unliked_count, ignored_count))



if __name__ == "__main__":
    td = TweetDeleter(days_to_keep=0)
    td.authenticate_from_config()
    td.delete_tweets()
    td.unlike_tweets()