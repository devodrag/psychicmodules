from .. import loader, utils
import aiohttp
from bs4 import BeautifulSoup

@loader.tds
class RandomWords(loader.Module):
    """Модуль для получения случайных английских слов и их перевода на русский через MyMemory с резервным парсингом Google Переводчика"""

    strings = {
        "name": "RandomWords",
        "no_word": "⚠️ Не удалось получить слово или перевод!",
        "loading": "⏳ Получаю слово...",
        "translation_error": "⚠️ Ошибка перевода через MyMemory: {}. Пытаюсь через Google Переводчик...",
        "google_translation_error": "⚠️ Ошибка парсинга Google Переводчика: {}",
        "word_fetch_error": "⚠️ Ошибка при получении слова: {}"
    }

    async def get_random_word(self):
        """Получает случайное слово и его перевод через MyMemory с резервным парсингом Google Переводчика"""
        async with aiohttp.ClientSession() as session:
            try:
                # Получаем случайное слово с randomword.com
                async with session.get("https://randomword.com/") as response:
                    if response.status != 200:
                        return None, None, self.strings["word_fetch_error"].format("HTTP " + str(response.status))
                    text = await response.text()
                    start = text.find('id="random_word">') + len('id="random_word">')
                    end = text.find('</div>', start)
                    word = text[start:end].strip()

                if not word:
                    return None, None, self.strings["word_fetch_error"].format("Слово не найдено на странице")

                # Пытаемся получить перевод с MyMemory
                translation = None
                try:
                    async with session.get(
                        f"https://api.mymemory.translated.net/get?q={word}&langpair=en|ru"
                    ) as response:
                        if response.status == 200:
                            data = await response.json()
                            translation = (
                                data.get("responseData", {}).get("translatedText", "Перевод не найден")
                                or "Перевод не найден"
                            )
                            if translation.lower() == word.lower() or not translation:
                                translation = None
                except Exception as e:
                    print(f"Ошибка MyMemory: {str(e)}")
                    translation = None

                # Если MyMemory не дал перевод, пробуем парсинг Google Переводчика
                if not translation:
                    try:
                        headers = {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
                        }
                        async with session.get(
                            f"https://translate.google.com/m?sl=en&tl=ru&q={word}",
                            headers=headers
                        ) as response:
                            if response.status != 200:
                                return word, "Перевод не найден", self.strings["google_translation_error"].format("HTTP " + str(response.status))
                            html = await response.text()
                            soup = BeautifulSoup(html, "html.parser")
                            translation_element = soup.find("div", class_="result-container")
                            translation = translation_element.text.strip() if translation_element else "Перевод не найден"
                            if translation.lower() == word.lower() or not translation:
                                translation = "Перевод не найден"
                    except Exception as e:
                        print(f"Ошибка парсинга Google Переводчика: {str(e)}")
                        return word, "Перевод не найден", self.strings["google_translation_error"].format(str(e))

                return word, translation, None
            except Exception as e:
                print(f"Ошибка при получении слова или перевода: {str(e)}")
                return None, None, self.strings["word_fetch_error"].format(str(e))

    @loader.command()
    async def randomword(self, message):
        """Выдает случайное английское слово и его перевод на русский"""
        await utils.answer(message, self.strings["loading"])
        word, translation, error = await self.get_random_word()

        if error:
            await utils.answer(message, error)
            return

        if word:
            response = (
                f"🌍 <b>Слово:</b> {word}\n"
                f"🇷🇺 <b>Перевод:</b> {translation}"
            )
            await utils.answer(message, response)
        else:
            await utils.answer(message, self.strings["no_word"])

    async def client_ready(self, client, db):
        """Метод, вызываемый при готовности клиента"""
        self.client = client