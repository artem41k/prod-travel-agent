skip = 'Пропустить'
try_again = '%s\nПопробуйте ещё раз'
i_dont_believe = 'Не верю:)'

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
