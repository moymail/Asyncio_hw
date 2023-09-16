import requests
import datetime

URL = "https://swapi.dev/api/people/"


def get_people_1():
    result = requests.get(URL).json()
    return result['count']


def get_people_2():
    n = get_people_1()
    L = []
    for i in range(n + 1):
        result = requests.get(URL+f"{i}").json()
        L.append(result)
    return L


if __name__ == '__main__':
    start = datetime.datetime.now()
    r = get_people_2()
    for i in r:
        print(i)
    finish = datetime.datetime.now()
    print("Время работы: ", finish - start)
