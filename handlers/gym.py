import logging

from aiogram import Router
from aiogram.fsm.state import StatesGroup, State

logger = logging.getLogger(__name__)
router = Router(name="gym")


class GymStates(StatesGroup):
    choice = State()