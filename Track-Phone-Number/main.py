from tkinter import *
import requests
import webbrowser
from opencage.geocoder import OpenCageGeocode

API_KEY = 'num_live_qr6f39KWNiNgxhUmes7tOJO9CZMu4Kig5k6VuHxz'
NUMLOOKUP_URL = 'https://api.numlookupapi.com/v1/validate'
OPENCAGE_API_KEY = '74e25940d3734ded8b1fb6ccad76ae35'


def get_phone_info(phone_number):
    url = f"{NUMLOOKUP_URL}/{phone_number}?apikey={API_KEY}"
    response = requests.get(url)
    data = response.json()

    if not data.get('valid', False):
        return {"valid": False}

    return data


def get_phone_brand(phone_info):
    if 'brand' in phone_info:
        return phone_info['brand']
    return "Unknown"


def get_ip_location():
    geocoder = OpenCageGeocode(OPENCAGE_API_KEY)
    response = requests.get("https://ipapi.co/json/")
    data = response.json()
    lat = data.get('latitude', '')
    lon = data.get('longitude', '')
    if lat and lon:
        result = geocoder.reverse_geocode(lat, lon)
        if result:
            return result[0]['formatted']
    return None


def track():
    phone_number = entry.get()
    if not phone_number.startswith('+'):
        result_text.config(
            text=
            "Invalid number format. Use + followed by country code and number."
        )
        return

    phone_info = get_phone_info(phone_number)

    if not phone_info.get('valid', False):
        result_text.config(text="No information found for this number.")
        return

    result_text.config(
        text=f"Valid: {phone_info['valid']}\n"
        f"Number: {phone_info.get('number', '')}\n"
        f"Local Format: {phone_info.get('local_format', '')}\n"
        f"International Format: {phone_info.get('international_format', '')}\n"
        f"Country Prefix: {phone_info.get('country_prefix', '')}\n"
        f"Country Code: {phone_info.get('country_code', '')}\n"
        f"Country Name: {phone_info.get('country_name', '')}\n"
        f"Location: {get_ip_location()}\n"
        f"Carrier: {phone_info.get('carrier', '')}\n"
        f"Line Type: {phone_info.get('line_type', '')}\n"
        f"Brand: {get_phone_brand(phone_info)}\n"
        f"Latitude: {phone_info.get('latitude', '')}\n"
        f"Longitude: {phone_info.get('longitude', '')}\n")

    lat = phone_info.get('latitude')
    lon = phone_info.get('longitude')

    if lat is not None and lon is not None:
        open_maps(lat, lon)


def open_maps(lat, lon):
    maps_url = f"https://www.google.com/maps/place/{lat},{lon}"
    webbrowser.open(maps_url)


def open_location_in_maps():
    location = get_ip_location()
    if location:
        open_maps(location)


def handle_copy_paste(event):
    if event.keysym == 'c' and event.state == 4:
        root.clipboard_clear()
        root.clipboard_append(entry.get())
    elif event.keysym == 'v' and event.state == 4:
        entry.delete(0, END)
        entry.insert(0, root.clipboard_get())


root = Tk()
root.title("Detailed Phone Number Tracker")
root.geometry("600x700")
root.resizable(False, False)
root.configure(bg='#E6E6FA')

entry_frame = Frame(root, bg='#E6E6FA')
entry_frame.pack(pady=20)

entry_label = Label(entry_frame,
                    text="Enter Phone Number:",
                    font=("Arial", 14),
                    bg='#E6E6FA')
entry_label.pack(side=LEFT, padx=10)
entry = Entry(entry_frame, width=25, bd=2, font=("Arial", 16))
entry.pack(side=LEFT, padx=10)

entry.bind('<Control-c>', handle_copy_paste)
entry.bind('<Control-v>', handle_copy_paste)

button = Button(root, text="Track", command=track, font=("Arial", 14))
button.pack(pady=20)

result_frame = Frame(root, bg='#E6E6FA')
result_frame.pack(pady=20)

result_label = Label(result_frame,
                     text="Result:",
                     font=("Arial", 16),
                     bg='#E6E6FA')
result_label.pack(pady=10)

result_text = Label(result_frame,
                    width=60,
                    height=20,
                    wraplength=500,
                    justify=LEFT,
                    anchor='nw',
                    font=("Arial", 12),
                    bg='white')
result_text.pack()

# Location Button
location_button = Button(result_frame,
                         text="Open in Maps",
                         command=open_location_in_maps,
                         font=("Arial", 12))
location_button.pack(pady=10)

root.mainloop()
