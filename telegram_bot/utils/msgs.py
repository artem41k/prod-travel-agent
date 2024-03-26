skip = 'Пропустить'
stop = 'Стоп'
try_again = '%s\nПопробуйте ещё раз'
i_dont_believe = 'Не верю:)'
internal_error = (
    'Произошла какая-то ошибка😕\n'
    'Попробуйте ещё раз, вдруг повезёт)'
)
max_length_error = try_again % 'Превышена максимальная длина'
not_digits = try_again % 'Сообщение должно состоять только из цифр'

operation_cancelled = 'Действие отменено'

# Start & Registration

start_msg = (
    'Привет!\nЯ - Travel Agent, и я буду помогать вам управлять вашими '
    'путешествиями и строить маршруты\n\n'
    'Для начала, нужно зарегистрироваться)\nПри регистрации вы можете '
    'пропускать некоторые шаги'
)

ask_for_name = (
    'Укажите ваше имя\n<code>Вы можете пропустить этот шаг, '
    'тогда мы возьмём имя, которое у вас указано в Telegram</code>'
)

ask_for_age = (
    'Супер! Теперь укажите ваш возраст (только цифры)\n'
    '<code>Вы можете пропустить этот шаг</code>'
)

age_parse_error = (
    try_again %
    'Неправильно указан возраст. Убедитесь что вы вводите только цифры'
)

location_format = '[Город], [Страна]'

ask_for_location = (
    'Отлично! Теперь укажите, где вы живёте '
    '(из какого планируете начинать путешествия)\n'
    f'Формат: <b>{location_format}</b>\n'
    '<code>Вы можете поделиться своей геолокацией, '
    'а я попробую определить ваш город и страну</code>'
)

wrong_location = try_again % (
    'Неправильно написаны город и страна, '
    f'убедитесь что вы написали в формате <b>{location_format}</b>'
)

ask_for_bio = (
    'Теперь вы можете рассказать немного о себе, если хотите'
)

hello_again = 'Здравствуйте снова, %s!'

# Profile

profile_button = 'Профиль👤'
profile_is_ready = 'Поздравляю, ваш профиль готов!'
profile_msg_header = '<b>👤Ваш профиль</b>'

profile_labels = {
    'name': 'Имя',
    'age': 'Возраст',
    'location': 'Местоположение',
    'bio': 'О себе',
}


def construct_profile_props_msg(**kwargs) -> str:
    msg = '\n'
    for prop, label in profile_labels.items():
        if value := kwargs.get(prop):
            msg += f'\n<b>{label}</b>: {value}'
    return msg


def get_profile_msg(**kwargs) -> str:
    return profile_msg_header + construct_profile_props_msg(**kwargs)


# Main menu
menu_button_text = 'В главное меню🏠'
main_menu_text = '<b>Главное меню</b>'

# Trips

trips_button = 'Путешествия💼🌴'
add_trip_button = 'Добавить путешествие🆕'
add_locations_button = 'Добавить локации📍'
edit_locations_button = 'Изменить локации📍'
edit_trip_name_button = 'Изменить название'
edit_trip_description_button = 'Изменить описание'
add_button = 'Добавить🆕'
change_order_button = 'Изменить порядок🔁'
delete_some_button = 'Удалить некоторые❌'
edit_trip_button = 'Редактировать📝'
delete_trip_button = 'Удалить путешествие❌'
route_button = 'Маршрут🗺'
share_location_button = 'Поделиться местоположением📍'
soonest_trip_button = 'Ближайшая поездка🔜'

show_trip = 'Открыть путешествие'

trips_header = '<b>Ваши путешествия</b>'

create_trip = (
    'Давайте создадим путешествие!\n'
    'Для начала напишите имя путешествия\n'
    '<code>Не более 64 символов</code>'
)
ask_for_description = 'Теперь вы можете добавить описание'
trip_created = 'Отлично, путешествие создано!'

locations_title = 'Локации:\n'
location_string = '<b>📍%s</b>\n<i>%s - %s</i>\n'


