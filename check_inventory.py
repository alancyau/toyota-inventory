import json
import requests
import haversine as hs
from haversine import Unit


START_COORDINATES = (34.0522, -118.2437)
RADIUS = 200  # In miles
CAR_MODEL = 'grcorolla'
CAR_YEAR = 2023


def load_dealers(file):
    with open(file) as json_file:
        return json.load(json_file)


def calc_dealer_distance(dealer_database):
    dealers_in_radius = []
    for dealer in dealer_database:
        dealer_coordinates = (dealer['latitude'], dealer['longitude'])
        distance = hs.haversine(START_COORDINATES,dealer_coordinates,unit=Unit.MILES)
        if distance < RADIUS:
            dealers_in_radius.append(dealer['code'])
    return dealers_in_radius


def get_inventory(dealers):
    inventory = []
    for dealer in dealers:
    # json objects to the send to the toyota api
        data = {
        "brand": "TOY",
        "mode": "content",
        "group": True,
        "groupmode": "full",
        "relevancy": False,
        "pagesize": 200,
        "pagestart": 0,
        "filter": {
            "year": [CAR_YEAR],
            "series": [CAR_MODEL],
            "dealers": [dealer],
            "andfields": ["accessory", "packages", "dealer"]
        }
        }
        headers = {'content-type': 'application/json'}
        json_object = json.dumps(data)
        # send POST request with data and headers objects
        r = requests.post("https://www.toyota.com/config/services/inventory/search/getInventory",
                        data=json_object,
                        headers=headers
                        )
        # convert response from POST request to json and query data for array of objects with each individual auto data
        json_response = r.json()
        response_array = json_response["body"]["response"]["docs"]
        for response in response_array:
            # save selected data to dict
            car = {
                "dealer": dealer,
                "dealer_name": "",
                "msrp_total": [response["priceInfo"]["totalMSRP"]],
                "msrp_base": [response["priceInfo"]["totalMSRP"]],
                "model_title": [response["model"]["title"]],
                "color": [response["exteriorcolor"]["title"]],
                "VIN": [response["vin"]]
            }
            inventory.append(car)
    return inventory


def decode_dealer(inventory, dealer_database):
    print('decoding dealers')
    for car in inventory:
        code = car['dealer']
        for dealer in dealer_database:
            if code == dealer['code']:
                car['dealer_name'] = dealer['name']
    return inventory


if __name__ == '__main__':
    dealer_database = load_dealers('toyota_dealers.json')
    dealers_in_radius = calc_dealer_distance(dealer_database)
    inventory = get_inventory(dealers_in_radius)
    inventory = decode_dealer(inventory, dealer_database)
    for i in inventory:
        print(f'{i} \n')
