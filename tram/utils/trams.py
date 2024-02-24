import json
import os
from django.conf import settings
from .graphs import Graph
from .graphs import  view_shortest_path_weighted
from .graphs import dijkstra_algorithm
from math import radians, cos, sin, sqrt
#from .graphs import * 
# path changed from Lab2 version
# TODO: copy your json file from Lab 1 here
TRAM_FILE = os.path.join(settings.BASE_DIR, 'static/tramnetwork.json')

from lab1 import tramdata as td





class TramNetwork(Graph):
    def __init__(self, lines, stops, times):
        super().__init__(stops)
        self._linedict = lines
        self._stopdict = stops
        self._timedict = times
        self.graph = Graph(stops)

        for stop_name in self._stopdict.keys():
            self.add_vertex(stop_name)

        for tram_line, stops in self._linedict.items():
            for stop1, stop2 in zip(stops, stops[1:]):
                self.add_edge(stop1, stop2)
    def view_shortest_path_weighted(self, start, end, cost_func=lambda u, v: 1):
        distances, paths = self.graph.dijkstra_algorithm(start, cost_func)

    def all_lines(self):
        return list(self._linedict.keys())
    
    def all_stops(self):
        return list(self._stopdict.keys())

    def extreme_positions(self):
        latitudes, longitudes = zip(*[(loc['lat'], loc['lon']) for loc in self._stopdict.values()])
        return min(latitudes), min(longitudes), max(latitudes), max(longitudes)
    
    def geo_distance(self, a, b):
        earth_radius = 6371.0
        lat_1, lon_1 = radians(self._stopdict[a]['lat']), radians(self._stopdict[a]['lon'])
        lat_2, lon_2 = radians(self._stopdict[b]['lat']), radians(self._stopdict[b]['lon'])
        delta_lat = lat_2 - lat_1
        delta_lon = lon_2 - lon_1
        mean_lat = (lat_1 + lat_2) / 2

        distance = earth_radius * sqrt(delta_lat ** 2 + (cos(mean_lat) * delta_lon) ** 2)
        return distance
    
    def line_stops(self, line):
        return self._linedict.get(line, [])
    
    def stop_lines(self, a):
        return td.lines_via_stop(self._linedict, a)
    
    def stop_position(self, a):
        return self._stopdict.get(a, None)
    
    def transition_time(self, line, a, b):
        if line not in self._linedict or a not in self._linedict[line] or b not in self._linedict[line]:
            return False

        on_line = self._linedict[line]
        beg_index = on_line.index(a)
        end_index = on_line.index(b)

        if beg_index == end_index:
            return 0

        if beg_index < end_index:
            S_b_V = on_line[beg_index: end_index + 1]
        else:
            S_b_V = on_line[end_index: beg_index + 1]

        time = 0

        for indx in range(len(S_b_V) - 1):
            C_stop = S_b_V[indx]
            N_stop = S_b_V[indx + 1]

            if C_stop in self._timedict and N_stop in self._timedict[C_stop]:
                time += self._timedict[C_stop][N_stop]
            else:
                time += self._timedict[N_stop][C_stop]

        return time
    def find_lines_between_stops(network, start_stop, end_stop):
        lines_between_stops = []

        for line_key, stops_on_line in network._linedict.items():
            if start_stop in stops_on_line and end_stop in stops_on_line:
                lines_between_stops.append(line_key)

        sorted_lines = sorted(lines_between_stops, key=lambda line: int(line))
        return sorted_lines
    
    def calculate_travel_time(self, start_stop, end_stop):
        total_time = 0
        main_line = self.find_lines_between_stops(start_stop, end_stop)[0]
        stops_on_common_line = self._linedict[main_line]
        start_index = stops_on_common_line.index(start_stop)
        end_index = stops_on_common_line.index(end_stop)

        if start_index == end_index:
            return total_time

        if start_index < end_index:
            S_b_V = stops_on_common_line[start_index: end_index + 1]
        else:
            S_b_V = stops_on_common_line[end_index: start_index + 1]

        for indx in range(len(S_b_V) - 1):
            C_stop = S_b_V[indx]
            N_stop = S_b_V[indx + 1]

            if C_stop in self._timedict and N_stop in self._timedict[C_stop]:
                total_time += self._timedict[C_stop][N_stop]
            else:
                total_time += self._timedict[N_stop][C_stop]

        return total_time



class TramLine:
    def __init__(self, num, stops):
        self._number = num
        self._stops = stops
        
    def get_number(self):
        return self._number
    
    def get_stops(self):
        return self._stops


class TramStop:
    def __init__(self, name, lines=None, lan=0, lon=0):
        self._name = name
        self._lines = lines or []  
        self._position = (lan, lon)

    def lines(self):
        return self._lines 
    
    def name(self):
        return self._name

    def pos(self):
        return self._position

    def set_pos(self, lan, lon):
        self._position = (lan, lon)

    def add_line(self, line):
        self._lines.append(line)



def readTramNetwork(tramfile=TRAM_FILE):
    with open(tramfile, 'r') as file:
        network = json.load(file)
        #tram_network = TramNetwork(lines, stops, times) 
        tram_network = TramNetwork(network["lines"], network['stops'], network['times'])
        return tram_network
# def display_shortest_path():
#     graph = readTramNetwork()

#     A, B = input('Enter start and end stops separated by a comma: ').split(',')
#     view_shortest_path_weighted(graph, A, B)
#     # Check if the input contains a comma
#     # if ',' not in A,B:
#     #     print("Invalid input. Please enter start and end stops separated by a comma.")
#     #     return

#     # start, end = map(str.strip, user_input.split(','))

#     # view_shortest_path_weighted(tram_network, start, end)

# if __name__ == '__main__':
    
#     display_shortest_path()









# Bonus task 1: take changes into account and show used tram lines

def specialize_stops_to_lines(network):
    # TODO: write this function as specified
    return network


def specialized_transition_time(spec_network, a, b, changetime=10):
    # TODO: write this function as specified
    return changetime


def specialized_geo_distance(spec_network, a, b, changedistance=0.02):
    # TODO: write this function as specified
    return changedistance

