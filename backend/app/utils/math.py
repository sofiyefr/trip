import math

def distance(x, y):
    lat1, lon1 = x.latitude, x.longitude
    lat2, lon2 = y.latitude, y.longitude
    # Radius of Earth in kilometers. Use 3956 for miles
    R = 6371.0

    # Convert latitude and longitude from degrees to radians
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    # Haversine formula
    a = math.sin(delta_phi / 2.0) ** 2 + \
        math.cos(phi1) * math.cos(phi2) * \
        math.sin(delta_lambda / 2.0) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance_km = R * c
    return distance_km

def route_distance(route):
    total_distance = 0
    for i in range(len(route) - 1):
        total_distance += distance(route[i].city, route[i + 1].city)
    return total_distance


def salesman_optimize(locations):
    """
    This function takes a list of locations and returns the optimized order of locations
    to minimize the total distance traveled.
    """
    from itertools import permutations

    min_distance = float('inf')
    best_route = None

    # Enumerate possible pairs of locations and find best swap
    best_pair = None
    base_distance = route_distance(locations)
    for i in range(1, len(locations) - 2):
        for j in range(i + 1, len(locations) - 1):
            # Swap locations
            locations[i], locations[j] = locations[j], locations[i]
            # Calculate distance
            current_distance = route_distance(locations)
            # Check if this is the best swap
            if current_distance < base_distance:
                base_distance = current_distance
                best_pair = (i, j)
            # Swap back
            locations[i], locations[j] = locations[j], locations[i]

    # If we found a better pair, swap them
    if best_pair:
        i, j = best_pair
        locations[i], locations[j] = locations[j], locations[i]


    # Return the optimized route
    return locations    
