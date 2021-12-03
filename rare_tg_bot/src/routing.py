import requests
import time
import datetime
from secret import API_KEY

API_ROOT_ENDPOINT = 'https://courier.yandex.ru/vrs/api/v1'


def get_rout_url(payload=None):
    """

    :param payload: Тело запроса - в нем содержаться координаты точек которые надо посетить
    :return: ссылку на маршрут в картах
    """
    if payload is None:
        payload = {
            'depot': {'id': 0, 'time_window': depot_time + '-23:59', 'point': {'lat': 55.733777, 'lon': 37.588118}},
            'locations': [
                {'id': 1, 'time_window': '00:00-23:59', 'point': {'lat': 55.684872, 'lon': 37.595965}},
                {'id': 2, 'time_window': '00:00-23:59', 'point': {'lat': 55.739796, 'lon': 37.689102}},
                {'id': 3, 'time_window': '00:00-23:59', 'point': {'lat': 55.809657, 'lon': 37.520314}},
                {'id': 4, 'time_window': '00:00-23:59', 'point': {'lat': 55.744764, 'lon': 37.558224}},
                {'id': 5, 'time_window': '00:00-23:59', 'point': {'lat': 55.788563, 'lon': 37.670101}},
            ],
            'vehicle': {'id': 0},
            'options': {'time_zone': 3}
        }

    # Отправляем запрос
    response = requests.post(
        API_ROOT_ENDPOINT + '/add/svrp',
        params={'apikey': API_KEY}, json=payload)

    poll_stop_codes = {
        requests.codes.ok,
        requests.codes.gone,
        requests.codes.internal_server_error
    }

    # Опрос сервера о готовности результата оптимизации маршрута
    if response.status_code == requests.codes.accepted:
        request_id = response.json()['id']
        poll_url = '{}/result/svrp/{}'.format(API_ROOT_ENDPOINT, request_id)

        response = requests.get(poll_url)
        while response.status_code not in poll_stop_codes:
            time.sleep(1)
            response = requests.get(poll_url)

        # Вывод ссылки на маршрут
        if response.status_code != 200:
            print('Error {}: {}'.format(response.text, response.status_code))
        else:
            pass
            for route in response.json()['result']['routes']:
                yamaps_url = 'https://yandex.ru/maps/?mode=routes&rtext='
                for waypoint in route['route']:
                    point = waypoint['node']['value']['point']
                    yamaps_url += '{}%2c{}~'.format(point['lat'], point['lon'])
                return yamaps_url


def routs_for_every_truck(dict_payloads):
    """
    :param dict_payloads: dict в формате {driver_id_0: payload_0, driver_id_1: payload_1, ...}
    :return: Возвращает словарь с ссылками на построенный маршрут в картах
    """
    ans_dict = {}
    for driver_info in dict_payloads.items():
        ans_dict[driver_info[0]] = get_rout_url(driver_info[1])
    return ans_dict


if __name__ == '__main__':
    depot_time = datetime.datetime.now().strftime('%H:%M')
    dct_pld = {0: {
        'depot': {'id': 0, 'time_window': depot_time + '-23:59', 'point': {'lat': 55.733777, 'lon': 37.588118}},
        'locations': [
            {'id': 1, 'time_window': '00:00-23:59', 'point': {'lat': 55.684872, 'lon': 37.595965}},
            {'id': 2, 'time_window': '00:00-23:59', 'point': {'lat': 55.739796, 'lon': 37.689102}},
            {'id': 3, 'time_window': '00:00-23:59', 'point': {'lat': 55.809657, 'lon': 37.520314}},
            {'id': 4, 'time_window': '00:00-23:59', 'point': {'lat': 55.744764, 'lon': 37.558224}},
            {'id': 5, 'time_window': '00:00-23:59', 'point': {'lat': 55.788563, 'lon': 37.670101}},
        ],
        'vehicle': {'id': 0},
        'options': {'time_zone': 3}
    }
    }
