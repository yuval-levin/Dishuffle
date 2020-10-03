import requests
import hashlib
import random


def hashed_dish(restaurant, dish_name):
    combined = dish_name + restaurant
    # return hashlib.md5(combined.encode('utf-8')).hexdigest()
    return combined


def return_random_dish(lat, long, set_of_unwanted_dishes):
    with requests.session() as session:
        main_page = session.get(
            'https://restaurant-api.wolt.com/v1/pages/front?lat={0}&lon={1}'.format(lat, long)).json()
        sections = main_page['sections']
        food_categories = None
        UNWANTED = ['Alcohol', 'Pharmacy', 'Grocery']

        for section in sections:
            if section['name'] == 'category-list':
                categories_section = section.get('items', [])
                food_categories = [category['link']['target'] for category in categories_section if
                                   category['title'] not in UNWANTED]
        '''dishes is a list of tuples : name,description,price,img '''
        # if food_categories is None, we return None. unfortunately user has no wolt available in address
        if food_categories is None: return None

        category_address = 'https://restaurant-api.wolt.com/v3/venues/lists/{0}?lon={1}&lat={2}'.format(
            random.choice(food_categories),
            long, lat)

        restaurants = session.get(category_address).json()['results']
        restaurant = random.choice(restaurants)

        restaurant_id = restaurant['active_menu']['$oid']
        address = 'https://restaurant-api.wolt.com/v3/menus/{0}'.format(restaurant_id)
        restaurant_page = session.get(address).json()
        restaurant_name = restaurant['name'][1]['value']

        menu = restaurant_page.get('results', [{}])[0].get('items', [])
        dish = random.choice(menu)

        if set_of_unwanted_dishes is None: set_of_unwanted_dishes = []
        # while loop to avoid "chopsticks" or drinks or unwanted dishes
        while (dish['baseprice'] / 100) < 30 or hashed_dish(restaurant_name,
                                                            dish['name'][0]['value']) in set_of_unwanted_dishes:
           dish = random.choice(menu)
        price = dish['baseprice'] / 100
        name = dish['name'][0]['value']
        img = None
        try:
            img = dish['image']
        except:
            pass

        description = dish['description'][0]['value']

        restaurant_url = restaurant['public_url']
        return (name, restaurant_name, description, price, img, restaurant_url)

