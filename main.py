import re
from pprint import pprint
# читаем адресную книгу в формате CSV в список contacts_list
import csv
with open("phonebook_raw.csv") as f:
  rows = csv.reader(f, delimiter=",")
  contacts_list = list(rows)

# TODO 1: выполните пункты 1-3 ДЗ
# ваш код
def rewrite():
  pattern_phone = re.compile("(\+?7?|8)( ?)(\(?)([\d]{3})(\)?|\-?)( ?)([\d]{3})(\-?)([\d]{2})(\-?)([\d]{2})( ?)( ?)(\(?)"
                             "([доб]{0,3}\.? ?)([\d]{0,4})")
  result_list = []
  first = True
  for list in contacts_list:
    # первая строка это заголовки, поэтому оставляем без изменений
    if first:
      result_list.append(list)
      first = False
      continue
    # сложим поля ФИО(даже если пустые) и разобъём снова, но уже правильно
    fullname = list[0] + ' ' + list[1] + ' ' + list[2]
    new_name = fullname.split()
    # прогоним номер телефона через RegExp
    phone = re.findall(pattern_phone, list[5])
    new_phone =''
    # и еси что-то осталось(то есть номер есть), то соберем уже по нашему шабону
    if len(phone) > 0:
      new_phone = '+7(' + phone[0][3] + ')' + phone[0][6] + '-' + phone[0][8] + '-' + phone[0][10]
      if len(phone[0][14]) > 0:
        new_phone = new_phone + ' доб.' + phone[0][15]
    pre_list = [new_name[0] if len(new_name) > 0 else '',
                new_name[1] if len(new_name) > 1 else '',
                new_name[2] if len(new_name) > 2 else '',
                list[3], list[4], new_phone, list[6]]
    # а теперь прежде чем записать данные в общий список проверим по ФИ нет ли там уже такого
    for double in result_list:
      if double[0] == pre_list[0] and double[1] == pre_list[1]:
        pre_list[2] = double[2] if len(double[2]) > 0 else pre_list[2]
        pre_list[3] = double[3] if len(double[3]) > 0 else pre_list[3]
        pre_list[4] = double[4] if len(double[4]) > 0 else pre_list[4]
        pre_list[5] = double[5] if len(double[5]) > 0 else pre_list[5]
        pre_list[6] = double[6] if len(double[6]) > 0 else pre_list[6]
        result_list.remove(double)
    # включение результата в общий список
    result_list.append(pre_list)
  return result_list

# TODO 2: сохраните получившиеся данные в другой файл
# код для записи файла в формате CSV
with open("phonebook.csv", "w") as f:
  datawriter = csv.writer(f, delimiter=',')
  # Вместо contacts_list подставьте свой список
  datawriter.writerows(rewrite())