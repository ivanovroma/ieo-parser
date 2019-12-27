import parser
import db
import helper
import datetime
import time
import logging
 

def loop():
    # Получаем список IEO с сайта
    parsed = parser.get_list()
    
    # Если что то пошло не так, повторим попытку через 120 секунд
    success = parsed['success']
    if not success:
        return parsed
    
    parsed_list = parsed['list']
    
    # Получаем список IEO из db
    saved_list = db.get_list()

    # Проверяем наличие новых IEO
    new_ieo_list = helper.compare_lists(saved_list, parsed_list)

    error = {
        'success': False,
        'message': '',
        'subject': ''
    }

    # Для каждого нового IEO парсим социалки
    for new_ieo in new_ieo_list:
        parsed_ieo = parser.get_one(new_ieo)

        # Если что то пошло не так, то добавим ieo без ссылок
        success = parsed_ieo['success']
        if not success:
            message = parsed_ieo.get('message')
            subject = parsed_ieo.get('subject')

            logging.warning(f'{message} - {subject}')

            # Если не удалось загрузить страницу, повторим попытку через 120 секунд
            if (message == 'get_html_fail'):
                error['message'] = message
                error['subject'] = subject
                break

            db.write_one(new_ieo)
            continue

        # Все ок, пишем в db
        db.write_one(parsed_ieo['ieo'])
    else:
        added = len(new_ieo_list) > 0

        if added:
            print(f'Добавил в db {str(len(new_ieo_list))} проектов')

        return {'success': True}

    return error

def getNextCheckTime():
    now = datetime.datetime.now()
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    wake_up_time = datetime.datetime(tomorrow.year, tomorrow.month, tomorrow.day, 0, 0)
    delta = wake_up_time - now

    timer = delta.seconds

    hours = timer // 3600
    minutes = (timer % 3600) // 60
    seconds = timer - (hours * 3600) - (minutes * 60)

    print(f'Следующая проверка через {hours}ч. {minutes}м. {seconds}с.')

    return timer

if __name__ == '__main__':
    logging.basicConfig(filename='warnings.log', filemode='w', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

    while True:
        try:
            result = loop()

            success = result.get('success')
            if success:
                print('Проверка прошла успешно.')
                timer = getNextCheckTime()
                
                time.sleep(timer)
            else:
                minuts = 2
                message = result.get('message')
                
                logging.warning(f'{message}')
                print(f'Что-то пошло не так, следущая попытка через {minuts}м.')
                
                time.sleep(minuts * 60)
        except KeyboardInterrupt:
            print('\nПока!')
            break
