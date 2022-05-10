"""controller.py: application logic for the inventory items management app"""
""" 
Jesus Zeno: I have added another function to allow the data to be viewed in the update tab
"""

import mvc_exceptions as mvc_exc
import basic_backend
import view_g

def start_app():
    items = basic_backend.read_items()
    view_g.start_gui()

def show_items():
    items = basic_backend.read_items()
    item_type = basic_backend.item_type
    view_g.show_number_list(item_type, items)

def show_item(item_name):
    try:
        item = basic_backend.read_item(item_name)
        item_type = basic_backend.item_type
        view_g.show_item(item_type, item_name, item)
    except mvc_exc.ItemNotStored as e:
        view_g.display_missing_item_error(item_name, e)
        exit

# Adding function to show the item in the update tab
def show_item_in_update(item_name):
    try:
        item = basic_backend.read_item(item_name)
        item_type = basic_backend.item_type
        view_g.show_item_in_update(item_type, item_name, item)
    except mvc_exc.ItemNotStored as e:
        view_g.display_missing_item_error_in_update(item_name, e)
        exit

def insert_item(name, price, quantity):
    assert price > 0, 'price must be greater than 0'
    assert quantity >= 0, 'quantity must be greater than or equal to 0'
    try:
        basic_backend.create_item(name, price, quantity)
        item_type=basic_backend.item_type
        view_g.display_item_stored(name, item_type)
    except mvc_exc.ItemAlreadyStored as e:
        item_type = basic_backend.item_type
        view_g.display_item_already_stored_error(name, item_type, e)


def update_item(name, price, quantity):
    assert price > 0, 'price must be greater than 0'
    assert quantity >= 0, 'quantity must be greater than or equal to 0'
    item_type = basic_backend.item_type

    try:
        older = basic_backend.read_item(name)
        basic_backend.update_item(name, price, quantity)
        view_g.display_item_updated(
            name, older['price'], older['quantity'], price, quantity)
    except mvc_exc.ItemNotStored as e:
        view_g.display_item_not_yet_stored_error(name, item_type, e)
        # if the item is not yet stored and we performed an update, we have
        # 2 options: do nothing or call insert_item to add it.
        # self.insert_item(name, price, quantity)

def delete_item(name):
    item_type = basic_backend.item_type
    try:
        basic_backend.delete_item(name)
        view_g.display_item_deletion(name)
    except mvc_exc.ItemNotStored as e:
        view_g.display_item_not_yet_stored_error(name, item_type, e)

