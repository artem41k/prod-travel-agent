skip = 'Пропустить'
stop = 'Стоп'
try_again = '%s\nПопробуйте ещё раз'
i_dont_believe = 'Не верю:)'
internal_error = (
    'Произошла какая-то ошибка😕\n'
    'Попробуйте ещё раз, вдруг повезёт)'
)
max_length_error = try_again % 'Превышена максимальная длина'

# Start & Registration

start_msg = (
    'Привет!\nЯ - Travel Agent, и я буду помогать вам управлять вашими '
    'путешествиями, строить маршруты и добавлять к ним заметки\n\n'
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
add_button = 'Добавить🆕'
change_order_button = 'Изменить порядок🔁'
delete_some_button = 'Удалить некоторые❌'
edit_trip_button = 'Редактировать📝'
delete_trip_button = 'Удалить путешествие❌'

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


def get_locations_msg(locations: list) -> str:
    return construct_locations(locations, enum=True) + '\n' + choose_action
