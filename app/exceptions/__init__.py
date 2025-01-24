from __future__ import annotations

from .base import BaseAiogramBotTemplateError, DetailedAiogramBotTemplateError
from .keyboard_utils import (
    NotEnoughArgsToCreateButtonError,
    PaymentButtonMustBeFirstError,
    TooManyArgsToCreateButtonError,
    UnknownKeyboardButtonPropertyError,
    WrongKeyboardSchemaError,
)

__all__ = [
    "BaseAiogramBotTemplateError",
    "DetailedAiogramBotTemplateError",
    "NotEnoughArgsToCreateButtonError",
    "PaymentButtonMustBeFirstError",
    "TooManyArgsToCreateButtonError",
    "UnknownKeyboardButtonPropertyError",
    "WrongKeyboardSchemaError",
]
