from math import radians, cos, sin, asin, sqrt

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r

def validate_location(accLocation, scanLocation):
    accLocation = accLocation.split(',')
    scanLocation = scanLocation.split(',')
    center_point = [{'lat': float(accLocation[0]), 'lng': float(accLocation[1])}]
    test_point = [{'lat': float(scanLocation[0]), 'lng': float(scanLocation[1])}]

    lat1 = center_point[0]['lat']
    lon1 = center_point[0]['lng']
    lat2 = test_point[0]['lat']
    lon2 = test_point[0]['lng']

    radius = 0.05 # in kilometer

    a = haversine(lon1, lat1, lon2, lat2)

    print('Distance (km) : ', a)
    if a <= radius:
        print('Inside the area')
        return True
    else:
        print('Outside the area')
        return False