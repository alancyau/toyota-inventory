import json
import haversine as hs
from haversine import Unit


START_COORDINATES = (28.426846,77.088834)
RADIUS = 10000  # In miles
MODEL = 'car_model'


def dealer_distance(dealers):
    dealers_within_radius = []
    for dealer in dealers:
        dealer_coordinates = (dealer['latitude'], dealer['longitude'])
        distance = hs.haversine(START_COORDINATES,dealer_coordinates,unit=Unit.MILES)
        if distance < RADIUS:
            dealers_within_radius.append(dealer['code'])
    return dealers_within_radius



def load_dealers(file):
    with open(file) as json_file:
        return json.load(json_file)


def main():
    dealers = load_dealers('toyota_dealers.json')
    data = dealer_distance(dealers)
    print(data)


if __name__ == "__main__":
    main()