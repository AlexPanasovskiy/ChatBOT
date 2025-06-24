import generation as gen

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart


router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Привет!')

@router.message()
async def handle_message(message: Message):
    question = message.text
    answer = gen.generate_answer(question)
    await message.answer(answer)