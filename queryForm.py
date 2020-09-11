# queryForm.py takes data submitted by the user through the form and constructs an sql query to grab data that 
# matches their specifications 

from datetime import datetime
from geopy.geocoders import Nominatim
from connect import connect


def query_filter_form(data, per_page, offset, offline_debug=False):
    # this will be used to get the lat/long of cities, allowing for cars nearby searches
    geo = Nominatim(user_agent="CraigslistFilter")

    # grab data from user
    location = data['location']
    manufacturer = data['manufacturer']
    model = data['model']
    cond = data['condition']
    cyl = data['cylinders']
    fuel = data['fuel']
    tran = data['transmission']
    title = data['title_status']
    vin = data['vin']
    drive = data['drive']
    size = data['size']
    vehicle_type = data['vehicle_type']
    color = data['paint_color']
    price_start = data['price_start']
    price_end = data['price_end']
    year_start = data['year_start']
    year_end = data['year_end']
    odom_start = data['odometer_start']
    odom_end = data['odometer_end']
    sort_by = data['sort_by'].replace("high to low", "DESC").replace("low to high", "ASC")

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
        query = f"SELECT url, region, price, year, manufacturer, model, image_url FROM vehicles {sort_clause} LIMIT {per_page} OFFSET {offset};"
        len_query = f"SELECT count(*) FROM vehicles;"
    else:
        query = f"SELECT url, region, price, year, manufacturer, model, image_url FROM vehicles WHERE {where_clause} {sort_clause} LIMIT {per_page} OFFSET {offset};"
        len_query = f"SELECT count(*) FROM vehicles WHERE {where_clause};"

    conn = connect(offline_debug)
    curs = conn.cursor()
    curs.execute(query, value_tuple)
    vehicle_res = curs.fetchall()
    curs.execute(len_query, value_tuple)
    len_res = curs.fetchall()[0][0]
    conn.close()

    # return our results
    return vehicle_res, len_res

def query_table_form(data, offline_debug=False):
    # this will be used to get the lat/long of cities, allowing for cars nearby searches
    geo = Nominatim(user_agent="CraigslistFilter")

    # grab data from user
    location = data['location']
    manufacturer = data['manufacturer']
    model = data['model']
    cond = data['condition']
    cyl = data['cylinders']
    fuel = data['fuel']
    tran = data['transmission']
    title = data['title_status']
    vin = data['vin']
    drive = data['drive']
    size = data['size']
    vehicle_type = data['vehicle_type']
    color = data['paint_color']
    price_start = data['price_start'] if data['price_start'] != None else 100
    price_end = data['price_end'] if data['price_end'] != None else 5000000
    year_start = data['year_start'] if data['year_start'] != None else 1880
    year_end = data['year_end'] if data['year_end'] != None else datetime.now().year + 1
    odom_start = data['odometer_start'] if data['odometer_start'] != None else 0
    odom_end = data['odometer_end'] if data['odometer_end'] != None else 1000000
    display_field = data['display_field']
    group_by = data['group_by']

    # construct dict of strings for the query
    criteria_dict = {location: "location", manufacturer: "manufacturer", model: "model", cond: "condition",
                     cyl: "cylinders", tran: "transmission", vin: "vin", fuel: "fuel",
                     drive: "drive", size: "size", vehicle_type: "type", title: "title_status",
                     color: "paint_color", price_start: "price", price_end: "price", year_start: "year",
                     year_end: "year"}

    where_clause = ""
    value_tuple = ()
    for k, v in criteria_dict.items():
        # if not k then the field was left blank and we do not include it in the query, otherwise we search by it
        if k is not None and k != "":
            # these if statements allow for searching by minimum/maximum values
            if v == "year":
                # query between the two values
                where_clause = where_clause + f"{v} BETWEEN %s AND %s AND "
                value_tuple = value_tuple + (year_start, year_end,)
            # repeat
            elif v == "odometer":
                where_clause = where_clause + f"{v} BETWEEN %s AND %s AND "
                value_tuple = value_tuple + (odom_start, odom_end,)
            elif v == "price":
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

    # finally our query
    if not where_clause:
        query = f"SELECT {display_field}, {group_by} FROM vehicles LIMIT 20000;"
        len_query = f"SELECT count(*) FROM vehicles;"
    else:
        query = f"SELECT {display_field}, {group_by} FROM vehicles WHERE {where_clause} LIMIT 50000;"
        len_query = f"SELECT count(*) FROM vehicles WHERE {where_clause};"

    conn = connect(offline_debug)
    curs = conn.cursor()
    curs.execute(query, value_tuple)
    vehicle_res = curs.fetchall()
    curs.execute(len_query, value_tuple)
    len_res = curs.fetchall()[0][0]
    conn.close()

    if group_by == "price":
        min_group_by = price_start
    elif group_by == "odometer":
        min_group_by = odom_start
    elif group_by == "year":
        min_group_by = year_start

    # return our results
    return vehicle_res, len_res, min_group_by
