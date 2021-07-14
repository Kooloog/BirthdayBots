import os
import time
import schedule


def run_code():
    os.system("python3 post_to_bot.py")


schedule.every().day.at("14:00").do(run_code)

while True:
    schedule.run_pending()
    time.sleep(1)
