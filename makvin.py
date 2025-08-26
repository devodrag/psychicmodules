from herokutl import TelegramClient, events
import asyncio
from .. import loader, utils

@loader.tds
class MakvinInsult(loader.Module):
    """Модуль для отправки оскорблений с настраиваемой задержкой"""
    
    strings = {
        "name": "MakvinInsult",
        "word_added": "✅ Слово <b>{}</b> добавлено в список оскорблений!",
        "word_removed": "✅ Слово <b>{}</b> удалено из списка оскорблений!",
        "word_not_found": "❌ Слово <b>{}</b> не найдено в списке оскорблений!",
        "no_args": "❌ Укажите слово для добавления/удаления!",
        "delay_updated": "✅ Задержка установлена на <b>{}</b> секунд",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "delay",
                0.1,
                "Задержка между сообщениями (в секундах)",
                validator=loader.validators.Float(minimum=0.0, maximum=5.0)
            )
        )

        self.insults = [
            "воспрепятствовать", "мне", "здесь", "ебанная", "шлюха", "нахуй", "я", "тебе",
            "сказал", "убегай", "нахуй", "отсюда", "терпила", "ебанная", "ты", "же",
            "попросту", "здесь", "не", "выживешь", "под", "гнетом", "и", "издевками",
            "падаль", "ебучая", "наислабейшая", "чернейшая", "проституточная", "я", "тебе",
            "тут", "нахуй", "все
