import asyncio
import aiohttp
import requests
import datetime

from Models import Base, Session, SwapiPeople
from dsn import engine

URL = "https://swapi.dev/api/people/"


def _sor(result: list):
    list_ = []
    for r in result:
        if r.get('name'):
            dict_person = {
                'name': r['name'],
                'height': r['height'],
                'mass': r['mass'],
                'hair_color': r['hair_color'],
                'skin_color': r['skin_color'],
                'eye_color': r['eye_color'],
                'birth_year': r['birth_year'],
                'gender': r['gender'],
                'homeworld': r['homeworld'],
                'films': r['films'],
                'species': r['species'],
                'vehicles': r['vehicles'],
                'starships': r['starships']
            }
            list_.append(dict_person)
    return list_


def _get_people_1():
    result = requests.get(URL).json()
    return result['count']


async def download_links(st_1: str, st_2: str, result, client_session):
    links_ = result.get(st_1, [])
    cor_links_1 = [client_session.get(link_) for link_ in links_]
    requests_ = await asyncio.gather(*cor_links_1)
    cor_links_2 = [request_.json() for request_ in requests_]
    requests_ = await asyncio.gather(*cor_links_2)
    list_ = [i[st_2] for i in requests_]
    return list_


async def _get_people_2(id_: int, client_session):
    async with client_session.get(URL + f"{id_}") as response:
        result = await response.json()
        cor_films = download_links('films', 'title', result, client_session)
        cor_species = download_links('species', "classification", result, client_session)
        cor_starships = download_links('starships', "name", result, client_session)
        cor_vehicles = download_links('vehicles', "name", result, client_session)
        list_ = [cor_films, cor_species, cor_starships, cor_vehicles]
        cor_result = await asyncio.gather(*list_)
        result['films'] = ", ".join(cor_result[0])
        result['species'] = ", ".join(cor_result[1])
        result['starships'] = ", ".join(cor_result[2])
        result['vehicles'] = ", ".join(cor_result[3])
        return result


async def past_to_db(result: list):
    async with Session() as session:
        objects_list = [SwapiPeople(**i) for i in result]
        session.add_all(objects_list)
        await session.commit()


async def cor():
    async with engine.begin() as con:
        await con.run_sync(Base.metadata.create_all)

    async with aiohttp.ClientSession() as client_session:
        n = _get_people_1()
        list_ = [_get_people_2(i, client_session) for i in range(1, n + 1)]
        result = await asyncio.gather(*list_)

    result_sort = _sor(result)

    await past_to_db(result_sort)

    return result_sort


if __name__ == '__main__':
    start = datetime.datetime.now()
    res = asyncio.run(cor())
    finish = datetime.datetime.now()
    print("Время работы: ", finish - start)
