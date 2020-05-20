# queryForm.py takes data submitted by the user through the form and constructs an sql query to grab data that 
# matches their specifications 

from datetime import datetime
from geopy.geocoders import Nominatim
from connect import connect


def query_form(data):
    # this will be used to get the lat/long of cities, allowing for cars nearby searches
    geo = Nominatim(user_agent="CraigslistFilter")

    # grab data from user
    location = data.location.data
    manufacturer = data.manufacturer.data
    model = data.model.data
    cond = data.condition.data
    cyl = data.cylinders.data
    fuel = data.fuel.data
    tran = data.transmission.data
    title = data.title_status.data
    vin = data.vin.data
    drive = data.drive.data
    size = data.size.data
    vehicle_type = data.vehicle_type.data
    color = data.paint_color.data
    price_start = data.price_start.data
    price_end = data.price_end.data
    year_start = data.year_start.data
    year_end = data.year_end.data
    odom_start = data.odometer_start.data
    odom_end = data.odometer_end.data
    sort_by = data.sort_by.data.replace("high to low", "DESC").replace("low to high", "ASC")

    # construct dict of strings for the query
    criteria_dict = {location: "location", manufacturer: "manufacturer", model: "model", cond: "condition",
                     cyl: "cylinders", tran: "transmission", vin: "vin", fuel: "fuel",
                     drive: "drive", size: "size", vehicle_type: "type", title: "title_status",
                     color: "paint_color", price_start: "price", price_end: "price", year_start: "year",
                     year_end: "year",
                     odom_start: "odometer", odom_end: "odometer"}

    where_clause = ""
    value_tuple = ()
    for k, v in criteria_dict.items():
        # if not k then the field was left blank and we do not include it in the query, otherwise we search by it
        if k is not None and k != "":
            # these if statements allow for searching by minimum/maximum values
            if v == "year":
                # for example we must handle blank min/max's so if they are blank they are set to the default min/max
                if year_start is None:
                    year_start = 1880
                # again with maximum
                if year_end is None:
                    year_end = datetime.now().year + 1
                # query between the two values
                where_clause = where_clause + f"{v} BETWEEN %s AND %s AND "
                value_tuple = value_tuple + (year_start, year_end,)
            # repeat
            elif v == "odometer":
                if odom_start is None:
                    odom_start = 0
                if odom_end is None:
                    odom_end = 10000000
                where_clause = where_clause + f"{v} BETWEEN %s AND %s AND "
                value_tuple = value_tuple + (odom_start, odom_end,)
            elif v == "price":
                if price_start is None:
                    price_start = 0
                if price_end is None:
                    price_end = 10000000
                where_clause = where_clause + f"{v} BETWEEN %s AND %s AND "
                value_tuple = value_tuple + (price_start, price_end,)
            elif v == "model":
                where_clause = where_clause + f"{v} LIKE %s AND "
                value_tuple = value_tuple + (k.lower(),)
            elif v == "location":
                # all results near a city
                lat, long = 0, 0
                loc = geo.geocode(location)
                if loc:
                    lat, long = loc.latitude, loc.longitude
                    where_clause = where_clause + "lat BETWEEN %s AND %s AND long BETWEEN %s AND %s AND "
                    value_tuple = value_tuple + (lat - .5, lat + .5, long - .5, long + .5,)
            else:
                where_clause = where_clause + f"{v} LIKE %s AND "
                value_tuple = value_tuple + (k,)

    # remove the last AND after the loop completes
    where_clause = where_clause[:-5]

    sort_clause = ""
    if sort_by is not None and sort_by != "":
        sort_clause = f"ORDER BY {sort_by} NULLS LAST "

    # finally our query
    if not where_clause:
        query = f"SELECT * FROM vehicles {sort_clause} LIMIT 204;"
    else:
        query = f"SELECT * FROM vehicles WHERE {where_clause} {sort_clause} LIMIT 204;"

    conn = connect()
    curs = conn.cursor()
    curs.execute(query, value_tuple)
    res = curs.fetchall()
    conn.close()

    # return our results
    return res
