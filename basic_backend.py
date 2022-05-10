"""
Jesus Zeno
This program will be a simple CRUD data management program that will be able to have persistent
data by saving a file record. It will initialize a pre-determined list of items if there is no
csv on file to pull items from. If there is a csv on file, it will use that as the starting point.

I have modified this from the first homework assignment to fit with the tkinter app code that was
Provided in class. It will perform all the previous tasks using the GUI that was setup.
"""

import pandas as pd
import mvc_exceptions as mvc_exc

"""Global variables"""
item_type = "product"
items = list()
"""INITIALIZE ITEMS"""
# Make initial list of dictionaries for system. Initial list will be used if there is none on file yet.
my_items = [
    {'name': 'bread', 'price': 2.5, 'quantity': 20},
    {'name': 'milk', 'price': 4.0, 'quantity': 10},
    {'name': 'eggs', 'price': 4.0, 'quantity': 5},
]

"""Backend functions"""
def create_item(name, price, quantity):
    # get items from csv in later function
    updated_csv = read_csv_to_list()
    # search first if that item already exists
    results = list(filter(lambda x: x['name'] == name, updated_csv))
    # if we find an existing item with the name, we raise an exception
    if results:
        raise mvc_exc.ItemAlreadyStored('"{}" already stored!'.format(name))
    # if not, we append the item to the dictionary
    else:
        items.append({'name': name, 'price': price, 'quantity': quantity})
        pandas_to_csv(items, "Updated Items")


# bulk create times
def create_items(app_items):
    global items
    items = app_items


# read a particular item
def read_item(name):
    updated_csv = read_csv_to_list()
    # find items that match the name of item given
    myitems = list(filter(lambda x: x['name'] == name, updated_csv))
    # if it exists, then return it or raise exception
    if myitems:
        return myitems[0]
    else:
        raise mvc_exc.ItemNotStored(
            'Can\'t read "{}" because it\'s not stored'.format(name))


# read all items
def read_items():
    # Attempt to open the file if it already exists. If it doesn't it will use the initialized list
    # in the code above. This way if we close this program and reopen it, we can pick up where we
    # left off instead of losing previous progress.
    try:
        with open('Updated Items.csv') as f:
            updated_csv = read_csv_to_list()
            reading_all_df = pd.DataFrame(updated_csv)
            print("file already exists")
            # Let's look at what we have in the df to easily see what we are working with.
            print(read_csv_to_list())
            # Initialize list of items from csv on file.
            create_items(read_csv_to_list())
    except IOError:
        print("File not accessible")
        # Save input of the initialized list
        pandas_to_csv(my_items, "Updated Items")
        # Create the items from initialized list
        reading_all_df = pd.DataFrame(create_items(my_items))

    # global item
    return reading_all_df


def update_item(name, price, quantity):
    global items
    # updated_csv = read_csv_to_list()
    # Python 3.x removed tuple parameters unpacking (PEP 3113), so we have to do it manually
    # (i_x is a tuple, idxs_items is a list of tuples)
    # I tried doing this and the delete function similarly to the others with the updated_csv = read_csv_to_list()
    # line and have the updated_csv variable replace items within the function. It was not actually
    # updating or deleting. They still work as intended though so I left these as is.
    idxs_items = list(filter(lambda i_x: i_x[1]['name'] == name, enumerate(items)))
    if idxs_items:
        i, item_to_update = idxs_items[0][0], idxs_items[0][1]
        items[i] = {'name': name, 'price': price, 'quantity': quantity}
        pandas_to_csv(items, "Updated Items")
    else:
        raise mvc_exc.ItemNotStored(
            'Can\'t update "{}" because it\'s not stored'.format(name))


def delete_item(name):
    global items
    # Python 3.x removed tuple parameters unpacking (PEP 3113), so we have to do it manually
    # (i_x is a tuple, idxs_items is a list of tuples)
    idxs_items = list(filter(lambda i_x: i_x[1]['name'] == name, enumerate(items)))
    if idxs_items:
        i, item_to_delete = idxs_items[0][0], idxs_items[0][1]
        # print("idxs_items[0][0], idxs_items[0][1]: ", idxs_items[0][0], " item in list, value:",
        # idxs_items[0][1])
        del items[i]
        pandas_to_csv(items, "Updated Items")
    else:
        raise mvc_exc.ItemNotStored(
            'Can\'t delete "{}" because it\'s not stored'.format(name))

def pandas_to_csv(dataframe_items, filename):
    # Make pandas dataframe and print it so we can see it in a more friendly way
    dataframe = pd.DataFrame(dataframe_items)
    print("This is the df: \n", dataframe)
    # Put pandas df into a csv
    dataframe.to_csv('{}.csv'.format(filename), index=None)


