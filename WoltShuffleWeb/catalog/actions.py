import hashlib
import random
import time
from django.core.cache import caches
from . import wolt_scraping
import environ

cache = caches['default']
CACHING_PERIOD_SEC = 7 * 24 * 60 * 60  # CR ENV VARIABLE

env = environ.Env()
environ.Env.read_env()


def return_random_dish(lat, long, unwanted_dishes_set, username):
    user_changed_address = update_user_address(username, lat)
    # if food_categories is None, we return None. unfortunately user has no Wolt available in address
    unwanted_dishes_set = unwanted_dishes_set or []

    session = wolt_scraping.create_wolt_session()
    main_page = wolt_scraping.get_wolt_main_page(session, username, lat, long, user_changed_address)
    if main_page is env("BROKEN_API"):
        return env("BROKEN_API")

    food_categories = filter_food_categories(main_page['sections'])

    # if food_categories is None, we return None. unfortunately user has no Wolt available in address
    if food_categories is None: return None
    food_category = random.choice(food_categories)
    category_address = 'https://restaurant-api.wolt.com/v3/venues/lists/{0}?lon={1}&lat={2}'.format(
        food_category,
        long, lat)
    restaurant, dish = choose_random_dish(unwanted_dishes_set, session, username, category_address,
                                          food_category)
    if restaurant is env("CLOSED_VENUES"):  # meaning all venues were closed
        return env("CLOSED_VENUES")
    return wolt_scraping.dish_details(dish, restaurant)


def update_user_address(username, lat):
    cached_lat = cache.get('lat' + username)  # in case user changes address
    user_changed_address = False
    if cached_lat is not None and cached_lat != lat:
        user_changed_address = True
    cache.set('lat' + username, lat, CACHING_PERIOD_SEC)

    return user_changed_address


def hash_dish_name(restaurant, dish_name):
    combined = dish_name + restaurant
    return hashlib.md5(combined.encode('utf-8')).hexdigest()
    return combined


def filter_food_categories(sections):
    food_categories = None
    UNWANTED = ['Alcohol', 'Pharmacy', 'Grocery']

    for section in sections:
        if section['name'] == 'category-list':
            categories_section = section.get('items', [])
            food_categories = [category['link']['target'] for category in categories_section if
                               category['title'] not in UNWANTED]
    return food_categories


def choose_random_dish(set_of_unwanted_dishes, session, username, category_address,
                       food_category):
    dish = None
    restaurant = None
    while dish is None:
        restaurant = wolt_scraping.get_restaurant(session, username, category_address, food_category, False)
        if restaurant is env("CLOSED_VENUES"):  # meaning all restaurants were closed
            return None, None
        if restaurant is env("BROKEN_API"):
            return env("BROKEN_API")

        restaurant_name = restaurant['name'][1]['value'] if len(restaurant['name']) > 1 else restaurant['name'][0][
            'value']
        restaurant_id = restaurant['active_menu']['$oid']
        menu = wolt_scraping.get_restaurant_menu(session, restaurant_id)
        dish = choose_loop_from_restaurant(restaurant_name, menu, set_of_unwanted_dishes)

    return restaurant, dish


def choose_loop_from_restaurant(restaurant_name, menu, set_of_unwanted_dishes):
    t0 = time.time()
    dish = random.choice(menu)

    while (dish['baseprice'] / 100) < 30 or \
            hash_dish_name(restaurant_name, dish['name'][0]['value']) in set_of_unwanted_dishes:
        dish = random.choice(menu)
        t1 = time.time()
        if t1 - t0 > 3: return None  # to avoid infinite loops in restaurants
        # e.g. if user marked all restaurant dishes as unwanted
        # or if restaurant only has items cheaper then 30
    return dish
