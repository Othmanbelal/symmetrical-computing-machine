# visualization of shortest path in Lab 3, modified to work with Django

from .trams import readTramNetwork
from .graphs import dijkstra_algorithm
from .color_tram_svg import color_svg_network
import os
from django.conf import settings

# TODO: uncomment this when it works with your own code


def show_shortest(dep, dest, cost=lambda u, v: 1):
   
    network = readTramNetwork()

    
    distance_geo, shortpath_geo = dijkstra_algorithm(network, dep, cost_func=network.geo_distance)
    shortest_geo = shortpath_geo[dest]
    distance_traveled_geo = distance_geo[dest]

    # Find quickest path based on travel time
    time, quickpath = dijkstra_algorithm(network, dep, cost_func=network.calculate_travel_time)
    quickest = quickpath[dest]
    total_time = time[dest]

    
    timepath = f'Quickest: {", ".join(quickest)}. Time it took: {total_time:.2f} min.'

    
    geopath = f'Shortest: {", ".join(shortest_geo)}. Distance traveled: {distance_traveled_geo:.3f} km.'
    def colors(v):
        if v in shortest_geo:
            return 'cyan'
        else:
            return 'white'
   

    # Color the SVG network with the specified colormap
    color_svg_network(colormap=colors)

    # Return the formatted path texts for display
    return timepath, geopath
