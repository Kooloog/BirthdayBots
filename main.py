# This is the program that the server executing this software is constantly running.

import os
import time
import schedule


# Very simple function that simply runs the important code
def run_code():
    os.system("python3 post_to_bot.py")


# This line executes the above function every day at 2pm CEST (my timezone)
schedule.every().day.at("14:00").do(run_code)

# And now we wait :)
while True:
    schedule.run_pending()
    time.sleep(1)
