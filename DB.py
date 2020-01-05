import json

class DB:
    def __write(self, new_list):
        with open('db.json', 'w') as file:
            json.dump(new_list, file, indent=2)

    def get_not_success(self):
        saved_list = self.get_list()
        not_success_list = []

        for ieo in saved_list:
            success = ieo['success_link_downloaded']

            if not success:
                not_success_list.append(ieo)

        return not_success_list

    def get_list(self):
        try:
            with open('db.json') as file:
                data = json.load(file)
            return data
        except:
            return []
        

    def append_list(self, append_ieo_list):
        saved_list = self.get_list()
        new_ieo_list = append_ieo_list + saved_list

        self.__write(new_ieo_list)

    def update_every(self, update_list):
        saved_list = self.get_list()

        for update_ieo in update_list:
            update_ieo_href = update_ieo['href']

            for saved_ieo in saved_list:
                saved_ieo_href = saved_ieo['href']

                if update_ieo_href == saved_ieo_href:
                    saved_ieo['success_link_downloaded'] = True
                    saved_ieo['links'] = update_ieo['links']

        self.__write(saved_list)
