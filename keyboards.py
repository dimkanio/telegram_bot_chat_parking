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

anonym_btn = InlineKeyboardButton('🕶 Отправить \nанонимно', callback_data='anonym_btn')
direct_btn = InlineKeyboardButton('👓 Переслать \nот моего имени', callback_data='direct_btn')
message_btn_markup = InlineKeyboardMarkup().add(anonym_btn).add(direct_btn).add(cancel_dialog)

cancel_direct_dialog = InlineKeyboardButton('❌ Не отвечать', callback_data='cancel_dialog')
reply_anon_btn = InlineKeyboardButton('🕶 Ответить \nанонимно', callback_data='reply_anonym_btn')
reply_direct_btn = InlineKeyboardButton('👓 Ответить', callback_data='reply_direct_btn')

message_direct_dialog_btn_markup = InlineKeyboardMarkup().add(reply_direct_btn, reply_anon_btn, cancel_direct_dialog)
#message_direct_dialog_btn_markup.row(reply_direct_btn, reply_anon_btn, cancel_direct_dialog)

message_anon_dialog_btn_markup = InlineKeyboardMarkup().add(reply_anon_btn, reply_direct_btn, cancel_direct_dialog)
#message_anon_dialog_btn_markup.row(reply_anon_btn, reply_direct_btn, cancel_direct_dialog)

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

############################ INFO ############################################
common_counts = InlineKeyboardButton('📈 Общие счетчики', callback_data='common_cntrs_btn')
common_draw = InlineKeyboardButton('🗺 Карта паркинга', callback_data='common_map_btn')
common_btn_markup = InlineKeyboardMarkup().add(common_counts).add(common_draw).add(home_btn)
