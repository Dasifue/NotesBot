"Основной выполняемый модуль"

import os
import asyncio

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from database import Base, Note, session, engine, utils

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "bot token")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


class NoteStates(StatesGroup):
    "Notes FSM"
    title = State()
    content = State()


@dp.message(Command("start"))
async def start(message: Message) -> None:
    "Функция приветствует пользователя и возвращает клавиатуру"
    text = f"Hello, {message.from_user.username}!"  # type: ignore
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Добавить заметку", callback_data="add_note")],
        [InlineKeyboardButton(text="Мои заметки", callback_data="my_notes")]
    ])
    await message.answer(text=text, reply_markup=markup)


@dp.callback_query(lambda call: call.data == "my_notes")
async def get_notes(call: CallbackQuery) -> None:
    "Функция отправляет пользователю его заметки"
    notes = await utils.select_many(session, owner_id=call.message.chat.id) # type: ignore
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=note.title, callback_data=f"note_id:{note.id}")]
        for note in notes
    ])
    text = "Ваши заметки"
    await call.message.answer(text=text, reply_markup=markup)  # type: ignore


@dp.callback_query(lambda call: call.data.startswith("note_id:"))
async def get_note(call: CallbackQuery) -> None:
    "Функция отправляет пользователю конкретную заметку"
    note_id=int(call.data[8:])  # type: ignore
    note = await utils.select_one(session, note_id=note_id)  # type: ignore
    markup = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="Удалить", callback_data=f"delete:{note_id}")
    ]])
    await call.message.answer(text=f"{note.title}\n{note.content}\n{note.created}", reply_markup=markup)  # type: ignore


@dp.callback_query(lambda call: call.data.startswith("delete:"))
async def delete_note(call: CallbackQuery) -> None:
    "Функция удаляет заметки"
    note_id=int(call.data[7:])  # type: ignore
    await utils.delete(session, note_id=note_id)
    await call.message.edit_text(text="Удалено!")  # type: ignore


@dp.callback_query(lambda call: call.data == "add_note")
async def pre_create_note(call: CallbackQuery, state: FSMContext) -> None:
    "Функция запускает машину состояний"
    await state.set_state(NoteStates.title)
    await call.message.answer(text="Введите название заметки")  # type: ignore


@dp.message(NoteStates.title)
async def set_title(message: Message, state: FSMContext) -> None:
    "Функция сохраняет название заметки и переходит к следующей стадии"
    await state.update_data(title=message.text, owner_id=message.from_user.id)  # type: ignore
    await state.set_state(NoteStates.content)
    await message.answer(text="Хорошо! Теперь отправьте содержимое заметки")


@dp.message(NoteStates.content)
async def set_content(message: Message, state: FSMContext) -> None:
    "Функция сохраняет текст заметки"
    await state.update_data(content=message.text)

    await utils.insert_obj(
        async_session=session,
        obj=Note(**(await state.get_data()))
    )

    await state.clear()
    await message.answer(text="Отлично! Заметка сохранена")


async def main() -> None:
    "Функция создаёт таблицы в бд и запускает проект"
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
