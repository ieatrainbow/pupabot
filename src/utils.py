import config

# Глобальные переменные для хранения данных
pupa_quotes = []
pupa_wisdom = []
technik_quotes = []


async def load_quotes():
    global pupa_quotes, pupa_wisdom, technik_quotes
    
    with open(f'{config.data_folder}/text/pupa_q.txt', 'r', encoding='UTF-8') as pupa_q:
        pupa_quotes = pupa_q.read().split('\n')
    
    with open(f'{config.data_folder}/text/pupa_w.txt', 'r', encoding='UTF-8') as pupa_w:
        pupa_wisdom = pupa_w.read().split(';')
    
    with open(f'{config.data_folder}/text/technik_q.txt', 'r', encoding='UTF-8') as technik_q:
        technik_quotes = technik_q.read().split('\n')


def get_pupa_quotes():
    return pupa_quotes


def get_pupa_wisdom():
    return pupa_wisdom


def get_technik_quotes():
    return technik_quotes