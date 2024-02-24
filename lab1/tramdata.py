import sys
import json
from math import cos, sqrt, pi

# files given
STOP_FILE = './data/tramstops.json'
LINE_FILE = './data/tramlines.txt'

# file to give
TRAM_FILE = './tramnetwork.json'

def build_tram_stops(jsonobject):
    tram_Station = {}
    with open(STOP_FILE, 'r') as file:
        stops = json.load(file)
        
    for stop_name, stop_info in stops.items():
        position = stop_info['position']
        tram_Station[stop_name] = {'lat': float(position[0]), 'lon': float(position[1])}

    return tram_Station


def build_tram_lines(lines):

    tram_lines = {}
    delta_time= {}

    with open(LINE_FILE, 'r', encoding='utf-8') as file:
        lines_raw = file.read()
        Lines_seperated = lines_raw.split("\n\n")

        for line in Lines_seperated[:-1]:
            Stops_seperated = line.split("\n")
            line_key = Stops_seperated.pop(0).rstrip(':')
            tram_lines[line_key] = [stop.split("  ")[0] for stop in Stops_seperated]

            Stop_time = [int(stop.split(":")[1]) for stop in Stops_seperated]
            Stop_name = [stop.split("  ")[0] for stop in Stops_seperated]

            for n in range(len(Stop_name)-1):
                duration = Stop_time[n+1] - Stop_time[n]
                if Stop_time[n+1] != 0:
                    if Stop_name[n] not in delta_time:
                        delta_time[Stop_name[n]] = {Stop_name[n+1]: duration}
                    elif Stop_name[n+1] not in delta_time[Stop_name[n]]:
                        delta_time[Stop_name[n]][Stop_name[n+1]] = duration

        return tram_lines, delta_time

def build_tram_network(stopfile, linefile):

    tram_stops = build_tram_stops(stopfile)
    tram_lines, delta_time = build_tram_lines(linefile)
    tram_network = {'stops': {}, 'lines': {}, 'times': {}}

    for key, value in tram_stops.items():
        tram_network['stops'][key] = value

    for key, value in tram_lines.items():
        tram_network['lines'][key] = value

    for key, value in delta_time.items():
        tram_network['times'][key] = value

    with open(TRAM_FILE, 'w', encoding='utf-8') as json_file:
        json.dump(tram_network, json_file)
# def build_tram_network(stopfile, linefile):

#     tram_network = {
#         'stops': build_tram_stops(stopfile),
#         'lines': {},
#         'times': {}
#     }

#     tram_lines, delta_time = build_tram_lines(linefile)

#     tram_network['lines'] = tram_lines
#     tram_network['times'] = delta_time

#     with open(TRAM_FILE, 'w', encoding='utf-8') as json_file:
#         json.dump(tram_network, json_file)


def lines_via_stop(linedict, stop):

    lines_v_station = [key for key, value in linedict.items() if stop in value]

    sorted_lines = sorted(lines_v_station, key=lambda x: int(x))
    return sorted_lines


def lines_between_stops(linedict, stop1, stop2):

    Stations_btw_points = []

    for key, value in linedict.items():
        if stop1 in value and stop2 in value:
            start_index = value.index(stop1)
            end_index = value.index(stop2)
            if start_index < end_index:
                stops_btw = value[start_index:end_index + 1]
            else:
                stops_btw = value[end_index:start_index + 1]

            if stop1 in stops_btw and stop2 in stops_btw:
                Stations_btw_points.append(key)

    sorted_stops = sorted(Stations_btw_points, key=lambda x: int(x))
    return sorted_stops


def time_between_stops(linedict, timedict, line, stop1, stop2):
    time = 0

    # Strip leading and trailing spaces from stop names
    stop1 = stop1.strip()
    stop2 = stop2.strip()

    if stop1 in linedict[line] and stop2 in linedict[line]:
        stops_on_line = linedict[line]
        start_index = stops_on_line.index(stop1)
        end_index = stops_on_line.index(stop2)

        if start_index == end_index:
            return time

        stops_between_values = stops_on_line[start_index: end_index + 1] if start_index < end_index else stops_on_line[end_index: start_index + 1]

        for indx in range(len(stops_between_values) - 1):
            if stops_between_values[indx] in timedict and stops_between_values[indx + 1] in timedict[stops_between_values[indx]]:
                time += timedict[stops_between_values[indx]][stops_between_values[indx + 1]]
            else:
                time += timedict[stops_between_values[indx + 1]][stops_between_values[indx]]

        return time
    
    return False





def distance_between_stops(stopdict, stop1, stop2):

    R = 6371.0   # Radius of The Earth  in km
    lat_1, lon_1 = [stopdict[stop1][coord] * pi/180 for coord in ['lat', 'lon']]
    lat_2, lon_2 = [stopdict[stop2][coord] * pi/180 for coord in ['lat', 'lon']]
    dlat, dlon = lat_2 - lat_1, lon_2 - lon_1
    meanlat = (lat_1 + lat_2) / 2
    
    distance = R * sqrt(dlat **2 + (cos(meanlat) * dlon) **2 )
    
    return distance


def answer_query(tramdict, query):
    
    with open(TRAM_FILE, 'r', encoding='utf-8') as json_file:
        network = json.load(json_file)

        if 'via' in query:
            stop = query.split('via ')[1]
            return lines_via_stop(network['lines'], stop)
    
        elif 'between' in query:
            stop1, stop2 = query.split("between ")[1].split(" and ")
            return lines_between_stops(network['lines'], stop1, stop2)

        elif 'time' in query:
            line, stops = query.split("time with ")[1].split(" from ")
            stop1, stop2 = stops.split(" to ")
            return time_between_stops(network['lines'], network['times'], line, stop1, stop2)

        elif 'distance' in query:
            stop1, stop2 = query.split("distance from ")[1].split(" to ")
            return distance_between_stops(network['stops'], stop1, stop2)

        else:
            return False


def dialogue(tramfile=TRAM_FILE):

    with open(TRAM_FILE, 'r', encoding='utf-8'):
        while True:
            query = input('> ')
            if query.lower() == 'quit':
                break
            
            if any(word in query for word in ['via', 'between', 'distance', 'time']):
                answer = answer_query(tramfile, query)
                print(answer if answer else 'Unknown argument')
            else:
                print('Sorry, please try again')


if __name__ == '__main__':
    if sys.argv[1:] == ['init']:
        build_tram_network(STOP_FILE,LINE_FILE)
    else:
        dialogue()