def read_csv_to_list():
    # Read the csv to a pandas dataframe
    items_from_csv_pd = pd.read_csv("Updated Items.csv")
    # Transform df to list of dictionaries.
    items_from_csv = items_from_csv_pd.to_dict('records')
    return items_from_csv


def main():
    # Attempt to open the file if it already exists. If it doesn't it will use the initialized list
    # in the code above. This way if we close this program and reopen it, we can pick up where we
    # left off instead of losing previous progress.
    try:
        with open('Updated Items.csv') as f:
            print("hey, file already exists")
            # Let's look at what we have in the df to easily see what we are working with.
            print(read_csv_to_list())
            # Initialize list of items from csv on file.
            create_items(read_csv_to_list())
    except IOError:
        print("File not accessible")
        # Save input of the initialized list
        pandas_to_csv(my_items, "Updated Items")
        # Create the items from initialized list
        create_items(my_items)

    """CREATE ANY ITEM"""
    # if we try to re-create an object we get an ItemAlreadyStored exception
    try:
        # Prompt user to see if they want to create item. If yes, get info for item.
        user_create = str(input("Do you want to create an item? Type yes or no: "))
        # Make while loop so user can continue to add items if needed
        while user_create == 'yes':
            user_item_create = str(input("What item do you want to store? "))
            user_price_create = float(input("How much is the item? "))
            # Let's make sure the user gives you a positive amount
            while user_price_create <= 0:
                print("The price needs to be positive. Please try again.")
                user_price_create = float(input("How much is the item? "))
            user_quantity_create = int(input("How many of the item are you storing? "))
            # Let's make sure the user gives you a positive amount
            while user_quantity_create <= 0:
                print("The amount needs to be positive. Please try again.")
                user_quantity_create = int(input("How many of the item are you storing? "))
            create_item(user_item_create, user_price_create, user_quantity_create)
            # Check if user still needs to add item
            user_create = str(input("Do you want to create an item? Type yes or no: "))
            # Save the new list to csv
            pandas_to_csv(items, "Updated Items")
    except Exception as e:
        print(e)
        exit()

    """READ ALL ITEMS"""
    print('READ ALL items')
    print(read_items())

    """READ A SPECIFIC ITEM"""
    # if we try to read an object not stored we get an ItemNotStored exception
    user_read = str(input("Do you want to read an item? Type yes or no: "))
    # Make while loop to see if user needs to read item
    while user_read == 'yes':
        user_item_read = str(input("What item do you want to read? "))
        print(read_item(user_item_read))
        # Check if user needs to read anything else
        user_read = str(input("Do you want to read another item? Type yes or no: "))

    """UPDATE ANY ITEM"""
    user_update = str(input("Do you want to update an item? Type yes or no: "))
    # Make while loop to check if user needs tup update item
    while user_update == 'yes':
        user_item_update = str(input("What item do you want to update? "))
        user_price_update = float(input("How much is the item? "))
        # Let's make sure the user gives you a positive price
        while user_price_update <= 0:
            print("The price needs to be positive. Please try again.")
            user_price_update = float(input("How much is the item? "))
        user_quantity_update = int(input("How many of the item are stored? "))
        # Let's make sure the user gives you a positive amount
        while user_quantity_update <= 0:
            print("The amount needs to be positive. Please try again.")
            user_quantity_update = int(input("How many of the item are stored? "))
        update_item(user_item_update, user_price_update, user_quantity_update)
        # Save new list to csv
        pandas_to_csv(items, "Updated Items")
        # Show info for what was updated
        print("Updated Item Info:\n", read_item(user_item_update))
        # Check if user still needs to update item
        user_update = str(input("Do you want to update an item? Type yes or no: "))
    # if we try to update an object not stored we get an ItemNotStored exception

    """DELETE ANY ITEM"""
    user_delete = str(input("Do you want to delete an item? Type yes or no: "))
    # Make while loop to see if user needs to delete item
    while user_delete == 'yes':
        user_item_delete = str(input("What item do you want to delete? "))
        delete_item(user_item_delete)
        # Save new list to csv
        pandas_to_csv(items, "Updated Items")
        # Check if user needs to delete anything else
        user_delete = str(input("Do you want to delete an item? Type yes or no: "))
    # if we try to delete an object not stored we get an ItemNotStored exception

    print('READ ALL items')
    print(read_items())
    # Final save of all work
    pandas_to_csv(items, "Updated Items")

if __name__ == '__main__':
    main()
