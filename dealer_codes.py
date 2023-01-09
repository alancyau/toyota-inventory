import json
import requests


def get_dealer_codes(zip_codes):
    data = []
    for idx, zip in enumerate(zip_codes):
        print(idx)
        response = requests.get(f'https://www.toyota.com/service/tcom/locateDealer/zipCode/{zip}')
        response_json = response.json()
        dealer_codes = [x['code'] for x in response_json['dealers']]  # Filter to dealer codes
        data.extend(dealer_codes)
    return data


# Remove duplicate dealer codes
def clean_dealer_codes(dealers):
    clean_data = []
    [clean_data.append(x) for x in dealers if x not in clean_data] 

    with open(r'dealer_codes.txt', 'w') as fp:
        for item in clean_data:
            fp.write("%s\n" % item)


def load_zip(file):
    with open('us_cities.json', 'r') as f:
        data = json.load(f)
        return [x['zip_code'] for x in data]


def main():
    zip_codes = load_zip('us_cities.json')
    dealers = get_dealer_codes(zip_codes)
    clean_dealer_codes(dealers)
    print(dealers)


if __name__ == "__main__":
    main()