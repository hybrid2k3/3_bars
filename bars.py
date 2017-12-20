import json
from math import radians, cos, sin, asin, sqrt
import sys


def haversine(lat1, lon1, lat2, lon2):
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, (lon1, lat1, lon2, lat2))

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    km = 6367 * c
    return km


def load_data(filepath):
    with open(filepath, encoding='utf-8') as json_file:
        json_json_data = json.load(json_file)
        lenjson = (len(json_json_data['features']))  # считаем кол-во элементов
        i = 0
        all_seatcount = []
        all_address = []
        all_coordins = []
        all_name = []
        all_bars_list = []
        while i < lenjson:  # создаем списки
            bar_seats_count = json_json_data['features'][i]['properties']['Attributes']['SeatsCount']
            bar_address = json_json_data['features'][i]['properties']['Attributes']['Address']
            bar_name = json_json_data['features'][i]['properties']['Attributes']['Name']
            lat_long = json_json_data['features'][i]['geometry']['coordinates']
            all_seatcount.append(bar_seats_count)
            all_address.append(bar_address)
            all_coordins.append(lat_long)
            all_name.append(bar_name)
            all_bars_list.append([bar_name, bar_address, lat_long, bar_seats_count])
            i += 1
        return all_bars_list


def get_biggest_bar(json_data):
    big_bar_count = []
    i = 0
    while i < len(json_data):
        for element in json_data:
            big_bar = element[3]
            big_bar_count.append(big_bar)
            i = i + 1
    max_seat_count = (max(big_bar_count))
    max_seat_index = big_bar_count.index(max_seat_count)
    print('Самый большой бар называется - {}. Находится по адресу {}, кол-во посадочных мест равно - {}'.format(
        json_data[max_seat_index][0], json_data[max_seat_index][1], json_data[max_seat_index][3]))


def get_smallest_bar(json_data):
    small_bar_count = []
    i = 0
    while i < len(json_data):
        for element in json_data:
            small_bar = element[3]
            small_bar_count.append(small_bar)
            i = i + 1
    max_seat_count = (min(small_bar_count))
    max_seat_index = small_bar_count.index(max_seat_count)
    print('Самый маленький бар называется - {}. Находится по адресу {}, кол-во посадочных мест равно - {}'.format(
        json_data[max_seat_index][0], json_data[max_seat_index][1], json_data[max_seat_index][3]))


def get_closest_bar(json_data, longitude, latitude):
    distance = []
    i = 0
    while i < len(json_data):
        for element in json_data:
            dist = haversine(latitude, longitude, element[2][1], element[2][0])
            distance.append(dist)
            i = i + 1
    round_distance = (round(min(distance), 2))
    minimal_dst_bar = min(distance)
    bar_index = distance.index(minimal_dst_bar)
    restor_addr = json_data[bar_index][1]
    restor_name = json_data[bar_index][0]
    print('До ближайшего бара {} км. Находиться по адресу: {}. Называется: {}'.format(round_distance, restor_addr,
                                                                                      restor_name))


if __name__ == '__main__':
    json_data = load_data(sys.argv[1])
    get_biggest_bar(json_data)
    get_smallest_bar(json_data)
    longitude = float(input('Введите долготу'))
    latitude = float(input('Введите широту'))
    get_closest_bar(json_data, longitude, latitude)
