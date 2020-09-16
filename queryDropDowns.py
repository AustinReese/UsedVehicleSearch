# this is a work in progress that will grab unique column values to allow for dropdown menus instead of text boxes in
# the search form


def query_drop_downs():
    drop_downs = {}
    cylinders = [('4 cylinders',), (None,), ('10 cylinders',), ('8 cylinders',), ('6 cylinders',), ('5 cylinders',),
                 ('3 cylinders',), ('other',), ('12 cylinders',)]
    fuel = [(None,), ('other',), ('hybrid',), ('gas',), ('diesel',), ('electric',)]
    title_status = [(None,), ('salvage',), ('parts only',), ('missing',), ('lien',), ('clean',), ('rebuilt',)]
    drive = [(None,), ('rwd',), ('fwd',), ('4wd',)]
    vehicle_type = [(None,), ('wagon',), ('sedan',), ('SUV',), ('bus',), ('truck',), ('mini-van',), ('convertible',),
                    ('pickup',), ('hatchback',), ('other',), ('offroad',), ('coupe',), ('van',)]
    paint_color = [('purple',), ('orange',), ('green',), ('blue',), ('brown',), ('grey',), ('yellow',), ('black',),
                   ('white',), ('red',), (None,), ('silver',), ('custom',)]
    manufacturer = [(None,), ('chevrolet',), ('mazda',), ('acura',), ('audi',), ('nissan',), ('mini',),
                    ('mercedes-benz',), ('chrysler',), ('ram',), ('kia',), ('pontiac',), ('bmw',), ('hennessey',),
                    ('infiniti',), ('volkswagen',), ('morgan',), ('ford',), ('harley-davidson',), ('jaguar',),
                    ('fiat',), ('hyundai',), ('volvo',), ('gmc',), ('rover',), ('alfa-romeo',), ('honda',),
                    ('mercury',), ('aston-martin',), ('buick',), ('lexus',), ('tesla',), ('toyota',), ('saturn',),
                    ('land rover',), ('mitsubishi',), ('cadillac',), ('subaru',), ('lincoln',), ('jeep',), ('porche',),
                    ('datsun',), ('ferrari',), ('dodge',)]
    condition = [('excellent',), ('new',), ('good',), ('fair',), (None,), ('salvage',), ('like new',)]
    size = [('sub-compact',), (None,), ('mid-size',), ('compact',), ('full-size',)]
    transmission = [(None,), ('other',), ('manual',), ('automatic',)]

    transmissions = []

    for item in transmission:
        item = item[0]
        if item is not None:
            transmissions.append((item, item))
    transmissions.append(("", ""))
    transmissions.sort()
    drop_downs["transmission"] = transmissions
    sizes = []
    for item in size:
        item = item[0]
        if item is not None:
            sizes.append((item, item))
    sizes.append(("", ""))
    sizes.sort()
    drop_downs["size"] = sizes
    cyls = []
    for item in cylinders:
        item = item[0]
        if item is not None:
            cyls.append((item, item))
    cyls.append(("", ""))
    cyls.sort()
    drop_downs["cylinders"] = cyls
    fuels = []
    for item in fuel:
        item = item[0]
        if item is not None:
            fuels.append((item, item))
    fuels.append(("", ""))
    fuels.sort()
    drop_downs["fuel"] = fuels
    title_status_list = []
    for item in title_status:
        item = item[0]
        if item is not None:
            title_status_list.append((item, item))
    title_status_list.append(("", ""))
    title_status_list.sort()
    drop_downs["title_status"] = title_status_list
    drives = []
    for item in drive:
        item = item[0]
        if item is not None:
            drives.append((item, item))
    drives.append(("", ""))
    drives.sort()
    drop_downs["drive"] = drives
    vehicle_types = []
    for item in vehicle_type:
        item = item[0]
        if item is not None:
            vehicle_types.append((item, item))
    vehicle_types.append(("", ""))
    vehicle_types.sort()
    drop_downs["vehicle_type"] = vehicle_types
    paint_colors = []
    for item in paint_color:
        item = item[0]
        if item is not None:
            paint_colors.append((item, item))
    paint_colors.append(("", ""))
    paint_colors.sort()
    drop_downs["paint_color"] = paint_colors
    manufacturers = []
    for item in manufacturer:
        item = item[0]
        if item is not None:
            manufacturers.append((item, item))
    manufacturers.append(("", ""))
    manufacturers.sort()
    drop_downs["manufacturer"] = manufacturers
    conditions = []
    for item in condition:
        item = item[0]
        if item is not None:
            conditions.append((item, item))
    conditions.append(("", ""))
    conditions.sort()
    drop_downs["condition"] = conditions
    states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA",
              "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
              "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
              "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
              "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
    state_tuples = [("", "")]
    for item in states:
        state_tuples.append((item, item))
    drop_downs["states"] = state_tuples

    sort_by_list = ["Price low to high", "Price high to low", "Odometer low to high", "Odometer high to low",
                    "Year low to high", "Year high to low"]
    sort_by_tuples = [("", "")]
    for item in sort_by_list:
        sort_by_tuples.append((item, item))
    drop_downs["sort_by"] = sort_by_tuples

    drop_downs["numerical_fields"] = [(item, item) for item in ["price", "odometer", "year"]]
    drop_downs["numerical_fields_backwards"] = [(item, item) for item in ["year", "odometer", "price"]]

    return drop_downs
