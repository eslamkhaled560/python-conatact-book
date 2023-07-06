import csv
import PySimpleGUI as sg
from datetime import datetime
import re

# Create file with today's datetime
file_name = f"contactbook_{datetime.today().strftime('%d%m%Y')}.csv"

# Validate email input (email@example.com)
def validate_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if re.match(pattern, email):
        return True
    else:
        return False


def validate_phone(phone_num):
    '''
    Return True if a phone numbr input matches a specific pattern
    - Only digits included
    - May start with plus (+) sign, and have one or more hyphen (-) signs in between
    - May contain commas (,) to separete two or more numbers 
    '''
    pattern = r'^\+?\d+(?:-?\d+)*(?:,\+?\d+(?:-?\d+)*)?$'
    if re.match(pattern, phone_num):
        return True
    else:
        return False


def save_contact(username, email, phone_numbers, address):
    # Open file and write information
    with open(file_name, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([username, email, ','.join(phone_numbers), address, datetime.now()])


def update_contact(username, new_email, new_phone_numbers, new_address):
    # Get contacts
    with open(file_name, 'r') as csvfile:
        contacts = list(csv.reader(csvfile))

    # Loop and find the specified contact using username then update it
    updated_contacts = []
    for contact in contacts:
        if contact[0] == username:
            contact[1] = new_email
            contact[2] = ','.join(new_phone_numbers)
            contact[3] = new_address
            contact[4] = datetime.now()
        updated_contacts.append(contact)

    # Open file and save updated changes
    with open(file_name, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(updated_contacts)


def delete_contact(username):
    # Get contacts
    with open(file_name, 'r') as csvfile:
        contacts = list(csv.reader(csvfile))

    # Return a list of all contact except the deleted one based on username
    updated_contacts = [contact for contact in contacts if contact[0] != username]

    # Open file and save changes
    with open(file_name, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(updated_contacts)


def list_contacts(order_by=None):
    # Get contacts
    with open(file_name, 'r') as csvfile:
        contacts = list(csv.reader(csvfile))

    # Sort contacts by name or date
    if order_by == 'name':
        sorted_contacts = sorted(contacts, key=lambda x: x[0])
    elif order_by == 'date':
        sorted_contacts = sorted(contacts, key=lambda x: x[4])
    else:
        sorted_contacts = contacts

    # Print contacts information
    for contact in sorted_contacts:
        print(f"Username: {contact[0]}")
        print(f"Email: {contact[1]}")
        print(f"Phone Numbers: {contact[2].split(',')}")
        print(f"Address: {contact[3]}")
        print(f"Insertion Date: {contact[4]}")
        print()


def search_contact_by_firstname(first_name):
    # Get contacts
    with open(file_name, 'r') as csvfile:
        contacts = list(csv.reader(csvfile))

    found_contacts = []
    for contact in contacts:
        # Find the contacts that starts with the provided first name
        if contact[0].lower().startswith(first_name.lower()):
            found_contacts.append(contact)

    # List contacts found
    if found_contacts:
        for contact in found_contacts:
            print(f"Username: {contact[0]}")
            print(f"Email: {contact[1]}")
            print(f"Phone Numbers: {contact[2].split(',')}")
            print(f"Address: {contact[3]}")
            print(f"Insertion Date: {contact[4]}")
            print()
    else:
        print("No contacts found with the provided first name.")


# Define the GUI layout
layout = [
    [sg.Text('Username:'), sg.Input(key='-USERNAME-')],
    [sg.Text('Email:'), sg.Input(key='-EMAIL-')],
    [sg.Text('Phone Numbers (comma-separated):'), sg.Input(key='-PHONE-')],
    [sg.Text('Address:'), sg.Input(key='-ADDRESS-')],
    [sg.Button('Save'), sg.Button('Update'), sg.Button('Delete'), sg.Button('List Contacts')],
    [sg.Text('Search by First Name:'), sg.Input(key='-SEARCH-'), sg.Button('Search')],
]

# Create the window
window = sg.Window('Contact Book', layout)

# Event loop to process UI events
while True:
    event, values = window.read()

    # End program after closing the window
    if event == sg.WINDOW_CLOSED:
        break

    # Get contact details from user input and perform a save action
    if event == 'Save':
        username = values['-USERNAME-']
        email = values['-EMAIL-']
        phone_numbers = values['-PHONE-'].split(',')
        address = values['-ADDRESS-']
        # Validate input email and phone number
        if validate_email(email):
            if validate_phone(values['-PHONE-']):
                save_contact(username, email, phone_numbers, address)
                sg.popup('Contact saved successfully.')
            else:
                sg.popup('Please enter a valid phone number(s)')
        else:
            sg.popup('Please enter a valid email address')

    # Get contact details from user input and perform an update action
    if event == 'Update':
        username = values['-USERNAME-']
        email = values['-EMAIL-']
        phone_numbers = values['-PHONE-'].split(',')
        address = values['-ADDRESS-']
        # Validate updated email and phone number
        if validate_email(email):
            if validate_phone(values['-PHONE-']):
                update_contact(username, email, phone_numbers, address)
                sg.popup('Contact updated successfully.')
            else:
                sg.popup('Please enter a valid phone number(s)')
        else:
            sg.popup('Please enter a valid email address')

    # Get username from user input and perform a deletion action
    if event == 'Delete':
        username = values['-USERNAME-']
        delete_contact(username)
        sg.popup('Contact deleted successfully.')

    # List contacts button
    if event == 'List Contacts':
        list_contacts()

    # Get first name from user input and search for it in contacts
    if event == 'Search':
        first_name = values['-SEARCH-']
        search_contact_by_firstname(first_name)

# Close the window
window.close()
