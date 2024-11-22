from shiny import reactive, render

from shiny.express import ui

# Imports from Python Standard Library to simulate live data 
import random
from datetime import datetime

from faicons import icon_svg

# PLANNING: We want to get a fake temp and time stamp every
# N seconds. Use constants for update interval so it's easy to 
# modify 

# Set a constant UPDATE INTERVAL for all live data. Constants
# are usually defined in uppercase letters
# Use a type hint to make it clear that it's an integer (: int)
UPDATE_INTERVAL_SECS: int = 1

# Initialize a REACTIVE CALC that our display components can call
# to get the latest data and display it. The calculation is 
# invalidated every UPDATE_INTERAVAL_SECS to trigger updates

# It returns everything needed to display the data. 
# Very easy to expand or modify. 

@reactive.calc()
def reactive_calc_combined():

    # Invalidate this calculation every UPDATE_INTERVAL_SEC to trigger updates
    reactive.invalidate_later(UPDATE_INTERVAL_SECS)

    # Data generation logic. Get random between -18 and -16 C, round to 1 decimal place
    temp = round(random.uniform(-18, -16), 1)

    # Get a timestamp fro "now" and use string format strftime() method to format it
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    latest_dictionary_entry = {"temp": temp, "timestamp": timestamp}

    # Return everything we need
    return latest_dictionary_entry

ui.page_opts(title="PyShiny Express: Live Data (Basic", fillable=True)

with ui.sidebar(open="open"):
    ui.h2("Antarctic Explorer", class_="text-center")
    ui.p(
        "A demonstration of real-time temperature readings in Antarctica.",
        class_="text-center",
    )

ui.h2("Current Temperature")

@render.text
def display_temp():
    """"Get the latest reading and return a temperature string"""
    latest_dictionary_entry = reactive_calc_combined()
    return f"{latest_dictionary_entry['temp']}"

ui.p("warmer than usual")

icon_svg("sun")

ui.hr()

ui.h2("Current Date and Time")

@render.text
def display_time():
    """"Get the latest reading and return a timestamp string"""
    latest_dictionary_entry = reactive_calc_combined()
    return f"{latest_dictionary_entry['timestamp']}"
    


