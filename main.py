import requests
from dotenv import load_dotenv
import os
import sys
import argparse
import json
import time
from datetime import datetime, timedelta

# Python 3.7<=
# Please install packages with 
# pip install requests python-dotenv

class Client:
        
    def __init__(self, product_id, token, maksimit, filters):
        self.BASE_URL = "https://api.kide.app/api"
        self.TOKEN = token
        self.id = product_id
        self.filters = filters
        self.inventoryId = None
        self.maksimit = maksimit
        self.quantity = 1
        self.start_at = None
        self.index = 0
        self.maxIndex = 1

    def nextIndex(self):
        if self.index + 1 <= self.maxIndex:
            self.index = self.index + 1
        else:
            print("Max variant index reached")
            print("No ticket this time :^(")
            sys.exit("Exiting...")

    def getStartAt(self):
        return self.start_at

    def reserveProduct(self):
        headers = {
        "Authorization": f"Bearer {self.TOKEN}", 
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
        }

        body = {
            "toCreate":[
                {
                "inventoryId": self.inventoryId,
                "quantity": self.quantity,
                "productVariantUserForm": None
                }
            ],
            "toCancel":[]
        }
        try:
            r = requests.post(f"{self.BASE_URL}/reservations", json=body, headers=headers)
            if r.status_code == 200:
                return r.json()
            return None
        except Exception as e:
            print(e)
            return None

    def fetchInfo(self):
        try:
            r = requests.get(f"{self.BASE_URL}/products/{self.id}")
            data = r.json()
            self.start_at = data["model"]["product"]["dateSalesFrom"]
            return data["model"]["product"]["name"]
        except:
            return None


    def fetchProduct(self):
        try:
            r = requests.get(f"{self.BASE_URL}/products/{self.id}")
            data = r.json()
            variants = data["model"]["variants"]
            self.maxIndex = len(variants) - 1

            if len(variants) == 0:
                return None

            if self.filters is not None:
                for filter in self.filters:
                    for variant in variants:
                        if filter in variant["name"] or filter in variant["description"]:
                            self.filters = None
                            name = variant["name"]
                            print(f"Found item '{name}'")
                            if self.maksimit:
                                self.quantity = variant["productVariantMaximumReservableQuantity"]
                            self.inventoryId = variant["inventoryId"]
                            return True

            if self.maksimit:
                self.quantity = variants[self.index]["productVariantMaximumReservableQuantity"]
            self.inventoryId = variants[self.index]["inventoryId"]

            name = variants[self.index]["name"]
            print(f"Found item '{name}'")

            return True

        except Exception as e:
            print(e)
            return False

def parseArgs():
    load_dotenv()
    TOKEN = os.getenv("TOKEN")

    if TOKEN is None:
        print("Error no token found")
        print("Create a .env file with TOKEN=<your_kide_jwt> in the same directory")
        sys.exit()

    parser = argparse.ArgumentParser()
    parser.add_argument("-i","--id", help="Id of the event", type=str, required=True)
    parser.add_argument("-f", "--filter", help="Looks for a word in the name and the description of the product. Multi usage allowed", dest="filters", action='append', type=str, required=False)
    parser.add_argument("-m", "--maksimit", help="Reserve the maxinum amount of tickets", action=argparse.BooleanOptionalAction, required=False)
    parser.add_argument("-n","--no-wait-log", help="Don't refresh time until reservation starts", dest='no_wait_log', action=argparse.BooleanOptionalAction, type=bool, required=False)
    args = parser.parse_args()
    return args, TOKEN


def main():
    args, TOKEN = parseArgs()
    client = Client(product_id=args.id, token=TOKEN, maksimit=args.maksimit, filters=args.filters)
    product = client.fetchInfo()

    if product == None:
        print("Invalid URL!")
        sys.exit()

    print(f"Starting booking for {product}")

    if args.filters is not None:
        print(f"Using filter(s) '{', '.join(args.filters)}'")
    print("======")
    while True:
        now = datetime.now()
        product_time = datetime.fromisoformat(client.getStartAt()[:-6])
        if product_time > now:
            if args.no_wait_log is not True:
                print(f"Product reservation starts in {product_time - now}")
            time.sleep(1)
            continue

        product = client.fetchProduct()

        if product is None:
            print("No item found yet, trying again")
            time.sleep(0.1)
            continue

        res = client.reserveProduct()
        if res is None:
            print("Error reserving item, possibly already fully booked")
            print("Trying next item")
            print("======")

            client.nextIndex()
            continue
        name = res["model"]["reservations"][0]["variantName"]
        print(f"Success, reserved {client.quantity} ticket(s) of '{name}'")
        break

main()