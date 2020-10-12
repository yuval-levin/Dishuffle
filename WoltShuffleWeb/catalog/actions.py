import hashlib
import requests
import random
from django.core.cache import caches
from . import wolt_scraping
from . import constants

import time
cache = caches['default']
CACHING_PERIOD_SEC = 7 * 24 * 60 * 60  # CR ENV VARIABLE


def return_random_dish(lat, long, unwanted_dishes_set, username):
    user_changed_address = update_user_address(username, lat)
    # if food_categories is None, we return None. unfortunately user has no Wolt available in address
    unwanted_dishes_set = unwanted_dishes_set or []
    t0 = time.time()
    with requests.session() as session:
        main_page = wolt_scraping.get_wolt_main_page(session, username, lat, long, user_changed_address)
        if main_page == constants.BROKEN_API:
            return constants.BROKEN_API

        food_categories = filter_food_categories(main_page['sections'])

        # if food_categories is None, we return None. unfortunately user has no Wolt available in address
        if food_categories is None: return None

        restaurant = None
        iterations_count = 0
        while restaurant == constants.CLOSED_VENUES or restaurant is None:
            # sometimes chosen category is fully closed - e.g. in early morning, hamburgers are closed
            # so we choose category again

            food_category = random.choice(food_categories)

            category_address = wolt_scraping.create_food_category_address(food_category, long, lat)

            restaurant, dish = choose_random_dish(unwanted_dishes_set, session, username, category_address,
                                                  food_category)
            if iterations_count > constants.LAX_ITERATION_LIMIT: return None  # avoiding infinite loop of ALL closed venues in ALL categories
            if restaurant == constants.BROKEN_API:
                return None
        t1 = time.time()
        print(t1-t0)
        return wolt_scraping.dish_details(dish, restaurant)


def update_user_address(username, lat):
    cache_key = f"lat{username}"
    cached_lat = cache.get(cache_key)  # in case user changes address
    user_changed_address = False
    if cached_lat is not None and cached_lat != lat:
        user_changed_address = True
    cache.set(cache_key, lat, CACHING_PERIOD_SEC)

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
    iterations_count = 0
    while dish is None:
        print(food_category)
        restaurant = wolt_scraping.get_restaurant(session, username, category_address, food_category, False)
        if restaurant == constants.CLOSED_VENUES:  # meaning all restaurants were closed in this category
            return constants.CLOSED_VENUES, None
        if restaurant == constants.BROKEN_API:
            return constants.BROKEN_API

        restaurant_name = wolt_scraping.get_restaurant_name(restaurant)
        restaurant_id = wolt_scraping.get_restaurant_id(restaurant)
        menu = wolt_scraping.get_restaurant_menu(session, restaurant_id)
        dish = choose_random_dish_from_restaurant(restaurant_name, menu, set_of_unwanted_dishes)
        iterations_count += 1
        if iterations_count > constants.TIGHT_ITERATION_LIMIT: return None, None  # in case category has no open restaurants or perhaps all dishes
        # in it are 'NEVER AGAIN'

    return restaurant, dish


def choose_random_dish_from_restaurant(restaurant_name, menu, set_of_unwanted_dishes):
    iterations_count = 0
    dish = random.choice(menu)
    # Loop is used instead of pre-filtered list to avoid going through all dishes (too long of list)
    while (dish['baseprice'] / 100) < 30 or \
            hash_dish_name(restaurant_name, dish['name'][0]['value']) in set_of_unwanted_dishes:
        dish = random.choice(menu)
        if iterations_count > constants.LAX_ITERATION_LIMIT: return None  # to avoid infinite loops in restaurants
        # e.g. if user marked all restaurant dishes as unwanted
        # or if restaurant only has items cheaper then 30

    return dish
