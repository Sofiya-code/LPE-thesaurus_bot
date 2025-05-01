import logging
import sys
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters
from telegram.constants import ChatAction

# Конфигурация логгирования
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

# Константы
TELEGRAM_TOKEN = "7713193261:AAGbTg3Sv1uOe6wpTtksKZ0arLPt6fHGiyQ"

# Константы для клавиатур
MAIN_KEYBOARD = InlineKeyboardMarkup([
    [InlineKeyboardButton(" 🔍 Поиск термина", callback_data="search")],
    [InlineKeyboardButton(" 📚 Категории терминов", callback_data="categories")],
    [InlineKeyboardButton(" ℹ️ Помощь", callback_data="help")],
    [InlineKeyboardButton(" ✨ Информация", callback_data="info")]
])

CATEGORIES_KEYBOARD = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("🔤 Лингвистика", callback_data="cat_linguistics"),
        InlineKeyboardButton("📚 Педагогика", callback_data="cat_pedagogy")
    ],
    [
        InlineKeyboardButton("💰 Экономика", callback_data="cat_economics"),
        InlineKeyboardButton("⬅️ Назад", callback_data="back_to_main")
    ]
])

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик ошибок"""
    logger.error(f"Exception while handling an update: {context.error}")
    if update and update.effective_message:
        await update.effective_message.reply_text(
            "Произошла ошибка при обработке запроса. Пожалуйста, попробуйте позже."
        )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /start"""
    try:
        await update.message.reply_text(
            "👋 Привет! Я бот-словарь терминов\n\nВыберите действие:",
            reply_markup=MAIN_KEYBOARD
        )
    except Exception as e:
        logger.error(f"Error in start command: {e}")
        await error_handler(update, context)

