import parser
import db
import helper
import datetime
import time

def loop():
    # Получаем список IEO с сайта
    parsed_list = parser.get_list()
    
    # Если что то пошло не так, повторим попытку через 120 секунд
    success = parsed_list['success']
    if not success:
        set_timer(120)
        return
    
    # Получаем список IEO из db
    saved_list = db.get_list()
    parsed_list = parsed_list['list']

    # Проверяем наличие новых IEO
    new_ieo_list = helper.compare_lists(saved_list, parsed_list)

    # Для каждого нового IEO парсим социалки
    for new_ieo in new_ieo_list:
        parsed_ieo = parser.get_one(new_ieo)

        # Если что то пошло не так, помечаем IEO как не валидный
        success = parsed_ieo['success']
        if not success:
            new_ieo['status'] = parsed_ieo['message']
            db.write_one(new_ieo)
            continue

        # Все ок, пишем в db
        db.write_one(parsed_ieo['ieo'])
    else:
        print(f'Добавил в db {str(len(new_ieo_list))} проектов')
        good_bay()

def set_timer(timer, hours=0, minutes=0):
    if (hours and minutes):
        print(f'Следующая проверка через {hours}ч. {minutes}м.')
    else:
        print(f'Отложим на {timer} секунд')
        
    time.sleep(timer)

    print('Пробуем снова')
    loop()

def good_bay():
    now = datetime.datetime.now()
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    
    wake_up_time = datetime.datetime(tomorrow.year, tomorrow.month, tomorrow.day, 0, 0)

    delta = wake_up_time - now
    seconds = delta.seconds
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60

    set_timer(seconds, hours, minutes)

if __name__ == '__main__':
    loop()
