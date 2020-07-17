# Importing the libraries
import requests
from bs4 import BeautifulSoup
import smtplib
from tkinter import *
import os.path


# Back End


def validityChecker(plink, pid, pclass):
    is_valid = True
    page = requests.get(plink)
    soup = BeautifulSoup(page.content, 'html.parser')
    price_id = soup.find(id=pid)
    price_class = soup.find_all(class_=pclass)
    if price_id != None:
        price = price_id
    elif price_class != "" or price_class != None:
        price = price_class

    elif price_id == None:
        is_valid = False
    elif price_class == "" or price_class == None:
        is_valid = False
    price = str(price)

    if price != None or price != "":
        # Extracting the price from the string
        price_list = price.split(">")
        price = price_list[1]
        price_list = price.split("<")
        price = price_list[0]
    else:
        price = "0"
    price = str(price)

    return is_valid, price


def register():
    # Getting the values from the entries
    product_name = entry_name.get()
    product_id = entry_id.get()
    product_header = entry_header.get()
    product_link = entry_link.get()
    # Checking if values are valid
    is_valid, item_price = validityChecker(
        product_link, product_id, product_header)
    if is_valid == False:
        print("Sorry Application Doesn't Support This Product")
    else:
        # Opening the file that contains the contents
        if os.path.isfile(product_name) == True:
            file = open(product_name, 'r')
            content = file.read()
        else:
            content = ""
        # If the file exists exit function
        if content != "":
            print("Item Already Registered")
            sync()
        else:
            file = open(product_name, 'w+')
            report = f"{str(item_price)}\n{product_name}\n{product_id}\n{product_header}\n{product_link}"
            file.write(report)
            print("Item Registered")
        file.close()


def sync():
    file_name = entry_name.get()
    # Checking if file exists
    # If file dosent exist
    if os.path.isfile(file_name) == False:
        print("Item Not Registered")
    else:
        file = open(file_name, 'r')
        content = file.read()
        # Extracting the properties
        list_of_properties = content.split("\n")
        previous_price = list_of_properties[0]
        item_id = list_of_properties[2]
        item_class = list_of_properties[3]
        link = list_of_properties[4]
        # Searching for the price
        page = requests.get(link)
        soup = BeautifulSoup(page.content, 'html.parser')
        id_price = soup.find(id=item_id)
        # If the id returns Null
        if id_price == None:
            id_price = soup.find_all(class_=item_class)\

        id_price = str(id_price)
        # Extracting the price from the string
        price_list = id_price.split(">")
        price = price_list[1]
        price_list = price.split("<")
        current_price = price_list[0]
        discount = int(float(current_price[2:])) - \
            int(float(previous_price[2:]))
        # Next Action based on discount
        if discount == 0:
            print("No Discount Recorded")
        elif discount > 0:
            print("Price Increased")
        else:
            print("There is a discount !!! Copy the link below to purchase now")
            entry_link.insert(0, link)

    pass


# Front End
root = Tk()
root.title("Amazon.com")
root.iconbitmap('download.ico')
canvas = Canvas(root, width=500, height=500)
canvas.pack()
main_label = Label(canvas, text="Amazon Price Tracker", bg='#f0d137')
main_label.place(relx=0.1, rely=0, relwidth=0.8, relheight=0.1)
entry_name_label = Label(canvas, text="Enter Product Name")
entry_name_label.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.1)
entry_name = Entry(canvas)
entry_name.place(relx=0.1, rely=0.2, relwidth=0.8, relheight=0.05)
entry_id_label = Label(canvas, text="Enter Product ID")
entry_id_label.place(relx=0.1, rely=0.3, relwidth=0.8, relheight=0.1)
entry_id = Entry(canvas)
entry_id.place(relx=0.1, rely=0.4, relwidth=0.8, relheight=0.05)
entry_header_label = Label(canvas, text="Enter Product header")
entry_header_label.place(relx=0.1, rely=0.5, relwidth=0.8, relheight=0.1)
entry_header = Entry(canvas)
entry_header.place(relx=0.1, rely=0.6, relwidth=0.8, relheight=0.05)
entry_link_label = Label(canvas, text="Enter Product Link")
entry_link_label.place(relx=0.1, rely=0.7, relwidth=0.8, relheight=0.1)
entry_link = Entry(canvas)
entry_link.place(relx=0.1, rely=0.8, relwidth=0.8, relheight=0.05)
enter_button = Button(canvas, text="Enter", command=register)
enter_button.place(relx=0.4, rely=0.9, relwidth=0.2, relheight=0.05)
sync_button = Button(canvas, text="Sync", command=sync)
sync_button.place(relx=0.9, rely=0, relwidth=0.1, relheight=0.05)
root.mainloop()
