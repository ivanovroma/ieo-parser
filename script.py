from DB import DB
from Parser import Parser
from Timer import Timer
from Logger import Logger
import helpers
 

def loop():
    logger.start()

    # Сначала попробуем загрузить данные по тем проектам, которые до этого не удалось загрузить
    not_success_list = db.get_not_success()

    logger.recheck(not_success_list)

    update_ieo = parser.recheck(not_success_list)
    
    success = update_ieo['success']
    if not success:
        logger.warning('Не удалось завершить обновление данных', update_ieo)
        return {'success': False}
    update_ieo_list = update_ieo['list']

    logger.update(update_ieo_list)

    db.update_every(update_ieo_list)


    # Получаем список IEO с сайта
    logger.info('Получаю актуальный список IEO')
    parsed = parser.get_list()
    
    success = parsed['success']
    if not success:
        logger.warning('Не удалось загрузить список', parsed)
        return {'success': False}

    parsed_list = parsed['list']
    logger.info(f'Получен актуальный список из {len(parsed_list)} IEO')
    

    # Получаем список IEO из db
    saved_list = db.get_list()

    # Сверяем списки
    new_list = helpers.compare_lists(saved_list, parsed_list)


    # Для каждого нового IEO парсим данные
    logger.info(f'Обнаружено {len(new_list)} новых IEO, получаю данные по ним')
    parsed_every = parser.get_every(new_list)
    
    # Если что то пошло не так, повторим попытку позже
    success = parsed_every['success']
    if not success:
        logger.warning('Не удалось загрузить данные по проектам', parsed_every)
        return {'success': False}
    
    parsed_every_list = parsed_every['list']


    # Записываем полученные данные в db
    db.append_list(parsed_every_list)
    logger.finish(parsed_every_list)

    return {'success': True}


if __name__ == '__main__':
    db = DB()
    parser = Parser()
    timer = Timer()
    logger = Logger()

    while True:
        try:
            result = loop()
            timer.sleep(result)
        except KeyboardInterrupt:
            print('\nПока!')
            break
