from .. import loader, utils
from telethon.tl.types import Message, UserStatusOffline, User
import logging

logger = logging.getLogger(__name__)

@loader.tds
class AutoResponderMod(loader.Module):
    """Автоответчик для HerokuUserBot"""
    
    strings = {
        "name": "AutoResponder",
        "config_message": "Сообщение автоответчика",
        "no_message_set": "⚠️ Сообщение автоответчика не установлено в конфиге!"
    }

    strings_ru = {
        "config_message": "Сообщение автоответчика",
        "no_message_set": "⚠️ Сообщение автоответчика не установлено в конфиге!"
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "auto_message",
                "Я сейчас оффлайн, напишу позже!",
                lambda: self.strings["config_message"],
                validator=loader.validators.String()
            )
        )
        self._replied_chats = set()  # Хранит ID чатов, где автоответчик уже сработал

    async def client_ready(self, client, db):
        self.client = client
        self.db = db

    async def watcher(self, message):
        """Следит за входящими сообщениями в ЛС и отправляет автоответ, если пользователь оффлайн."""
        try:
            if not isinstance(message, Message) or message.out:
                return

            # Проверяем, что сообщение из ЛС (от пользователя, не группы)
            chat = await message.get_chat()
            if not isinstance(chat, User):
                return

            # Проверяем статус пользователя
            user = await self.client.get_me()
            if not isinstance(user.status, UserStatusOffline):
                self._replied_chats.discard(message.chat_id)  # Сбрасываем, если пользователь онлайн
                return

            # Проверяем, не отправляли ли уже автоответ в этот чат
            if message.chat_id in self._replied_chats:
                return

            # Проверяем, задано ли сообщение в конфиге
            if not self.config["auto_message"] or not self.config["auto_message"].strip():
                logger.debug("Сообщение автоответчика не установлено или пустое")
                return

            # Отправляем автоответ
            await utils.answer(message, self.config["auto_message"])
            self._replied_chats.add(message.chat_id)
            logger.debug(f"Автоответ отправлен в чат {message.chat_id}: {self.config['auto_message']}")
        except Exception as e:
            logger.debug(f"Ошибка в watcher: {e}", exc_info=False)
