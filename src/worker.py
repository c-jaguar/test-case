import asyncio
from orm import ORM


def bgtask01():
    """Crutch for running async task in rq. Calculates item sum weight by type."""
    loop = asyncio.get_event_loop()
    coro = ORM.select_item_weight_sum()
    result = loop.run_until_complete(coro)
    return result


def bgtask01_print(dto):
    """Poor attempt to make table-like output to html page."""
    dict_i = dict(dto).keys()
    dict_v = dict(dto).values()
    result = list()
    result.append("____________________________")
    result.append("|____type____|___weight___|")
    for x, y in zip(dict_i, dict_v):
        x = str(x[1]).center(12, '_')
        y = str(y[1]).center(13, '_')
        result.append(f"|{x}|{y}|")
    print(f"{result=}")
    return result
