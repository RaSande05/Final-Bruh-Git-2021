from aiogram.utils.markdown import hlink
from aiogram import Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils import executor
import os
from admin_states import Cases
from sql_command_execution import sql_command
from routing import routs_for_every_truck
import ast
from aiogram.utils.exceptions import BotBlocked, ChatNotFound, RetryAfter

# Создаем Админ-бота
bot = Bot(token='5086616394:AAEDlK13PmMC07dRMHLZH5isYqcVgBfYKD0')
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())

# Создаем бота для рассылки водителям
bot_send_rout_to_driver = Bot(token='5074289027:AAE0yMryVaA2ngwAX8FumIUn9PZ0xenIQzo')

# Список id Администраторов
ADMINS_ID = [383367365]
path_main_db = os.path.join(os.path.expanduser('~'), 'Track_solver', 'src', 'main_data.db')

# Создаем бд если ее нет
sql_command("""CREATE TABLE IF NOT EXISTS main_users_data(
"track_id" INT PRIMARY KEY,
"userid_telegram" INT,
"rout" TEXT);""")

# Добавляем кнопки
inline_btn_add_driver = InlineKeyboardButton('Добваить водителя', callback_data='button_add_driver')
inline_btn_delete_driver = InlineKeyboardButton('Удалить водителя', callback_data='button_delete_driver')
inline_btn_back_to_main = InlineKeyboardButton('Назад', callback_data='button_back_to_main')
inline_settings_kb = InlineKeyboardMarkup().add(inline_btn_add_driver, inline_btn_delete_driver,
                                                inline_btn_back_to_main)

inline_btn_main_settings = InlineKeyboardButton('Настройки', callback_data='button_driver_settings')
inline_btn_driver_rout_info = InlineKeyboardButton('Информация о маршруте', callback_data='btn_rout_info')
inline_btn_send_routs = InlineKeyboardButton('Разослать маршруты', callback_data='btn_send_routs')
inline_main_kb = InlineKeyboardMarkup().add(inline_btn_driver_rout_info, inline_btn_send_routs,
                                            inline_btn_main_settings)


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    """
    Функция запуска бота
    """
    admin_id = message.chat.id
    if admin_id in ADMINS_ID:
        await bot.send_message(chat_id=admin_id,
                               text="Готов к работе", reply_markup=inline_main_kb)
    else:
        pass


@dp.callback_query_handler(lambda c: c.data == 'button_driver_settings')
async def process_callback_button_driver_settings(callback_query: types.CallbackQuery):
    """
    Поведение при нажатии кнопки настроек
    """
    await bot.edit_message_text(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id,
                                text='Настройки',
                                reply_markup=inline_settings_kb)
    await bot.answer_callback_query(callback_query.id)


@dp.callback_query_handler(lambda c: c.data == 'button_back_to_main')
async def process_callback_button_back_to_main(callback_query: types.CallbackQuery):
    """
    Поведение при нажатии кнопки назад
    """
    await bot.edit_message_text(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id,
                                text='Готов к работе',
                                reply_markup=inline_main_kb)
    await bot.answer_callback_query(callback_query.id)


@dp.callback_query_handler(lambda c: c.data == 'btn_rout_info')
async def process_callback_button_rout_info(callback_query: types.CallbackQuery):
    """
    Поведение при нажатии кнопки Информация о маршруте
    """
    await bot.edit_message_text(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id,
                                text='Напишите id грузовика чтобы получить информацию о его маршруте')
    await bot.answer_callback_query(callback_query.id)
    await Cases.STATE_CARS_INFO.set()


@dp.message_handler(state=Cases.STATE_CARS_INFO)
async def cars_info(message: types.Message, state: FSMContext):
    """
    Функция принимает сообщение об id машины и возвращает ее маршрут
    """
    id_text = message.text
    admin_id = message.chat.id
    if admin_id in ADMINS_ID:
        if id_text.isdigit():
            rout = sql_command("""SELECT rout FROM main_users_data WHERE track_id = ?;""",
                               params=(int(id_text),), data_base_name='main_data.db')
            loc = preprocess_data(rout)
            if loc == -1:
                await message.reply("Ошибка ввода, попробуйте еще раз\n\nНет такого грузовика")
            else:
                payload = {int(id_text): {
                    'depot': loc[0],
                    'locations': loc[1::],
                    'vehicle': {'id': 0},
                    'options': {'time_zone': 3}
                }}
                txt = routs_for_every_truck(payload)
                await state.reset_state()
                await bot.send_message(chat_id=message.chat.id, text=hlink('Ссылка на маршрут', txt[int(id_text)]),
                                       parse_mode=types.ParseMode.HTML)
                await bot.send_message(chat_id=admin_id,
                                       text="Готов к работе", reply_markup=inline_main_kb)
        else:
            await message.reply("Ошибка ввода, попробуйте еще раз")
    else:
        pass


@dp.callback_query_handler(lambda c: c.data == 'btn_send_routs')
async def process_callback_button_send_routs(callback_query: types.CallbackQuery):
    """
    Поведение при нажатии кнопки Разослать маршруты
    """
    await bot.edit_message_text(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id,
                                text='Маршруты отправляются...')
    await send_routs()
    await bot.send_message(chat_id=callback_query.from_user.id, text='Готово')
    await bot.send_message(chat_id=callback_query.from_user.id,
                           text="Готов к работе", reply_markup=inline_main_kb)


def preprocess_data(data):
    """
    Преобразование данных из БД в нужный вид
    :param data: Строка с информацией о точках остоновки по маршруту
    :return: Нужный вид этих данных
    """
    locations = []
    try:
        for indx, js in enumerate(data[0][0].split(';')):
            locations.append({'id': indx + 1, 'time_window': '00:00-23:59', 'point': ast.literal_eval(js)})
    except IndexError:
        return -1
    return locations


async def send_routs():
    """
    Функция рассылает информацию о маршрутах для каждого водителя
    """
    id_drivers = sql_command("""SELECT userid_telegram FROM main_users_data;""", data_base_name='main_data.db')
    for id_driver in id_drivers:
        try:
            rt = sql_command("""SELECT rout FROM main_users_data WHERE userid_telegram = ?;""",
                             params=(int(id_driver[0]),), data_base_name='main_data.db')
            tr_id = sql_command("""SELECT track_id FROM main_users_data WHERE userid_telegram = ?;""",
                                params=(int(id_driver[0]),), data_base_name='main_data.db')
            loc = preprocess_data(rt)
            if loc == -1:
                pass
            else:
                payload = {tr_id[0]: {
                    'depot': loc[0],
                    'locations': loc[1::],
                    'vehicle': {'id': 0},
                    'options': {'time_zone': 3}
                }}
                txt = routs_for_every_truck(payload)
                await bot_send_rout_to_driver.send_message(chat_id=id_driver[0],
                                                           text=hlink('Ссылка на маршрут', txt[tr_id[0]]),
                                                           parse_mode=types.ParseMode.HTML)
        except (BotBlocked, ChatNotFound, RetryAfter, KeyError) as err:
            print(err)


if __name__ == '__main__':
    # Запускаем чтение сообщений от пользователей
    executor.start_polling(dp)
