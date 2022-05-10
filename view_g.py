"""
view.py: view module for inventory items management app
Jesus Zeno: I had modified the price input type from int to float so prices can be more exact
and realistic. Also, the GUI can show a list of all the items in inventory. I also added a feature
to allow us to search an item in the update tab so we can see what the current values are of the
item we want to update.
"""

__author__      = "Silvia Nittel"
__copyright__   = "Copyright 2022, SIE508, University of Maine"
__credits__     = ["Silvia Nittel"]

import basic_backend
import mvc_exceptions as mvc_exc
import controller
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

window = None
tab_parent = None
tab1 = None
tab2 = None
tab3 = None
tab4 = None
tab5 = None

name = None
price = None
quantity = None
search_name = None
search_name_in_update = None
delete_name = None
update_name = None
update_price = None
update_quantity = None

table = None
data = None

def start_gui():
    window = tk.Tk()
    window.title("Inventory Management")
    window.geometry("680x450")
    window.grid()

    create_menu(window)
    create_tab1(tab1)
    create_tab2(tab2)
    create_tab3(tab3)
    create_tab4(tab4)
    create_tab5(tab5)
    window.mainloop()

def create_menu(window):

    global tab_parent, tab1, tab2, tab3, tab4, tab5

    tab_parent = ttk.Notebook(window)
    tab1 = ttk.Frame(tab_parent)
    tab2 = ttk.Frame(tab_parent)
    tab3 = ttk.Frame(tab_parent)
    tab4 = ttk.Frame(tab_parent)
    tab5 = ttk.Frame(tab_parent)

    tab_parent.bind("<<NotebookTabChanged>>", on_tab_selected)

    tab_parent.add(tab1, text="Create record")
    tab_parent.add(tab2, text="Search records")
    tab_parent.add(tab3, text="Update record")
    tab_parent.add(tab4, text="Delete record")
    tab_parent.add(tab5, text="Show Full Inventory")
    tab_parent.pack(expand=1, fill='both')

def on_tab_selected(event):

    selected_tab = event.widget.select()
    tab_text = event.widget.tab(selected_tab, "text")

    if tab_text == "Show Records":
        print("tab switch")
        create_tab1(tab1)
    '''
    if tab_text == "Add New Record":
        blank_textboxes_tab_two = True

    if tab_text == "Search":
        blank_textboxes_tab_two = True
    '''

#when a new item is inserted ++++++++++++++++++++++++++++++++++++++++++++++++++++
def create_tab1(tab):
    global name, price, quantity

    name = tk.StringVar()
    price = tk.StringVar()
    quantity = tk.StringVar()

    nameLabelTabOne = tk.Label(tab, text="Name: ").grid(row=0, column=0, padx=15, pady=15)
    priceLabelTabOne = tk.Label(tab, text="Price: ").grid(row=1, column=0, padx=15, pady=15)
    quantityTabOne = tk.Label(tab, text="Quantity: ").grid(row=2, column=0, padx=15, pady=15)

    nameEntryTabOne = tk.Entry(tab, textvariable=name).grid(row=0, column=1, padx=15, pady=15)
    priceEntryTabOne = tk.Entry(tab, textvariable=price).grid(row=1, column=1, padx=15, pady=15)
    quantityEntryTabOne = tk.Entry(tab, textvariable=quantity).grid(row=2, column=1, padx=15,
                                                                                    pady=15)
    buttonInsert = tk.Button(tab, text="Create new item", command=insert_item)
    buttonInsert.grid(row=4, column=1, padx=15, pady=15)

def insert_item():
    controller.insert_item(name.get(), float(price.get()), int(quantity.get()))

#when a new item is inserted
def display_item_stored(item, item_type):
    messagebox.showinfo("Inventory Management", 'We have just added some {} to our {} list!'
          .format(item.upper(), item_type))

#error when we already have this item stored
def display_item_already_stored_error(item, item_type, err):
    messagebox.showinfo("Inventory Management", 'Hey! We already have {} in our {} list!'
          .format(item.upper(), item_type))

#when searching for an item++++++++++++++++++++++++++++++++++++++++++++++++++++
def create_tab2(tab):
    global search_name

    search_name = tk.StringVar()
    nameLabelTabTwo = tk.Label(tab, text="Item Name: ").grid(row=0, column=0, padx=15, pady=15)
    nameEntryTabTwo = tk.Entry(tab, textvariable=search_name).grid(row=0, column=1, padx=15, pady=15)

    buttonSearch = tk.Button(tab, text="Search item", command=search_item)
    buttonSearch.grid(row=4, column=1, padx=15, pady=15)

def search_item():
    global table
    # destroy old frame with table
    if table:
        table.destroy()

    controller.show_item(search_name.get())

def show_item(item_type, item_name, item):
    global data
    data = []
    data.append(item)
    item_type = item_type
    _showdata(tab2)

#when the searched item does not exist
def display_missing_item_error(item, err):
    messagebox.showinfo("Inventory Management", 'We are sorry, we have no {}!'.format(item.upper()))

# helper function for show_item()
def _showdata(tab):
    global table
    global data
    # destroy old frame with table
    if table:
        table.destroy()

    table = ttk.Treeview(tab, columns=(1, 2, 3), height=10, show="headings")

    table.heading(1, text="Name")
    table.heading(2, text="Price")
    table.heading(3, text="Quantity")

    table.column(1, width=100)
    table.column(2, width=50)
    table.column(3, width=60)

    table.grid(row=1, column=1, columnspan=3, padx=15, pady=15)
    # fill frame with table
    num_elem = len(data)
    for r in range(num_elem):
        table.insert('', 'end', values=(data[r]['name'], str(data[r]['price']), str(data[r]['quantity']) ))


