from shiny import reactive, render

from shiny.express import ui

# Imports from Python Standard Library to simulate live data 
import random
from datetime import datetime
from collections import deque

# Import pandas for working with data
import pandas as pd

from faicons import icon_svg

# PLANNING: We want to get a fake temp and time stamp every
# N seconds. Use constants for update interval so it's easy to 
# modify 

# Set a constant UPDATE INTERVAL for all live data. Constants
# are usually defined in uppercase letters
# Use a type hint to make it clear that it's an integer (: int)

UPDATE_INTERVAL_SECS: int = 1

# Initialize a REACTIVE VALUE with a common data structure
# The reactive value is used to store state (information)
# Used by all the display components that show this live data.
# This reactive value is a wrapper around a DEQUE of readings

DEQUE_SIZE: int = 5
reactive_value_wrapper = reactive.value(deque(maxlen=DEQUE_SIZE))

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

    # Get a timestamp for "now" and use string format strftime() method to format it
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_dictionary_entry = {"temp": temp, "timestamp": timestamp}

    # get the deque and append the new entry
    reactive_value_wrapper.get().append(new_dictionary_entry)

    # Get a snapshot of the current deque for any further processing
    deque_snapshot = reactive_value_wrapper.get()

    # For Display: Convert deque to DataFrame for display
    df = pd.DataFrame(deque_snapshot)

    # For Display: Get the latest dictionary entry
    latest_dictionary_entry = new_dictionary_entry

    # Return a tuple with everything we need
    # Every time we call this function, we'll get all these values
    return deque_snapshot, df, latest_dictionary_entry

    
# Define the Shiny UI Page layout - Page Options

ui.page_opts(title="PyShiny Express: Live Data With Value Card (Font Awesome Icon + 3 Strings)", fillable=True)

with ui.sidebar(open="open"):
    
    ui.h2("Antarctic Explorer", class_="text-center")
    
    ui.p(
        "A demonstration of real-time temperature readings in Antarctica.",
        class_="text-center",
    )

    ui.h2()
    ui.h6("Links:")
    ui.a(
        "GitHub Source",
        href="https://github.com/bvrtachnik/cintel-05-cintel",
        target="_blank",
    )
    ui.a(
        "GitHub App",
        href="https://bvrtachnik.github.io/cintel-05-cintel/",
        target="_blank",
    )
    ui.a("PyShiny", href="https://shiny.posit.co/py/", target="_blank")

# In Shiny Express, everything not in the sidebar is in the main panel

with ui.layout_columns():
    with ui.value_box(
        showcase=icon_svg("sun"),
        theme="bg-gradient-blue-purple"
    ):

        "Current Temperature"
        @render.text
        def display_temp():
            """"Get the latest reading and return a temperature string"""
            deque_snapshot, df, latest_dictionary_entry = reactive_calc_combined()
            return f"{latest_dictionary_entry['temp']} C"

        "warmer than usual"

with ui.layout_columns():
    with ui.card():
        ui.card_header("Current Data (placeholder only)")

with ui.layout_columns():
    with ui.card():
        ui.card_header("Current Chart (placeholder only)")
