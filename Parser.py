from bs4 import BeautifulSoup
import requests
from Logger import Logger
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

logger = Logger()

class Parser:
    __base_url = 'https://icobench.com'
    __recheck_list = []

    def __get_html(self, route):
        url = self.__base_url + route

        simple_response = self.__simple_request(url)
        
        if not simple_response['success']:
            return simple_response
        
        protected = self.__check_protection(simple_response['soup']) 
        
        if not protected:
            return simple_response

        return self.__selenium_request(url)

    def __simple_request(self, url):
        try:
            body = requests.get(url)
            soup = BeautifulSoup(body.text, 'html.parser')
            
            return {
                'success': True,
                'soup': soup
            }
        except:
            return {
                'success': False,
                'message': 'simple_request_fail',
                'url': url
            }

    def __check_protection(self, soup):
        is_cloudflare = bool(soup.find_all(text='DDoS protection by Cloudflare'))

        return is_cloudflare

    def __selenium_request(self, url):
        def wait():
            result_soup = {}
            i = 1
            while True:
                time.sleep(7 if i == 1 else 2)
                body = browser.page_source
                soup = BeautifulSoup(body, 'html.parser')

                protected = self.__check_protection(soup)

                if not protected:
                    result_soup = soup
                    break

                i += 1
            
            return {
                'success': True,
                'soup': result_soup
            }

        options = Options()
        options.headless = True
        browser = webdriver.Firefox(options=options, log_path='./logs/geckodriver.log')
        browser.get(url)

        result = wait()

        browser.close()
        
        return result

    def get_list(self):
        response = self.__get_html('/ieo')

        success = response['success']
        if not success:
            return response

        soup = response['soup']

        ieocols = soup.find(id='ieocols')
        if not ieocols:
            return {
                'success': False,
                'message': 'ieocols_not_found',
                'subject': '/ieo'
            }
        
        table = ieocols.find('table')

        if not table:
            return {
                'success': False,
                'message': 'table_not_found',
                'subject': '/ieo'
            }

        trs = table.find_all('tr')
        valid_trs = len(trs) > 0
        if not valid_trs:
            return {
                'success': False,
                'message': 'rows_not_found',
                'subject': '/ieo'
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
                'url': self.__base_url + a.get('href'),
                'success_link_downloaded': False,
                'links': []
            })

        return {
            'success': True,
            'list': parsed_list
        }

    def __get_one(self, ieo):
        name_ieo = ieo['name']
        href_ieo = ieo['href']
        
        response = self.__get_html(href_ieo)

        success = response['success']
        if not success:
            return response

        soup = response['soup']
        socials = soup.find('div', class_='socials')
        if not socials:
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

    def get_every(self, new_ieo_list):
        error = {
            'success': False,
            'message': '',
            'subject': ''
        }

        parsed_list = []

        # Для каждого нового IEO парсим социалки
        for new_ieo in new_ieo_list:
            parsed = self.__get_one(new_ieo)

            success = parsed['success']
            if not success:
                # Если не удалось загрузить страницу, повторим попытку позже
                if (parsed.get('message') == 'get_html_fail'):
                    error['message'] = parsed.get('message')
                    error['subject'] = parsed.get('subject')
                    break

                logger.warning('Не удалось получить данные об IEO', parsed)

                parsed_list.append(new_ieo)
                continue


            parsed_ieo = parsed['ieo']

            name = parsed_ieo['name']
            logger.info(f'Полученны данные по проекту {name}')
            
            parsed_ieo['success_link_downloaded'] = True

            # Все ок, пишем в db
            parsed_list.append(parsed_ieo)
        else:
            return {
                'success': True,
                'list': parsed_list
            }

        return error
    
    def recheck(self, not_success_list):
        result = []

        recheck = self.get_every(not_success_list)

        success = recheck['success']
        if not success:
            return recheck

        recheck_list = recheck['list']

        for ieo in recheck_list:
            success = ieo['success_link_downloaded']
            if not success:
                continue
            
            result.append(ieo)

        return {
            'success': True,
            'list': result
        }