#when update an item++++++++++++++++++++++++++++++++++++++++++++++++++++
def create_tab3(tab):
    global update_name, update_price, update_quantity, search_name_in_update

    update_name = tk.StringVar()
    update_price = tk.StringVar()
    update_quantity = tk.StringVar()
    search_name_in_update = tk.StringVar()

    nameLabelTabThree = tk.Label(tab, text="Item Name: ").grid(row=0, column=0, padx=15, pady=15)
    nameEntryTabThree = tk.Entry(tab, textvariable=update_name).grid(row=0, column=1, padx=15, pady=15)

    priceLabelTabThree = tk.Label(tab, text="New Price: ").grid(row=1, column=0, padx=15, pady=15)
    priceEntryTabThree = tk.Entry(tab, textvariable=update_price).grid(row=1, column=1, padx=15, pady=15)

    quantityTabThree = tk.Label(tab, text="New Quantity: ").grid(row=2, column=0, padx=15, pady=15)
    quantityEntryTabThree = tk.Entry(tab, textvariable=update_quantity).grid(row=2, column=1, padx=15,pady=15)

    # Adding search function field and entry to the update tab
    searchLabelTabThree = tk.Label(tab, text="Search Item Name: ").grid(row=0, column=2, padx=15, pady=15)
    searchEntryTabThree = tk.Entry(tab, textvariable=search_name_in_update).grid(row=0, column=2, padx=15, pady=15)

    buttonUpdate = tk.Button(tab, text="Update item", command=update_item)
    buttonUpdate.grid(row=4, column=1, padx=15, pady=15)

    # Add button and function to search items
    buttonSearch = tk.Button(tab, text="Search item", command=search_item_in_update)
    buttonSearch.grid(row=4, column=2, padx=15, pady=15)


# These functions will help us display the values of the item we will update.
def search_item_in_update():
    global table
    # destroy old frame with table
    if table:
        table.destroy()

    controller.show_item_in_update(search_name_in_update.get())


def show_item_in_update(item_type, item_name, item):
    global data
    data = []
    data.append(item)
    item_type = item_type
    _showdata_in_update(tab3)


#when the searched item does not exist
def display_missing_item_error_in_update(item, err):
    messagebox.showinfo("Inventory Management", 'We are sorry, we have no {}!'.format(item.upper()))


# helper function for show_item()
def _showdata_in_update(tab):
    global table
    global data
    # destroy old frame with table
    if table:
        table.destroy()

    table = ttk.Treeview(tab, columns=(1, 2, 3), height=10, show="headings")

    table.heading(1, text="Name")
    table.heading(2, text="Price")
    table.heading(3, text="Quantity")

    table.column(1, width=100)
    table.column(2, width=50)
    table.column(3, width=60)

    table.grid(row=1, column=2, columnspan=3, padx=15, pady=15)
    # fill frame with table
    num_elem = len(data)
    for r in range(num_elem):
        table.insert('', 'end', values=(data[r]['name'], str(data[r]['price']), str(data[r]['quantity']) ))


def update_item():
    controller.update_item(update_name.get(), float(update_price.get()), int(update_quantity.get()))


def display_item_updated(item, o_price, o_quantity, n_price, n_quantity):
    messagebox.showinfo("Inventory Management", 'Change {} price: {} --> {}'
          .format(item, o_price, n_price))
    messagebox.showinfo("Inventory Management", 'Change {} quantity: {} --> {}'
          .format(item, o_quantity, n_quantity))


# when item we want to delete or update does not exist
def display_item_not_yet_stored_error(item, item_type, err):
    messagebox.showinfo("Inventory Management", 'We don\'t have any {} in our {} list. Please insert it first!'
          .format(item.upper(), item_type))


# when we delete an item ++++++++++++++++++++++++++++++++++++++++++++++++++++
def create_tab4(tab):
    global delete_name

    delete_name = tk.StringVar()
    nameLabelTabFour = tk.Label(tab, text="Item Name: ").grid(row=0, column=0, padx=15, pady=15)
    nameEntryTabFour = tk.Entry(tab, textvariable=delete_name).grid(row=0, column=1, padx=15, pady=15)

    buttonDelete = tk.Button(tab, text="Delete item", command=delete_item)
    buttonDelete.grid(row=4, column=1, padx=15, pady=15)


def delete_item():
    controller.delete_item(delete_name.get())


def display_item_deletion(name):
    messagebox.showinfo("Inventory Management", 'We have just removed {} from our list'.format(name))


def create_tab5(tab):
    global table
    # destroy old frame with table
    if table:
        table.destroy()

    controller.show_items()


# helper function for show_item()
def _show_all_data(tab):
    global table
    global data

    # destroy old frame with table
    if table:
        table.destroy()

    table = ttk.Treeview(tab, columns=(1, 2, 3), height=10, show="headings")

    table.heading(1, text="Name")
    table.heading(2, text="Price")
    table.heading(3, text="Quantity")

    table.column(1, width=100)
    table.column(2, width=50)
    table.column(3, width=60)

    table.grid(row=1, column=1, columnspan=3, padx=15, pady=15)

    # Fill frame with table
    table['columns'] = data.columns.values.tolist()

    for i in data.columns.values.tolist():
        table.column(i, width=60)
        table.heading(i, text=i)
    for index, row in data.iterrows():
        table.insert("", 'end', text=index, values=list(row))

    # Make a button to refresh the whole inventory
    button_Refresh = tk.Button(tab, text="Refresh items", command=controller.show_items)
    button_Refresh.grid(row=4, column=1, padx=15, pady=15)


# a function to show the entire inventory, but we don't have a tab yet
def show_number_list(item_type, items):
    global data
    data = items
    item_type = item_type
    _show_all_data(tab5)