async def search_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды поиска"""
    try:
        await update.message.reply_text(
            "Введите термин для поиска:",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("Назад", callback_data="back_to_main")
            ]])
        )
    except Exception as e:
        logger.error(f"Error in search command: {e}")
        await error_handler(update, context)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик нажатий на кнопки"""
    try:
        query = update.callback_query
        await query.answer()

        if query.data == "search":
            await query.message.edit_text(
                "Введите термин для поиска:",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("Назад", callback_data="back_to_main")
                ]])
            )
        elif query.data == "categories":
            await query.message.edit_text(
                "Выберите категорию:",
                reply_markup=CATEGORIES_KEYBOARD
            )
        elif query.data.startswith("cat_"):
            category = query.data.split("_")[1]
            category_mapping = {
                "linguistics": "лингвистика",
                "pedagogy": "педагогика", 
                "economics": "экономика"
            }
            mapped_category = category_mapping.get(category)
            
            if mapped_category in TERMS:
                context.user_data['current_category'] = mapped_category
                await query.message.edit_text(
                    f"Вы выбрали категорию: {mapped_category}\nВведите термин для поиска:",
                    reply_markup=InlineKeyboardMarkup([[
                        InlineKeyboardButton("К категориям", callback_data="categories")
                    ]])
                )
            else:
                await query.message.edit_text(
                    "Извините, категория не найдена.",
                    reply_markup=CATEGORIES_KEYBOARD
                )
        elif query.data == "back_to_main":
            await query.message.edit_text(
                "Выберите действие:",
                reply_markup=MAIN_KEYBOARD
            )
        elif query.data == "help":
            help_text = (
                "📖 Руководство по использованию бота\n\n"
                "🔍 Как искать термины:\n"
                "1. Нажмите '🔍 Поиск термина'\n"
                "2. Введите слово или часть слова\n"
                "3. Бот найдет все совпадения\n\n"
                "📚 Можно выбрать конкретную категорию:\n"
                "1. Нажмите '📚 Категории терминов'\n"
                "2. Выберите нужную категорию\n"
                "3. Введите термин для поиска\n\n"
                "✨ Разработано студентами курса «Цифровой переводчик»"
            )
            await query.message.edit_text(
                help_text,
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("Назад", callback_data="back_to_main")
                ]])
            )
        elif query.data == "info":
            info_text = (
                " 💡 Это разработка студентов курса «Цифровой переводчик».\n\n"
                " 🎯 Цель проекта: оптимизировать поиск терминов, их значений в паре языков (русский-английский) для обеспечения их адекватного/эквивалентного перевода в области лингвистики, педагогики и экономики.\n\n"
                " 🚀 Основные преимущества:\n"
                " 1️⃣ Постоянная доступность ✅\n"
                " 2️⃣ Учет контекста вводимого термина 💡\n"
                " 3️⃣ Экономия времени при переводе в узкоспециальной отрасли⏱️\n\n"
                " 👨‍💻 Создатели проекта:\n"
                " - Цандер София, 139 (тимлид);\n"
                " - Тимофеева Виталия, 139;\n"
                " - Махмутова Залина, 139;\n"
                " - Мухаметзянова Аделя, 139;\n"
                " - Баянов Данил, 139;\n"
                " - Амиров Рамиль, 139."
            )
            await query.message.edit_text(
                info_text,
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("Назад", callback_data="back_to_main")
                ]])
            )
    except Exception as e:
        logger.error(f"Error in button handler: {e}")
        await error_handler(update, context)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик текстовых сообщений"""
    try:
        await send_typing_action(update.effective_chat.id, context)
        search_term = update.message.text.lower().strip()
        if not search_term:
            await update.message.reply_text(
                "Пожалуйста, введите поисковый запрос.",
                reply_markup=MAIN_KEYBOARD
            )
            return

        current_category = context.user_data.get('current_category')
        matches = []

        if current_category:
            category_terms = TERMS.get(current_category, {})
            for term, details in category_terms.items():
                if search_term in term.lower():
                    matches.append(f"Термин: {term}\n" + "\n".join(f"{k}: {v}" for k, v in details.items()))
        else:
            for category, terms in TERMS.items():
                for term, details in terms.items():
                    if search_term in term.lower():
                        matches.append(f"Термин: {term} (категория: {category})\n" + 
                                    "\n".join(f"{k}: {v}" for k, v in details.items()))

        if matches:
            # Разбиваем результаты на части по 3 термина
            chunks = [matches[i:i + 3] for i in range(0, len(matches), 3)]

            # Отправляем первое сообщение с информацией о количестве
            await update.message.reply_text(
                f"🔍 Найдено терминов: {len(matches)}",
                reply_markup=MAIN_KEYBOARD
            )

            # Отправляем каждую часть отдельным сообщением
            for chunk in chunks:
                chunk_text = "\n\n".join(chunk)
                await update.message.reply_text(chunk_text)
        else:
            await update.message.reply_text(
                "❌ Термин не найден. Попробуйте другой запрос.",
                reply_markup=MAIN_KEYBOARD
            )
    except Exception as e:
        logger.error(f"Error in message handler: {e}")
        await error_handler(update, context)

async def send_typing_action(chat_id, context):
    """Отправляет индикатор набора текста"""
    try:
        await context.bot.send_chat_action(
            chat_id=chat_id,
            action=ChatAction.TYPING
        )
    except Exception as e:
        logger.error(f"Error sending typing action: {e}")

# Словарь терминов
TERMS = {
    "лингвистика": {
        "Поликодовость": {
            "📚Определение RU": "Характеристика текста, в котором сочетаются разные семиотические системы.",
            "📚Определение EN": "A polycode is a characteristic of a text that combines different semiotic systems.",
            "🔍Источник": "http://elib.sfukras.ru/bitstream/handle/2311/135862/vkr._kotelnikova_marina._dokument_na_normokontrol_1_1_pdf.io_.pdf?sequence=1"
        },
        "Метафора": {
            "📚Определение RU":
            "Слово или выражение, употребляемое в переносном значении, в основе которого лежит сравнение предмета или явления с каким-либо другим на основании их общего признака.",
            "📚Определение EN":
            "A metaphor is a word or expression used figuratively, which is based on comparing an object or phenomenon with another one based on their common feature.",
            "🔍Источник": "https://znanierussia.ru/articles/Метафора"
        },
        "Метонимия": {
            "📚Определение RU":
            "Вид тропа, словосочетание, в котором одно слово заменяется другим, обозначающим предмет (явление), находящийся в той или иной (пространственной, временной и т. п.) связи с предметом, который обозначается заменяемым словом.",
            "📚Определение EN":
            "A type of trope, a phrase in which one word is replaced by another, denoting an object (phenomenon) that is in one way or another (spatial, temporal, etc.) related to the object that is designated by the replaced word.",
            "🔍Источник": "https://scienceforum.ru/2021/article/2018025566"
        },
        "Эллипсис": {
            "📚Определение RU":
            "Намеренный пропуск слов, не существенных для смысла выражения.",
            "📚Определение EN":
            "The deliberate omission of words that are irrelevant to the meaning of an expression.",
            "🔍Источник": "https://kartaslov.ru/карта-знаний/Эллипсис"
        },
        "Градация": {
            "📚Определение RU":
            "Стилистическая фигура, состоящая в таком расположении частей высказывания (слов, отрезков предложения), при котором каждая последующая заключает в себе усиливающееся (реже уменьшающееся) смысловое или эмоционально-экспрессивное значение, благодаря чему создается нарастание (реже ослабление) производимого ими впечатления.",
            "📚Определение EN":
            "A stylistic figure consisting in such an arrangement of parts of an utterance (words, sentence segments), in which each subsequent contains an increasing (less often decreasing) semantic or emotionally expressive meaning, which creates an increase (less often a weakening) the impression they make.",
            "🔍Источник":
            "https://dic.academic.ru/dic.nsf/lingvistic/288/градация"
        },
        "Полисиндетон (многосоюзие)": {
            "📚Определение RU":
            "Принцип построения текста, при котором последующие повествовательные единицы (или их части) присоединяются к предыдущим одним и тем же (обычно сочинительным) союзом.",
            "📚Определение EN":
            "A principle of text construction in which subsequent narrative units (or parts thereof) are joined to the previous ones by the same (usually compositional) union.",
            "🔍Источник": "https://old.bigenc.ru/linguistics/text/2220689"
        },
        "Асиндетон": {
            "📚Определение RU":
            "Бессоюзие, стилистическая фигура, заключающаяся в опущении союзов.",
            "📚Определение EN":
            "A non-conjunction, a stylistic figure consisting in the omission of conjunctions.",
            "🔍Источник":
            "https://dic.academic.ru/dic.nsf/dic_fwords/43333/асиндетон"
        },
        "Анафора": {
            "📚Определение RU":
            "Лингвистическое явление, зависимость интерпретации некоторого выражения от другого выражения, обычно ранее встречавшегося в тексте.",
            "📚Определение EN":
            "A linguistic phenomenon, the dependence of the interpretation of some expression on another expression, usually previously found in the text.",
            "🔍Источник":
            "https://kartaslov.ru/карта-знаний/Анафора+%28лингвистика%29"
        },
        "Эпифора": {
            "📚Определение RU":
            "Стилистическая фигура, художественный приём, заключающийся в повторении конечных языковых единиц (звуков, слов, грамматических форм) смежных отрезков речи.",
            "📚Определение EN":
            "A stylistic device consisting in the repetition of finite linguistic units (sounds, words, grammatical forms) of adjacent speech segments.",
            "🔍Источник":
            "https://itest.kz/ru/ent/russkaya-literatura/rody-i-zhanry-folklora-i-literatury-osnovnye-literaturovedcheskie-ponyatiya/lecture/sredstva-hudozhestvennoj-vyrazitelnosti-tropy-stilisticheskie-figury"
        },
        "Языковая игра": {
            "📚Определение RU":
            "Определённый тип речевого поведения говорящих, основанный на преднамеренном (сознательном, продуманном) нарушении системных отношений языка.",
            "📚Определение EN":
            "A certain type of speech behavior of speakers based on a deliberate (conscious, thoughtful) violation of the systemic relations of language.",
            "🔍Источник": "https://stylistics.academic.ru/271/Языковая_игра"
        },
        "Выразительные средства": {
            "📚Определение RU":
            "Специальные художественно-риторические приёмы, лексические и грамматические средства языка, привлекающие внимание к высказыванию.",
            "📚Определение EN":
            "Special literary and rhetorical techniques, lexical and grammatical means of language that attract attention to the utterance.",
            "🔍Источник":
            "https://spravochnick.ru/literatura/leksiko-grammaticheskie_sredstva_vyrazitelnosti/"
        },
        "Семантические единицы": {
            "📚Определение RU":
            "Отдельные слова и выражения, которые передают сущность и картину заданной информации.",
            "📚Определение EN":
            "Individual words and expressions that convey the essence and picture of a given information.",
            "🔍Источник":
            "https://na-journal.ru/10-2023-filologiya-lingvistika/6602-semantika-kak-klyuchevaya-sostavlyayushchaya-yazyka"
        },
        "Лакуна": {
            "📚Определение RU":
            "Национально-специфический элемент культуры, нашедший отражение в языке и речи носителей этой культуры, который либо полностью не понимается, либо недопонимается носителями иной лингвокультуры в процессе коммуникации.",
            "📚Определение EN":
            "A nationally specific element of culture reflected in the language and speech of native speakers of this culture, which is either not fully understood or misunderstood by native speakers of another linguistic culture in the process of communication.",
            "🔍Источник": "https://ru.ruwiki.ru/wiki/Лакуна_(лингвистика)"
        },
        "Инверсия": {
            "📚Определение RU":
            "Изменение обычного порядка слов и словосочетаний, составляющих предложение.",
            "📚Определение EN":
            "A change in the usual order of words and phrases that make up a sentence.",
            "🔍Источник": "https://dic.academic.ru/dic.nsf/es/77069/ИНВЕРСИЯ"
        },
        "Стилистика": {
            "📚Определение RU":
            "Раздел языкознания, изучающий систему стилей языка, описывающий нормы и способы употребления литературного языка в различных условиях языкового общения, в разных видах и жанрах письменности.",
            "📚Определение EN":
            "The study of the devices in languages (such as rhetorical figures and syntactical patterns) that are considered to produce expressive or literary style.",
            "🔍Источник":
            "Словарь русского языка: В 4-х т. / РАН, Ин-т лингвистич. исследований; Под ред. А. П. Евгеньевой. — 4-е изд., стер. — М.: Рус. яз.; Полиграфресурсы, 1999; https://www.britannica.com/science/stylistics"
        },
        "Прагматика": {
            "📚Определение RU":
            "Раздел семиотики, изучающий свойства знаковой системы, которые возникают в результате отношения к ней пользующихся ею людей.",
            "📚Определение EN":
            "The study of how linguistic utterances are typically used to communicate propositions, intentions, attitudes, or other aspects of meaning that are not wholly expressed in the literal meanings and grammatical structures of spoken words and sentences.",
            "🔍Источник":
            "Словарь русского языка: В 4-х т. / РАН, Ин-т лингвистич. исследований; Под ред. А. П. Евгеньевой. — 4-е изд., стер. — М.: Рус. яз.; Полиграфресурсы, 1999; https://www.britannica.com/science/pragmatics"
        },
        "Семантика": {
            "📚Определение RU":
            "Раздел языкознания, изучающий это содержание, информацию.",
            "📚Определение EN":
            "Systematic study of meaning.",
            "🔍Источник":
            "Лингвистический энциклопедический словарь (1990); By Crimmins, Mark"
        },
        "Языковая картина мира": {
            "📚Определение RU":
            "Исторически сложившаяся в обыденном сознании данного языкового коллектива и отражённая в языке совокупность представлений о мире, определённый способ восприятия и устройства мира, концептуализации действительности.",
            "📚Определение EN":
            "Subjective model of the objective world, the system of language units used in representation of conceptual model of the world from individuals' mind.",
            "🔍Источник":
            "Зализняк Анна А. Языковая картина мира // «Кругосвет»"
        },
        "Каламбур": {
            "📚Определение RU":
            "Фигура речи, состоящая в юмористическом (пародийном) использовании разных значений одного и того же слова или двух сходно звучащих слов.",
            "📚Определение EN":
            "A humorous use of a word in such a way as to suggest different meanings or applications, or a play on words.",
            "🔍Источник":
            "[Ахманова, 2005, с. 69]; https://www.britannica.com/art/pun"
        },
        "Ирония": {
            "📚Определение RU":
            "Стилистический оборот, фраза, слово, в которых преднамеренно утверждается противоположное тому, что думают о лице или предмете.",
            "📚Определение EN":
            "A linguistic and literary device, in spoken or written form, in which real meaning is concealed or contradicted.",
            "🔍Источник":
            "Словарь русского языка: В 4-х т. / РАН, Ин-т лингвистич. исследований; Под ред. А. П. Евгеньевой. — 4-е изд., стер. — М.: Рус. яз.; Полиграфресурсы, 1999; https://www.britannica.com/art/irony"
        },
        "Лингвокультурология": {
            "📚Определение RU":
            "Дисциплина, изучающая проявление, отражение и фиксацию культуры в языке и дискурсе, непосредственно связанную с изучением национальной картины мира, языкового сознания, особенностей ментально-лингвального комплекса.",
            "📚Определение EN":
            "The study of language as a cultural phenomenon, in which interrelated language and culture are the subject.",
            "🔍Источник":
            "Красных В. В. Этнопсихолингвистика и лингвокультурология. — М., 2002. — С. 12; Sharifian, Farzad (2011). Cultural Conceptualisations and Language: Theoretical Framework and Applications. Amsterdam/Philadelphia: John Benjamins."
        },
        "Ономастика": {
            "📚Определение RU":
            "Раздел языкознания, изучающий собственные имена (онимы).",
            "📚Определение EN":
            "The science or study of the origin and forms of proper names of persons or places.",
            "🔍Источник":
            "Большая российская энциклопедия 2004–2017; https://www.britannica.com/science/synchronic-linguistics"
        },
        "Концептуализация": {
            "📚Определение RU":
            "Процесс определения набора когнитивных признаков (в том числе — и категориальных) какого-либо явления реального или воображаемого мира, которые позволяют человеку хранить в сознании и пополнять новой информацией сколько-нибудь очерченное понятие и/или представление об этом явлении и отличать его от других феноменов.",
            "📚Определение EN":
            "The process or result of forming a concept or concepts out of observations, experience, data.",
            "🔍Источник":
            "Стернин И. А. Типы значений и концепт // Концептуальное пространство языка : сб. науч. тр. / Под ред. проф. Е. С. Кубряковой. — Тамбов : Изд-во ТГУ им. Г. Р. Державина, 2005. — С. 257—282"
        },
        "Узус": {
            "📚Определение RU":
            "Общепринятое употребление единицы языка (слова, фразеологизма и т. д.) в отличие от его окказионального (временного и индивидуального) употребления (напр., неологизмы не являются узуальными единицами языка).",
            "📚Определение EN":
            "The way in which a word or phrase is normally and correctly used and as the points of grammar, syntax, style, and the choice of words.",
            "🔍Источник":
            "Большая российская энциклопедия 2004–2017; H. W. Fowler's A Dictionary of Modern English Usage"
        },
        "Доместикация": {
            "📚Определение RU":
            "Это этноцентрический подход, при котором текст оригинала зачастую сокращается, акцент делается на культурных ценностях языка перевода, а «автор приближается к читателю».",
            "📚Определение EN":
            "A translation strategy in which a transparent, fluent style is adopted in order to minimize the strangeness of the foreign text for the target language reader.",
            "🔍Источник":
            "Л. Венути; L. Venuti, The Translator’s Invisibility: A History of Translation (Routledge, London & New York, 1995)"
        },
        "Парадигма": {
            "📚Определение RU":
            "Совокупность (или класс) языковых единиц в лингвистике, связанных парадигматическими отношениями (объединённых по одному общему признаку и противопоставленных — по другому), а также упорядоченная схема или модель, определяющая такие языковые единицы.",
            "📚Определение EN":
            "A distinct set of concepts or thought patterns, including theories, research methods, postulates, and standards for what constitute legitimate contributions to a field.",
            "🔍Источник":
            "Кубрякова Е. С. Парадигма // Лингвистический энциклопедический словарь / Главный редактор В. Н. Ярцева. — М.: Советская энциклопедия, 1990. — 685 с. — ISBN 5-85270-031-2; The Oxford Dictionary of Philosophy (2008)"
        },
"аббревиатура": {
            "📚Определение RU": "сложносокращенное слово, составленное из начальных элементов: универмаг, вуз, ООН",
            "📚Определение EN": "An abbreviation is a shortened form of a word or a group of words.",
            "🔍Источник": "https://superinf.ru/view_helpstud.php?id=279"
        },

"abbreviation": {
            "📚Определение RU": "сложносокращенное слово, составленное из начальных элементов: универмаг, вуз, ООН",
            "📚Определение EN": "An abbreviation is a shortened form of a word or a group of words.",
            "🔍Источник": "https://englishprowess.com/abbreviation/"
        },

"агглютинация": {
            "📚Определение RU": "механическое присоединение стандартных однозначных аффиксов к неизменяемым основам или корням: бола – болалар – болаларга; ид(ти) – иди – идите.",
            "📚Определение EN": "An agglutination is a linguistic process in which words or affixes are joined together without spaces or intervening vowels, often resulting in long compound words. It occurs in languages where multiple morphemes can be concatenated to convey additional meaning. For example, in Turkish, "kitab" means "book," and adding "-ı" and "-lar" creates "kitabları," meaning "their books.",
            "🔍Источник": "https://superinf.ru/view_helpstud.php?id=279"
        },

"agglutination": {
            "📚Определение RU": "механическое присоединение стандартных однозначных аффиксов к неизменяемым основам или корням: бола – болалар – болаларга; ид(ти) – иди – идите.",
            "📚Определение EN": "An agglutination is a linguistic process in which words or affixes are joined together without spaces or intervening vowels, often resulting in long compound words. It occurs in languages where multiple morphemes can be concatenated to convey additional meaning. For example, in Turkish, "kitab" means "book," and adding "-ı" and "-lar" creates "kitabları," meaning "their books.",
            "🔍Источник": "https://pronounceonline.com/word/agglutination/"
        },

"аккомодация": {
            "📚Определение RU": "частичное приспособление артикуляций смежных согласного и гласного звуков: нёс [н’ос], ряд [р’ат], what [w‹t], was [wəz].",
            "📚Определение EN": "An accommodation is the process by which participants in a conversation adjust their accent, diction, or other aspects of language according to the speech style of the other participant. Also called linguistic accommodation, speech accommodation, and communication accommodation.",
            "🔍Источник": "https://superinf.ru/view_helpstud.php?id=279"
        },

"accommodation": {
            "📚Определение RU": "частичное приспособление артикуляций смежных согласного и гласного звуков: нёс [н’ос], ряд [р’ат], what [w‹t], was [wəz].",
            "📚Определение EN": "An accommodation is the process by which participants in a conversation adjust their accent, diction, or other aspects of language according to the speech style of the other participant. Also called linguistic accommodation, speech accommodation, and communication accommodation.",
            "🔍Источник": "https://www.thoughtco.com/what-is-accommodation-speech-1688964"
        },
"активная лексика ": {
            "📚Определение RU": "часть словарного состава языка, активно употребляющая во всех сферах жизни общества.",
            "📚Определение EN": "An active vocabulary is apart of the vocabulary of a language that is actively used in all spheres of society.",
            "🔍Источник": "https://superinf.ru/view_helpstud.php?id=279"
        },

"active vocabulary": {
            "📚Определение RU": "часть словарного состава языка, активно употребляющая во всех сферах жизни общества.",
            "📚Определение EN": "An active vocabulary is apart of the vocabulary of a language that is actively used in all spheres of society",
            "🔍Источник": "https://www.thoughtco.com/what-is-active-vocabulary-speech-1688964"
        },

"антонимы": {
            "📚Определение RU": "слова, принадлежащие к одной и той же части речи, имеющие противоположные, но соотносительные друг с другом значения: молодой – старый, день – ночь.",
            "📚Определение EN": "An antonym is a word having a meaning opposite to that of another word, such as hot and cold, short and tall. An antonym is the antonym of synonym.",
            "🔍Источник": "https://superinf.ru/view_helpstud.php?id=279"
        },

"antonyms": {
            "📚Определение RU": "слова, принадлежащие к одной и той же части речи, имеющие противоположные, но соотносительные друг с другом значения: молодой – старый, день – ночь.",
            "📚Определение EN": "An antonym is a word having a meaning opposite to that of another word, such as hot and cold, short and tall. An antonym is the antonym of synonym.",
            "🔍Источник": "https://www.thoughtco.com/what-is-antonym-words-1689110"
        },

"архаизмы": {
            "📚Определение RU": "устаревшее наименование существующих реалий; устаревшие слова, замененные в современном языке синонимами: ловитва – «охота», лоно – «грудь», выя – «шея».",
            "📚Определение EN": "An archaism is a word or phrase (or a particular meaning of a word or phrase) that is no longer in common use and is considered extremely old-fashioned.",
            "🔍Источник": "https://superinf.ru/view_helpstud.php?id=279"
        },

"archaism": {
            "📚Определение RU": "устаревшее наименование существующих реалий; устаревшие слова, замененные в современном языке синонимами: ловитва – «охота», лоно – «грудь», выя – «шея».",
            "📚Определение EN": "An archaism is a word or phrase (or a particular meaning of a word or phrase) that is no longer in common use and is considered extremely old-fashioned.",
            "🔍Источник": "https://www.thoughtco.com/archaism-words-and-syntax-1689130"
        },

"ассимиляция": {
            "📚Определение RU": "уподобление звуков друг другу в пределах слова или словосочетания: косточка – кости [кости], книжечка – книжка [книшкъ], высокий – высший [вышыi], обман – [¬мман].",
            "📚Определение EN": "An assimilation is a general term in phonetics for the process by which a speech sound becomes similar or identical to a neighboring sound. In the opposite process, dissimilation, sounds become less similar to one another. The term "assimilation" comes from the Latin meaning, "make similar to.".",
            "🔍Источник": "https://superinf.ru/view_helpstud.php?id=279"
        },

"assimilation ": {
            "📚Определение RU": "уподобление звуков друг другу в пределах слова или словосочетания: косточка – кости [кости], книжечка – книжка [книшкъ], высокий – высший [вышыi], обман – [¬мман].",
            "📚Определение EN": "An assimilation is a general term in phonetics for the process by which a speech sound becomes similar or identical to a neighboring sound. In the opposite process, dissimilation, sounds become less similar to one another. The term "assimilation" comes from the Latin meaning, "make similar to."",
            "🔍Источник": "https://www.thoughtco.com/what-is-assimilation-phonetics-1689141"
        },

"аффикс": {
            "📚Определение RU": " служебная морфема, видоизменяющая значение корня или выражающая отношение между словами в словосочетании и предложении.",
            "📚Определение EN": "An  affix— a word which create either a different form of that word or a new word with a different meaning. ",
            "🔍Источник": "https://superinf.ru/view_helpstud.php?id=279"
        },

"affix": {
            "📚Определение RU": " служебные морфемы, видоизменяющие значение корня или выражающие отношение между словами в словосочетании и предложении.",
            "📚Определение EN": "An affix— a word which create either a different form of that word or a new word with a different meaning.",
            "🔍Источник": "https://www.thoughtco.com/what-is-affix-words-1688976"
        },

 "аффиксация ": {
            "📚Определение RU": "создание нового слова посредством присоединения к производящей основе (или слову) тех или иных аффиксов; способ выражения грамматических значений при помощи аффиксов.",
            "📚Определение EN": "An affixation is the process of adding a morpheme—or affix—to a word to create either a different form of that word or a new word with a different meaning; affixation is the most common way of making new words in English.",
            "🔍Источник": "https://superinf.ru/view_helpstud.php?id=279"
        },

"affixation": {
            "📚Определение RU": " создание нового слова посредством присоединения к производящей основе (или слову) тех или иных аффиксов; способ выражения грамматических значений при помощи аффиксов.",
            "📚Определение EN": "An affixation is the process of adding a morpheme—or affix—to a word to create either a different form of that word or a new word with a different meaning; affixation is the most common way of making new words in English.",
            "🔍Источник": "https://www.thoughtco.com/what-is-affixation-words-1688976"
        },

 "глагол": {
            "📚Определение RU": "знаменательная часть речи, объединяющая в своём составе слова, обозначающие действие или состояние.",
            "📚Определение EN": "A verb is an important part of the English language and is classified under the Parts of Speech chapter. It is very important for all students, especially for those who are preparing for competitive exams. More than two questions are asked about this topic in every competitive examination. A verb is a word that says what happens to somebody or what somebody or something does. Verbs we can modify verbs by using auxiliary verbs or verb phrases to show different conditions, aspects, and moods. Let us learn about verbs in detail along with various types with definitions and examples of each.",
            "🔍Источник": "https://superinf.ru/view_helpstud.php?id=279"
        },

"verb": {
            "📚Определение RU": " знаменательная часть речи, объединяющая в своём составе слова, обозначающие действие или состояние.",
            "📚Определение EN": "A verb is an important part of the English language and is classified under the Parts of Speech chapter. It is very important for all students, especially for those who are preparing for competitive exams. More than two questions are asked about this topic in every competitive examination. A verb is a word that says what happens to somebody or what somebody or something does. Verbs we can modify verbs by using auxiliary verbs or verb phrases to show different conditions, aspects, and moods. Let us learn about verbs in detail along with various types with definitions and examples of each.",
            "🔍Источник": "https://www.geeksforgeeks.org/verbs/"
        },

 "грамматическая категория": {
            "📚Определение RU": "совокупность однородных грамматических форм, противопоставленных друг другу: категория вида - противопоставление (оппозиция) несовершенного вида совершенному; категория числа - оппозиция единственного и множественного числа.",
            "📚Определение EN": "A grammatical category is a class of units (such as noun and verb) or features (such as number and case) that share a common set of characteristics. They are the building blocks of language, allowing us to communicate with one another. There are no hard and fast rules for what defines these shared traits, however, making it difficult for linguists to agree on precisely what is and is not a grammatical category.",
            "🔍Источник": "https://superinf.ru/view_helpstud.php?id=279"
        },

" grammatical category": {
            "📚Определение RU": "совокупность однородных грамматических форм, противопоставленных друг другу: категория вида - противопоставление (оппозиция) несовершенного вида совершенному; категория числа - оппозиция единственного и множественного числа.",
            "📚Определение EN": "A grammatical category is a class of units (such as noun and verb) or features (such as number and case) that share a common set of characteristics. They are the building blocks of language, allowing us to communicate with one another. There are no hard and fast rules for what defines these shared traits, however, making it difficult for linguists to agree on precisely what is and is not a grammatical category.",
            "🔍Источник": "https://www.thoughtco.com/what-is-a-grammatical-category-1690910"
        },

 "денотат": {
            "📚Определение RU": "предмет или явление внеязыковой действительности, которые нужно назвать словом.",
            "📚Определение EN": "A denotation refers to the direct or dictionary meaning of a word, in contrast to its figurative or associated meanings (connotations). To understand the difference, think of how words would be used in writing about science or legal matters (with a precision of meaning) vs. how words would be used in poetry (rich with allusion, metaphor, and other shades of meaning than just their straight dictionary meanings).",
            "🔍Источник": "https://superinf.ru/view_helpstud.php?id=279"
        },

"denotation": {
            "📚Определение RU": "предмет или явление внеязыковой действительности, которые нужно назвать каким - либо словом.",
            "📚Определение EN": "A denotation refers to the direct or dictionary meaning of a word, in contrast to its figurative or associated meanings (connotations). To understand the difference, think of how words would be used in writing about science or legal matters (with a precision of meaning) vs. how words would be used in poetry (rich with allusion, metaphor, and other shades of meaning than just their straight dictionary meanings).",
            "🔍Источник": "https://www.thoughtco.com/what-is-denotation-1690436"
        },
 "денотативное значение слова": {
            "📚Определение RU": "отношение фонетического слова к конкретному обозначаемому предмету, объекту речи.",
            "📚Определение EN": " The notional content of a word is expressed by the denotative or denotational meaning also called referential or extentional meaning. Denotative meaning is the interrelation between the sound form of the linguistic sign and the concept, on the one hand, and the object named, on the other hand.",
            "🔍Источник": "https://superinf.ru/view_helpstud.php?id=279"
        },

"denotational meaning": {
            "📚Определение RU": "отношение фонетического слова к конкретному обозначаемому предмету, объекту речи.",
            "📚Определение EN": " The notional content of a word is expressed by the denotative or denotational meaning also called referential or extentional meaning. Denotative meaning is the interrelation between the sound form of the linguistic sign and the concept, on the one hand, and the object named, on the other hand.",
            "🔍Источник": "https://studfile.net/preview/9583508/page:6/"
        },
 "диалектизмы": {
            "📚Определение RU": "слова, составляющие принадлежность диалектов того или иного языка.",
            "📚Определение EN": " A dialectism is a word, phrase, or pronunciation that is characteristic of a particular region or social group, and differs from the standard language used in that region.",
            "🔍Источник": "https://superinf.ru/view_helpstud.php?id=279"
        },

"dialectism": {
            "📚Определение RU": "слова, составляющие принадлежность диалектов того или иного языка.",
            "📚Определение EN": " A dialectism is a word, phrase, or pronunciation that is characteristic of a particular region or social group, and differs from the standard language used in that region.",
            "🔍Источник": "https://finesentence.com/meaning/dialectism"
        },
 "синхрония": {
            "📚Определение RU": "состояние языка в определённый момент его развития как системы одновременно существующих взаимосвязанных и взаимообусловленных элементов.",
            "📚Определение EN": " A synchrony considers a language at a moment in time without taking its history into account.",
            "🔍Источник": "https://superinf.ru/view_helpstud.php?id=279"
        },

"synchrony ": {
            "📚Определение RU": "состояние языка в определённый момент его развития как системы одновременно существующих взаимосвязанных и взаимообусловленных элементов.",
            "📚Определение EN": " A synchrony considers a language at a moment in time without taking its history into account.",
            "🔍Источник": "https://ru.wikipedia.org/wiki/Диахрония_и_синхрония"

        },
 "диахрония ": {
            "📚Определение RU": "- динамика языка, развитие языка во времени, изучение языка в процессе развития.",
            "📚Определение EN": " A diachrony considers the development and evolution of a language through history.",
            "🔍Источник": "https://superinf.ru/view_helpstud.php?id=279"
        },

"diachrony ": {
            "📚Определение RU": "слова, составляющие принадлежность диалектов того или иного языка.",
            "📚Определение EN": " A diachrony considers the development and evolution of a language through history.",
            "🔍Источник": "https://ru.wikipedia.org/wiki/Диахрония_и_синхрония"
        },

 "интонация": {
            "📚Определение RU": "- совокупность ритмомелодических компонентов речи, служащая средством выражения синтаксических значений и эмоционально - экспрессивной окраски высказывания.",
            "📚Определение EN": " An intonation serves for the external design of the sentence, as it gives the sentence semantic completeness, as well as various emotional coloring.",
            "🔍Источник": "https://superinf.ru/view_helpstud.php?id=279"
        },

"intonation ": {
            "📚Определение RU": "совокупность ритмомелодических компонентов речи, служащая средством выражения синтаксических значений и эмоционально - экспрессивной окраски высказывания.",
            "📚Определение EN": " An intonation serves for the external design of the sentence, as it gives the sentence semantic completeness, as well as various emotional coloring.",
            "🔍Источник": "https://englopedia.com/intonation-and-its-types-and-features/"
        },

 "историзмы ": {
            "📚Определение RU": "- устаревшие слова, вышедшие из употребления в связи с исчезновением предметов или явлений объективной действительности: боярин, стольник, алтын.",
            "📚Определение EN": " historisms are obsolete words that have fallen out of use due to the disappearance of objects or phenomena of objective reality.",
            "🔍Источник": "https://superinf.ru/view_helpstud.php?id=279"
        },

"historisms ": {
            "📚Определение RU": "устаревшие слова, вышедшие из употребления в связи с исчезновением предметов или явлений объективной действительности: боярин, стольник, алтын.",
            "📚Определение EN": " historisms are obsolete words that have fallen out of use due to the disappearance of objects or phenomena of objective reality.",
            "🔍Источник": "https://englopedia.com/historisms-and-its-types-and-features/"
        },
 "морфология ": {
            "📚Определение RU": "раздел языкознания, изучающий грамматические свойства слов, их словоизменение (парадигматику слов), а также способы выражения абстрактных грамматических значений, разрабатывает учение о частях речи.",
            "📚Определение EN": " a morphology is the linguistic discipline that describes and analyzes the processes and rules of word formation and creation, their internal structure, the composition and organization of their constituents.",
            "🔍Источник": "https://superinf.ru/view_helpstud.php?id=279"
        },

"morphology ": {
            "📚Определение RU": "раздел языкознания, изучающий грамматические свойства слов, их словоизменение (парадигматику слов), а также способы выражения абстрактных грамматических значений, разрабатывает учение о частях речи.",
            "📚Определение EN": " a morphology is the linguistic discipline that describes and analyzes the processes and rules of word formation and creation, their internal structure, the composition and organization of their constituents.",
            "🔍Источник": "https://englopedia.com/morphology-types-and-its-topics-with-description/"
        },

 "неологизм": {
            "📚Определение RU": "новые слова, обозначающие новую реалию (предмет или понятие), появившиеся в языке недавно, сохраняющие оттенок свежести и необычности,  входящие в пассивную лексику: спонсор, видеоклип, факс, ваучер, компьютер, дисплей.",
            "📚Определение EN": " a neologism is a word, word, term or expression that is introduced or created in a certain language. They are born from the need to express a new concept of reality, such as “bitcoin”, “clicking”, “selfie” or “emoji”.",
            "🔍Источник": "https://superinf.ru/view_helpstud.php?id=279"
        },

"neologism": {
            "📚Определение RU": "новые слова, обозначающие новую реалию (предмет или понятие), появившиеся в языке недавно, сохраняющие оттенок свежести и необычности,  входящие в пассивную лексику: спонсор, видеоклип, факс, ваучер, компьютер, дисплей.",
            "📚Определение EN": " a neologism is a word, word, term or expression that is introduced or created in a certain language. They are born from the need to express a new concept of reality, such as “bitcoin”, “clicking”, “selfie” or “emoji”.",
            "🔍Источник": "https://englopedia.com/neologism-concept-types-and-examples-with-detail/"
        },

 "омонимия ": {
            "📚Определение RU": "звуковые совпадение различных по значению единиц: ключ «родник» и ключ «инструмент», брак «изъян» и брак «женитьба».",
            "📚Определение EN": " an homonymy is the relation between words with identical forms but different meanings—that is, the condition of being homonyms. A stock example is the word bank as it appears in "river bank" and "savings ​bank.»",
            "🔍Источник": "https://superinf.ru/view_helpstud.php?id=279"
        },

"homonymy ": {
            "📚Определение RU": "звуковые совпадение различных по значению единиц: ключ «родник» и ключ «инструмент», брак «изъян» и брак «женитьба».",
            "📚Определение EN": "an homonymy is the relation between words with identical forms but different meanings—that is, the condition of being homonyms. A stock example is the word bank as it appears in "river bank" and "savings ​bank..",
            "🔍Источник": "https://www.thoughtco.com/homonymy-words-and-meanings-1690839"
        },

 "паронимы": {
            "📚Определение RU": "созвучные однокоренные слова, принадлежащие к одной части речи, имеющие структурное сходство, но различающиеся своим значением: представить - предоставить, советник - советчик, надеть (шапку) - одеть (ребенка).",
            "📚Определение EN": " an homonymy is the relation between words with identical forms but different meanings—that is, the condition of being homonyms. A stock example is the word bank as it appears in "river bank" and "savings bank.»",
            "🔍Источник": "https://superinf.ru/view_helpstud.php?id=279"
        },

"paronyms": {
            "📚Определение RU": "созвучные однокоренные слова, принадлежащие к одной части речи, имеющие структурное сходство, но различающиеся своим значением: представить - предоставить, советник - советчик, надеть (шапку) - одеть (ребенка).",
            "📚Определение EN": "Paronyms or paronym words  are words that are spelled similarly and are pronounced similarly, but have different meanings. Paronymy relations are studied through semantics.",
            "🔍Источник": "https://englopedia.com/paronyms/"
        },


 "полисемия": {
            "📚Определение RU": "наличие у одного и того же слова нескольких связанных между собой значений: доска «строительный материал», доска «оборудование класса» и т.д.",
            "📚Определение EN": " a polysemy is the ability of words to have more than one meaning. A word with several meanings is called polysemantic. Monosemantic words, which have only one meaning, are comparatively few; they are mainly scientific terms (e.g. hydrogen) or rare words (e.g. flamingo).»",
            "🔍Источник": "https://superinf.ru/view_helpstud.php?id=279"
        },

"polysemy": {
            "📚Определение RU": "наличие у одного и того же слова нескольких связанных между собой значений: доска «строительный материал», доска «оборудование класса» и т.д.",
            "📚Определение EN": "a polysemy is the ability of words to have more than one meaning. A word with several meanings is called polysemantic. Monosemantic words, which have only one meaning, are comparatively few; they are mainly scientific terms (e.g. hydrogen) or rare words (e.g. flamingo).",
            "🔍Источник": "https://studfile.net/preview/4518508/page:5/"
        },

 "префикс": {
            "📚Определение RU": "морфема, стоящая перед корнем, служит для образования новых слов (дед-прадед) или форм слов (забавный - презабавный).",
            "📚Определение EN": " a prefix is a group of letters added to the beginning of a word to change its meaning. Prefixes do not change a word’s grammatical category (noun, verb, adjective), but they modify its meaning. For example: Moral → Amoral (prefix "a-" means "without".»",
            "🔍Источник": "https://superinf.ru/view_helpstud.php?id=279"
        },

"prefix": {
            "📚Определение RU": "морфема, стоящая перед корнем, служит для образования новых слов (дед-прадед) или форм слов (забавный - презабавный).",
            "📚Определение EN": "a prefix is a group of letters added to the beginning of a word to change its meaning. Prefixes do not change a word’s grammatical category (noun, verb, adjective), but they modify its meaning. For example: Moral → Amoral (prefix "a-" means "without".",
            "🔍Источник":https://pushtolearn.com/post/common-prefixes-in-english"
        },

 "редукция": {
            "📚Определение RU": "изменение звуковых характеристик гласных или согласных в слабой позиции: мороз [м¬рос], обоз [¬бос].",
            "📚Определение EN": " reduction is a historical process of weakening, shortening or disappearance of vowel sounds in unstressed syllable. The neutral sound represents the reduced form of almost any vowel or diphthong in the unstressed position: combine /'kɒmbaɪn/ - combine /kəm'baɪn/.»",
            "🔍Источник": "https://superinf.ru/view_helpstud.php?id=279"
        },

"reduction": {
            "📚Определение RU": "изменение звуковых характеристик гласных или согласных в слабой позиции: мороз [м¬рос], обоз [¬бос].",
            "📚Определение EN": "reduction is a historical process of weakening, shortening or disappearance of vowel sounds in unstressed syllable. The neutral sound represents the reduced form of almost any vowel or diphthong in the unstressed position: combine /'kɒmbaɪn/ - combine /kəm'baɪn/.",
            "🔍Источник":https://studfile.net/preview/9756780/page:4/"
        },

 "семасиология": {
            "📚Определение RU": "наука о значениях слов и словосочетаний.",
            "📚Определение EN": "semasiology is the branch of lexicology that is devoted to the study of meaning.",
            "🔍Источник": "https://superinf.ru/view_helpstud.php?id=279"
        },

"semasiology ": {
            "📚Определение RU": "наука о значениях слов и словосочетаний.",
            "📚Определение EN": "semasiology is the branch of lexicology that is devoted to the study of meaning.",
            "🔍Источник":https://studfile.net/preview/9756780/page:4/"
        },

 "синекдоха": {
            "📚Определение RU": "перенос наименования по признаку количества: часть вместо целого и наоборот: стада в десять голов.",
            "📚Определение EN": "synecdoche is a trope or figure of speech in which a part of something is used to represent the whole (for example, ABCs for alphabet) or (less commonly) the whole is used to represent a part.",
            "🔍Источник": "https://superinf.ru/view_helpstud.php?id=279"
        },

"synecdoche": {
            "📚Определение RU": "перенос наименования по признаку количества: часть вместо целого и наоборот: стада в десять голов.",
            "📚Определение EN": "synecdoche is a trope or figure of speech in which a part of something is used to represent the whole (for example, ABCs for alphabet) or (less commonly) the whole is used to represent a part.",
            "🔍Источник": https://www.thoughtco.com/synecdoche-figure-of-speech-1692172"
        },

 "синоним": {
            "📚Определение RU": "слова, разные по звучанию, но близкие по значению, принадлежащие к одной части речи и имеющие полностью или частично совпадающие значения: страх - ужас.",
            "📚Определение EN": "synonym is a word having the same or nearly the same meaning as another word in certain contexts. ",
            "🔍Источник": "https://superinf.ru/view_helpstud.php?id=279"
        },

"synonym": {
            "📚Определение RU": "слова, разные по звучанию, но близкие по значению, принадлежащие к одной части речи и имеющие полностью или частично совпадающие значения: страх - ужас.",
            "📚Определение EN": "synonym is a word having the same or nearly the same meaning as another word in certain contexts. ",
            "🔍Источник": https://www.thoughtco.com/synonym-definition-1692177"
        },

"слово": {
            "📚Определение RU": "основная структурно - семантическая единица языка, служащая для именования денотатов, обладающая совокупностью семантических, фонетических и грамматических признаков, специфичных для каждого языка.",
            "📚Определение EN": " word is the smallest unit of grammar that can stand alone as a complete utterance, separated by spaces in written language and potentially by pauses in speech.",
            "🔍Источник": "https://superinf.ru/view_helpstud.php?id=279"
        },

"word ": {
            "📚Определение RU": "основная структурно - семантическая единица языка, служащая для именования денотатов, обладающая совокупностью семантических, фонетических и грамматических признаков, специфичных для каждого языка.",
            "📚Определение EN": "word is the smallest unit of grammar that can stand alone as a complete utterance, separated by spaces in written language and potentially by pauses in speech.",
            "🔍Источник": https://www.thoughtco.com/word-definition-1692177"
        },

"уровни языка": {
            "📚Определение RU": "ярусы общей языковой системы, каждая из которых обладает набором своих единиц и правил их функционирования: фонетический, морфологический, лексический, синтаксический.",
            "📚Определение EN": " levels of language are the tiers of a common language system, each of which has a set of its own units and rules of their functioning: phonetic, morphological, lexical, syntactic.",
            "🔍Источник": "https://superinf.ru/view_helpstud.php?id=279"
        },

"levels of language": {
            "📚Определение RU": "ярусы общей языковой системы, каждая из которых обладает набором своих единиц и правил их функционирования: фонетический, морфологический, лексический, синтаксический.",
            "📚Определение EN": "levels of language are the tiers of a common language system, each of which has a set of its own units and rules of their functioning: phonetic, morphological, lexical, syntactic.",
            "🔍Источник": https://www.thoughtco.com/levels-of-language-definition-1692177"
        },

"фонетика": {
            "📚Определение RU": "раздел языкознания, изучающий звуковые единицы языка, их акустические и артикуляционные свойства, законы функционирования звуков речи, распределения ударения в словах, чередования гласных и согласных.",
            "📚Определение EN": " phonetics is the branch of linguistics that deals with speech sounds and their production, combination, description, and representation by written symbols.",
            "🔍Источник": "https://superinf.ru/view_helpstud.php?id=279"
        },

"phonetics ": {
            "📚Определение RU": "раздел языкознания, изучающий звуковые единицы языка, их акустические и артикуляционные свойства, законы функционирования звуков речи, распределения ударения в словах, чередования гласных и согласных.",
            "📚Определение EN": "phonetics is the branch of linguistics that deals with speech sounds and their production, combination, description, and representation by written symbols.",
            "🔍Источник": https://englopedia.com/phonetics-definition-and-examples/"
        },
"аверсия": {
            "📚Определение RU": Разновидность олицетворения, обращение к неодушевленным предметам или умершим:.",
            "📚Определение EN": "extreme dislike or disinclination; repugnance.",
            "🔍Источник": "Словарь лингвистических терминов Т.В. Жеребило. Collins dictionary. "
        },

"aversion": {
            "📚Определение RU": " Разновидность олицетворения, обращение к неодушевленным предметам или умершим.",
            "📚Определение EN": " extreme dislike or disinclination; repugnance.",
            "🔍Источник": " Словарь лингвистических терминов Т.В. Жеребило. Collins dictionary."
        },
"американизмы": {
            "📚Определение RU": Слова, выражения, свойственные американскому варианту английского языка, заимствованные в другие языки.",
            "📚Определение EN": "an expression that is typical of people living in the United States of America.",
            "🔍Источник": "Словарь лингвистических терминов Т.В. Жеребило. Collins dictionary. "
        },

"americanisms": {
            "📚Определение RU": " Слова, выражения, свойственные американскому варианту английского языка, заимствованные в другие языки.",
            "📚Определение EN":  an expression that is typical of people living in the United States of America.",
            "🔍Источник": " Словарь лингвистических терминов Т.В. Жеребило. Collins dictionary."
        },
"анахронизм": {
            "📚Определение RU": Вид речевой ошибки, основанной на употреблении слов, терминов, понятий, не соответствующих изображаемой эпохе.",
            "📚Определение EN": "chronological inconsistency in some arrangement, especially a juxtaposition of people, events, objects, language terms and customs from different time periods.",
            "🔍Источник": "Словарь лингвистических терминов Т.В. Жеребило. dictionary.cambridge. "
        },

"anachronism": {
            "📚Определение RU": "Вид речевой ошибки, основанной на употреблении слов, терминов, понятий, не соответствующих изображаемой эпохе.",
            "📚Определение EN": "chronological inconsistency in some arrangement, especially a juxtaposition of people, events, objects, language terms and customs from different time periods.",
            "🔍Источник": " Словарь лингвистических терминов Т.В. Жеребило. dictionary.cambridge."
        },
" артикль": {
            "📚Определение RU": "Член, частица, прилагаемая в некоторых языках к существительному и придающая ему значение рода, определенности или неопределенности и некоторые другие значения.",
"📚Определение EN": "any member of a class of dedicated words that are used with noun phrases to mark the identifiability of the referents of the noun phrases.",
            "🔍Источник": "Словарь лингвистических терминов Т.В. Жеребило. dictionary.cambridge"
        },

" article ": {
            "📚Определение RU": " Член, частица, прилагаемая в некоторых языках к существительному и придающая ему значение рода, определенности или неопределенности и некоторые другие значения.",
            "📚Определение EN": "any member of a class of dedicated words that are used with noun phrases to mark the identifiability of the referents of the noun phrases.",
            "🔍Источник": " Словарь лингвистических терминов Т.В. Жеребило dictionary.cambridge"
        },
"аналогия": {
            "📚Определение RU": "один из законов функционирования и развития языка, в соответствии с которым образование и изменение языковых единиц и их форм происходит под влиянием, по образцу уже существующих единиц и форм.",
            "📚Определение EN": "process by which new words and inflections are created on the basis of regularities in the form of existing ones.",
            "🔍Источник": "Словарь лингвистических терминов Т.В. Жеребило. Oxford Languages "
        },

"analogy": {
            "📚Определение RU": " один из законов функционирования и развития языка, в соответствии с которым образование и изменение языковых единиц и их форм происходит под влиянием, по образцу уже существующих единиц и форм.",
            "📚Определение EN": "process by which new words and inflections are created on the basis of regularities in the form of existing ones.",
            "🔍Источник": " Словарь лингвистических терминов Т.В. Жеребило. Collins dictionary."
        },
"аллегория": {
            "📚Определение RU": "иносказание; выражение отвлеченного понятия посредством образа ",
            "📚Определение EN": "story, poem, or picture that can be interpreted to reveal a hidden meaning, typically a moral or political one..",
            "🔍Источник": "Словарь лингвистических терминов Т.В. Жеребило. Oxford Languages."
        },

"allegory": {
            "📚Определение RU": "иносказание; выражение отвлеченного понятия посредством образа.",
            "📚Определение EN": "story, poem, or picture that can be interpreted to reveal a hidden meaning, typically a moral or political one.",
            "🔍Источник": " Словарь лингвистических терминов Т.В. Жеребило. Oxford Languages."
        },
"билингвизм": {
            "📚Определение RU": "Взаимодействие двух или трех языков в одном и том же языковом коллективе, языковом социуме.",
            "📚Определение EN": "fluency in or use of two languages.",
            "🔍Источник": "Словарь лингвистических терминов Т.В. Жеребило. Oxford Languages."
        },

"bilingualism": {
            "📚Определение RU": "Взаимодействие двух или трех языков в одном и том же языковом коллективе, языковом социуме
            "📚Определение EN": "fluency in or use of two languages.",
            "🔍Источник": " Словарь лингвистических терминов Т.В. Жеребило. Oxford Languages."
        },
"валентность": {
            "📚Определение RU": "Реализация сочетаемостных свойств синтаксически господствующих и зависимых слов.",
            "📚Определение EN": "number of grammatical elements with which a particular word, especially a verb, combines in a sentence.",
            "🔍Источник": "Словарь лингвистических терминов Т.В. Жеребило. Oxford Languages."
        },

"valency": {
            "📚Определение RU": "Реализация сочетаемостных свойств синтаксически господствующих и зависимых слов.",
            "📚Определение EN": "number of grammatical elements with which a particular word, especially a verb, combines in a sentence.",
            "🔍Источник": " Словарь лингвистических терминов Т.В. Жеребило. Oxford Languages."
        },
"вульгаризм": {
            "📚Определение RU": " Грубое слово или выражение, не принятое в литературном языке.",
            "📚Определение EN": "expression or usage considered non-standard or characteristic of uneducated speech or writing.",
            "🔍Источник": "Словарь лингвистических терминов Т.В. Жеребило. Oxford Languages."
        },

 "vulgarism ": {
            "📚Определение RU": "Грубое слово или выражение, не принятое в литературном языке.",
            "📚Определение EN": "expression or usage considered non-standard or characteristic of uneducated speech or writing.",
            "🔍Источник": " Словарь лингвистических терминов Т.В. Жеребило. Oxford Languages."
        },
"генерализация": {
            "📚Определение RU": "Использование в процессе анализа языковых особенностей родо-видовой абстракции
            "📚Определение EN": "form of abstraction whereby common properties of specific instances are formulated as general concepts or claims.",
            "🔍Источник": "Словарь лингвистических терминов Т.В. Жеребило. www.dictionary.com. Retrieved 30 November 2019. "
        },

"generalization": {
            "📚Определение RU": "Использование в процессе анализа языковых особенностей родо-видовой абстракции ",
            "📚Определение EN": "form of abstraction whereby common properties of specific instances are formulated as general concepts or claims.",
            "🔍Источник": " Словарь лингвистических терминов Т.В. Жеребило. www.dictionary.com. Retrieved 30 November 2019."
        },
"диалект": {
            "📚Определение RU": "Местное или социальное наречие, говор, являющиеся разновидностью общенародного языка.",
            "📚Определение EN": "particular form of a language which is peculiar to a specific region or social group.",
            "🔍Источник": "Словарь лингвистических терминов Т.В. Жеребило. Oxford Languages."
        },

"dialect": {
            "📚Определение RU": "Местное или социальное наречие, говор, являющиеся разновидностью общенародного языка.",
            "📚Определение EN": "particular form of a language which is peculiar to a specific region or social group.",
            "🔍Источник": " Словарь лингвистических терминов Т.В. Жеребило. Oxford Languages."
        },
"дифференциация": {
            "📚Определение RU": " Образование различных родственных языков и диалектов на основе праязыка.",
            "📚Определение EN": "formation of various related languages and dialects on the basis of the primary language.",
            "🔍Источник": "Словарь лингвистических терминов Т.В. Жеребило. Löbner (2002)."
        },

"differentiation": {
            "📚Определение RU": "Образование различных родственных языков и диалектов на основе праязыка.",
            "📚Определение EN": "formation of various related languages and dialects on the basis of the primary language	.",
            "🔍Источник": " Словарь лингвистических терминов Т.В. Жеребило. Löbner (2002)."
        },
"дискурс": {
            "📚Определение RU": "связная речь в устной и письменной форме.",
            "📚Определение EN": "natural spoken or written language in context, especially when complete texts are being considered.",
            "🔍Источник": "Словарь лингвистических терминов Т.В. Жеребило. Collins dictionary. "
        },

"discourse": {
            "📚Определение RU": "связная речь в устной и письменной форме.",
            "📚Определение EN": "natural spoken or written language in context, especially when complete texts are being considered.",
            "🔍Источник": " Словарь лингвистических терминов Т.В. Жеребило. Collins dictionary."
        },
"диалог": {
            "📚Определение RU": "Форма устной речи, разговор двух или нескольких лиц; речевая связь посредством обмена словами, фразами по к.-л. теме.",
            "📚Определение EN": "discussion between two or more people or groups, especially one directed towards exploration of a particular subject or resolution of a problem.",
            "🔍Источник": "Словарь лингвистических терминов Т.В. Жеребило.  Oxford Languages."
        },

"dialogue": {
            "📚Определение RU": "Форма устной речи, разговор двух или нескольких лиц; речевая связь посредством обмена словами, фразами по к.-л. теме.",
"📚Определение EN": "discussion between two or more people or groups, especially one directed towards exploration of a particular subject or resolution of a problem.",
            "🔍Источник": " Словарь лингвистических терминов Т.В. Жеребило.  Oxford Languages."
        },

"жаргонизм": {
            "📚Определение RU": "Слово из жаргона (искусственного языка), понятного лишь определенному кругу людей.",
            "📚Определение EN": "special words or expressions used by a profession or group that are difficult for others to understand.",
            "🔍Источник": "Словарь лингвистических терминов Т.В. Жеребило.  Oxford Languages."
        },

"jargon": {
            "📚Определение RU": "Слово из жаргона (искусственного языка), понятного лишь определенному кругу людей.",
            "📚Определение EN": "special words or expressions used by a profession or group that are difficult for others to understand.",
            "🔍Источник": " Словарь лингвистических терминов Т.В. Жеребило.  Oxford Languages."
        },
"заимствование": {
            "📚Определение RU": "Процесс и результат перехода из одного языка в другой слов, грамматических конструкций, морфем, фонем.",
            "📚Определение EN": "type of language change in which a language or dialect undergoes change as a result of contact with another language or dialect.",
            "🔍Источник": "Словарь лингвистических терминов Т.В. Жеребило.  Oxford Languages."
        },

"borrowing": {
            "📚Определение RU": "Процесс и результат перехода из одного языка в другой слов, грамматических конструкций, морфем, фонем.",
            "📚Определение EN": "type of language change in which a language or dialect undergoes change as a result of contact with another language or dialect.",
            "🔍Источник": " Словарь лингвистических терминов Т.В. Жеребило.  Oxford Languages."
        },
" звукоподражания": {
            "📚Определение RU": "Неполнознаменательная часть речи, служащая для имитации звуков живой и неживой природы и тем самым создающая представление о процессах, признаках и предметах реального мира.",
            "📚Определение EN": "the formation of a word from a sound associated with what is named.",
            "🔍Источник": "Словарь лингвистических терминов Т.В. Жеребило.  Oxford Languages."
        },

"onomatopoeia": {
            "📚Определение RU": "Неполнознаменательная часть речи, служащая для имитации звуков живой и неживой природы и тем самым создающая представление о процессах, признаках и предметах реального мира.",
            "📚Определение EN": "the formation of a word from a sound associated with what is named.",
            "🔍Источник": " Словарь лингвистических терминов Т.В. Жеребило.  Oxford Languages."
        },
"идиома": {
            "📚Определение RU": "Неразложимое словосочетание, значение которого не совпадает со значением составляющих его слов, взятых в отдельности.",
            "📚Определение EN": "phrase or expression that largely or exclusively carries a figurative or non-literal meaning, rather than making any literal sense.",
            "🔍Источник": "Словарь лингвистических терминов Т.В. Жеребило.  The Oxford companion to the English language (1992:495f.)."
        },

"idiom": {
            "📚Определение RU": "Неразложимое словосочетание, значение которого не совпадает со значением составляющих его слов, взятых в отдельности.",
            "📚Определение EN": "phrase or expression that largely or exclusively carries a figurative or non-literal meaning, rather than making any literal sense.",
            "🔍Источник": " Словарь лингвистических терминов Т.В. Жеребило.  The Oxford companion to the English language (1992:495f.)."
        },
"интерлингвистика": {
            "📚Определение RU": "Область языкознания, исследующая проблемы, возникающие в связи с созданием и функционированием международных искусственных языков ",
            "📚Определение EN": "study of interlingual similarities and relationships especially for the purpose of devising an interlanguage.",
            "🔍Источник": "Словарь лингвистических терминов Т.В. Жеребило.  https://www.merriam-webster.com."
        },

"interlinguistics": {
            "📚Определение RU": "Область языкознания, исследующая проблемы, возникающие в связи с созданием и функционированием международных искусственных языков ",
            "📚Определение EN":  study of interlingual similarities and relationships especially for the purpose of devising an interlanguage.",
            "🔍Источник": " Словарь лингвистических терминов Т.В. Жеребило.  https://www.merriam-webster.com."
        },
"интерференция": {
            "📚Определение RU": "Взаимодействие и взаимовлияние двух языковых систем в условиях, когда население пользуется сразу двумя языками (билингвизм).",
            "📚Определение EN": "influence of one language (or variety) on another in the speech of bilinguals who use both languages.",
            "🔍Источник": "Словарь лингвистических терминов Т.В. Жеребило.  Oxford language."
        },

"interference": {
            "📚Определение RU": "Взаимодействие и взаимовлияние двух языковых систем в условиях, когда население пользуется сразу двумя языками (билингвизм).",
            "📚Определение EN": "influence of one language (or variety) on another in the speech of bilinguals who use both languages.",
            "🔍Источник": " Словарь лингвистических терминов Т.В. Жеребило.  Oxford language."
        },
"импликация": {
"📚Определение RU": "Логическая операция, приблизительно соответствующая сложному обороту, составленному из двух высказываний, соединенных между собой составным союзом "если, то…"",
            "📚Определение EN": "relationship between statements that holds true when one logically "follows from" one or more others.",
            "🔍Источник": "Словарь лингвистических терминов Т.В. Жеребило.  dictionary.cambridge."
        },

"implication": {
            "📚Определение RU": "Логическая операция, приблизительно соответствующая сложному обороту, составленному из двух высказываний, соединенных между собой составным союзом "если, то…".",
            "📚Определение EN": "relationship between statements that holds true when one logically "follows from" one or more others.",
            "🔍Источник": " Словарь лингвистических терминов Т.В. Жеребило.  dictionary.cambridge."
        },
"калькирование": {
            "📚Определение RU": "Способ заимствования, выражающийся в переводе иноязычных морфем или значения иноязычного слова средствами заимствующего языка.",
            "📚Определение EN": "word or phrase borrowed from another language by literal word-for-word or root-for-root translation.",
            "🔍Источник": "Словарь лингвистических терминов Т.В. Жеребило. Oxford language."
        },

"calque": {
            "📚Определение RU": "Способ заимствования, выражающийся в переводе иноязычных морфем или значения иноязычного слова средствами заимствующего языка.",
            "📚Определение EN":  "word or phrase borrowed from another language by literal word-for-word or root-for-root translation.",
            "🔍Источник": " Словарь лингвистических терминов Т.В. Жеребило. Oxford language."
        },
"когерентность": {
            "📚Определение RU": "Согласованное протекание во времени нескольких процессов.",
            "📚Определение EN": "term of text linguistics used to refer to sense relations between single units (sentences or propositions) of a text.",
            "🔍Источник": "Словарь лингвистических терминов Т.В. Жеребило.  Oxford language."
        },

"coherence": {
            "📚Определение RU": "Согласованное протекание во времени нескольких процессов.",
            "📚Определение EN": "term of text linguistics used to refer to sense relations between single units (sentences or propositions) of a text.",
            "🔍Источник": " Словарь лингвистических терминов Т.В. Жеребило.  Oxford language."
        },
"когнитивная лингвистика": {
            "📚Определение RU": "Направление, в центре внимания которого находится язык как общий когнитивный механизм, как когнитивный инструмент – система знаков, играющих роль в репрезентации (кодировании) и трансформировании информации.",
            "📚Определение EN": "interdisciplinary branch of linguistics, combining knowledge and research from cognitive science, cognitive psychology, neuropsychology and linguistics.",
            "🔍Источник": "Словарь лингвистических терминов Т.В. Жеребило.  Robinson, Peter (2008). Handbook of Cognitive Linguistics and Second Language Acquisition. Routledge. pp. 3–8."
        },

"cognitive linguistics": {
            "📚Определение RU": "Направление, в центре внимания которого находится язык как общий когнитивный механизм, как когнитивный инструмент – система знаков, играющих роль в репрезентации (кодировании) и трансформировании информации.",
            "📚Определение EN": "interdisciplinary branch of linguistics, combining knowledge and research from cognitive science, cognitive psychology, neuropsychology and linguistics.",
            "🔍Источник": " Словарь лингвистических терминов Т.В. Жеребило.  Robinson, Peter (2008). Handbook of Cognitive Linguistics and Second Language Acquisition. Routledge. pp. 3–8."
        },
"когнитивная грамматика": {
            "📚Определение RU": "Грамматические концепции и грамматические модели описания языков, ориентированные на рассмотрение когнитивных аспектов языковых явлений: восприятия, памяти, мышления, внимания.",
            "📚Определение EN": "theory of grammar that seeks to characterize, in a psychologically realistic way, those structures and abilities that constitute a speaker's grasp of linguistic convention, and to relate them to other cognitive processes.",
            "🔍Источник": "Словарь лингвистических терминов Т.В. Жеребило.  Oxford language."
        },

"cognitive grammar": {
            "📚Определение RU": "Грамматические концепции и грамматические модели описания языков, ориентированные на рассмотрение когнитивных аспектов языковых явлений: восприятия, памяти, мышления, внимания.",
            "📚Определение EN": "theory of grammar that seeks to characterize, in a psychologically realistic way, those structures and abilities that constitute a speaker's grasp of linguistic convention, and to relate them to other cognitive processes.",
            "🔍Источник": " Словарь лингвистических терминов Т.В. Жеребило.  Oxford language."
        },
"лексема": {
            "📚Определение RU": "Единица словаря языка.",
            "📚Определение EN": "basic lexical unit of a language consisting of one word or several words, the elements of which do not separately convey the meaning of the whole.",
            "🔍Источник": "Словарь лингвистических терминов Т.В. Жеребило.  Oxford language."
        },

"lexeme": {
            "📚Определение RU": "Единица словаря языка.",
            "📚Определение EN": "basic lexical unit of a language consisting of one word or several words, the elements of which do not separately convey the meaning of the whole.",
            "🔍Источник": " Словарь лингвистических терминов Т.В. Жеребило.  Oxford language."
        },
"лексикология": {
            "📚Определение RU": "Раздел языкознания, занимающийся изучением лексики.", "📚Определение EN": "branch of linguistics that analyzes the lexicon of a specific language.",
            "🔍Источник": "Словарь лингвистических терминов Т.В. Жеребило. Babich, Galina Nikolaevna (2016)."
        },
"lexicology": {
            "📚Определение RU": "Раздел языкознания, занимающийся изучением лексики.",
            "📚Определение EN": "branch of linguistics that analyzes the lexicon of a specific language.",
            "🔍Источник": " Словарь лингвистических терминов Т.В. Жеребило. Babich, Galina Nikolaevna (2016)."
  },
"метаязык": {
            "📚Определение RU": "Язык, используемый для описания самого языка, важнейшей составляющей которого являются термины.",
            "📚Определение EN": "a form of language or set of terms used for the description or analysis of another language.",
            "🔍Источник": "Словарь лингвистических терминов Т.В. Жеребило. Oxford Languages."
        },
"metalanguage": {
            "📚Определение RU": "Язык, используемый для описания самого языка, важнейшей составляющей которого являются термины.",
            "📚Определение EN": "form of language or set of terms used for the description or analysis of another language.",
            "🔍Источник": " Словарь лингвистических терминов Т.В. Жеребило. Oxford Languages."
  },
"метонимия": {
            "📚Определение RU": "Замена слова другим на основе связи их значений по смежности.",
            "📚Определение EN": "substitution of the name of an attribute or adjunct for that of the thing meant.",
            "🔍Источник": "Словарь лингвистических терминов Т.В. Жеребило. Oxford Languages."
        },
"metonymy": {
            "📚Определение RU": "Замена слова другим на основе связи их значений по смежности.",
            "📚Определение EN": "substitution of the name of an attribute or adjunct for that of the thing meant.",
            "🔍Источник": " Словарь лингвистических терминов Т.В. Жеребило. Oxford Languages."
        },

    },
    "педагогика": {
        "Дидактика": {
            "📚Определение RU":
            "Теория образования и обучения, отрасль педагогики.",
            "📚Определение EN":
            "The theory of education and learning is a branch of pedagogy.",
            "🔍Источник":
            "https://pedagogical.academic.ru/196/%D0%94%D0%98%D0%94%D0%90%D0%9A%D0%A2%D0%98%D0%9A%D0%90"
        },
        "Педагогика": {
            "📚Определение RU":
            "Наука о воспитании детей.",
            "📚Определение EN":
            "The science of educating children.",
            "🔍Источник":
            "https://vygotsky.academic.ru/100/%D0%BF%D0%B5%D0%B4%D0%B0%D0%B3%D0%BE%D0%B3%D0%B8%D0%BA%D0%B0"
        },
        "Образование": {
            "📚Определение RU":
            "Процесс усвоения знаний, обучение, просвещение.",
            "📚Определение EN":
            "The process of acquiring knowledge, learning, and enlightenment.",
            "🔍Источник": "https://dic.academic.ru/dic.nsf/ushakov/894386"
        },
        "Воспитание": {
            "📚Определение RU":
            "Процесс социализации индивида, становления и развития его как личности на протяжении всей жизни в ходе собственной активности и под влиянием природной, социальной и культурной среды, в т. ч. специально организованной целенаправленной деятельности родителей и педагогов.",
            "📚Определение EN":
            "The process of socialization of an individual, the formation and development of their personality throughout life, through their own activity and under the influence of natural, social, and cultural environments, including specifically organized and purposeful activities by parents and educators.",
            "🔍Источник":
            "https://psychology.academic.ru/348/%D0%B2%D0%BE%D1%81%D0%BF%D0%B8%D1%82%D0%B0%D0%BD%D0%B8%D0%B5"
        },
        "Самообразование": {
            "📚Определение RU":
            "Овладение знаниями, навыками, умениями по инициативе самого обучающегося в отношении предмета знаний (чем заниматься), объема и источника познания, установления продолжительности и времени проведения занятий, а также выбора форм удовлетворения познавательных интересов и потребностей.",
            "📚Определение EN":
            "The acquisition of knowledge, skills, and competencies initiated by the learner regarding the subject of study (what to engage in), the scope and sources of knowledge, the establishment of the duration and timing of activities, as well as the choice of forms to satisfy cognitive interests and needs.",
            "🔍Источник":
            "https://methodological_terms.academic.ru/1751/%D0%A1%D0%90%D0%9C%D0%9E%D0%9E%D0%91%D0%A0%D0%90%D0%97%D0%9E%D0%92%D0%90%D0%9D%D0%98%D0%95"
        },
        "Педагогическая культура": {
            "📚Определение RU":
            "Совокупность достижений в области обучения и воспитания.",
            "📚Определение EN":
            "A set of achievements in the field of education and upbringing.",
            "🔍Источник":
            "https://professional_education.academic.ru/1876/%D0%9F%D0%95%D0%94%D0%90%D0%93%D0%9E%D0%93%D0%98%D0%A7%D0%95%D0%A1%D0%9A%D0%90%D0%AF_%D0%9A%D0%A3%D0%9B%D0%AC%D0%A3%D0%A3%D0%A0%D0%90"
        },
        "Педагогическая задача": {
            "📚Определение RU":
            "Результат осознания педагогом цели обучения или воспитания, а также условий и способов ее реализации на практике.",
            "📚Определение EN":
            "The result of the educator's awareness of the goals of teaching or upbringing, as well as the conditions and methods for their practical implementation.",
            "🔍Источник":
            "https://social_pedagogy.academic.ru/477/%D0%9F%D0%B5%D0%B4%D0%B0%D0%B3%D0%BE%D0%B3%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B0%D1%8F_%D0%B7%D0%B0%D0%B4%D0%B0%D1%87%D0%B0"
        },
        "Педагогическая ситуация": {
            "📚Определение RU":
            "Составная часть педагогического процесса, характеризующая его состояние в данный момент и в данных условиях.",
            "📚Определение EN":
            "A component of the pedagogical process, characterizing its state at a given moment and under specific conditions.",
            "🔍Источник":
            "https://spiritual_culture.academic.ru/1635/%D0%9F%D0%B5%D0%B4%D0%B0%D0%B3%D0%BE%D0%B3%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B0%D1%8F_%D1%81%D0%B8%D1%82%D1%83%D0%B0%D1%86%D0%B8%D1%8F"
        },
        "Педагогическая диагностика": {
            "📚Определение RU":
            "Совокупность приемов контроля и оценки, направленных на совершенствование учебного процесса.",
            "📚Определение EN":
            "A set of methods for monitoring and evaluating aimed at improving the educational process.",
            "🔍Источник":
            "https://methodological_terms.academic.ru/1296/%D0%9F%D0%95%D0%94%D0%90%D0%93%D0%9E%D0%93%D0%98%D0%A7%D0%95%D0%A1%D0%9A%D0%90%D0%AF_%D0%94%D0%98%D0%90%D0%93%D0%9D%D0%9E%D0%A1%D0%A2%D0%98%D0%9A%D0%90"
        },
        "Педагогическая деятельность учителя": {
            "📚Определение RU":
            "Деятельность педагога, направленная на планирование, организацию и реализацию процесса образования, целью которого на занятиях по языку является формирование коммуникативной компетенции учащихся на изучаемом языке.",
            "📚Определение EN":
            "The activities of an educator aimed at planning, organizing, and implementing the educational process.",
            "🔍Источник":
            "https://methodological_terms.academic.ru/1295/%D0%9F%D0%95%D0%94%D0%90%D0%93%D0%9E%D0%93%D0%98%D0%A7%D0%95%D0%A1%D0%9A%D0%90%D0%AF_D0%94%D0%AF%D0%A2%D0%95%D0%9B%D0%AC%D0%9D%D0%9E%D0%A1%D0%A2%D0%AC_%D0%A3%D0%A7%D0%98%D0%A2%D0%95%D0%9B%D0%AF"
        },
        "Педагогическая система": {
            "📚Определение RU":
            "Целостное единство всех факторов, способствующих достижению поставленных целей развития воспитанников.",
            "📚Определение EN":
            "A holistic unity of all factors that contribute to achieving the set goals for the development of students.",
            "🔍Источник":
            "https://spiritual_culture.academic.ru/1634/%D0%9F%D0%B5%D0%B4%D0%B0%D0%B3%D0%BE%D0%B3%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B0%D1%8F_%D1%81%D0%B8%D1%81%D1%82%D0%B5%D0%BC%D0%B0"
        },
        "Методика учебного предмета": {
            "📚Определение RU":
            "Частная дидактика, теория обучения определённому учебному предмету.",
            "📚Определение EN":
            "A specific branch of didactics, focusing on the theory of teaching a particular subject.",
            "🔍Источник":
            "https://pedagogical_dictionary.academic.ru/1868/%D0%9М%D0%B5%D1%82%D0%BE%D0%B4%D0%B8%D0%BA%D0%B0_%D1%83%D1%87%D0%B5%D0%B1%D0%BD%D0%BE%D0%B3%D0%BE_%D0%BF%D1%80%D0%B5%D0%B4%D0%BC%D0%B5%D1%82%D0%B0"
        },
        "Педагогическая технология": {
            "📚Определение RU":
            "Направление в современной дидактике, касающееся исследований в области: a) применения технических средств обучения в учебном процессе, б) совершенствования структуры и повышения эффективности учебного процесса.",
            "📚Определение EN":
            "A direction in modern didactics that focuses on research in the following areas: a) the application of technical means of education in the learning process, b) the improvement of the structure and enhancementof the effectiveness of the educational process.",
            "🔍Источник":
            "https://methodological_terms.academic.ru/1301/%D0%9F%D0%95%D0%94%D0%90%D0%93%D0%9E%D0%93%D0%98%D0%A7%D0%95%D0%A1%D0%9A%D0%90%D0%AF_%D0%A2%D0%95%D0%A5%D0%9D%D0%9E%D0%9B%D0%9E%D0%93%D0%98%D0%AF"
        },
        "Технология обучения": {
            "📚Определение RU":
            "Совокупность наиболее рациональных способов научной организации труда, обеспечивающих достижение поставленной цели обучения за минимальное время с наименьшей затратой сил и средств.",
            "📚Определение EN":
            "A set of the most rational methods for the scientific organization of labor aimed at achieving the educational goals with minimal time, effort, and resource expenditure.",
            "🔍Источник":
            "https://methodological_terms.academic.ru/2070/%D1%82%D0%B5%D1%85%D0%BD%D0%BE%D0%BB%D0%BE%D0%B3%D0%B8%D1%8F_%D0%BE%D0%B1%D1%83%D1%87%D0%B5%D0%BD%D0%B8%D1%8F"
        },
        "Проектная методика": {
            "📚Определение RU":
            "Одна из технологий обучения, в том числе иностранному языку, основанная на моделировании социального взаимодействия в малой группе в ходе учебного процесса.",
            "📚Определение EN":
            "This is a teaching technology, including foreign language instruction, based on simulating social interaction in small groups during the learning process.",
            "🔍Источник":
            "https://methodological_terms.academic.ru/1526/%D0%BF%D1%80%D0%BE%D0%B5%D0%BA%D1%82%D0%BD%D0%B0%D1%8F_%D0%BC%D0%B5%D1%82%D0%BE%D0%B4%D0%B8%D0%BA%D0%B0"
        },
        "Факультативные занятия": {
            "📚Определение RU":
            "Один из видов дифференциации обучения по интересам.",
            "📚Определение EN":
            "A form of differentiated education based on interests, allowing students to choose subjects of their preference.",
            "🔍Источник":
            "https://rus-pedagogical-dict.slovaronline.com/3312-%D0%A4%D0%B0%D0%BA%D1%83%D0%BB%D1%8C%D1%82%D0%B0%D1%82%D0%B8%D0%B2%D0%BD%D1%8B%D0%B5%20%D0%B7%D0%B0%D0%BD%D1%8F%D1%82%D0%B8%D1%8F"
        },
        "Дифференциация обучения": {
            "📚Определение RU":
            "Форма организации учебной деятельности, учитывающая склонности, интересы, способности учащихся.",
            "📚Определение EN":
            "A form of organizing educational activities that takes into account the inclinations, interests, and abilities of students.",
            "🔍Источник":
            "https://rus-pedagogical-dict.slovaronline.com/1004-%D0%94%D0%B8%D1%84%D1%84%D0%B5%D1%80%D0%B5%D0%BD%D1%86%D0%B8%D0%B0%D1%86%D0%B8%D1%8F%20%D0%BE%D0%B1%D1%83%D1%87%D0%B5%D0%BD%D0%B8%D1%8F"
        },
        "Педагогика эволюционная": {
            "📚Определение RU":
            "Педагогика, в которой обучение рассматривается как процесс познавательной деятельности, соответствующий естественным законам развития ребенка.",
            "📚Определение EN":
            "Pedagogy in which learning is viewed as a process of cognitive activity that corresponds to the natural laws of child development.",
            "🔍Источник":
            "https://rus-pedagogical-dict.slovaronline.com/2363-%D0%9F%D0%B5%D0%B4%D0%B0%D0%B3%D0%BE%D0%B3%D0%B8%D0%BA%D0%B0%20%D1%8D%D0%B2%D0%BE%D0%BB%D1%8E%D1%86%D0%B8%D0%BE%D0%BD%D0%BD%D0%B0%D1%8F"
        },
        "Дактилология": {
            "📚Определение RU":
            "Дактильная речь, ручная азбука, применяемая глухими людьми для общения.",
            "📚Определение EN":
            "Dactyl speech, a manual alphabet used by deaf individuals for communication.",
            "🔍Источник":
            "https://rus-pedagogical-dict.slovaronline.com/884-%D0%94%D0%B0%D0%BA%D1%82%D0%B8%D0%BB%D0%BE%D0%BB%D0%BE%D0%B3%D0%B8%D1%8F"
        },
        "Аттестация": {
            "📚Определение RU":
            "Процедура оценивания достижений учащихся и деятельности преподавателей на каждой ступени и уровне образования.",
            "📚Определение EN":
            "A procedure for assessing the achievements of students and the performance of teachers at each stage and level of education.",
            "🔍Источник":
            "https://afag-eyubova.blogspot.com/p/blog-page_6541.html"
        },
        "Аудиовизуальные средства обучения": {
            "📚Определение RU":
            "Особая группа технических средств обучения, получивших наиболее широкое распространение в учебном процессе, включающая экранные и звуковые пособия.",
            "📚Определение EN":
            "A special group of technical teaching aids that have become widely used in the educational process, including visual and auditory materials.",
            "🔍Источник":
            "https://afag-eyubova.blogspot.com/p/blog-page_6541.html"
        },
        "Валеологическое образование и воспитание": {
            "📚Определение RU":
            "Воспитание у учащихся потребности в здоровье, формирование у них научного понимания сущности здорового образа жизни и выработки соответствующего поведения.",
            "📚Определение EN":
            "Fostering a need for health among students, developing a scientific understanding of the essence of a healthy lifestyle, and cultivating appropriate behavior.",
            "🔍Источник":
            "https://afag-eyubova.blogspot.com/p/blog-page_6541.html"
        },
        "Внеурочная работа": {
            "📚Определение RU":
            "Составная часть учебно-воспитательного процесса в школе и профтехучилище, одна из форм организации свободного времени учащихся.",
            "📚Определение EN":
            "A component of the educational process in schools and vocational colleges, serving as a form of organizing students' free time.",
            "🔍Источник":
            "https://afag-eyubova.blogspot.com/p/blog-page_6541.html"
        },
        "Групповая работа": {
            "📚Определение RU":
            "Форма организации учебно-познавательной деятельности на уроке, предполагающая функционирование разных малых групп, работающих как над общими, так и над специфическими заданиями педагога.",
            "📚Определение EN":
            "A form of organizing educational and cognitive activities in the classroom, involving various small groups working on both common and specific tasks assigned by the teacher.",
            "🔍Источник":
            "https://afag-eyubova.blogspot.com/p/blog-page_6541.html"
        },
        "Дистанционное обучение": {
            "📚Определение RU":
            "Форма обучения, основанная на переписках с помощью электронных, телекоммуникационных средств и средств программного обеспечения.",
            "📚Определение EN":
            "A form of education based on correspondence using electronic, telecommunication means, and software tools.",
            "🔍Источник": ""
        },

"Дидактика": {
    "📚Определение RU": "теория образования и обучения, отрасль педагогики.",
    "📚Определение EN": "The theory of education and learning is a branch of pedagogy.",
    "🔍Источник": "https://pedagogical.academic.ru/196/%D0%94%D0%98%D0%94%D0%90%D0%9A%D0%A2%D0%98%D0%9A%D0%90"
},

"Didactics": {
    "📚Определение RU": "теория образования и обучения, отрасль педагогики.",
    "📚Определение EN": "The theory of education and learning is a branch of pedagogy.",
    "🔍Источник": "https://pedagogical.academic.ru/196/%D0%94%D0%98%D0%94%D0%90%D0%9A%D0%A2%D0%98%D0%9A%D0%90"
},

"Педагогика": {
    "📚Определение RU": "наука о воспитании детей.",
    "📚Определение EN": "The science of educating children.",
    "🔍Источник": "https://vygotsky.academic.ru/100/%D0%BF%D0%B5%D0%B4%D0%B0%D0%B3%D0%BE%D0%B3%D0%B8%D0%BA%D0%B0"
},

"Pedagogy": {
    "📚Определение RU": "наука о воспитании детей.",
    "📚Определение EN": "The science of educating children.",
    "🔍Источник": "https://vygotsky.academic.ru/100/%D0%BF%D0%B5%D0%B4%D0%B0%D0%B3%D0%BE%D0%B3%D0%B8%D0%BA%D0%B0"
},


"Образование": {
    "📚Определение RU": "процесс усвоения знаний, обучение, просвещение.",
    "📚Определение EN": "The process of acquiring knowledge, learning, and enlightenment.",
    "🔍Источник": "https://dic.academic.ru/dic.nsf/ushakov/894386"
},

"Education": {
    "📚Определение RU": "процесс усвоения знаний, обучение, просвещение.",
    "📚Определение EN": "The process of acquiring knowledge, learning, and enlightenment.",
    "🔍Источник": "https://dic.academic.ru/dic.nsf/ushakov/894386"
},

"Воспитание": {
    "📚Определение RU": "процесс социализации индивида, становления и развития его как личности на протяжении всей жизни.",
    "📚Определение EN": "The process of socialization of an individual, the formation and development of their personality throughout life.",
    "🔍Источник": "https://psychology.academic.ru/348/%D0%B2%D0%BE%D1%81%D0%BF%D0%B8%D1%82%D0%B0%D0%BD%D0%B8%D0%B5"
},

"Воспитание": {
    "📚Определение RU": "процесс социализации индивида, становления и развития его как личности на протяжении всей жизни.",
    "📚Определение EN": "The process of socialization of an individual, the formation and development of their personality throughout life.",
    "🔍Источник": "https://psychology.academic.ru/348/%D0%B2%D0%BE%D1%81%D0%BF%D0%B8%D1%82%D0%B0%D0%BD%D0%B8%D0%B5"
},

"Upbringing": {
    "📚Определение RU": "процесс социализации индивида, становления и развития его как личности на протяжении всей жизни.",
    "📚Определение EN": "The process of socialization of an individual, the formation and development of their personality throughout life.",
    "🔍Источник": "https://psychology.academic.ru/348/%D0%B2%D0%BE%D1%81%D0%BF%D0%B8%D1%82%D0%B0%D0%BD%D0%B8%D0%B5"
},

"Самообразование": {
    "📚Определение RU": "овладение знаниями, навыками, умениями по инициативе самого обучающегося.",
    "📚Определение EN": "The acquisition of knowledge, skills, and competencies initiated by the learner.",
    "🔍Источник": "https://methodological_terms.academic.ru/1751/%D0%A1%D0%90%D0%9C%D0%9E%D0%9E%D0%91%D0%A0%D0%90%D0%97%D0%9E%D0%92%D0%90%D0%9D%D0%98%D0%95"
},

"Self-education": {
    "📚Определение RU": "овладение знаниями, навыками, умениями по инициативе самого обучающегося.",
    "📚Определение EN": "The acquisition of knowledge, skills, and competencies initiated by the learner.",
    "🔍Источник": "https://methodological_terms.academic.ru/1751/%D0%A1%D0%90%D0%9C%D0%9E%D0%9E%D0%91%D0%A0%D0%90%D0%97%D0%9E%D0%92%D0%90%D0%9D%D0%98%D0%95"
},


"Педагогическая культура": {
    "📚Определение RU": "совокупность достижений в области обучения и воспитания.",
    "📚Определение EN": "A set of achievements in the field of education and upbringing.",
    "🔍Источник": "https://professional_education.academic.ru/1876/%D0%9F%D0%95%D0%94%D0%90%D0%93%D0%9E%D0%93%D0%98%D0%A7%D0%95%D0%A1%D0%9A%D0%90%D0%AF_%D0%9A%D0%A3%D0%9B%D0%AC%D0%A2%D0%A3%D0%A0%D0%90"
}, 

"Pedagogical culture": {
    "📚Определение RU": "совокупность достижений в области обучения и воспитания.",
    "📚Определение EN": "A set of achievements in the field of education and upbringing.",
    "🔍Источник": "https://professional_education.academic.ru/1876/%D0%9F%D0%95%D0%94%D0%90%D0%93%D0%9E%D0%93%D0%98%D0%A7%D0%95%D0%A1%D0%9A%D0%90%D0%AF_%D0%9A%D0%A3%D0%9B%D0%AC%D0%A2%D0%A3%D0%A0%D0%90"
},


"Педагогическая задача": {
    "📚Определение RU": "результат осознания педагогом цели обучения или воспитания, а также условий и способов ее реализации.",
    "📚Определение EN": "The result of the educator's awareness of the goals of teaching or upbringing, as well as the conditions and methods for their implementation.",
    "🔍Источник": "https://social_pedagogy.academic.ru/477/%D0%9F%D0%B5%D0%B4%D0%B0%D0%B3%D0%BE%D0%B3%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B0%D1%8F_%D0%B7%D0%B0%D0%B4%D0%B0%D1%87%D0%B0"
},

"Pedagogical task": {
    "📚Определение RU": "результат осознания педагогом цели обучения или воспитания, а также условий и способов ее реализации.",
    "📚Определение EN": "The result of the educator's awareness of the goals of teaching or upbringing, as well as the conditions and methods for their implementation.",
    "🔍Источник": "https://social_pedagogy.academic.ru/477/%D0%9F%D0%B5%D0%B4%D0%B0%D0%B3%D0%BE%D0%B3%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B0%D1%8F_%D0%B7%D0%B0%D0%B4%D0%B0%D1%87%D0%B0"
},

"Методика учебного предмета": {
    "📚Определение RU": "частная дидактика, теория обучения определённому учебному предмету.",
    "📚Определение EN": "A specific branch of didactics, focusing on the theory of teaching a particular subject.",
    "🔍Источник": "https://pedagogical_dictionary.academic.ru/1868/%D0%9C%D0%B5%D1%82%D0%BE%D0%B4%D0%B8%D0%BA%D0%B0_%D1%83%D1%87%D0%B5%D0%B1%D0%BD%D0%BE%D0%B3%D0%BE_%D0%BF%D1%80%D0%B5%D0%B4%D0%BC%D0%B5%D1%82%D0%B0"
},

"Teaching methodology of a subject": {
    "📚Определение RU": "частная дидактика, теория обучения определённому учебному предмету.",
    "📚Определение EN": "A specific branch of didactics, focusing on the theory of teaching a particular subject.",
    "🔍Источник": "https://pedagogical_dictionary.academic.ru/1868/%D0%9C%D0%B5%D1%82%D0%BE%D0%B4%D0%B8%D0%BA%D0%B0_%D1%83%D1%87%D0%B5%D0%B1%D0%BD%D0%BE%D0%B3%D0%BE_%D0%BF%D1%80%D0%B5%D0%B4%D0%BC%D0%B5%D1%82%D0%B0"
},

"Технология обучения": {
    "📚Определение RU": "совокупность наиболее рациональных способов научной организации труда, обеспечивающих достижение поставленной цели обучения.",
    "📚Определение EN": "A set of the most rational methods for the scientific organization of labor aimed at achieving educational goals.",
    "🔍Источник": "https://methodological_terms.academic.ru/2070/%D1%82%D0%B5%D1%85%D0%BD%D0%BE%D0%BB%D0%BE%D0%B3%D0%B8%D1%8F_%D0%BE%D0%B1%D1%83%D1%87%D0%B5%D0%BD%D0%B8%D1%8F"
},

"Learning technology": {
    "📚Определение RU": "совокупность наиболее рациональных способов научной организации труда, обеспечивающих достижение поставленной цели обучения.",
    "📚Определение EN": "A set of the most rational methods for the scientific organization of labor aimed at achieving educational goals.",
    "🔍Источник": "https://methodological_terms.academic.ru/2070/%D1%82%D0%B5%D1%85%D0%BD%D0%BE%D0%BB%D0%BE%D0%B3%D0%B8%D1%8F_%D0%BE%D0%B1%D1%83%D1%87%D0%B5%D0%BD%D0%B8%D1%8F"
},

"Проектная методика": {
    "📚Определение RU": "одна из технологий обучения, основанная на моделировании социального взаимодействия в малой группе.",
    "📚Определение EN": "A teaching technology based on simulating social interaction in small groups.",
    "🔍Источник": "https://methodological_terms.academic.ru/1526/%D0%BF%D1%80%D0%BE%D0%B5%D0%BA%D1%82%D0%BD%D0%B0%D1%8F_%D0%BC%D0%B5%D1%82%D0%BE%D0%B4%D0%B8%D0%BA%D0%B0"
}, 

"Project-based methodology": {
    "📚Определение RU": "одна из технологий обучения, основанная на моделировании социального взаимодействия в малой группе.",
    "📚Определение EN": "A teaching technology based on simulating social interaction in small groups.",
    "🔍Источник": "https://methodological_terms.academic.ru/1526/%D0%BF%D1%80%D0%BE%D0%B5%D0%BA%D1%82%D0%BD%D0%B0%D1%8F_%D0%BC%D0%B5%D1%82%D0%BE%D0%B4%D0%B8%D0%BA%D0%B0"
},

"Факультативные занятия": {
    "📚Определение RU": "один из видов дифференциации обучения по интересам.",
    "📚Определение EN": "A form of differentiated education based on interests, allowing students to choose subjects of their preference.",
    "🔍Источник": "http://rus-pedagogical-dict.slovaronline.com/3312-%D0%A4%D0%B0%D0%BA%D1%83%D0%BB%D1%8C%D1%82%D0%B0%D1%82%D0%B8%D0%B2%D0%BD%D1%8B%D0%B5_%D0%B7%D0%B0%D0%BD%D1%8F%D1%82%D0%B8%D1%8F"
},

"Elective classes": {
    "📚Определение RU": "один из видов дифференциации обучения по интересам.",
    "📚Определение EN": "A form of differentiated education based on interests, allowing students to choose subjects of their preference.",
    "🔍Источник": "http://rus-pedagogical-dict.slovaronline.com/3312-%D0%A4%D0%B0%D0%BA%D1%83%D0%BB%D1%8C%D1%82%D0%B0%D1%82%D0%B8%D0%B2%D0%BD%D1%8B%D0%B5_%D0%B7%D0%B0%D0%BD%D1%8F%D1%82%D0%B8%D1%8F"
},

"Дифференциация обучения": {
    "📚Определение RU": "форма организации учебной деятельности, учитывающая склонности, интересы, способности учащихся.",
    "📚Определение EN": "A form of organizing educational activities that takes into account students' inclinations, interests, and abilities.",
    "🔍Источник": "https://rus-pedagogical-dict.slovaronline.com/1004-%D0%94%D0%B8%D1%84%D1%84%D0%B5%D1%80%D0%B5%D0%BD%D1%86%D0%B8%D0%B0%D1%86%D0%B8%D1%8F_%D0%BE%D0%B1%D1%83%D1%87%D0%B5%D0%BD%D0%B8%D1%8F"
}, 

"Differentiation of learning": {
    "📚Определение RU": "форма организации учебной деятельности, учитывающая склонности, интересы, способности учащихся.",
    "📚Определение EN": "A form of organizing educational activities that takes into account students' inclinations, interests, and abilities.",
    "🔍Источник": "https://rus-pedagogical-dict.slovaronline.com/1004-%D0%94%D0%B8%D1%84%D1%84%D0%B5%D1%80%D0%B5%D0%BD%D1%86%D0%B8%D0%B0%D1%86%D0%B8%D1%8F_%D0%BE%D0%B1%D1%83%D1%87%D0%B5%D0%BD%D0%B8%D1%8F"
},

"Педагогика эволюционная": {
    "📚Определение RU": "педагогика, в которой обучение рассматривается как процесс познавательной деятельности, соответствующий естественным законам развития ребенка.",
    "📚Определение EN": "Pedagogy in which learning is viewed as a process of cognitive activity that corresponds to the natural laws of child development.",
    "🔍Источник": "https://rus-pedagogical-dict.slovaronline.com/2363-%D0%9F%D0%B5%D0%B4%D0%B0%D0%B3%D0%BE%D0%B3%D0%B8%D0%BA%D0%B0_%D1%8D%D0%B2%D0%BE%D0%BB%D1%8E%D1%86%D0%B8%D0%BE%D0%BD%D0%BD%D0%B0%D1%8F"
},

"Evolutionary pedagogy": {
    "📚Определение RU": "педагогика, в которой обучение рассматривается как процесс познавательной деятельности, соответствующий естественным законам развития ребенка.",
    "📚Определение EN": "Pedagogy in which learning is viewed as a process of cognitive activity that corresponds to the natural laws of child development.",
    "🔍Источник": "https://rus-pedagogical-dict.slovaronline.com/2363-%D0%9F%D0%B5%D0%B4%D0%B0%D0%B3%D0%BE%D0%B3%D0%B8%D0%BA%D0%B0_%D1%8D%D0%B2%D0%BE%D0%BB%D1%8E%D1%86%D0%B8%D0%BE%D0%BD%D0%BD%D0%B0%D1%8F"
},

"Дактилология": {
    "📚Определение RU": "дактильная речь, ручная азбука, применяемая глухими людьми для общения.",
    "📚Определение EN": "Dactyl speech, a manual alphabet used by deaf individuals for communication.",
    "🔍Источник": "https://rus-pedagogical-dict.slovaronline.com/884-%D0%94%D0%B0%D0%BA%D1%82%D0%B8%D0%BB%D0%BE%D0%BB%D0%BE%D0%B3%D0%B8%D1%8F"
},

"Dactylology": {
    "📚Определение RU": "дактильная речь, ручная азбука, применяемая глухими людьми для общения.",
    "📚Определение EN": "Dactyl speech, a manual alphabet used by deaf individuals for communication.",
    "🔍Источник": "https://rus-pedagogical-dict.slovaronline.com/884-%D0%94%D0%B0%D0%BA%D1%82%D0%B8%D0%BB%D0%BE%D0%BB%D0%BE%D0%B3%D0%B8%D1%8F"
},

"Аттестация": {
    "📚Определение RU": "процедура оценивания достижений учащихся и деятельности преподавателей на каждой ступени и уровне образования.",
    "📚Определение EN": "A procedure for assessing students' achievements and teachers' performance at each stage and level of education.",
    "🔍Источник": "https://afag-eyubova.blogspot.com/p/blog-page_6541.html"
},

"Assessment": {
    "📚Определение RU": "процедура оценивания достижений учащихся и деятельности преподавателей на каждой ступени и уровне образования.",
    "📚Определение EN": "A procedure for assessing students' achievements and teachers' performance at each stage and level of education.",
    "🔍Источник": "https://afag-eyubova.blogspot.com/p/blog-page_6541.html"
},

"Аудиовизуальные средства обучения": {
    "📚Определение RU": "особая группа технических средств обучения, включающая экранные и звуковые пособия.",
    "📚Определение EN": "A special group of teaching aids that includes visual and auditory materials.",
    "🔍Источник": "https://afag-eyubova.blogspot.com/p/blog-page_6541.html"
},

"Audiovisual learning aids": {
    "📚Определение RU": "особая группа технических средств обучения, включающая экранные и звуковые пособия.",
    "📚Определение EN": "A special group of teaching aids that includes visual and auditory materials.",
    "🔍Источник": "https://afag-eyubova.blogspot.com/p/blog-page_6541.html"
},


"Валеологическое образование и воспитание": {
    "📚Определение RU": "воспитание у учащихся потребности в здоровье, формирование у них научного понимания сущности здорового образа жизни.",
    "📚Определение EN": "Fostering a need for health among students and developing their scientific understanding of a healthy lifestyle.",
    "🔍Источник": "https://afag-eyubova.blogspot.com/p/blog-page_6541.html"
},

"Valeological education and upbringing": {
    "📚Определение RU": "воспитание у учащихся потребности в здоровье, формирование у них научного понимания сущности здорового образа жизни.",
    "📚Определение EN": "Fostering a need for health among students and developing their scientific understanding of a healthy lifestyle.",
    "🔍Источник": "https://afag-eyubova.blogspot.com/p/blog-page_6541.html"
},

"Внеурочная работа": {
    "📚Определение RU": "составная часть учебно-воспитательного процесса в школе, одна из форм организации свободного времени учащихся.",
    "📚Определение EN": "A component of the educational process in schools, serving as a form of organizing students' free time.",
    "🔍Источник": "https://afag-eyubova.blogspot.com/p/blog-page_6541.html"
},

"Extracurricular activities": {
    "📚Определение RU": "составная часть учебно-воспитательного процесса в школе, одна из форм организации свободного времени учащихся.",
    "📚Определение EN": "A component of the educational process in schools, serving as a form of organizing students' free time.",
    "🔍Источник": "https://afag-eyubova.blogspot.com/p/blog-page_6541.html"
},


"Групповая работа": {
    "📚Определение RU": "форма организации учебно-познавательной деятельности на уроке, предполагающая функционирование разных малых групп.",
    "📚Определение EN": "A form of organizing educational and cognitive activities in the classroom involving various small groups.",
    "🔍Источник": "https://afag-eyubova.blogspot.com/p/blog-page_6541.html"
},

"Group work": {
    "📚Определение RU": "форма организации учебно-познавательной деятельности на уроке, предполагающая функционирование разных малых групп.",
    "📚Определение EN": "A form of organizing educational and cognitive activities in the classroom involving various small groups.",
    "🔍Источник": "https://afag-eyubova.blogspot.com/p/blog-page_6541.html"
},


"Дистанционное обучение": {
    "📚Определение RU": "форма обучения, основанная на переписках с помощью электронных, телекоммуникационных средств и средств программного обеспечения.",
    "📚Определение EN": "A form of education based on correspondence using electronic, telecommunication means, and software tools.",
    "🔍Источник": "https://afag-eyubova.blogspot.com/p/blog-page_6541.html"
},

"Distance learning": {
    "📚Определение RU": "форма обучения, основанная на переписках с помощью электронных, телекоммуникационных средств и средств программного обеспечения.",
    "📚Определение EN": "A form of education based on correspondence using electronic, telecommunication means, and software tools.",
    "🔍Источник": "https://afag-eyubova.blogspot.com/p/blog-page_6541.html"
},

"Инварианты педагогические": {
    "📚Определение RU": "педагогические истины, не подлежащие пересмотру.",
    "📚Определение EN": "Pedagogical truths that are not subject to revision.",
    "🔍Источник": "https://afag-eyubova.blogspot.com/p/blog-page_6541.html"
},

"Pedagogical invariants": {
    "📚Определение RU": "педагогические истины, не подлежащие пересмотру.",
    "📚Определение EN": "Pedagogical truths that are not subject to revision.",
    "🔍Источник": "https://afag-eyubova.blogspot.com/p/blog-page_6541.html"
},

"Индивидуализация обучения": {
    "📚Определение RU": "один из дидактических принципов, учитывающий личностные особенности обучаемых, их социальный и академический опыт.",
    "📚Определение EN": "A didactic principle that takes into account the personal characteristics, social and academic experiences of learners.",
    "🔍Источник": "https://afag-eyubova.blogspot.com/p/blog-page_6541.html"
},

"Individualization of learning": {
    "📚Определение RU": "один из дидактических принципов, учитывающий личностные особенности обучаемых, их социальный и академический опыт.",
    "📚Определение EN": "A didactic principle that takes into account the personal characteristics, social and academic experiences of learners.",
    "🔍Источник": "https://afag-eyubova.blogspot.com/p/blog-page_6541.html"
},

"Исследовательский метод обучения": {
    "📚Определение RU": "организация поисковой, познавательной деятельности учащихся путем постановки педагогом задач, требующих самостоятельного творческого решения.",
    "📚Определение EN": "The organization of exploratory and cognitive activities of students through tasks set by the teacher that require independent creative solutions.",
    "🔍Источник": "https://afag-eyubova.blogspot.com/p/blog-page_6541.html"
},

"Research-based teaching method": {
    "📚Определение RU": "организация поисковой, познавательной деятельности учащихся путем постановки педагогом задач, требующих самостоятельного творческого решения.",
    "📚Определение EN": "The organization of exploratory and cognitive activities of students through tasks set by the teacher that require independent creative solutions.",
    "🔍Источник": "https://afag-eyubova.blogspot.com/p/blog-page_6541.html"
},

"Конспект урока": {
    "📚Определение RU": "содержит формулировку темы, задачи урока, этапы урока, оборудование, задания для учащихся.",
    "📚Определение EN": "Includes the formulation of the topic, lesson objectives, stages of the lesson, equipment, and tasks for students.",
    "🔍Источник": "https://afag-eyubova.blogspot.com/p/blog-page_6541.html"
},

"Lesson plan": {
    "📚Определение RU": "содержит формулировку темы, задачи урока, этапы урока, оборудование, задания для учащихся.",
    "📚Определение EN": "Includes the formulation of the topic, lesson objectives, stages of the lesson, equipment, and tasks for students.",
    "🔍Источник": "https://afag-eyubova.blogspot.com/p/blog-page_6541.html"
},

"Личностно-ориентированное содержание образования": {
    "📚Определение RU": "подход в проектировании содержания профессионального образования, направленный на развитие личности.",
    "📚Определение EN": "An approach to designing vocational education content aimed at personal development.",
    "🔍Источник": "https://afag-eyubova.blogspot.com/p/blog-page_6541.html"
},

"Personality-oriented education content": {
    "📚Определение RU": "подход в проектировании содержания профессионального образования, направленный на развитие личности.",
    "📚Определение EN": "An approach to designing vocational education content aimed at personal development.",
    "🔍Источник": "https://afag-eyubova.blogspot.com/p/blog-page_6541.html"
},

"Инклюзивное образование": {
    "📚Определение RU": "подход, обеспечивающий равный доступ к образованию для всех обучающихся с учетом разнообразия их потребностей.",
    "📚Определение EN": "An approach that ensures equal access to education for all students, taking into account the diversity of their needs.",
    "🔍Источник": "https://unesdoc.unesco.org/ark:/48223/pf0000246974"
},

"Inclusive education": {
    "📚Определение RU": "подход, обеспечивающий равный доступ к образованию для всех обучающихся с учетом разнообразия их потребностей.",
    "📚Определение EN": "An approach that ensures equal access to education for all students, taking into account the diversity of their needs.",
    "🔍Источник": "https://unesdoc.unesco.org/ark:/48223/pf0000246974"
},

"Формирующее оценивание": {
    "📚Определение RU": "система оценивания, направленная на выявление учебных достижений для коррекции процесса обучения.",
    "📚Определение EN": "An assessment system aimed at identifying learning achievements to adjust the teaching process.",
    "🔍Источник": "https://www.oecd.org/education/ceri/assessmentforlearning.htm"
},

"Formative assessment": {
    "📚Определение RU": "система оценивания, направленная на выявление учебных достижений для коррекции процесса обучения.",
    "📚Определение EN": "An assessment system aimed at identifying learning achievements to adjust the teaching process.",
    "🔍Источник": "https://www.oecd.org/education/ceri/assessmentforlearning.htm"
},

"Смешанное обучение": {
    "📚Определение RU": "образовательный подход, сочетающий традиционные и цифровые методы обучения.",
    "📚Определение EN": "An educational approach combining traditional and digital teaching methods.",
    "🔍Источник": "https://teachonline.ca/tools-trends/blended-learning"
},

"Blended learning": {
    "📚Определение RU": "образовательный подход, сочетающий традиционные и цифровые методы обучения.",
    "📚Определение EN": "An educational approach combining traditional and digital teaching methods.",
    "🔍Источник": "https://teachonline.ca/tools-trends/blended-learning"
},

"Критическое мышление": {
    "📚Определение RU": "способность анализировать информацию, выявлять логические ошибки и принимать обоснованные решения.",
    "📚Определение EN": "The ability to analyze information, identify logical fallacies, and make reasoned decisions.",
    "🔍Источник": "https://www.criticalthinking.org/pages/defining-critical-thinking/766"
},

"Critical thinking": {
    "📚Определение RU": "способность анализировать информацию, выявлять логические ошибки и принимать обоснованные решения.",
    "📚Определение EN": "The ability to analyze information, identify logical fallacies, and make reasoned decisions.",
    "🔍Источник": "https://www.criticalthinking.org/pages/defining-critical-thinking/766"
},

"Педагогический дизайн": {
    "📚Определение RU": "систематический процесс создания эффективных образовательных программ и материалов.",
    "📚Определение EN": "A systematic process of designing effective educational programs and materials.",
    "🔍Источник": "https://www.instructionaldesign.org/"
},

"Instructional design": {
    "📚Определение RU": "систематический процесс создания эффективных образовательных программ и материалов.",
    "📚Определение EN": "A systematic process of designing effective educational programs and materials.",
    "🔍Источник": "https://www.instructionaldesign.org/"
},

"Электронное обучение": {
    "📚Определение RU": "образовательный процесс с использованием информационных технологий и электронных средств обучения.",
    "📚Определение EN": "Educational process using information technologies and electronic learning tools.",
    "🔍Источник": "https://elearningindustry.com/what-is-elearning"
},

"E-learning": {
    "📚Определение RU": "образовательный процесс с использованием информационных технологий и электронных средств обучения.",
    "📚Определение EN": "Educational process using information technologies and electronic learning tools.",
    "🔍Источник": "https://elearningindustry.com/what-is-elearning"
},

"Геймификация в образовании": {
    "📚Определение RU": "применение игровых элементов и механик в неигровом образовательном процессе.",
    "📚Определение EN": "Application of game elements and mechanics in non-game educational process.",
    "🔍Источник": "https://www.gamified.uk/gamification-education/"
},

"Gamification in education": {
    "📚Определение RU": "применение игровых элементов и механик в неигровом образовательном процессе.",
    "📚Определение EN": "Application of game elements and mechanics in non-game educational process.",
    "🔍Источник": "https://www.gamified.uk/gamification-education/"
},

"Компетентностный подход": {
    "📚Определение RU": "ориентация образовательного процесса на формирование у обучающихся практических навыков и компетенций.",
    "📚Определение EN": "Orientation of the educational process towards developing practical skills and competencies in students.",
    "🔍Источник": "https://www.oecd.org/education/competency-based-education.htm"
},

"Competency-based approach": {
    "📚Определение RU": "ориентация образовательного процесса на формирование у обучающихся практических навыков и компетенций.",
    "📚Определение EN": "Orientation of the educational process towards developing practical skills and competencies in students.",
    "🔍Источник": "https://www.oecd.org/education/competency-based-education.htm"
},

"Педагогическое сопровождение": {
    "📚Определение RU": "система профессиональной деятельности педагога, направленная на поддержку развития обучающегося.",
    "📚Определение EN": "System of teacher's professional activity aimed at supporting student development.",
    "🔍Источник": "https://eric.ed.gov/?id=ED573643"
},

"Pedagogical support": {
    "📚Определение RU": "система профессиональной деятельности педагога, направленная на поддержку развития обучающегося.",
    "📚Определение EN": "System of teacher's professional activity aimed at supporting student development.",
    "🔍Источник": "https://eric.ed.gov/?id=ED573643"
},

"Образовательная среда": {
    "📚Определение RU": "совокупность условий, влияющих на обучение и развитие участников образовательного процесса.",
    "📚Определение EN": "Set of conditions affecting the learning and development of participants in the educational process.",
    "🔍Источник": "https://www.education.gov.uk/publications/standard/publicationDetail/Page1/DfES+0621+2004"
},

"Educational environment": {
    "📚Определение RU": "совокупность условий, влияющих на обучение и развитие участников образовательного процесса.",
    "📚Определение EN": "Set of conditions affecting the learning and development of participants in the educational process.",
    "🔍Источник": "https://www.education.gov.uk/publications/standard/publicationDetail/Page1/DfES+0621+2004"
},

"Метапредметные результаты": {
    "📚Определение RU": "освоенные обучающимися универсальные учебные действия, обеспечивающие овладение ключевыми компетенциями.",
    "📚Определение EN": "Mastered universal learning activities that ensure the acquisition of key competencies by students.",
    "🔍Источник": "https://fgos.ru/lms/wmc/wpcurs/page.php?id=142"
},

"Metasubject results": {
    "📚Определение RU": "освоенные обучающимися универсальные учебные действия, обеспечивающие овладение ключевыми компетенциями.",
    "📚Определение EN": "Mastered universal learning activities that ensure the acquisition of key competencies by students.",
    "🔍Источник": "https://fgos.ru/lms/wmc/wpcurs/page.php?id=142"
},

"Функциональная грамотность": {
    "📚Определение RU": "способность человека использовать приобретённые знания для решения жизненных задач в различных сферах.",
    "📚Определение EN": "A person's ability to use acquired knowledge to solve life problems in various areas.",
    "🔍Источник": "https://минобрнауки.рф/документы/3423"
},

"Functional literacy": {
    "📚Определение RU": "способность человека использовать приобретённые знания для решения жизненных задач в различных сферах.",
    "📚Определение EN": "A person's ability to use acquired knowledge to solve life problems in various areas.",
    "🔍Источник": "https://минобрнауки.рф/документы/3423"
},

"Педагогическая технология": {
    "📚Определение RU": "совокупность методов, средств и приёмов, используемых для достижения планируемых образовательных результатов.",
    "📚Определение EN": "A set of methods, tools and techniques used to achieve planned educational outcomes.",
    "🔍Источник": "https://pedagogika.org/index.php/pedagogika-xxi-veka/115-pedagogicheskie-tekhnologii"
},

"Educational technology": {
    "📚Определение RU": "совокупность методов, средств и приёмов, используемых для достижения планируемых образовательных результатов.",
    "📚Определение EN": "A set of methods, tools and techniques used to achieve planned educational outcomes.",
    "🔍Источник": "https://pedagogika.org/index.php/pedagogika-xxi-veka/115-pedagogicheskie-tekhnologii"
},

"Универсальные учебные действия": {
    "📚Определение RU": "совокупность способов действий обучающегося, обеспечивающих самостоятельное усвоение новых знаний.",
    "📚Определение EN": "A set of student's actions that ensure independent acquisition of new knowledge.",
    "🔍Источник": "https://fgos.ru/lms/wmc/wpcurs/page.php?id=141"
},

"Universal learning activities": {
    "📚Определение RU": "совокупность способов действий обучающегося, обеспечивающих самостоятельное усвоение новых знаний.",
    "📚Определение EN": "A set of student's actions that ensure independent acquisition of new knowledge.",
    "🔍Источник": "https://fgos.ru/lms/wmc/wpcurs/page.php?id=141"
},

"Современные образовательные технологии": {
    "📚Определение RU": "инновационные подходы к организации образовательного процесса в условиях реализации ФГОС.",
    "📚Определение EN": "Innovative approaches to organizing the educational process in the context of the implementation of the Federal State Educational Standard.",
    "🔍Источник": "https://edu.ru/works/uchiteljam/sovremennye-obrazovatelnye-tekhnologii/"
},

"Modern educational technologies": {
    "📚Определение RU": "инновационные подходы к организации образовательного процесса в условиях реализации ФГОС.",
    "📚Определение EN": "Innovative approaches to organizing the educational process in the context of the implementation of the Federal State Educational Standard.",
    "🔍Источник": "https://edu.ru/works/uchiteljam/sovremennye-obrazovatelnye-tekhnologii/"
},

"Цифровая образовательная среда": {
    "📚Определение RU": "совокупность электронных ресурсов и технологий, используемых для организации образовательного процесса в цифровом формате.",
    "📚Определение EN": "A set of electronic resources and technologies used to organize the educational process in digital format.",
    "🔍Источник": "https://edu.gov.ru/national-project/digital-educational-environment/"
},

"Digital educational environment": {
    "📚Определение RU": "совокупность электронных ресурсов и технологий, используемых для организации образовательного процесса в цифровом формате.",
    "📚Определение EN": "A set of electronic resources and technologies used to organize the educational process in digital format.",
    "🔍Источник": "https://edu.gov.ru/national-project/digital-educational-environment/"
},

"Индивидуальная образовательная траектория": {
    "📚Определение RU": "персонализированный путь освоения учебной программы с учетом способностей и потребностей обучающегося.",
    "📚Определение EN": "Personalized path of mastering the curriculum, taking into account the student's abilities and needs.",
    "🔍Источник": "https://ioe.hse.ru/indobraz"
},

"Individual educational trajectory": {
    "📚Определение RU": "персонализированный путь освоения учебной программы с учетом способностей и потребностей обучающегося.",
    "📚Определение EN": "Personalized path of mastering the curriculum, taking into account the student's abilities and needs.",
    "🔍Источник": "https://ioe.hse.ru/indobraz"
},

"Проектная деятельность в школе": {
    "📚Определение RU": "метод обучения, основанный на выполнении учащимися исследовательских или практических проектов.",
    "📚Определение EN": "A teaching method based on students' implementation of research or practical projects.",
    "🔍Источник": "https://prosv.ru/pages/project-activity.html"
},

"Project activities at school": {
    "📚Определение RU": "метод обучения, основанный на выполнении учащимися исследовательских или практических проектов.",
    "📚Определение EN": "A teaching method based on students' implementation of research or practical projects.",
    "🔍Источник": "https://prosv.ru/pages/project-activity.html"
},

"Форсайт-сессия в образовании": {
    "📚Определение RU": "технология коллективного проектирования будущего образования с учетом современных трендов.",
    "📚Определение EN": "A technology for collective design of the future of education, taking into account current trends.",
    "🔍Источник": "https://foresight.hse.ru/education"
},

"Foresight session in education": {
    "📚Определение RU": "технология коллективного проектирования будущего образования с учетом современных трендов.",
    "📚Определение EN": "A technology for collective design of the future of education, taking into account current trends.",
    "🔍Источник": "https://foresight.hse.ru/education"
},

"Кейс-метод обучения": {
    "📚Определение RU": "технология обучения на основе анализа реальных или смоделированных профессиональных ситуаций.",
    "📚Определение EN": "A teaching technology based on the analysis of real or simulated professional situations.",
    "🔍Источник": "https://case.hse.ru/method"
},

"Case method of teaching": {
    "📚Определение RU": "технология обучения на основе анализа реальных или смоделированных профессиональных ситуаций.",
    "📚Определение EN": "A teaching technology based on the analysis of real or simulated professional situations.",
    "🔍Источник": "https://case.hse.ru/method"
},

"Образовательные квесты": {
    "📚Определение RU": "интерактивная образовательная технология, основанная на игровом сюжете с поэтапным решением задач.",
    "📚Определение EN": "Interactive educational technology based on a game plot with step-by-step problem solving.",
    "🔍Источник": "https://eduregion.ru/press-center/articles/obrazovatelnye-kvesty/"
},

"Educational quests": {
    "📚Определение RU": "интерактивная образовательная технология, основанная на игровом сюжете с поэтапным решением задач.",
    "📚Определение EN": "Interactive educational technology based on a game plot with step-by-step problem solving.",
    "🔍Источник": "https://eduregion.ru/press-center/articles/obrazovatelnye-kvesty/"
},

"Наставничество в образовании": {
    "📚Определение RU": "система сопровождения и поддержки обучающихся более опытными педагогами или студентами.",
    "📚Определение EN": "A system of support and guidance for students by more experienced teachers or students.",
    "🔍Источник": "https://минобрнауки.рф/наставничество"
},

"Mentoring in education": {
    "📚Определение RU": "система сопровождения и поддержки обучающихся более опытными педагогами или студентами.",
    "📚Определение EN": "A system of support and guidance for students by more experienced teachers or students.",
    "🔍Источник": "https://минобрнауки.рф/наставничество"
},

"Сторителлинг в обучении": {
    "📚Определение RU": "методика преподавания через создание и рассказывание историй для лучшего усвоения материала.",
    "📚Определение EN": "Teaching methodology through creating and telling stories for better material assimilation.",
    "🔍Источник": "https://www.elibrary.ru/item.asp?id=38567228"
},

"Storytelling in education": {
    "📚Определение RU": "методика преподавания через создание и рассказывание историй для лучшего усвоения материала.",
    "📚Определение EN": "Teaching methodology through creating and telling stories for better material assimilation.",
    "🔍Источник": "https://www.elibrary.ru/item.asp?id=38567228"
},

"Рефлексия в образовательном процессе": {
    "📚Определение RU": "процесс осмысления и анализа обучающимися своей учебной деятельности и её результатов.",
    "📚Определение EN": "The process of students' comprehension and analysis of their learning activities and results.",
    "🔍Источник": "https://cyberleninka.ru/article/n/refleksiya-v-obrazovatelnom-protsesse"
},

"Reflection in educational process": {
    "📚Определение RU": "процесс осмысления и анализа обучающимися своей учебной деятельности и её результатов.",
    "📚Определение EN": "The process of students' comprehension and analysis of their learning activities and results.",
    "🔍Источник": "https://cyberleninka.ru/article/n/refleksiya-v-obrazovatelnom-protsesse"
},

"Педагогическая инноватика": {
    "📚Определение RU": "область педагогической науки, изучающая процессы создания, освоения и распространения педагогических новшеств.",
    "📚Определение EN": "The area of pedagogical science that studies the processes of creating, mastering and disseminating pedagogical innovations.",
    "🔍Источник": "https://pedagogika.org/pedagogicheskaya-innovatika"
},

"Pedagogical innovatics": {
    "📚Определение RU": "область педагогической науки, изучающая процессы создания, освоения и распространения педагогических новшеств.",
    "📚Определение EN": "The area of pedagogical science that studies the processes of creating, mastering and disseminating pedagogical innovations.",
    "🔍Источник": "https://pedagogika.org/pedagogicheskaya-innovatika"
},

"Дидактический конструктор": {
    "📚Определение RU": "набор методических инструментов для проектирования учебных занятий в соответствии с ФГОС.",
    "📚Определение EN": "A set of methodological tools for designing lessons in accordance with the Federal State Educational Standard.",
    "🔍Источник": "https://fgos.ru/didactic-constructor"
},

"Didactic constructor": {
    "📚Определение RU": "набор методических инструментов для проектирования учебных занятий в соответствии с ФГОС.",
    "📚Определение EN": "A set of methodological tools for designing lessons in accordance with the Federal State Educational Standard.",
    "🔍Источник": "https://fgos.ru/didactic-constructor"
},

"Образовательный тьюторинг": {
    "📚Определение RU": "индивидуальное сопровождение обучающегося в процессе образования, направленное на раскрытие его потенциала.",
    "📚Определение EN": "Individual support of a student in the educational process aimed at revealing their potential.",
    "🔍Источник": "https://ioe.hse.ru/tutoring"
},

"Educational tutoring": {
    "📚Определение RU": "индивидуальное сопровождение обучающегося в процессе образования, направленное на раскрытие его потенциала.",
    "📚Определение EN": "Individual support of a student in the educational process aimed at revealing their potential.",
    "🔍Источник": "https://ioe.hse.ru/tutoring"
},

"Педагогический скрайбинг": {
    "📚Определение RU": "методика визуализации учебного материала через создание образов и схем в реальном времени.",
    "📚Определение EN": "A technique for visualizing educational material by creating images and diagrams in real time.",
    "🔍Источник": "https://www.elibrary.ru/item.asp?id=41234567"
},

"Pedagogical scribing": {
    "📚Определение RU": "методика визуализации учебного материала через создание образов и схем в реальном времени.",
    "📚Определение EN": "A technique for visualizing educational material by creating images and diagrams in real time.",
    "🔍Источник": "https://www.elibrary.ru/item.asp?id=41234567"
},

"Когнитивное обучение": {
    "📚Определение RU": "подход в образовании, основанный на закономерностях работы человеческого мышления и познавательных процессов.",
    "📚Определение EN": "An educational approach based on the patterns of human thinking and cognitive processes.",
    "🔍Источник": "https://psyjournals.ru/cognitive_learning"
},

"Cognitive learning": {
    "📚Определение RU": "подход в образовании, основанный на закономерностях работы человеческого мышления и познавательных процессов.",
    "📚Определение EN": "An educational approach based on the patterns of human thinking and cognitive processes.",
    "🔍Источник": "https://psyjournals.ru/cognitive_learning"
},

"Цифровой педагогический профиль": {
    "📚Определение RU": "совокупность цифровых компетенций и характеристик педагога в условиях цифровой трансформации образования.",
    "📚Определение EN": "The set of digital competencies and characteristics of a teacher in the context of digital transformation of education.",
    "🔍Источник": "https://digital.edu.ru/digital-profile"
},

"Digital pedagogical profile": {
    "📚Определение RU": "совокупность цифровых компетенций и характеристик педагога в условиях цифровой трансформации образования.",
    "📚Определение EN": "The set of digital competencies and characteristics of a teacher in the context of digital transformation of education.",
    "🔍Источник": "https://digital.edu.ru/digital-profile"
},
    },
    "экономика": {
        "инвестиции": {
            "📚Определение RU":
            "Ресурсы, вкладываемые в создание производственных или потребительских благ; как правило, имеется в виду вложение денег, но могут подразумеваться также материальные или трудовые ресурсы; в русском языке часто употребляется во множественном числе.",
            "📚Определение EN":
            "Resources invested in the creation of production or consumption goods; usually refers to the investment of money, but can also mean material or labor resources; in Russian it is often used in the plural.",
            "🔍Источник":
            "https://eng-rus-economy-dict.slovaronline.com/79385-investment"
        },
        "заработная плата": {
            "📚Определение RU":
            "Эк. тр., часто мн. заработная плата, зарплата (сумма, выплачиваемая работодателем наемному работнику в зависимости от количества отработанного времени или выполненного объема работ; часто устанавливается на почасовой или понедельной основе; обычно термин применяется к оплате труда рабочих и неквалифицированных работников; в статистике национального дохода рассматривается как элемент национального дохода наряду с процентом и рентой).",
            "📚Определение EN":
            "Ec. tr., often m. wage, salary (amount paid by an employer to an employee based on the amount of time worked or the amount of work performed; often set on an hourly or weekly basis; the term is usually applied to the wages of laborers and unskilled workers; in national income statistics, it is considered as an element of national income along with interest and rent).",
            "🔍Источник":
            "https://eng-rus-economy-dict.slovaronline.com/134217-wage"
        },
        "актив": {
            "📚Определение RU":
            "Эк. (любой объект, который может быть предметом владения частным лицом, организацией или государством и может использоваться для получения выгоды).",
            "📚Определение EN":
            "Econ. (any object that can be held by an individual, organization or the State and can be used to obtain a benefit).",
            "🔍Источник":
            "https://eng-rus-economy-dict.slovaronline.com/28966-asset"
        },
        "пассивный (залог)": {
            "📚Определение RU":
            "Пассивный (об инвестициях, при которых инвестор не принимает активного участия в управлении инвестируемым предприятием; также о доходах или убытках, связанных с деятельностью, в которых получатель дохода не принимает активного участия).",
            "📚Определение EN":
            "Passive (investments in which the investor does not actively participate in the management of the investee; also income or losses from activities in which the income recipient does not actively participate).",
            "🔍Источник":
            "https://eng-rus-economy-dict.slovaronline.com/100479-passive"
        },
        "дебет": {
            "📚Определение RU":
            "Левая сторона бухгалтерских счетов; в активных счетах — приход (получение денежных средств, материалов, увеличение себестоимости готовой продукции, увеличение задолженности покупателей и т. д.), в пассивных — расход (погашение обязательств, уменьшение капитала или получение убытка); в банковском учете отражает списание средств со счета клиента.",
            "📚Определение EN":
            "The left side of the accounting accounts; in active accounts - inflow (receipt of cash, materials, increase in the cost of finished goods, increase in the debt of buyers, etc.), in passive accounts - expenditure (repayment of liabilities, reduction of capital or receipt of loss); in bank accounting reflects the writing off of funds from the customer's account.",
            "🔍Источник":
            "https://eng-rus-economy-dict.slovaronline.com/51409-debit"
        },
        "кредит": {
            "📚Определение RU":
            "Банк. кредит (предоставление одним лицом другому лицу на фиксированный срок определенной суммы денег или отсрочки платежа за товар или услуги в обмен на вознаграждение в форме процента).",
            "📚Определение EN":
            "Bank. credit (granting by one person to another person for a fixed period of time a certain amount of money or deferred payment for goods or services in exchange for remuneration in the form of interest).",
            "🔍Источник":
            "https://eng-rus-economy-dict.slovaronline.com/48566-credit"
        },
        "налог на добавленную стоимость (НДС)": {
            "📚Определение RU":
            "Форма налогообложения добавленной в ходе производства стоимости продукта (услуги); взимается на каждой стадии производства и при продаже товара конечному потребителю (добавляется к цене продукции или услуги и перекладывается на потребителей); иногда называется налогом на потребление; расчетную сумму НДС производитель переводит в государственный бюджет за вычетом НДС, уже включенного в цены купленных им материалов и компонентов, а конечный потребитель также платит НДС за вычетом налога, уплаченного на стадии производства.",
            "📚Определение EN":
            "A form of taxation of the value added to a product (service) during production; it is levied at each stage of production and when the goods are sold to the final consumer (added to the price of the product or service and passed on to consumers); sometimes called a consumption tax; the estimated amount of VAT is transferred by the producer to the state budget minus the VAT already included in the prices of materials and components purchased by him, and the final consumer also pays VAT minus the tax paid at the stage of production.",
            "🔍Источник":
            "https://eng-rus-economy-dict.slovaronline.com/21269-VAT"
        },
        "налогоплательщик": {
            "📚Определение RU":
            "Физическое или юридическое лицо, которое в соответствии с законом обязано уплачивать какой-л. налог или налоги.",
            "📚Определение EN":
            "A natural or legal person who is obliged by law to pay a tax or taxes.",
            "🔍Источник":
            "https://eng-rus-economy-dict.slovaronline.com/128378-taxpayer"
        },
        "валюта": {
            "📚Определение RU":
            "Национальная денежная единица какой-л. страны.",
            "📚Определение EN":
            "National currency of a country.",
            "🔍Источник":
            "https://eng-rus-economy-dict.slovaronline.com/49680-currency"
        },
        "оклад, жалованье, заработная плата": {
            "📚Определение RU":
            "Исчисляется на месячной или годовой основе и напрямую не зависит от количества отработанных часов или объемов выполненных работ; обычно термин применяется к оплате труда 'белых воротничков' (служащих, научно-технического персонала и т. п.) и высококвалифицированных работников.",
            "📚Определение EN":
            "Is calculated on a monthly or annual basis and is not directly related to the number of hours worked or the amount of work performed; the term is usually applied to the remuneration of white-collar workers (employees, scientific and technical personnel, etc.) and highly skilled workers.",
            "🔍Источник":
            "https://eng-rus-economy-dict.slovaronline.com/116927-salary"
        },
        "налог на заработную плату": {
            "📚Определение RU":
            "Любой налог, который основан на заработной плате работников и либо уплачивается работодателем, либо частично изымается работодателем из заработанной работниками суммы.",
            "📚Определение EN":
            "Any tax that is based on employees' pay, and is either paid by an employer or partly taken by an employer from what employees earn.",
            "🔍Источник":
            "https://dictionary.cambridge.org/dictionary/english/payroll-tax"
        },
        "подоходный налог": {
            "📚Определение RU":
            "Налог на деньги, которые человек зарабатывает своим трудом или компания зарабатывает на продаже товаров или услуг.",
            "📚Определение EN":
            "A tax on the money that a person earns from working or that a company earns from the sale of products or services.",
            "🔍Источник":
            "https://dictionary.cambridge.org/dictionary/english/income-tax?q=income%20tax%20"
        },
        "освобождение (от налога)": {
            "📚Определение RU":
            "Специальное разрешение не делать или не уплачивать что-либо.",
            "📚Определение EN":
            "Special permission not to do or pay something.",
            "🔍Источник":
            "https://dictionary.cambridge.org/dictionary/english/exemption?q=exemption%20"
        },
        "налог с доходов корпораций": {
            "📚Определение RU":
            "Налог, уплачиваемый предприятиями с их прибыли.",
            "📚Определение EN":
            "Tax paid by businesses on their profits.",
            "🔍Источник":
            "https://dictionary.cambridge.org/dictionary/english/corporation-tax"
        },
        "профицит бюджета": {
            "📚Определение RU":
            "Количество дополнительных денег, имеющихся у правительства, поскольку оно потратило меньше денег, чем заработало.",
            "📚Определение EN":
            "The amount of extra money available to a government because it has spent less money than it earned.",
            "🔍Источник":
            "https://dictionary.cambridge.org/dictionary/english/budget-surplus?q=budget%20surplus%20"
        },
        "процентная ставка": {
            "📚Определение RU":
            "Процентная сумма, которую вы платите за то, что занимаете деньги, или получаете за то, что даете их в долг, в течение определенного периода времени, обычно года.",
            "📚Определение EN":
            "The percentage amount that you pay for borrowing money, or get for lending money, for a period of time, usually a year.",
            "🔍Источник":
            "https://dictionary.cambridge.org/dictionary/english/interest-rate?q=interest%20rate%20"
        },
        "безработица": {
            "📚Определение RU":
            "Количество или процент людей в стране или районе, у которых нет работы.",
            "📚Определение EN":
            "The number or percentage of people in a country or area who do not have jobs.",
            "🔍Источник":
            "https://dictionary.cambridge.org/dictionary/english/unemployment?q=unemployment%20"
        },
        "фондовый рынок": {
            "📚Определение RU":
            "Деятельность по покупке и продаже акций конкретных компаний, а также люди и организации, вовлеченные в эту деятельность.",
            "📚Определение EN":
            "The activity of buying and selling shares in particular companies, and the people and organizations involved in this.",
            "🔍Источник":
            "https://dictionary.cambridge.org/dictionary/english/stock-market"
        },
        "ликвидность": {
            "📚Определение RU":
            "Возможность легко менять деньги на наличные.",
            "📚Определение EN":
            "The fact of being able to be changed into cash easily.",
            "🔍Источник":
            "https://dictionary.cambridge.org/dictionary/english/liquidity"
        },
        "индекс потребительских цен": {
            "📚Определение RU":
            "Список цен на основные товары и услуги, показывающий, как они меняются за определенный период времени, в качестве способа измерения инфляции.",
            "📚Определение EN":
            "A list of the prices of basic goods and services, showing how they change in a particular period of time, as a way of measuring inflation.",
            "🔍Источник":
            "https://dictionary.cambridge.org/dictionary/english/consumer-price-index?q=consumer%20price"
        },
        "экономический рост": {
            "📚Определение RU":
            "Постепенное увеличение реального объема производства в стране, измеряемое приростом реального ВНП, ВВП или дохода на душу населения.",
            "📚Определение EN":
            "A gradual increase in a country's real output, measured by an increase in real GNP, GDP or per capita income.",
            "🔍Источник":
            "https://1195.slovaronline.com/446-economic_growth._%D1%8D%D0%BA%D0%BE%D0%BD%D0%BE%D0%BC%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B8%D0%B9_%D1%80%D0%BE%D1%81%D1%82"
        },
        "дефляция": {
            "📚Определение RU":
            "Постоянное снижение общего уровня цен на товары и услуги.",
            "📚Определение EN":
            "Continuous reduction in the overall price level of goods and services.",
            "🔍Источник":
            "https://1195.slovaronline.com/1618-%D0%B4%D0%B5%D1%84%D0%BB%D1%8F%D1%86%D0%B8%D1%8F_,_deflation"
        },
        "инфляция": {
            "📚Определение RU":
            "Рост общего уровня цен на товары и услуги как результат обесценения бумажных денег и снижения их покупательной способности.",
            "📚Определение EN":
            "An increase in the general price level for goods and services as a result of the depreciation of paper money and a decrease in its purchasing power.",
            "🔍Источник":
            "https://1195.slovaronline.com/1624-%D0%B8%D0%BD%D1%84%D0%BB%D1%8F%D1%86%D0%B8%D1%8F_,_inflation"
        },
        "облигация": {
            "📚Определение RU":
            "Ценная бумага, выпускаемая частными компаниями или государством как средство заимствования долгосрочного капитала.",
            "📚Определение EN":
            "A security issued by private companies or the government as a means of borrowing long-term capital.",
            "🔍Источник":
            "https://1195.slovaronline.com/128-bond._%D0%BE%D0%B1%D0%BB%D0%B8%D0%B3%D0%B0%D1%86%D0%B8%D1%8F"
        },
        "рынок труда": {
            "📚Определение RU":
            "Рынок, на котором происходит обмен труда на заработную плату.",
            "📚Определение EN":
            "The market in which labor is exchanged for wages.",
            "🔍Источник":
            "https://1195.slovaronline.com/826-labour_market._%D1%80%D1%8B%D0%BD%D0%BE%D0%BA_%D1%82%D1%80%D1%83%D0%B4%D0%B0"
        },
        "субсидия": {
            "📚Определение RU":
            "Финансовая помощь, предоставляемая государством физическим и юридическим лицам, а также местным органам власти за счет бюджетных средств.",
            "📚Определение EN":
            "Financial assistance provided by the state to individuals and legal entities, as well as local authorities at the expense of budgetary funds.",
            "🔍Источник":
            "https://1195.slovaronline.com/1433-subsidy._%D1%81%D1%83%D0%B1%D1%81%D0%B8%D0%B4%D0%B8%D1%8F"
        },
        "национальный долг": {
            "📚Определение RU":
            "Внутренний и внешний долги центрального правительства.",
            "📚Определение EN":
            "The internal and external debts of the central government.",
            "🔍Источник":
            "https://rus-financial-investment-dict.slovaronline.com/1484-%D0%BD%D0%B0%D1%86%D0%B8%D0%BE%D0%BD%D0%B0%D0%BB%D1%8C%D0%BD%D1%8B%D0%B9_%D0%B4%D0%BE%D0%BB%D0%B3"
        },
        "центральный банк": {
            "📚Определение RU":
            "Ведущий банк страны, выступающий в качестве основного банкира государства и всей банковской системы, а также отвечающий за денежно-кредитную политику государства.",
            "📚Определение EN":
            "The leading bank of the country, acting as the main banker of the state and the entire banking system, and responsible for the monetary policy of the state.",
            "🔍Источник":
            "https://1195.slovaronline.com/209-central_bank._%D1%86%D0%B5%D0%BD%D1%82%D1%80%D0%B0%D0%BB%D1%8C%D0%BD%D1%8B%D0%B9_%D0%B1%D0%B0%D0%BD%D0%BA"
        },
        "ставка рефинансирования": {
            "📚Определение RU":
            "Процентная ставка, по которой Центральный банк предоставляет кредит коммерческим банкам для кредитования юридических и физических лиц.",
            "📚Определение EN":
            "The interest rate at which the Central Bank provides credit to commercial banks for lending to legal entities and individuals.",
            "🔍Источник": "https://rus"
        },
"доля рынка / на рынке": {
            "📚Определение RU": "Доля общего объема продаж на рынке, которая приходится на одну фирму",
            "📚Определение EN": "A proportion of total market sales accounted for by one firm.",
            "🔍Источник": "Килиевич А. Англо-русский глоссарий терминов и понятий в сфере государственного управления и политики, экономики и международной торговли. 2-е изд., испр. и доп. – Б.: 2013. – 786 с."
        },
"market share": {
            "📚Определение RU": "Доля общего объема продаж на рынке, которая приходится на одну фирму",
            "📚Определение EN": "A proportion of total market sales accounted for by one firm.",
            "🔍Источник": "Килиевич А. Англо-русский глоссарий терминов и понятий в сфере государственного управления и политики, экономики и международной торговли. 2-е изд., испр. и доп. – Б.: 2013. – 786 с."
        },

"частичная дотация": {
            "📚Определение RU": "Дотация, которая частично (на определенный процент) покрывает местные расходы.",
            "📚Определение EN": "It matches local expenditures at some fixed percentage.",
            "🔍Источник": "Килиевич А. Англо-русский глоссарий терминов и понятий в сфере государственного управления и политики, экономики и международной торговли. 2-е изд., испр. и доп. – Б.: 2013. – 786 с."
        },
"matching grant": {
            "📚Определение RU": "Дотация, которая частично (на определенный процент) покрывает местные расходы.",
            "📚Определение EN": "It matches local expenditures at some fixed percentage.",
            "🔍Источник": "Килиевич А. Англо-русский глоссарий терминов и понятий в сфере государственного управления и политики, экономики и международной торговли. 2-е изд., испр. и доп. – Б.: 2013. – 786 с."
        },

"существенный ущерб": {
            "📚Определение RU": "Ущерб, подпадаемый под законные требования применения антидемпинговых и компенсационных мер, понимается менее строго, чем серьезной ущерб, но иначе он, по-видимому, четко не определен.",
            "📚Определение EN": "The injury requirement of the AD (anti-dumping) and CVD (countervailing duties) statutes, understood to be less stringent than serious injury but otherwise apparently not precisely defined.",
            "🔍Источник": "Килиевич А. Англо-русский глоссарий терминов и понятий в сфере государственного управления и политики, экономики и международной торговли. 2-е изд., испр. и доп. – Б.: 2013. – 786 с."
        },
"material injury": {
            "📚Определение RU": "Ущерб, подпадаемый под законные требования применения антидемпинговых и компенсационных мер, понимается менее строго, чем серьезной ущерб, но иначе он, по-видимому, четко не определен.",
            "📚Определение EN": " The injury requirement of the AD (anti-dumping) and CVD (countervailing duties) statutes, understood to be less stringent than serious injury but otherwise apparently not precisely defined.",
            "🔍Источник": "Килиевич А. Англо-русский глоссарий терминов и понятий в сфере государственного управления и политики, экономики и международной торговли. 2-е изд., испр. и доп. – Б.: 2013. – 786 с."
        },

"торговля товарами": {
            "📚Определение RU": "Экспорт и импорт товаров. Контрастирует с торговлей услугами.",
            "📚Определение EN": "Exports and imports of goods. Contrasts with trade in services.",
            "🔍Источник": "Килиевич А. Англо-русский глоссарий терминов и понятий в сфере государственного управления и политики, экономики и международной торговли. 2-е изд., испр. и доп. – Б.: 2013. – 786 с."
        },
"merchandise trade": {
            "📚Определение RU": "Экспорт и импорт товаров. Контрастирует с торговлей услугами.",
            "📚Определение EN": "Exports and imports of goods. Contrasts with trade in services.",
            "🔍Источник": "Килиевич А. Англо-русский глоссарий терминов и понятий в сфере государственного управления и политики, экономики и международной торговли. 2-е изд., испр. и доп. – Б.: 2013. – 786 с."
        },

"микроэкономика": {
            "📚Определение RU": "Наука об общественном выборе, бизнес-выборе и индивидуальном выборе, позволяющая понять, как функционирует экономика.",
            "📚Определение EN": "The study of public choices, business choice, and personal choices to understand how the economy functions.",
            "🔍Источник": "Килиевич А. Англо-русский глоссарий терминов и понятий в сфере государственного управления и политики, экономики и международной торговли. 2-е изд., испр. и доп. – Б.: 2013. – 786 с."
        },
"microeconomics": {
            "📚Определение RU": "Наука об общественном выборе, бизнес-выборе и индивидуальном выборе, позволяющая понять, как функционирует экономика.",
            "📚Определение EN": "The study of public choices, business choice, and personal choices to understand how the economy functions.",
            "🔍Источник": "Килиевич А. Англо-русский глоссарий терминов и понятий в сфере государственного управления и политики, экономики и международной торговли. 2-е изд., испр. и доп. – Б.: 2013. – 786 с."
        },

"модель": {
            "📚Определение RU": "Представление или моделирование системы либо процесса, показывающее, как параметры, выгоды и издержки взаимодействуют друг с другом с тем, чтобы определить конечный результат, по которому можно оценить качество проекта.",
            "📚Определение EN": "A representation or simulation of a system or process showing how parameters, benefits and costs interact to produce a bottom-line result by which the project can be judged.",
            "🔍Источник": "Килиевич А. Англо-русский глоссарий терминов и понятий в сфере государственного управления и политики, экономики и международной торговли. 2-е изд., испр. и доп. – Б.: 2013. – 786 с."
        },
"model": {
            "📚Определение RU": " Представление или моделирование системы либо процесса, показывающее, как параметры, выгоды и издержки взаимодействуют друг с другом с тем, чтобы определить конечный результат, по которому можно оценить качество проекта.",
            "📚Определение EN": "A representation or simulation of a system or process showing how parameters, benefits and costs interact to produce a bottom-line result by which the project can be judged.",
            "🔍Источник": "Килиевич А. Англо-русский глоссарий терминов и понятий в сфере государственного управления и политики, экономики и международной торговли. 2-е изд., испр. и доп. – Б.: 2013. – 786 с."
        },

"слияние": {
            "📚Определение RU": "Слияние двух фирм при согласии акционеров объединить их акционерный капитал с целью создания новой единой компании.",
            "📚Определение EN": "An amalgamation of two firms where the respective shareholders agree to combine their equity capital to form a single new company.",
            "🔍Источник": "Килиевич А. Англо-русский глоссарий терминов и понятий в сфере государственного управления и политики, экономики и международной торговли. 2-е изд., испр. и доп. – Б.: 2013. – 786 с."
        },
"merger": {
            "📚Определение RU": "Слияние двух фирм при согласии акционеров объединить их акционерный капитал с целью создания новой единой компании.",
            "📚Определение EN": "An amalgamation of two firms where the respective shareholders agree to combine their equity capital to form a single new company.",
            "🔍Источник": "Килиевич А. Англо-русский глоссарий терминов и понятий в сфере государственного управления и политики, экономики и международной торговли. 2-е изд., испр. и доп. – Б.: 2013. – 786 с."
        },

"валютный союз": {
            "📚Определение RU": "Две или более стран, имеющих единую валюту.",
            "📚Определение EN": "Two or more countries sharing a common currency.",
            "🔍Источник": "Килиевич А. Англо-русский глоссарий терминов и понятий в сфере государственного управления и политики, экономики и международной торговли. 2-е изд., испр. и доп. – Б.: 2013. – 786 с."
        },
"monetary union": {
            "📚Определение RU": "Две или более стран, имеющих единую валюту.",
            "📚Определение EN": "Two or more countries sharing a common currency.",
            "🔍Источник": "Килиевич А. Англо-русский глоссарий терминов и понятий в сфере государственного управления и политики, экономики и международной торговли. 2-е изд., испр. и доп. – Б.: 2013. – 786 с."
        },

"денежная масса": {
            "📚Определение RU": "Общий объем денег в экономике.",
            "📚Определение EN": "An amount of money in an economy.",
            "🔍Источник": "Килиевич А. Англо-русский глоссарий терминов и понятий в сфере государственного управления и политики, экономики и международной торговли. 2-е изд., испр. и доп. – Б.: 2013. – 786 с."
        },
"money supply": {
            "📚Определение RU": "Общий объем денег в экономике.",
            "📚Определение EN": "An amount of money in an economy.",
            "🔍Источник": "Килиевич А. Англо-русский глоссарий терминов и понятий в сфере государственного управления и политики, экономики и международной торговли. 2-е изд., испр. и доп. – Б.: 2013. – 786 с."
        },

"монополия": {
            "📚Определение RU": "Структура рынка, при которой в отрасли действует только одна фирма.",
            "📚Определение EN": "A market structure where there is only one firm in the industry.",
            "🔍Источник": "Килиевич А. Англо-русский глоссарий терминов и понятий в сфере государственного управления и политики, экономики и международной торговли. 2-е изд., испр. и доп. – Б.: 2013. – 786 с."
        },
"monopoly": {
            "📚Определение RU": "Структура рынка, при которой в отрасли действует только одна фирма.",
            "📚Определение EN": "A market structure where there is only one firm in the industry.",
            "🔍Источник": "Килиевич А. Англо-русский глоссарий терминов и понятий в сфере государственного управления и политики, экономики и международной торговли. 2-е изд., испр. и доп. – Б.: 2013. – 786 с."
        },

"регулятивное действие": {
            "📚Определение RU": "Политика или программа, предназначенная для обеспечения соответствия определенным стандартам или процедурам, например, Федерального управления аэронавтики.",
            "📚Определение EN": " A policy or program action designed to insure compliance to certain standards or procedures, for example, those of the Federal Aeronautics Administration.",
            "🔍Источник": "Килиевич А. Англо-русский глоссарий терминов и понятий в сфере государственного управления и политики, экономики и международной торговли. 2-е изд., испр. и доп. – Б.: 2013. – 786 с."
        },
"regulative action": {
            "📚Определение RU": "Политика или программа, предназначенная для обеспечения соответствия определенным стандартам или процедурам, например, Федерального управления аэронавтики.",
            "📚Определение EN": "A policy or program action designed to insure compliance to certain standards or procedures, for example, those of the Federal Aeronautics Administration.",
            "🔍Источник": "Килиевич А. Англо-русский глоссарий терминов и понятий в сфере государственного управления и политики, экономики и международной торговли. 2-е изд., испр. и доп. – Б.: 2013. – 786 с."
        },

"возобновляемый ресурс": {
            "📚Определение RU": "Ресурс, возобновление которого возможно благодаря естественным процессам (например, благодаря гидрологическому циклу) или вследствие его собственного воспроизводства, обычно в течение промежутка времени, не превышающего несколько десятков лет.",
            "📚Определение EN": "A resource that is capable of being replenished through natural processes (e. g., the hydrological cycle) or its own reproduction, generally within a timespan that does not exceed a few decades.",
            "🔍Источник": "Килиевич А. Англо-русский глоссарий терминов и понятий в сфере государственного управления и политики, экономики и международной торговли. 2-е изд., испр. и доп. – Б.: 2013. – 786 с."
        },
"renewable resource": {
            "📚Определение RU": " Ресурс, возобновление которого возможно благодаря естественным процессам (например, благодаря гидрологическому циклу) или вследствие его собственного воспроизводства, обычно в течение промежутка времени, не превышающего несколько десятков лет.",
            "📚Определение EN": "A resource that is capable of being replenished through natural processes (e. g., the hydrological cycle) or its own reproduction, generally within a timespan that does not exceed a few decades.",
            "🔍Источник": "Килиевич А. Англо-русский глоссарий терминов и понятий в сфере государственного управления и политики, экономики и международной торговли. 2-е изд., испр. и доп. – Б.: 2013. – 786 с."
        },

"рента": {
            "📚Определение RU": "Рентой называется экономическая прибыль, т. е. любые платежи, превышающие минимальные суммы, необходимые для покрытия издержек производства.",
            "📚Определение EN": "We refer to economic profits – any payments in excess of the minimum amounts needed to cover the cost of supply – as rent.",
            "🔍Источник": "Килиевич А. Англо-русский глоссарий терминов и понятий в сфере государственного управления и политики, экономики и международной торговли. 2-е изд., испр. и доп. – Б.: 2013. – 786 с."
        },
"rent": {
            "📚Определение RU": "Рентой называется экономическая прибыль, т. е. любые платежи, превышающие минимальные суммы, необходимые для покрытия издержек производства.",
            "📚Определение EN": " We refer to economic profits – any payments in excess of the minimum amounts needed to cover the cost of supply – as rent.",
            "🔍Источник": "Килиевич А. Англо-русский глоссарий терминов и понятий в сфере государственного управления и политики, экономики и международной торговли. 2-е изд., испр. и доп. – Б.: 2013. – 786 с."
        },

"цепочка результатов": {
            "📚Определение RU": "Причинная последовательность действия по развитию, которая обусловливает их очередность для достижения намеченных целей, начиная с затрачиваемых ресурсов, далее через деятельность и произведенные продукты, наконец, как кульминация, получение конечных результатов, воздействий, а также учет обратных связей. B некоторых организациях сфера влияния рассматривается как часть Ц.Р.",
            "📚Определение EN": "The causal sequence for a development intervention that stipulates the necessary sequence to achieve desired objectives beginning with inputs, moving through activities and outputs, and culminating in outcomes, impacts, and feedback. In some agencies, reach is part of the R.C.",
            "🔍Источник": "Килиевич А. Англо-русский глоссарий терминов и понятий в сфере государственного управления и политики, экономики и международной торговли. 2-е изд., испр. и доп. – Б.: 2013. – 786 с."
        },
"results chain": {
            "📚Определение RU": "Причинная последовательность действия по развитию, которая обусловливает их очередность для достижения намеченных целей, начиная с затрачиваемых ресурсов, далее через деятельность и произведенные продукты, наконец, как кульминация, получение конечных результатов, воздействий, а также учет обратных связей. B некоторых организациях сфера влияния рассматривается как часть Ц.Р.",
            "📚Определение EN": "The causal sequence for a development intervention that stipulates the necessary sequence to achieve desired objectives beginning with inputs, moving through activities and outputs, and culminating in outcomes, impacts, and feedback. In some agencies, reach is part of the R.C.",
            "🔍Источник": "Килиевич А. Англо-русский глоссарий терминов и понятий в сфере государственного управления и политики, экономики и международной торговли. 2-е изд., испр. и доп. – Б.: 2013. – 786 с."
        },

"ревальвация": {
            "📚Определение RU": "Ситуация пересмотра правительством обменного курса в сторону его повышения.",
            "📚Определение EN": "Where the government re-pegs the exchange rate at a higher level.",
            "🔍Источник": "Килиевич А. Англо-русский глоссарий терминов и понятий в сфере государственного управления и политики, экономики и международной торговли. 2-е изд., испр. и доп. – Б.: 2013. – 786 с."
        },
"revaluation": {
            "📚Определение RU": "Ситуация пересмотра правительством обменного курса в сторону его повышения.",
            "📚Определение EN": " Where the government re-pegs the exchange rate at a higher level.",
            "🔍Источник": "Килиевич А. Англо-русский глоссарий терминов и понятий в сфере государственного управления и политики, экономики и международной торговли. 2-е изд., испр. и доп. – Б.: 2013. – 786 с."
        },

"фискальный тариф": {
            "📚Определение RU": "Тариф с минимальной защитной функцией, направленный главным образом на продуцирование постоянного потока государственных доходов. Для некоторых правительств развивающихся стран тарифы являются одним из основных источников доходов, и поэтому они могут не захотеть снизить тарифы, пока не будут установлены иные источники поступления доходов.",
            "📚Определение EN": "A tariff with a minimal protective function aimed mainly at producing a steady revenue stream for government. For some developing country governments, the tariff is one of the principal sources of income, and they may therefore be reluctant to cut tariffs, unless another revenue source can be identified.",
            "🔍Источник": "Килиевич А. Англо-русский глоссарий терминов и понятий в сфере государственного управления и политики, экономики и международной торговли. 2-е изд., испр. и доп. – Б.: 2013. – 786 с."
        },
"revenue tariff": {
            "📚Определение RU": " Тариф с минимальной защитной функцией, направленный главным образом на продуцирование постоянного потока государственных доходов. Для некоторых правительств развивающихся стран тарифы являются одним из основных источников доходов, и поэтому они могут не захотеть снизить тарифы, пока не будут установлены иные источники поступления доходов.",
            "📚Определение EN": "A tariff with a minimal protective function aimed mainly at producing a steady revenue stream for government. For some developing country governments, the tariff is one of the principal sources of income, and they may therefore be reluctant to cut tariffs, unless another revenue source can be identified.",
            "🔍Источник": "Килиевич А. Англо-русский глоссарий терминов и понятий в сфере государственного управления и политики, экономики и международной торговли. 2-е изд., испр. и доп. – Б.: 2013. – 786 с."
        },

"внешняя торговля": {
            "📚Определение RU": "Количество или стоимость/ценность экспорта и/или импорта.",
            "📚Определение EN": "The quantity or value of exports and/or imports.",
            "🔍Источник": "Килиевич А. Англо-русский глоссарий терминов и понятий в сфере государственного управления и политики, экономики и международной торговли. 2-е изд., испр. и доп. – Б.: 2013. – 786 с."
        },
"foreign trade": {
            "📚Определение RU": "Количество или стоимость/ценность экспорта и/или импорта.",
            "📚Определение EN": "The quantity or value of exports and/or imports.",
            "🔍Источник": "Килиевич А. Англо-русский глоссарий терминов и понятий в сфере государственного управления и политики, экономики и международной торговли. 2-е изд., испр. и доп. – Б.: 2013. – 786 с."
        },

"форвардные рынки": {
            "📚Определение RU": " Ф.Р. охватывают контракты, которые определяют будущие поставки товаров по оговоренным в контрактах ценам.",
            "📚Определение EN": "F.M. encompass contracts that specify future de- livery at a specified price.",
            "🔍Источник": "Килиевич А. Англо-русский глоссарий терминов и понятий в сфере государственного управления и политики, экономики и международной торговли. 2-е изд., испр. и доп. – Б.: 2013. – 786 с."
        },
"forward markets": {
            "📚Определение RU": "Ф.Р. охватывают контракты, которые определяют будущие поставки товаров по оговоренным в контрактах ценам.",
            "📚Определение EN": "F.M. encompass contracts that specify future de- livery at a specified price.",
            "🔍Источник": "Килиевич А. Англо-русский глоссарий терминов и понятий в сфере государственного управления и политики, экономики и международной торговли. 2-е изд., испр. и доп. – Б.: 2013. – 786 с."
        },

"фрагментация": {
            "📚Определение RU": "Расчленение производственного процесса на отдельные составные, которые могут осуществляться в различных местах, в том числе и в разных странах.",
            "📚Определение EN": "The splitting of production processes into separate parts that can be done in different locations, including in different countries.",
            "🔍Источник": "Килиевич А. Англо-русский глоссарий терминов и понятий в сфере государственного управления и политики, экономики и международной торговли. 2-е изд., испр. и доп. – Б.: 2013. – 786 с."
        },
"fragmentation": {
            "📚Определение RU": "Расчленение производственного процесса на отдельные составные, которые могут осуществляться в различных местах, в том числе и в разных странах.",
            "📚Определение EN": "The splitting of production processes into separate parts that can be done in different locations, including in different countries.",
            "🔍Источник": "Килиевич А. Англо-русский глоссарий терминов и понятий в сфере государственного управления и политики, экономики и международной торговли. 2-е изд., испр. и доп. – Б.: 2013. – 786 с."
        },

"рамочные / основные правила": {
            "📚Определение RU": "Договорное право, гражданское право, трудовое право и антимонопольное законодательство – все это можно считать Р.П.",
            "📚Определение EN": "Contract law, tort law, labor law, and antitrust law can all be thought of as F.R.",
            "🔍Источник": "Килиевич А. Англо-русский глоссарий терминов и понятий в сфере государственного управления и политики, экономики и международной торговли. 2-е изд., испр. и доп. – Б.: 2013. – 786 с."
        },
"framework rules": {
            "📚Определение RU": " Договорное право, гражданское право, трудовое право и антимонопольное законодательство – все это можно считать Р.П.",
            "📚Определение EN": "Contract law, tort law, labor law, and antitrust law can all be thought of as F.R.",
            "🔍Источник": "Килиевич А. Англо-русский глоссарий терминов и понятий в сфере государственного управления и политики, экономики и международной торговли. 2-е изд., испр. и доп. – Б.: 2013. – 786 с."
        },

"трансграничная торговля": {
            "📚Определение RU": "Перемещение товаров из одной таможенной территории на другую.",
            "📚Определение EN": "The movement of goods from one customs territory into another.",
            "🔍Источник": "Килиевич А. Англо-русский глоссарий терминов и понятий в сфере государственного управления и политики, экономики и международной торговли. 2-е изд., испр. и доп. – Б.: 2013. – 786 с."
        },
"cross-border trade": {
            "📚Определение RU": "Перемещение товаров из одной таможенной территории на другую.",
            "📚Определение EN": "The movement of goods from one customs territory into another.",
            "🔍Источник": "Килиевич А. Англо-русский глоссарий терминов и понятий в сфере государственного управления и политики, экономики и международной торговли. 2-е изд., испр. и доп. – Б.: 2013. – 786 с."
        },

"встречная торговля": {
            "📚Определение RU": "Торговля, при которой оплата полностью или частично производится товарами или услугами.",
            "📚Определение EN": "Trade in which part or all of payment is made in goods or services.",
            "🔍Источник": "Килиевич А. Англо-русский глоссарий терминов и понятий в сфере государственного управления и политики, экономики и международной торговли. 2-е изд., испр. и доп. – Б.: 2013. – 786 с."
        },
"countertrade": {
            "📚Определение RU": "Торговля, при которой оплата полностью или частично производится товарами или услугами.",
            "📚Определение EN": "Trade in which part or all of payment is made in goods or services.",
            "🔍Источник": "Килиевич А. Англо-русский глоссарий терминов и понятий в сфере государственного управления и политики, экономики и международной торговли. 2-е изд., испр. и доп. – Б.: 2013. – 786 с."
        },

"издержки протекционизма": {
            "📚Определение RU": "Защита внутренней экономики с помощью тарифов, квот и других ограничений, как правило, связана с издержками в защищаемой экономике, которые принимают одну из двух форм: нерационального размещения ресурсов и деформации структуры потребления.",
            "📚Определение EN": "The protection of domestic industry by tariff, quota or other restriction normally imposes a cost on the protected economy in the two forms of a misallocation of resources in production and a distortion in the pattern of consumption.",
            "🔍Источник": "Килиевич А. Англо-русский глоссарий терминов и понятий в сфере государственного управления и политики, экономики и международной торговли. 2-е изд., испр. и доп. – Б.: 2013. – 786 с."
        },
"cost of protection": {
            "📚Определение RU": "Защита внутренней экономики с помощью тарифов, квот и других ограничений, как правило, связана с издержками в защищаемой экономике, которые принимают одну из двух форм: нерационального размещения ресурсов и деформации структуры потребления.",
            "📚Определение EN": "The protection of domestic industry by tariff, quota or other restriction normally imposes a cost on the protected economy in the two forms of a misallocation of resources in production and a distortion in the pattern of consumption.",
            "🔍Источник": "Килиевич А. Англо-русский глоссарий терминов и понятий в сфере государственного управления и политики, экономики и международной торговли. 2-е изд., испр. и доп. – Б.: 2013. – 786 с."
        },

"совместное производство": {
            "📚Определение RU": " Часть недавно возникшего, но все более расширяющегося направления в области соучастия граждан. Оно предполагает совместное участие властей и граждан в производстве услуг и имеет место тогда, когда граждане (потребители государственных услуг) и органы власти (производитель государственных услуг) действуют совместно с целью оказания взаимовыгодных услуг (за исключением деятельности властей, в которой потребители не участвуют).",
            "📚Определение EN": "Is part of a recent but growing emphasis in the field of citizen participation. It implies both government and citizens engage in production of a service and occurs when citizens (consumers of public services) and government (producer of public services) act jointly to produce a service which is of benefit to both (excludes government activity in which consumers do not contribute).",
            "🔍Источник": "Килиевич А. Англо-русский глоссарий терминов и понятий в сфере государственного управления и политики, экономики и международной торговли. 2-е изд., испр. и доп. – Б.: 2013. – 786 с."
        },
"coproduction": {
            "📚Определение RU": "Часть недавно возникшего, но все более расширяющегося направления в области соучастия граждан. Оно предполагает совместное участие властей и граждан в производстве услуг и имеет место тогда, когда граждане (потребители государственных услуг) и органы власти (производитель государственных услуг) действуют совместно с целью оказания взаимовыгодных услуг (за исключением деятельности властей, в которой потребители не участвуют).",
            "📚Определение EN": "Is part of a recent but growing emphasis in the field of citizen participation. It implies both government and citizens engage in production of a service and occurs when citizens (consumers of public services) and government (producer of public services) act jointly to produce a service which is of benefit to both (excludes government activity in which consumers do not contribute).",
            "🔍Источник": "Килиевич А. Англо-русский глоссарий терминов и понятий в сфере государственного управления и политики, экономики и международной торговли. 2-е изд., испр. и доп. – Б.: 2013. – 786 с."
        },

"контрольная группа": {
            "📚Определение RU": "Группа, создаваемая путем случайного отбора из той же генеральной совокупности, что и группа программы, которая, однако, не получает услуг программы. К.Г. помогает понять, какой была бы группа программы, если бы она не получала услуг программы.",
            "📚Определение EN": "A group chosen randomly from the same population as the program group but that does not receive the program. It is a stand-in for what the program group would have looked like if it had not received the program.",
            "🔍Источник": "Килиевич А. Англо-русский глоссарий терминов и понятий в сфере государственного управления и политики, экономики и международной торговли. 2-е изд., испр. и доп. – Б.: 2013. – 786 с."
        },
"control group": {
            "📚Определение RU": "Группа, создаваемая путем случайного отбора из той же генеральной совокупности, что и группа программы, которая, однако, не получает услуг программы. К.Г. помогает понять, какой была бы группа программы, если бы она не получала услуг программы.",
            "📚Определение EN": "A group chosen randomly from the same population as the program group but that does not receive the program. It is a stand-in for what the program group would have looked like if it had not received the program.",
            "🔍Источник": "Килиевич А. Англо-русский глоссарий терминов и понятий в сфере государственного управления и политики, экономики и международной торговли. 2-е изд., испр. и доп. – Б.: 2013. – 786 с."
        },

"обусловленная защита": {
            "📚Определение RU": "Торговые барьеры, которые будут установлены в случае возникновения определенных обстоятельств (типа непредвиденных расходов). Примеры О.З. включают антидемпинговые или компенсационные пошлины (для компенсации субсидий) и защитные меры. Также используется термин управляемая / регулируемая защита.",
            "📚Определение EN": "Trade barriers that are imposed if certain circumstances (contingencies) are met. Examples include anti-dumping or countervailing duties (to offset subsidies) and safeguards. Also called administered protection.",
            "🔍Источник": "Килиевич А. Англо-русский глоссарий терминов и понятий в сфере государственного управления и политики, экономики и международной торговли. 2-е изд., испр. и доп. – Б.: 2013. – 786 с."
        },
"contingent protection": {
            "📚Определение RU": "Торговые барьеры, которые будут установлены в случае возникновения определенных обстоятельств (типа непредвиденных расходов). Примеры О.З. включают антидемпинговые или компенсационные пошлины (для компенсации субсидий) и защитные меры. Также используется термин управляемая / регулируемая защита.",
            "📚Определение EN": "Trade barriers that are imposed if certain circumstances (contingencies) are met. Examples include anti-dumping or countervailing duties (to offset subsidies) and safeguards. Also called administered protection.",
            "🔍Источник": "Килиевич А. Англо-русский глоссарий терминов и понятий в сфере государственного управления и политики, экономики и международной торговли. 2-е изд., испр. и доп. – Б.: 2013. – 786 с."
        },

"заразный эффект": {
            "📚Определение RU": "Феномен финансового кризиса, возникающего в одной стране и перетекающего в другую, которая затем страдает из-за тех самых проблем, что и первая.",
            "📚Определение EN": "The phenomenon of a financial crisis in one country spilling over to another, which then suffers many of the same problems.",
            "🔍Источник": "Килиевич А. Англо-русский глоссарий терминов и понятий в сфере государственного управления и политики, экономики и международной торговли. 2-е изд., испр. и доп. – Б.: 2013. – 786 с."
        },
"contagion": {
            "📚Определение RU": "Феномен финансового кризиса, возникающего в одной стране и перетекающего в другую, которая затем страдает из-за тех самых проблем, что и первая.",
            "📚Определение EN": "The phenomenon of a financial crisis in one country spilling over to another, which then suffers many of the same problems.",
            "🔍Источник": "Килиевич А. Англо-русский глоссарий терминов и понятий в сфере государственного управления и политики, экономики и международной торговли. 2-е изд., испр. и доп. – Б.: 2013. – 786 с."
        },

"налог на потребление": {
            "📚Определение RU": "Такое налогообложение может осуществляться в двух различных формах: либо потребитель сам платит налог, как в случае с налогом на расходы, либо налогом облагаются товары или услуги, покупаемые потребителем. B последнем случае налог платит фирма, предоставляющая товары или услуги.",
            "📚Определение EN": "The taxation can take two forms; one where the consumer himself is taxed as with an expenditure tax, and another where the goods or services which the consumer purchases are taxed. In the former case the tax is imposed on the firm supplying the good or service.",
            "🔍Источник": "Килиевич А. Англо-русский глоссарий терминов и понятий в сфере государственного управления и политики, экономики и международной торговли. 2-е изд., испр. и доп. – Б.: 2013. – 786 с."
        },
"consumption tax": {
            "📚Определение RU": "Такое налогообложение может осуществляться в двух различных формах: либо потребитель сам платит налог, как в случае с налогом на расходы, либо налогом облагаются товары или услуги, покупаемые потребителем. B последнем случае налог платит фирма, предоставляющая товары или услуги.",
            "📚Определение EN": "The taxation can take two forms; one where the consumer himself is taxed as with an expenditure tax, and another where the goods or services which the consumer purchases are taxed. In the former case the tax is imposed on the firm supplying the good or service.",
            "🔍Источник": "Килиевич А. Англо-русский глоссарий терминов и понятий в сфере государственного управления и политики, экономики и международной торговли. 2-е изд., испр. и доп. – Б.: 2013. – 786 с."
        },

"неизменная / постоянная цена": {
            "📚Определение RU": "Цена, приведенная к реальным показателям с помощью соответствующего индекса цен.",
            "📚Определение EN": "A price that has been deflated to real terms by an appropriate price index.",
            "🔍Источник": "Килиевич А. Англо-русский глоссарий терминов и понятий в сфере государственного управления и политики, экономики и международной торговли. 2-е изд., испр. и доп. – Б.: 2013. – 786 с."
        },
"constant price": {
            "📚Определение RU": " Цена, приведенная к реальным показателям с помощью соответствующего индекса цен.",
            "📚Определение EN": "A price that has been deflated to real terms by an appropriate price index.",
            "🔍Источник": "Килиевич А. Англо-русский глоссарий терминов и понятий в сфере государственного управления и политики, экономики и международной торговли. 2-е изд., испр. и доп. – Б.: 2013. – 786 с."
        },

"сложный процент": {
            "📚Определение RU": "Процедура, с помощью которой будущий процент начисляют на сумму, включающую начисленный ранее процент.",
            "📚Определение EN": "The procedure whereby future interest is paid on past interest earned.",
            "🔍Источник": "Килиевич А. Англо-русский глоссарий терминов и понятий в сфере государственного управления и политики, экономики и международной торговли. 2-е изд., испр. и доп. – Б.: 2013. – 786 с."
        },
"compound interest": {
            "📚Определение RU": "Процедура, с помощью которой будущий процент начисляют на сумму, включающую начисленный ранее процент.",
            "📚Определение EN": "The procedure whereby future interest is paid on past interest earned.",
            "🔍Источник": "Килиевич А. Англо-русский глоссарий терминов и понятий в сфере государственного управления и политики, экономики и международной торговли. 2-е изд., испр. и доп. – Б.: 2013. – 786 с."
        },
"бухгалтерский учет": {
            "📚Определение RU": "ведение учета денежных операций",
            "📚Определение EN": "cash management",
            "🔍Источник": "https://eng-rus-economy-dict.slovaronline.com/34279-book-keeping"
        },

"bookkeeping": {
            "📚Определение RU": "ведение учета денежных операций",
            "📚Определение EN": "cash management",
            "🔍Источник": "https://eng-rus-economy-dict.slovaronline.com/34279-book-keeping"
        },

"отчет о движении денежных средств": {
            "📚Определение RU": "форма финансовой отчетности, в которой отражаются источники поступления денежных средств и направления их расходования",
            "📚ОпределениеEN": "a form of financial reporting that reflects the sources of cash inflows and directions of their expenditure",
            "🔍Источник": "https://eng-rus-economy-dict.slovaronline.com/38562-cash%20flow%20statement"
        },

"cash flow statement": {
            "📚Определение RU": "форма финансовой отчетности, в которой отражаются источники поступления денежных средств и направления их расходования",
            "📚Определение EN": "a form of financial reporting that reflects the sources of cash inflows and directions of their expenditure",
            "🔍Источник": "https://eng-rus-economy-dict.slovaronline.com/38562-cash%20flow%20statement"
        },

"себестоимость": {
            "📚Определение RU": "затраты на производство продукции и услуг, выручка от реализации, которых получена в течение отчетного периода",
            "📚ОпределениеEN": "costs of production of products and services, the proceeds from the sale of which were received during the reporting period",
            "🔍Источник": "https://eng-rus-economy-dict.slovaronline.com/47563-cost%20of%20sales"
        },

"cost of sales": {
            "📚Определение RU": "затраты на производство продукции и услуг, выручка от реализации, которых получена в течение отчетного периода",
            "📚Определение EN": "costs of production of products and services, the proceeds from the sale of which were received during the reporting period",
            "🔍Источник": "https://eng-rus-economy-dict.slovaronline.com/47563-cost%20of%20sales"
        },

"отсроченный налог на прибыль": {
            "📚Определение RU": "статья в отчете о прибылях и убытках, увеличивающая или уменьшающая совокупные расходы по налогу на прибыль таким образом, чтобы они были равны произведению ставки налога на прибыль и бухгалтерской прибыли до налогообложения, откорректированной на статьи расходов и доходов",
            "📚ОпределениеEN": "an item in the income statement that increases or decreases the total income tax expense so that it equals the product of the income tax rate and accounting profit before income tax adjusted for items of expense and income",
            "🔍Источник": "https://eng-rus-economy-dict.slovaronline.com/52470-deferred%20tax"
        },

"deferred tax": {
            "📚Определение RU": "статья в отчете о прибылях и убытках, увеличивающая или уменьшающая совокупные расходы по налогу на прибыль таким образом, чтобы они были равны произведению ставки налога на прибыль и бухгалтерской прибыли до налогообложения, откорректированной на статьи расходов и доходов",
            "📚Определение EN": "an item in the income statement that increases or decreases the total income tax expense so that it equals the product of the income tax rate and accounting profit before income tax adjusted for items of expense and income",
            "🔍Источник": "https://eng-rus-economy-dict.slovaronline.com/52470-deferred%20tax"
        },

"торговый дефицит": {
            "📚Определение RU": "превышение стоимости импорта страны над ее экспортом",
            "📚Определение EN": "the excess of the value of a country's imports over its exports",
            "🔍Источник": "https://eng-rus-economy-dict.slovaronline.com/130145-trade%20deficit "
        },

"trade deficit": {
            "📚Определение RU": "превышение стоимости импорта страны над ее экспортом ",
            "📚Определение EN": "the excess of the value of a country's imports over its exports",
            "🔍Источник": "https://eng-rus-economy-dict.slovaronline.com/130145-trade%20deficit"
        },

"управленческий учет": {
            "📚Определение RU": "сбор, обработка и анализ финансовых данных",
            "📚ОпределениеEN": "collection, processing and analysis of financial data",
            "🔍Источник": "https://eng-rus-economy-dict.slovaronline.com/87408-managerial%20accounting "
        },

"managerial accounting": {
            "📚ОпределениеRU": "сбор,обработка и анализ финансовых данных",
            "📚Определение EN": "collection, processing and analysis of financial data",
            "🔍Источник": "https://eng-rus-economy-dict.slovaronline.com/87408-managerial%20accounting"
        },

"чистый убыток": {
            "📚Определение RU": " сумма, на которую общая сумма расходов превышает общую сумму доходов за данный отчетный период",
            "📚ОпределениеEN": "the amount by which total expenses exceed total income for the given reporting period ",
            "🔍Источник": "https://eng-rus-economy-dict.slovaronline.com/34279-book-keeping"
        },

"netloss": {
            "📚Определение RU": " сумма, на которую общая сумма расходов превышает общую сумму доходов за данный отчетный период",
            "📚Определение EN": "the amount by which total expenses exceed total income for the given reporting period ",
            "🔍Источник": "https://eng-rus-economy-dict.slovaronline.com/34279-book-keeping"
        },

"чистый капитал": {
            "📚Определение RU": " стоимость всех активов за вычетом обязательств",
            "📚ОпределениеEN": "the value of all assets less liabilities",
            "🔍Источник": "https://eng-rus-economy-dict.slovaronline.com/search?s=net+worth"
        },

"networth": {
            "📚Определение RU": " стоимость всех активов за вычетом обязательств",
            "📚Определение EN": "the value of all assets less liabilities",
            "🔍Источник": "https://eng-rus-economy-dict.slovaronline.com/search?s=net+worth"
        },

"нераспределенная прибыль": {
            "📚Определение RU": "чистая прибыль компании, не распределенная среди акционеров, а направленная в резервы или на другие цели (реинвестированная в бизнес)",
            "📚ОпределениеEN": "net profit of the company not distributed to shareholders but directed to reserves or for other purposes (reinvested in the business) ",
            "🔍Источник": "https://eng-rus-economy-dict.slovaronline.com/search?s=retained+earnings"
        },

"retainedearnings": {
            "📚Определение RU": "чистая прибыль компании, не распределенная среди акционеров, а направленная в резервы или на другие цели (реинвестированная в бизнес)",
            "📚Определение EN": "net profit of the company not distributed to shareholders but directed to reserves or for other purposes (reinvested in the business) ",
            "🔍Источник": "https://eng-rus-economy-dict.slovaronline.com/search?s=retained+earnings"
        },

"товарооборот": {
            "📚Определение RU": "реализованные товары в денежном выражении",
            "📚ОпределениеEN": "goods sold in monetary terms",
            "🔍Источник": "https://eng-rus-economy-dict.slovaronline.com/117376-sales%20revenue"
        },

"salesrevenue": {
            "📚Определение RU": "реализованные товары в денежном выражении",
            "📚Определение EN": "goods sold in monetary terms",
            "🔍Источник": "https://eng-rus-economy-dict.slovaronline.com/117376-sales%20revenue"
        },

"списывать (со счетов)": {
            "📚Определение RU": "сократить балансовую стоимость актива",
            "📚ОпределениеEN": "reduce the carrying amount of the asset",
            "🔍Источник": "https://eng-rus-economy-dict.slovaronline.com/136035-write%20off"
        },

"writeoff": {
            "📚Определение RU": "сократить балансовую стоимость актива",
            "📚Определение EN": "reduce the carrying amount of the asset",
            "🔍Источник": "https://eng-rus-economy-dict.slovaronline.com/136035-write%20off"
        },

"банковский клиринг": {
            "📚Определение RU": "система банковских расчетов, основанная на зачете взаимных банковских требований и обязательств",
            "📚ОпределениеEN": "a system of bank settlements based on the set-off of mutual bank claims and liabilities",
            "🔍Источник": "https://eng-rus-economy-dict.slovaronline.com/31447-bank%20clearing"
        },

"bankclearing": {
            "📚Определение RU": "система банковских расчетов, основанная на зачете взаимных банковских требований и обязательств",
            "📚Определение EN": "a system of bank settlements based on the set-off of mutual bank claims and liabilities",
            "🔍Источник": "https://eng-rus-economy-dict.slovaronline.com/31447-bank%20clearing"
        },

"массовое изъятие вкладов": {
            "📚Определение RU": "массовое изъятие вкладчиками депозитов из банка в связи с сомнениями в его финансовом положении или другими событиями",
            "📚ОпределениеEN": "mass withdrawal of deposits from the bank by depositors due to doubts about its financial position or other events",
            "🔍Источник": "https://eng-rus-economy-dict.slovaronline.com/31635-bank%20run"
        },

"bankrun": {
            "📚Определение RU": "массовое изъятие вкладчиками депозитов из банка в связи с сомнениями в его финансовом положении или другими событиями",
            "📚Определение EN": "mass withdrawal of deposits from the bank by depositors due to doubts about its financial position or other events",
            "🔍Источник": "https://eng-rus-economy-dict.slovaronline.com/31635-bank%20run"
        },

"широкие деньги": {
            "📚Определение RU": "денежный агрегат, включающий не только наличные деньги и депозиты до востребования, но и срочные депозиты",
            "📚ОпределениеEN": "monetary aggregate, which includes not only cash and demand deposits, but also time deposits",
            "🔍Источник": "https://eng-rus-economy-dict.slovaronline.com/35137-broad%20money"
        },

"broadmoney": {
            "📚Определение RU": "денежный агрегат, включающий не только наличные деньги и депозиты до востребования, но и срочные депозит",
            "📚Определение EN": "monetary aggregate, which includes not only cash and demand deposits, but also time deposits",
            "🔍Источник": "https://eng-rus-economy-dict.slovaronline.com/35137-broad%20money"
        },

"кредитное положение": {
            "📚Определение RU": "репутация, которую человек получает в зависимости от своевременности уплаты долгов, кредитной истории",
            "📚ОпределениеEN": "the reputation a person gets depending on the timeliness of paying debts, credit history",
            "🔍Источник": "https://eng-rus-economy-dict.slovaronline.com/48922-credit%20standing"
        },

"creditstanding": {
            "📚Определение RU": "репутация, которую человек получает в зависимости от своевременности уплаты долгов, кредитной истории",
            "📚Определение EN": "the reputation a person gets depending on the timeliness of paying debts, credit history",
            "🔍Источник": "https://eng-rus-economy-dict.slovaronline.com/48922-credit%20standing"
        },

"кредитоспособность": {
            "📚Определение RU": "оценка способности физического или юридического лица погасить кредит, основанная на изучении кредитной истории и анализе текущего финансового положения данного лица",
            "📚ОпределениеEN": "assessment of an individual's or legal entity's ability to repay a loan, based on a study of credit history and analysis of the person's current financial position",
            "🔍Источник": "https://eng-rus-economy-dict.slovaronline.com/49070-creditworthiness"
        },

"creditworthiness": {
            "📚Определение RU": "оценка способности физического или юридического лица погасить кредит, основанная на изучении кредитной истории и анализе текущего финансового положения данного лица",
            "📚Определение EN": "assessment of an individual's or legal entity's ability to repay a loan, based on a study of credit history and analysis of the person's current financial position",
            "🔍Источник": "https://eng-rus-economy-dict.slovaronline.com/49070-creditworthiness"
        },

"учетный дом": {
            "📚Определение RU": "банк или финансовая компания, специализирующиеся на краткосрочных операциях на денежном рынке",
            "📚ОпределениеEN": "a bank or financial company specializing in short-term money market operations",
            "🔍Источник": "https://eng-rus-economy-dict.slovaronline.com/55101-discount%20house"
        },

"discounthouse": {
            "📚Определение RU": "банк или финансовая компания, специализирующиеся на краткосрочных операциях на денежном рынке",
            "📚Определение EN": "a bank or financial company specializing in short-term money market operations",
            "🔍Источник": "https://eng-rus-economy-dict.slovaronline.com/55101-discount%20house"
        },

"лизинг": {
            "📚Определение RU": "временное пользование имуществом на договорных началах за соответствующую плату",
            "📚ОпределениеEN": "temporary use of property on a contractual basis for an appropriate fee",
            "🔍Источник": "https://eng-rus-economy-dict.slovaronline.com/82722-leasing"
        },

"leasing": {
            "📚Определение RU": "временное пользование имуществом на договорных началах за соответствующую плату",
            "📚Определение EN": "temporary use of property on a contractual basis for an appropriate fee",
            "🔍Источник": "https://eng-rus-economy-dict.slovaronline.com/82722-leasing"
        },

"ставка ссудного процента": {
            "📚Определение RU": "плата за кредит в процентном выражении к сумме кредита в расчете на определенный период времени",
            "📚ОпределениеEN": "loan fee as a percentage of the loan amount over a certain period of time",
            "🔍Источник": "https://eng-rus-economy-dict.slovaronline.com/32108-base%20lending%20rate"
        },

"lendingrate": {
            "📚Определение RU": "плата за кредит в процентном выражении к сумме кредита в расчете на определенный период времени",
            "📚Определение EN": "loan fee as a percentage of the loan amount over a certain period of time",
            "🔍Источник": "https://eng-rus-economy-dict.slovaronline.com/32108-base%20lending%20rate"
        },

"торговый банк": {
            "📚Определение RU": "банк, специализирующийся на оказании вспомогательных финансовых услуг",
            "📚ОпределениеEN": "a bank specializing in ancillary financial services",
            "🔍Источник": "https://eng-rus-economy-dict.slovaronline.com/35114-british%20merchant%20banking%20and%20securities%20association"
        },

"merchantbank": {
            "📚Определение RU": "банк, специализирующийся на оказании вспомогательных финансовых услуг",
            "📚Определение EN": "a bank specializing in ancillary financial services",
            "🔍Источник": "https://eng-rus-economy-dict.slovaronline.com/35114-british%20merchant%20banking%20and%20securities%20association"
        },

"денежная база": {
            "📚Определение RU": "часть предложения денег, находящаяся под непосредственным контролем центрального банка страны",
            "📚ОпределениеEN": "the part of the money supply that is under the direct control of a country's central bank",
            "🔍Источник": "https://eng-rus-economy-dict.slovaronline.com/90964-monetary%20base"
        },

"monetarybase": {
            "📚Определение RU": "часть предложения денег, находящаяся под непосредственным контролем центрального банка страны",
            "📚Определение EN": "the part of the money supply that is under the direct control of a country's central bank",
            "🔍Источник": "https://eng-rus-economy-dict.slovaronline.com/90964-monetary%20base"
        },

"денежно-кредитная политика": {
            "📚Определение RU": "политика государства в области управлением предложением денег и процентными ставками",
            "📚ОпределениеEN": "government policy in the area of money supply and interest rate management",
            "🔍Источник": "https://eng-rus-economy-dict.slovaronline.com/22898-accommodating%20monetary%20policy"
        },

"monetarypolicy": {
            "📚Определение RU": "политика государства в области управлением предложением денег и процентными ставками",
            "📚Определение EN": "government policy in the area of money supply and interest rate management",
            "🔍Источник": "https://eng-rus-economy-dict.slovaronline.com/22898-accommodating%20monetary%20policy"
        },

"узкие деньги": {
            "📚Определение RU": "денежный агрегат, включающий наличные деньги и счета до востребования",
            "📚ОпределениеEN": "monetary aggregate, which includes cash and demand accounts",
            "🔍Источник": "https://eng-rus-economy-dict.slovaronline.com/92533-narrow%20money"
        },

"narrowmoney": {
            "📚Определение RU": "денежный агрегат, включающий наличные деньги и счета до востребования",
            "📚Определение EN": "monetary aggregate, which includes cash and demand accounts",
            "🔍Источник": "https://eng-rus-economy-dict.slovaronline.com/92533-narrow%20money"
        },

"взаимозачет": {
            "📚Определение RU": "взаимная компенсация требований и обязательств, напр., между членами фондовой биржи или клиентами банка",
            "📚ОпределениеEN": "mutual compensation of claims and liabilities, e.g. between members of a stock exchange or bank customers",
            "🔍Источник": "https://eng-rus-economy-dict.slovaronline.com/93735-netting"
        },

"netting": {
            "📚Определение RU": "взаимная компенсация требований и обязательств, напр., между членами фондовой биржи или клиентами банка",
            "📚Определение EN": "mutual compensation of claims and liabilities, e.g. between members of a stock exchange or bank customers",
            "🔍Источник": "https://eng-rus-economy-dict.slovaronline.com/93735-netting"
        },

"гарантия выполнения": {
            "📚Определение RU": "документ, гарантирующий исполнение контракта или другого обязательства",
            "📚ОпределениеEN": "a document guaranteeing the performance of a contract or other obligation",
            "🔍Источник": "https://eng-rus-economy-dict.slovaronline.com/101915-performance%20bond"
        },

"performancebond": {
            "📚Определение RU": "документ, гарантирующий исполнение контракта или другого обязательства",
            "📚Определение EN": "a document guaranteeing the performance of a contract or other obligation",
            "🔍Источник": "https://eng-rus-economy-dict.slovaronline.com/101915-performance%20bond"
        },

"базовая ставка": {
            "📚Определение RU": "публикуемая банками ставка по краткосрочным кредитам первоклассным заемщикам",
            "📚ОпределениеEN": "the rate published by banks on short-term loans to first-class borrowers",
            "🔍Источник": "https://eng-rus-economy-dict.slovaronline.com/106109-prime%20rate"
        },

"primerate": {
            "📚Определение RU": "публикуемая банками ставка по краткосрочным кредитам первоклассным заемщикам",
            "📚Определение EN": "the rate published by banks on short-term loans to first-class borrowers",
            "🔍Источник": "https://eng-rus-economy-dict.slovaronline.com/106109-prime%20rate"
        },

"розничный банк": {
            "📚Определение RU": "банк, занимающийся обслуживанием физических лиц",
            "📚ОпределениеEN": "a bank that serves individuals",
            "🔍Источник": "https://eng-rus-economy-dict.slovaronline.com/114973-retail%20bank"
        },

"retailbank": {
            "📚Определение RU": "банк, занимающийся обслуживанием физических лиц",
            "📚Определение EN": "a bank that serves individuals",
            "🔍Источник": "https://eng-rus-economy-dict.slovaronline.com/114973-retail%20bank"
        },

"сберегательный счет": {
            "📚Определение RU": "счет в банке или ином финансовом учреждении, приносящий процентный доход и предназначенный для хранения сбережений",
            "📚ОпределениеEN": "An interest-bearing account at a bank or other financial institution to hold savings",
            "🔍Источник": "https://eng-rus-economy-dict.slovaronline.com/22777-access%20savings%20account"
        },

"savingsaccount": {
            "📚Определение RU": "счет в банке или ином финансовом учреждении, приносящий процентный доход и предназначенный для хранения сбережений",
            "📚Определение EN": "An interest-bearing account at a bank or other financial institution to hold savings",
            "🔍Источник": "https://eng-rus-economy-dict.slovaronline.com/22777-access%20savings%20account"
        },

"деловая этика": {
            "📚Определение RU": "совокупность принципов, которыми должны руководствоваться бизнесмены в своей деятельности",
            "📚ОпределениеEN": "a set of principles that should guide businessmen in their activities",
            "🔍Источник": "https://eng-rus-economy-dict.slovaronline.com/36017-business%20ethics"
        },

"businessethics": {
            "📚Определение RU": "совокупность принципов, которыми должны руководствоваться бизнесмены в своей деятельности",
            "📚Определение EN": "a set of principles that should guide businessmen in their activities",
            "🔍Источник": "https://eng-rus-economy-dict.slovaronline.com/36017-business%20ethics"
        },
}

def main() -> None:
    """Запуск бота"""
    try:
        application = Application.builder().token(TELEGRAM_TOKEN).build()

        # Добавляем обработчики
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("search", search_command))
        application.add_handler(CallbackQueryHandler(button_handler))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

        # Добавляем обработчик ошибок
        application.add_error_handler(error_handler)

        # Запускаем бота
        application.run_polling(allowed_updates=Update.ALL_TYPES)
    except Exception as e:
        logger.error(f"Error starting bot: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()