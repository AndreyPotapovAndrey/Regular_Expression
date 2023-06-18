from pprint import pprint
# читаем адресную книгу в формате CSV в список contacts_list
import csv
import re

PATTERN = r"(\+7|8)*[\s\(]*(\d{3})[\)\s-]*(\d{3})[-]*(\d{2})[-]*(\d{2})([\s\(])*(доб\.)*([\s])*(\d+)*([\)])*"
SUBST_PATTERN = r"+7 (\2) \3-\4-\5 \7\9"


def correct_phone(contact_string):
    return re.sub(PATTERN, SUBST_PATTERN, contact_string)


if __name__ == '__main__':

    with open("phonebook_raw.csv", encoding='utf-8') as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)

    contacts_list_new = list()
    final_list = list()
    for contacts in contacts_list:
        # Здесь мы берем первые 3 элемента списка(где находится ФИО)
        # соединяем в строку, потом делим на список
        fio_list = ' '.join(contacts[0:3]).split()
        # print(fio_list)
        # Чтобы размер соответствовал начальной длине списка(3 эл), в случае только имени
        # и фамилии, добавляем пустое поле, чтобы размер всей записи не поменялся
        if len(fio_list) != 3:
            fio_list.append('')
            # print(fio_list)
        # склеиваем новую правильную запись
        full_fio_list = fio_list + contacts[3:]
        # print(full_fio_list)

        contact_string = ','.join(full_fio_list)

        contact = correct_phone(contact_string).split(',')
        for contact_in_final_list in final_list:
            #         # если ФИ из текущего контакта совпадает с одним из значений в финальном списке
            if contact_in_final_list[:1] == contact[:1]:
                # удаляем запись из финального списк, чтобы не задваивались
                final_list.remove(contact_in_final_list)
                # складываем из двух записей одну
                contact = [x if x != "" else y for x, y in zip(contact_in_final_list, contact)]
        # если записи нет в финальном списке записываем ее, если была, то записываем составную запись
        final_list.append(contact)
    pprint(final_list)
    # 2. Сохраните получившиеся данные в другой файл.
    # Код для записи файла в формате CSV:
    with open("phonebook.csv", "w") as f:
        datawriter = csv.writer(f, delimiter=',')

        # Вместо contacts_list подставьте свой список:
        datawriter.writerows(final_list)
