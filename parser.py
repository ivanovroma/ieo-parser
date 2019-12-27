from bs4 import BeautifulSoup
import requests

def get_html(route):
    base_url = 'https://icobench.com'
    url = base_url + route

    try:
        response = {
            'success': True,
            'body': requests.get(url)
        }
    except:
        response = {
            'success': False,
            'message': 'get_html_fail',
            'subject': url
        }

    success = response['success']
    if not success:
        print(f'Не удалось загрузить страницу - {url}')
        return response

    body = response['body']
    soup = BeautifulSoup(body.text, 'html.parser')

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

    ieocols = soup.find(id='ieocols')
    if not ieocols:
        print('#ieocols не найден')
        return {
            'success': False,
            'message': 'ieocols_not_found',
        }
    
    table = ieocols.find('table')

    if not table:
        print('На полученной странице таблица не найдена')
        return {
            'success': False,
            'message': 'table_not_found',
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
            'links': [
                {
                    'name': 'ICOBench',
                    'url': 'https://icobench.com' + a.get('href')
                }
            ]
        })

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
            'message': 'socials_not_found',
            'subject': href_ieo
        }

    a_list = socials.find_all('a')

    links = ieo['links']
    for a in a_list:
        links.append({
            'name': a.get_text(strip=True),
            'url': a['href']
        })

    ieo['links'] = links

    return {
        'success': True,
        'ieo': ieo
    }
