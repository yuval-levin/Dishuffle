import random
from django.core.cache import caches
from . import actions
from . import constants

cache = caches['default']


class Dish:
    def __init__(self, name, price, restaurant, restaurant_url, description, img):
        self.name = name
        self.restaurant = restaurant
        self.restaurant_url = restaurant_url
        self.description = description
        self.price = price
        self.img = img


# Wolt's main page required longitude and latitude of user.
# the webpage created presents categories and restaurants available to those coordinates.
def get_wolt_main_page(session, username, lat, long, user_changed_address):
    main_page = None
    if not user_changed_address: main_page = cache.get(username)
    if main_page is None or user_changed_address:
        try:
            main_page = session.get(f"https://restaurant-api.wolt.com/v1/pages/front?lat={lat}&lon={long}").json()
            cache.set(username, main_page, actions.CACHING_PERIOD_SEC)  # stores the main page for this user for a week
        except:
            return constants.BROKEN_API

    return main_page


def create_food_category_address(food_category, long, lat):
    return f'https://restaurant-api.wolt.com/v3/venues/lists/{food_category}?lon={long}&lat={lat}'


# returns restaurant from category_address
def get_restaurant(session, username, category_address, food_category, user_changed_address):
    restaurants_cache = f"{username}{food_category}"
    restaurants = cache.get(restaurants_cache)

    if restaurants is None or user_changed_address:
        try:
            restaurants = session.get(category_address).json()['results']
        except:
            return constants.BROKEN_API
        cache.set(restaurants_cache, restaurants, actions.CACHING_PERIOD_SEC)  # stores the food category for this user
        # for a week
    restaurant = random.choice(restaurants)
    # prevent closed venues
    iterations_count = 0
    while not restaurant['online']:
        restaurant = random.choice(restaurants)
        iterations_count += 1
        if iterations_count > constants.LAX_ITERATION_LIMIT: return constants.CLOSED_VENUES  # avoiding infinite loop of closed venues in category

    return restaurant


def get_restaurant_menu(session, restaurant_id):
    address = 'https://restaurant-api.wolt.com/v3/menus/{0}'.format(restaurant_id)
    restaurant_page = session.get(address).json()
    menu = restaurant_page.get('results', [{}])[0].get('items', [])
    return menu


def get_restaurant_name(restaurant):
    return restaurant['name'][1]['value'] if len(restaurant['name']) > 1 else restaurant['name'][0][
        'value']


def get_restaurant_id(restaurant):
    return restaurant['active_menu']['$oid']


def dish_details(dish, restaurant):
    name = dish['name'][0]['value']
    restaurant_name = restaurant['name'][1]['value'] if len(restaurant['name']) > 1 else restaurant['name'][0][
        'value']
    price = dish['baseprice'] / 100
    description = dish['description'][0]['value']
    restaurant_url = restaurant['public_url']
    img = dish['image'] if 'image' in dish else None

    return Dish(name, price, restaurant_name, restaurant_url, description, img)
