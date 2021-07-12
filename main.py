# Leave this script open to scrape the
import csv
import requests
import time
import datetime as dt

def get_feed():
    site = r"http://parkingspaces.csuohio.edu/feed.php"
    ids = ['WG', 'CG', 'EG', 'SG']
    agent = r"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
    r = requests.get(site, headers={'user-agent': agent})
    out = r.json()
    return out

def process_feed(feed: list):
    result_dict = {}
    date = feed[0]['updated']
    outlist = []
    outlist.append(date)
    for lot in feed:
        name = lot['name']
        if "Total" in name:
            continue
        outlist.append(name)
        subscriber_cap = int(lot['SubscriberCapacity'])
        subscriber_occupied = int(lot['SubscriberCount'])
        trans_cap = int(lot['TransietCapacity'])
        trans_occupied = int(lot['TransietCount'])

        subscriber_open = subscriber_cap - subscriber_occupied
        trans_open = trans_cap - trans_occupied

        sub_open_perc = round(subscriber_open / subscriber_cap, 2)
        trans_open_perc = round(trans_open / trans_cap, 2)
        outlist.extend([subscriber_open, sub_open_perc, trans_open, trans_open_perc])
    return outlist

while True:
    out = get_feed()
    final = process_feed(out)
    csv_file = "CSU_parking_live.csv"
    try:
        with open(csv_file, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(final)
    except IOError:
        print("I/O error")
    print(f"Ran at {dt.datetime.now()}")
    print('Sleeping fifteen minutes.')
    time.sleep(15*60) # fifteen minute wait