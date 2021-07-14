import os
import time
import schedule


def run_code():
    os.system("python3 main.py")
    time.sleep(5)
    os.system("python3 principal.py")
    time.sleep(60)
    print("Done!")


schedule.every().day.at("14:00").do(run_code)

while True:
    schedule.run_pending()
    time.sleep(1)
