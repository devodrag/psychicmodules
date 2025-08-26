from herokutl import TelegramClient, events
import asyncio
from .. import loader, utils

@loader.tds
class MakvinInsult(loader.Module):
    """Модуль для отправки оскорблений с настраиваемой задержкой"""
    
    strings = {
        "name": "InsultBot",
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
            "тут", "нахуй", "все", "зубы", "отобью", "пидорасище", "кулаками", "за",
            "твои", "пропиздоны", "ебанная", "тряпка", "я", "тебе", "говорю", "вытирай",
            "слезы", "и", "показывай", "мне", "противостояние", "ведь", "ты", "ебанная",
            "тварь", "здесь", "будешь", "ловить", "в", "свои", "округлости", "маслянистые",
            "модернизированные", "харчевые", "слезы", "нахуй", "ну", "ты", "девочка",
            "рыдаешь", "не", "вывезешь", "эту", "битву", "тупая", "шалава", "соси",
            "член", "ебанашка", "у", "тя", "мать", "сдохла", "отец", "пьёт", "сестра",
            "сосет", "мне", "член", "а", "брат", "берет", "в", "жопу", "ну", "скажи",
            "еще", "мне", "аргументы", "у", "тя", "их", "нет", "ахаха", "все", "завали",
            "ебало", "шавка", "тупорылая", "ублюдская", "уебанская", "долбаебская",
            "пока", "шалава", "ной", "в", "хуй", "мой", "пж"
        ]

    @loader.command()
    async def makvin(self, message):
        """Отправляет список оскорблений с заданной задержкой"""
        await message.delete()
        for insult in self.insults:
            await message.respond(insult)
            await asyncio.sleep(self.config["delay"])

    @loader.command()
    async def addword(self, message):
        """Добавляет слово в список оскорблений: .addword <слово>"""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, self.strings["no_args"])
            return
        
        word = args.strip()
        if word not in self.insults:
            self.insults.append(word)
            await utils.answer(message, self.strings["word_added"].format(word))
        else:
            await utils.answer(message, f"❌ Слово <b>{word}</b> уже есть в списке!")

    @loader.command()
    async def removeword(self, message):
        """Удаляет слово из списка оскорблений: .removeword <слово>"""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, self.strings["no_args"])
            return
        
        word = args.strip()
        if word in self.insults:
            self.insults.remove(word)
            await utils.answer(message, self.strings["word_removed"].format(word))
        else:
            await utils.answer(message, self.strings["word_not_found"].format(word))
