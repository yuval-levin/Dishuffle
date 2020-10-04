import requests
import hashlib
import random
import time
from django.core.cache import caches

cache = caches['default']
CACHING_PERIOD = 604800


def return_random_dish(lat, long, set_of_unwanted_dishes, username):
    user_changed_address = user_address_update(username, lat)
    if set_of_unwanted_dishes is None: set_of_unwanted_dishes = []

    with requests.session() as session:
        main_page = get_main_page(session, username, lat, long, user_changed_address)
        food_categories = filter_food_categories(main_page['sections'])

        # if food_categories is None, we return None. unfortunately user has no Wolt available in address
        if food_categories is None: return None
        food_category = random.choice(food_categories)
        category_address = 'https://restaurant-api.wolt.com/v3/venues/lists/{0}?lon={1}&lat={2}'.format(
            food_category,
            long, lat)

        restaurant = get_restaurant(session, username, category_address, food_category, user_changed_address)

        dish = choose_random_dish(set_of_unwanted_dishes, session, username, category_address,
                                  food_category)
        return dish_details(dish, restaurant)


def user_address_update(username, lat):
    cached_lat = cache.get('lat' + username)  # in case user changes address
    user_changed_address = False
    if cached_lat is not None and cached_lat != lat:
        user_changed_address = True
    cache.set('lat' + username, lat, CACHING_PERIOD)

    return user_changed_address


def hashed_dish(restaurant, dish_name):
    combined = dish_name + restaurant
    return hashlib.md5(combined.encode('utf-8')).hexdigest()
    return combined


# returns restaurant from category_address
def get_restaurant(session, username, category_address, food_category, user_changed_address):
    restaurants_cache = username + food_category
    restaurants = cache.get(restaurants_cache)
    if restaurants is None or user_changed_address:
        restaurants = session.get(category_address).json()['results']
        cache.set(restaurants_cache, restaurants, CACHING_PERIOD)  # stores the main page for this user for a week

    restaurant = random.choice(restaurants)

    return restaurant


def get_main_page(session, username, lat, long, user_changed_address):
    main_page = cache.get(username)
    if main_page is None or user_changed_address:
        main_page = session.get(
            'https://restaurant-api.wolt.com/v1/pages/front?lat={0}&lon={1}'.format(lat, long)).json()
        cache.set(username, main_page, CACHING_PERIOD)  # stores the main page for this user for a week
    return main_page


def filter_food_categories(sections):
    food_categories = None
    UNWANTED = ['Alcohol', 'Pharmacy', 'Grocery']

    for section in sections:
        if section['name'] == 'category-list':
            categories_section = section.get('items', [])
            food_categories = [category['link']['target'] for category in categories_section if
                               category['title'] not in UNWANTED]
    return food_categories


def get_restaurant_menu(session, restaurant_id):
    address = 'https://restaurant-api.wolt.com/v3/menus/{0}'.format(restaurant_id)
    restaurant_page = session.get(address).json()
    menu = restaurant_page.get('results', [{}])[0].get('items', [])
    return menu


def dish_details(dish, restaurant):
    name = dish['name'][0]['value']
    restaurant_name = restaurant['name'][1]['value']
    price = dish['baseprice'] / 100
    description = dish['description'][0]['value']
    restaurant_url = restaurant['public_url']
    img = None
    try:
        img = dish['image']
    except:
        pass
    return (name, restaurant_name, description, price, img, restaurant_url)


def choose_random_dish(set_of_unwanted_dishes, session, username, category_address,
                       food_category):
    dish = None
    while dish is None:
        restaurant = get_restaurant(session, username, category_address, food_category, False)
        restaurant_name = restaurant['name'][1]['value'] if len(restaurant['name']) > 1 else restaurant['name'][0][
            'value']
        restaurant_id = restaurant['active_menu']['$oid']
        menu = get_restaurant_menu(session, restaurant_id)

        dish = choose_loop_from_restaurant(restaurant_name, menu, set_of_unwanted_dishes)

    return dish


def choose_loop_from_restaurant(restaurant_name, menu, set_of_unwanted_dishes):
    t0 = time.time()
    dish = random.choice(menu)

    while (dish['baseprice'] / 100) < 30 or hashed_dish(restaurant_name,
                                                        dish['name'][0]['value']) in set_of_unwanted_dishes:
        dish = random.choice(menu)
        t1 = time.time()
        if t1 - t0 > 3: return None  # to avoid infinite loops in restaurants
        # e.g. if user marked all restaurant dishes as unwanted
        # or if restaurant only has items cheaper then 30
    return dish
