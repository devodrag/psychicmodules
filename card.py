from .. import loader, utils
import asyncio

@loader.tds
class AutoCardPhoneGet(loader.Module):
    """Модуль для автоматической отправки 'ткарточка' в чат каждые 3 часа"""

    strings = {
        "name": "AutoCardPhoneGet",
        "status": "Модуль отправляет 'ткарточка' в чат phonegettalk каждые 3 часа."
    }

    async def client_ready(self, client, db):
        """Инициализация модуля при старте клиента"""
        self.client = client
        self.chat_id = -1002735741409  # ID чата
        asyncio.create_task(self.auto_send())

    async def auto_send(self):
        """Отправляет сообщение 'ткарточка' каждые 3 часа"""
        while True:
            try:
                await self.client.send_message(self.chat_id, "ткарточка")
                await asyncio.sleep(3 * 60 * 60)  # Ожидание 3 часов (10800 секунд)
            except Exception as e:
                print(f"AutoCardPhoneGet: Ошибка при отправке: {e}")
                await asyncio.sleep(60)  # Пауза 1 минута при ошибке

    @loader.command()
    async def cardstatus(self, message):
        """Проверяет статус модуля"""
        await utils.answer(message, self.strings["status"])