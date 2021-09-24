import apikeys
import calendar
import tweepy
import os
import requests
import datetime
import time
import locale

# CONNECTING TO THE ENGLISH ANIMAL CROSSING BOT ACCOUNT
acen_auth = tweepy.OAuthHandler(apikeys.acen_consumer_key, apikeys.acen_consumer_secret)
acen_auth.set_access_token(apikeys.acen_access_token, apikeys.acen_access_secret)
acen_api = tweepy.API(acen_auth)

# CONNECTING TO THE SPANISH ANIMAL CROSSING BOT ACCOUNT
aces_auth = tweepy.OAuthHandler(apikeys.aces_consumer_key, apikeys.aces_consumer_secret)
aces_auth.set_access_token(apikeys.aces_access_token, apikeys.aces_access_secret)
aces_api = tweepy.API(aces_auth)

# CONNECTING TO THE FIRE EMBLEM BOT ACCOUNT
fe_auth = tweepy.OAuthHandler(apikeys.fe_consumer_key, apikeys.fe_consumer_secret)
fe_auth.set_access_token(apikeys.fe_access_token, apikeys.fe_access_secret)
fe_api = tweepy.API(fe_auth)


# Receives a month and a day as integers, and converts the date to a proper string like "July 13th" or "March 21st".
def get_day_string(_month, _day):
    date_end = "th"
    if _day == 1 or _day == 21 or _day == 31:
        date_end = "st"
    elif _day == 2 or _day == 22:
        date_end = "nd"
    elif _day == 3 or _day == 23:
        date_end = "rd"

    return calendar.month_name[int(_month)] + " " + str(_day) + date_end


# Gets all info from the character stored in the birthday variable, creates the necessary strings, downloads their
# respective image from imgur and then posts the result on the right bot account.
def convert(birthday):
    # STEP 1: Generate the tweet's text, language depends on the bot.
    if birthday[4] == 'ACEN' or birthday[4] == 'FE':
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
        status = f"Today, {get_day_string(birthday[0], birthday[1])}, is {birthday[2]}'s{birthday[5]}birthday!"
    else:
        locale.setlocale(locale.LC_ALL, 'es_ES.UTF-8')
        status = f"Hoy, {birthday[1]} de {calendar.month_name[int(birthday[0])]}, ¡es el cumpleaños de "
        if birthday[5] != ' ':
            status += f"{birthday[2]}{birthday[5]}!"
        else:
            status += f"{birthday[2]}!"

    # STEP 2: Get the tweet's image from Imgur. The databases contain the link to each character's picture.
    imgur_get = requests.get("https://i.imgur.com/" + birthday[3], allow_redirects=True)
    open('picture.png', 'wb').write(imgur_get.content)

    # STEP 3: Post tweet (with both text and media) to the correct account.
    # UPDATE: Added loop due to common over-capacity errors that have been appearing lately
    while True:
        try:
            if birthday[4] == 'ACEN':
                acen_api.update_with_media('picture.png', status)
            elif birthday[4] == 'ACES':
                aces_api.update_with_media('picture.png', status)
            elif birthday[4] == 'FE':
                fe_api.update_with_media('picture.png', status)
        except tweepy.error.TweepError:
            continue
        break

    os.remove('picture.png')


# Main code starts here.
day = datetime.date.today().day
month = datetime.date.today().month
date_to_find = str(month) + "|" + str(day)

# With the current day and month stored, the program will search in all databases for the characters whose birthday
# is today. To do this, it seeks lines starting with "month|day". For example, 4|22 represents April 22nd.
for file in os.listdir("databases"):
    database = open('databases/' + file, "r", encoding="utf8")
    for line in database:
        if line.startswith(date_to_find):
            # If these lines are being executed, it means the program has found a character with their birthday being
            # the current day. Data from the character is converted to an array, then passed to the convert function.

            found = line.split('|')
            convert(found)
            time.sleep(15)  # Cool-down so that Twitter does not think I'm running a spam bot.
