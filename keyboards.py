from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

############################## START BTNS ################################
settings_btn = InlineKeyboardButton('🛠 Добавить/Изменить свои данные', callback_data='settings_btn')
messages_btn = InlineKeyboardButton('✉️ Отправить сообщение адресату', callback_data='messages_btn')
info_btn = InlineKeyboardButton('📊 Получить информацию', callback_data='info_btn')
help_btn = InlineKeyboardButton('❓ Помощь', callback_data='help_btn')
meet_btn_markup = InlineKeyboardMarkup().add(settings_btn).add(messages_btn).add(info_btn).add(help_btn)

home_btn = InlineKeyboardButton('⏪ В начало', callback_data='home_btn')

cancel_btn = InlineKeyboardButton('❌ Отменить ввод', callback_data='home_btn')
home_btn_markup = InlineKeyboardMarkup().add(cancel_btn)

cancel_dialog = InlineKeyboardButton('❌ Остановить пересылку сообщений', callback_data='cancel_dialog')
cancel_btn_markup = InlineKeyboardMarkup().add(cancel_dialog)

anonym_btn = InlineKeyboardButton('🕶 Отправить анонимно', callback_data='anonym_btn')
direct_btn = InlineKeyboardButton('👓 Переслать от моего имени', callback_data='direct_btn')
message_btn_markup = InlineKeyboardMarkup().add(anonym_btn).add(direct_btn).add(cancel_dialog)

############################## SETTINGS BTNS ################################
mm_settings_btn = InlineKeyboardButton('🅿️ Добавить/Изменить машиноместа', callback_data='mm_settings_btn')
auto_settings_btn = InlineKeyboardButton('🚗 Добавить/Изменить автомобили', callback_data='auto_settings_btn')
my_settings_btn = InlineKeyboardButton('☎️ Добавить/Изменить свои контакты', callback_data='my_settings_btn')
settings_btn_markup = InlineKeyboardMarkup().add(mm_settings_btn).add(auto_settings_btn).add(my_settings_btn).add(home_btn)

add_phon_btn = InlineKeyboardButton('☎️ Добавить номер телефона', callback_data='add_phon_btn')
del_phon_btn = InlineKeyboardButton('❗️ Удалить номер телефона', callback_data='del_phon_btn')
my_info_btn_markup = InlineKeyboardMarkup().add(add_phon_btn).add(del_phon_btn).add(home_btn)

add_mm_btn = InlineKeyboardButton('🅿️ Добавить машиноместо', callback_data='add_mm_btn')
del_mm_btn = InlineKeyboardButton('⛔️ Удалить машиноместо', callback_data='del_mm_btn')
mm_info_btn_markup = InlineKeyboardMarkup().add(add_mm_btn).add(del_mm_btn).add(home_btn)

add_auto_btn = InlineKeyboardButton('🚗 Добавить номер автомобиля', callback_data='add_auto_btn')
del_auto_btn = InlineKeyboardButton('🚶 Удалить номер автомобиля', callback_data='del_auto_btn')
auto_info_btn_markup = InlineKeyboardMarkup().add(add_auto_btn).add(del_auto_btn).add(home_btn)

############################## MESSAGES BTNS ################################
mm_message_btn = InlineKeyboardButton('🅿️ По номеру машиноместа', callback_data='mm_message_btn')
auto_message_btn = InlineKeyboardButton('🚗 По номеру автомобили', callback_data='auto_message_btn')
phone_message_btn = InlineKeyboardButton('☎️ По номеру телефона', callback_data='phone_message_btn')
messages_types_btn_markup = InlineKeyboardMarkup().add(mm_message_btn).add(auto_message_btn).add(phone_message_btn).add(home_btn)









info_request = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton('Отправить авто в базу бота?', request_contact=True)
).add(
    KeyboardButton('Отправить свою локацию 🗺️', request_location=True)
)


button1 = KeyboardButton('1️⃣')
button2 = KeyboardButton('2️⃣')
button3 = KeyboardButton('3️⃣')

markup3 = ReplyKeyboardMarkup().add(
    button1).add(button2).add(button3)

markup4 = ReplyKeyboardMarkup().row(
    button1, button2, button3
)

markup5 = ReplyKeyboardMarkup().row(
    button1, button2, button3
).add(KeyboardButton('Средний ряд'))

button4 = KeyboardButton('4️⃣')
button5 = KeyboardButton('5️⃣')
button6 = KeyboardButton('6️⃣')
markup5.row(button4, button5)
markup5.insert(button6)

markup_request = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton('Отправить свой контакт ☎️', request_contact=True)
).add(
    KeyboardButton('Отправить свою локацию 🗺️', request_location=True)
)

markup_big = ReplyKeyboardMarkup()

markup_big.add(
    button1, button2, button3, button4, button5, button6
)
markup_big.row(
    button1, button2, button3, button4, button5, button6
)

markup_big.row(button4, button2)
markup_big.add(button3, button2)
markup_big.insert(button1)
markup_big.insert(button6)
markup_big.insert(KeyboardButton('9️⃣'))


inline_btn_1 = InlineKeyboardButton('Первая кнопка!', callback_data='button1')
inline_kb1 = InlineKeyboardMarkup().add(inline_btn_1)

inline_kb_full = InlineKeyboardMarkup(row_width=2).add(inline_btn_1)
inline_kb_full.add(InlineKeyboardButton('Вторая кнопка', callback_data='btn2'))
inline_btn_3 = InlineKeyboardButton('кнопка 3', callback_data='btn3')
inline_btn_4 = InlineKeyboardButton('кнопка 4', callback_data='btn4')
inline_btn_5 = InlineKeyboardButton('кнопка 5', callback_data='btn5')
inline_kb_full.add(inline_btn_3, inline_btn_4, inline_btn_5)
inline_kb_full.row(inline_btn_3, inline_btn_4, inline_btn_5)
inline_kb_full.insert(InlineKeyboardButton("query=''", switch_inline_query=''))
inline_kb_full.insert(InlineKeyboardButton("query='qwerty'", switch_inline_query='qwerty'))
inline_kb_full.insert(InlineKeyboardButton("Inline в этом же чате", switch_inline_query_current_chat='wasd'))
inline_kb_full.add(InlineKeyboardButton('Уроки aiogram', url='https://surik00.gitbooks.io/aiogram-lessons/content/'))