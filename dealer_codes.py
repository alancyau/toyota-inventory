import json
import requests


def load_zip(file):
    with open('us_cities.json', 'r') as f:
        data = json.load(f)
        return [x['zip_code'] for x in data]


def get_dealer_codes(zip_codes):
    data = []
    for zip in zip_codes:
        response = requests.get(f'https://www.toyota.com/service/tcom/locateDealer/zipCode/{zip}')
        response_json = response.json()
        dealer_codes = [x['code'] for x in response_json['dealers']]  # Filter to dealer codes
        data.extend(dealer_codes)
    
    # Remote duplicate dealer codes
    clean_data = []
    [clean_data.append(x) for x in data if x not in clean_data]

    with open(r'dealer_codes.txt', 'w') as fp:
        for item in clean_data:
            fp.write("%s\n" % item)

    return clean_data


def decode_dealer_codes(dealer_codes):
    data = []
    for dealer in dealer_codes:
        url = f'https://www.toyota.com/service/tcom/dealerDetail/dealerCode/{dealer}'
        response = requests.get(url)
        response_json = response.json()
        temp = response_json['dealers'][0]
        data.append(temp)

    with open("toyota_dealers.json", "w") as outfile:
        json.dump(data, outfile, indent=4)


def main():
    zip_codes = load_zip('us_cities.json')
    dealers = get_dealer_codes(zip_codes)
    decode_dealer_codes(dealers)


if __name__ == "__main__":
    main()