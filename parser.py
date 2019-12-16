from bs4 import BeautifulSoup
import requests

def get_html(route):
    base_url = 'https://icobench.com'
    url = base_url + route
    print(f'Загружаю страницу - {url}')

    try:
        response = {
            'success': True,
            'body': requests.get(url)
        }
    except:
        response = {
            'success': False,
            'message': 'get_html_fail'
        }

    success = response['success']
    if not success:
        print(f'Не удалось загрузить страницу - {url}')
        return response

    body = response['body']
    soup = BeautifulSoup(body.text, 'html.parser')

    print(f'Успешно загрузил страницу - {url}')
    return {
        'success': True,
        'soup': soup
    }

def get_list():
    print('Загружаю список IEO')
    response = get_html('/ieo')

    success = response['success']
    if not success:
        print('Не удалось получить страницу с списком')
        return response

    soup = response['soup']
    
    table = soup.find(id='ieocols').find('table')

    if not table:
        print('На полученной странице таблица не найдена')
        return {
            'success': False,
            'message': 'table_not_found'
        }

    trs = table.find_all('tr')
    valid_trs = len(trs) > 0
    if not valid_trs:
        print('В полученной таблице строк не найдено')
        return {
            'success': False,
            'message': 'rows_not_found'
        }

    parsed_list = []
    for tr in trs:
        ico_data = tr.find('td', class_='ico_data')

        if not ico_data:
            continue

        a = ico_data.find('a', class_='name')

        parsed_list.append({
            'name': a.get_text(strip=True),
            'href': a.get('href'),
            'status': 'not_loaded',
            'valid': False,
            'links': [
                {
                    'name': 'ICOBench',
                    'url': 'https://icobench.com' + a.get('href')
                }
            ]
        })

    print(f'На странице обнаружено {str(len(parsed_list))} IEO')

    return {
        'success': True,
        'list': parsed_list
    }

def get_one(ieo):
    name_ieo = ieo['name']
    href_ieo = ieo['href']
    print(f'Загружаю данные по проекту {name_ieo}')
    
    response = get_html(href_ieo)

    success = response['success']
    if not success:
        print(f'Не удалось получить страницу с проектом {name_ieo}')
        return response

    soup = response['soup']
    socials = soup.find('div', class_='socials')
    if not socials:
        print('Не найдена информация о социальных сетях на странице')
        return {
            'success': False,
            'message': 'socials_not_found'
        }

    a_list = socials.find_all('a')

    links = ieo['links']
    for a in a_list:
        links.append({
            'name': a.get_text(strip=True),
            'url': a['href']
        })

    ieo['links'] = links
    ieo['valid'] = True
    ieo['status'] = 'success_socials_loaded'

    print(f'Получил данные по проекту', name_ieo)
    return {
        'success': True,
        'ieo': ieo
    }
