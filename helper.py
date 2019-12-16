def compare_lists(saved_list, parsed_list):
    # print('compare', saved_list, parsed_list)
    empty_db = len(saved_list) == 0
    empty_parsed = len(parsed_list) == 0

    if empty_db and not empty_parsed:
        print(f'Обнаружено {str(len(parsed_list))} новых IEO')
        return parsed_list

    new_ieo_list = []

    for parsed_ieo in parsed_list:
        parsed_href = parsed_ieo['href']

        for saved_ieo in saved_list:
            saved_href = saved_ieo['href']

            if saved_href == parsed_href:
                break
        else:
            new_ieo_list.append(parsed_ieo)

    print(f'Обнаружено {str(len(new_ieo_list))} новых IEO')
    return new_ieo_list