def construct_locations(
        locations: list, limit: int | None = None, enum: bool = False) -> str:
    msg = ''
    for index, location in enumerate(locations):
        if enum:
            msg += f'{index+1}. '
        msg += location_string % (
            location['name'], location['start_date'], location['end_date']
        )
        if limit:
            if index + 1 == limit:
                break
    return msg


def get_trip_msg(trip: dict) -> str:
    msg = f"<b>{trip['name']}</b>\n"
    if desc := trip.get('description'):
        msg += desc + '\n\n'
    start_date = trip.get('start_date')
    end_date = trip.get('end_date')
    if start_date and end_date:
        msg += f'<i>{start_date} - {end_date}</i>\n\n'

    if locations := trip.get('locations'):
        msg += locations_title + construct_locations(locations, limit=5)

    return msg


# Locations

add_location_format = (
    '<b>[Название города]<code>, [Название страны]</code>\n'
    '[ДД.ММ.ГГ] - [ДД.ММ.ГГ]</b>'
)

add_location_msg = (
    'Давайте добавим локации!\nПишите их в формате\n'
    f'{add_location_format}\n'
    '<code>Даты начала и конца посещения обязательно с новой строки</code>\n'
    '1 локация - 1 сообщение\nКогда захотите остановиться, '
    f'нажмите кнопку "{stop}" внизу экрана или напишите это слово вручную'
)

wrong_add_location = try_again % (
    'Неправильно написана локация\nУбедитесь, что вы строго следуете формату\n'
    f'{add_location_format}'
)

location_not_found = try_again % (
    'Локация не найдена\nПроверьте, правильно ли вы написали название города'
)

location_added = (
    '<b>Локация <i>%s</i> добавлена✅</b>\n'
    f'Добавьте ещё, или нажмите "{stop}"'
)

added_num_locations = '<b>Добавлено %d локаций✅</b>'

choose_action = 'Выберите, что вы хотите сделать:'
choose_what_to_edit = 'Выберите, что вы хотите изменить:'


def get_locations_msg(
        trip_name: str, locations: list, action: str = '') -> str:
    locations_msg = construct_locations(locations, enum=True)
    return f'{trip_name}\n\n{locations_msg}\n{action}'


delete_locations_text = (
    'Напишите номера локаций из списка, '
    'которые хотите удалить, без запятых и пробелов\n'
    'Например: <code>1234</code>'
)

successfully_deleted_label = '<b>Успешно удалены локации:</b>'
werent_in_list_label = '<b>Номера локаций, которых не было в списке:</b>'


def deleted_locations_msg(successful: list, werent_in_list: list) -> str:
    msg = ''
    if len(successful) > 0:
        msg += successfully_deleted_label
        for loc in successful:
            msg += f'\n<i>{loc["name"]}</i>'
    if len(werent_in_list) > 0:
        msg += werent_in_list_label
        for num in werent_in_list:
            msg += f'\n{num}'
    return msg


drive_by_car = '<b>🚗Маршрут на машине</b>\nОбщий путь: <code>%s км</code>'

sad_2004_error = (
    'Бесплатная версия API, которую я использую для построения '
    'маршрутов не даёт построить маршрут, который хотя бы приблизительно '
    'превышает 6000 км :(\nПопробуйте удалить самую дальнюю локацию, '
    'тогда всё должно построиться)'
)

trip_successfully_deleted = 'Путешествие %s удалено❌'


trip_edit_name = (
    'Напишите новое имя путешествия\n'
    '<code>Не более 64 символов</code>'
)
trip_edit_description = 'Напишите новое описание:'
name_edited = 'Имя изменено✅'
description_edited = 'Описание изменено✅'

# Profile
ask_for_edit_age = 'Укажите ваш возраст (только цифры)'

location_edited = 'Местоположение изменено✅'
age_edited = 'Возраст именён✅'
bio_edited = '"О себе" изменено✅'

are_you_sure_delete_trip = (
    '<b>Вы уверены что хотите удалить поездку <i>%s</i>?</b>'
)
sure = 'Да'
cancel = 'Отменить'
