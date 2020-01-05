import logging

logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%d-%b-%y %H:%M:%S')

class Logger:
    def recheck(self, recheck_list):
        recheck_list_len = len(recheck_list)

        if recheck_list_len == 0:
            return
        
        text = f'Пытаюсь повторно получить валидные данные по {recheck_list_len} ieo'

        logging.info(text)
        print(text)

    def warning(self, text, payload):
        message = payload['message']
        subject = payload['subject']
        text = f'{text} - { message } {subject}'

        logging.warning(text)
        print(text)

    def info(self, text):
        logging.info(text)
        print(text)

    def start(self):
        text = 'Новая проверка'

        logging.info(text)
        print(text)

    def update(self, updated_list):
        text = f'Полученны валидные данные по {len(updated_list)} ieo'

        logging.info(text)
        print(text)

    def finish(self, new_ieo_list):
        new_ieo_len = len(new_ieo_list)
        text = f'Проверка закончена. Добавлено {new_ieo_len} ieo'

        logging.info(text)
        print(text)
