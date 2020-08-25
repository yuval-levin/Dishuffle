
import requests
import json
import random
from os import path

from pprint import pprint

'''user_input_address=input("כתובת \n")'''
user_input_address="אבן גבירול 80"
LANGUAGE="he"
TYPES="address"
RADIUS=100000

with requests.session() as session:
    session.get('https://wolt.com/v1/analytics-tags')
    params = {"input": user_input_address, "language": LANGUAGE, "types": TYPES, "radius": RADIUS}
    drop_down_addresses = session.get('https://restaurant-api.wolt.com/v1/google/places/autocomplete/json',params=params).json()
    for address in drop_down_addresses['predictions']:
        pprint(address['description'])
    user_chosen_address = int(input("בחר את הכתובת \n"))
    place_id=drop_down_addresses['predictions'][user_chosen_address]['place_id']
    '''from here user will choose the current adress ^'''
    '''from drop_down_adress there's place_id. once we extract it, we will use it:'''
    '''and now we refer to google to get coordinates. this are vital for main page access.'''
    coordinates_request = session.get('https://restaurant-api.wolt.com/v1/google/geocode/json?place_id={0}&language=he'.format(place_id)).json()

    lat = coordinates_request['results'][0]['geometry']['location']['lat']
    long = coordinates_request['results'][0]['geometry']['location']['lng']

    main_page=session.get('https://restaurant-api.wolt.com/v1/pages/front?lat={0}&lon={1}'.format(lat,long)).json()
    sections = main_page['sections']
    food_categories=None
    UNWANTED = ['Alcohol', 'Pharmacy', 'Grocery']
    for section in sections:
        if section['name'] == 'category-list':
            categories_section = section.get('items',[])
            food_categories = [category['link']['target'] for category in categories_section if category['title'] not in UNWANTED]
    dishes = []
    '''dishes is a list of tuples : name,description,price,img '''

    if not path.exists('dishes.json'):
        for category in food_categories:
            category_address = 'https://restaurant-api.wolt.com/v3/venues/lists/{0}?lon={1}&lat={2}'.format(category,
                                                                                                            long, lat)
            category_page = session.get(category_address).json()
            for restaurant in category_page['results']:
                restaurant_id = restaurant['active_menu']['$oid']
                address = 'https://restaurant-api.wolt.com/v3/menus/{0}'.format(restaurant_id)
                restaurant_page = session.get(address).json()
                menu = restaurant_page.get('results', [{}])[0].get('items', [])
                for item in menu:
                    name = item['name'][0]['value']
                    img = None
                    try:
                        img = item['image']
                    except:
                        pass
                    price = item['baseprice'] / 100
                    description = item['description'][0]['value']
                    dishes.append((name, description, price, img))

        with open('dishes.json', 'w', encoding='utf8') as json_file:
            json.dump(dishes, json_file, ensure_ascii=False)
    else:
        with open('dishes.json', 'r',encoding='utf8') as json_file:
            dishes = json.load(json_file)
    random_dish = random.choice(dishes)
    print(random_dish[0])
    print(random_dish[1])










