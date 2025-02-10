import ahpy
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Храним состояния для пользователей
user_data = {}


async def send_welcome_message(context: ContextTypes.DEFAULT_TYPE):
    chat_id = context.job.chat_id
    await context.bot.send_message(chat_id=chat_id,
                                   text="Привет! Я бот для проведения многокритериального анализа (AHP).\nНапишите /start, чтобы начать.")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data[update.effective_chat.id] = {"criteria_names": [], "alternatives_names": [],
                                           "stage": "get_criteria_count"}
    await update.message.reply_text(
        "Добро пожаловать в AHP бот!\n\n"
        "Я помогу вам провести многокритериальный анализ с использованием метода анализа иерархий (AHP).\n"
        "Вот как это работает:\n"
        "1. Вы вводите количество критериев, по которым будут оцениваться альтернативы.\n"
        "2. Затем вы вводите названия этих критериев.\n"
        "3. Далее укажите количество альтернатив и их названия.\n"
        "4. После этого вам нужно будет сравнить критерии попарно, оценивая их относительную важность.\n"
        "5. Затем нужно будет сравнить альтернативы для каждого критерия.\n"
        "6. По завершении всех сравнений, я вычислю приоритеты и предложу наилучшее решение.\n\n"
        "Для ввода сравнения используйте числа, например: если первый элемент важнее второго, введите значение больше 1.\n"
        "Если наоборот, введите дробное число меньше 1 (например, 0.5).\n\n"
        "Начнем с ввода количества критериев. Введите его, чтобы продолжить."
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_chat.id
    if user_id not in user_data:
        await start(update, context)
        return

    user_state = user_data[user_id]
    stage = user_state["stage"]
    text = update.message.text

    if "err_counter" not in user_state:
        user_state["err_counter"] = 0

    if "meet_counter" not in user_state:
        user_state["meet_counter"] = 0

    if "prev_state" not in user_state:
        user_state["prev_state"] = "None"

    if user_state["stage"] == "get_criteria_count":
        if text.isdigit() and int(text) > 0:
            n = int(update.message.text)
            user_state["n"] = n
            user_state["stage"] = "get_criteria_names"
            await update.message.reply_text(f"Введите названия {n} критериев (по одному за сообщение):")
        else:
            await update.message.reply_text("Пожалуйста, введите корректное число больше нуля.")

            user_state["err_counter"] += 1
            if user_state["err_counter"] == 3:
                user_state["prev_state"] = "get_criteria_count"
                user_state["stage"] = "stubborn_user"
                user_state["err_counter"] = 0


    elif user_state["stage"] == "get_criteria_names":
        user_state["criteria_names"].append(update.message.text)
        if len(user_state["criteria_names"]) == user_state["n"]:
            user_state["stage"] = "get_alternative_count"
            await update.message.reply_text("Введите количество альтернатив:")
        else:
            await update.message.reply_text(f"Введите название критерия {len(user_state['criteria_names']) + 1}:")

    elif user_state["stage"] == "get_alternative_count":
        if text.isdigit() and int(text) > 0:
            m = int(update.message.text)
            user_state["m"] = m
            user_state["stage"] = "get_alternative_names"
            await update.message.reply_text(f"Введите названия {m} альтернатив (по одному за сообщение):")
        else:
            await update.message.reply_text("Пожалуйста, введите корректное число больше нуля.")

            user_state["err_counter"] += 1
            if user_state["err_counter"] == 3:
                user_state["prev_state"] = "get_alternative_count"
                user_state["stage"] = "stubborn_user"
                user_state["err_counter"] = 0

    elif user_state["stage"] == "get_alternative_names":
        user_state["alternatives_names"].append(update.message.text)
        if len(user_state["alternatives_names"]) == user_state["m"]:
            user_state["stage"] = "get_criteria_comparisons"
            await update.message.reply_text(
                f"Сравните критерии: {user_state['criteria_names'][0]} и {user_state['criteria_names'][1]} (введите число):")
        else:
            await update.message.reply_text(
                f"Введите название альтернативы {len(user_state['alternatives_names']) + 1}:")

    elif user_state["stage"] == "get_criteria_comparisons":
        if text.isdigit() and int(text) > 0:
            if "criteria_comparisons" not in user_state:
                user_state["criteria_comparisons"] = {}
                user_state["criteria_index"] = [0, 1]

            comparison = float(update.message.text)
            i, j = user_state["criteria_index"]
            user_state["criteria_comparisons"][
                (user_state["criteria_names"][i], user_state["criteria_names"][j])] = comparison
            user_state["criteria_comparisons"][
                (user_state["criteria_names"][j], user_state["criteria_names"][i])] = 1 / comparison

            if j < len(user_state["criteria_names"]) - 1:
                user_state["criteria_index"] = [i, j + 1]
            elif i < len(user_state["criteria_names"]) - 2:
                user_state["criteria_index"] = [i + 1, i + 2]
            else:
                user_state["stage"] = "get_alternative_comparisons"
                user_state["current_criteria"] = 0
                user_state["alt_index"] = [0, 1]
                await update.message.reply_text(
                    f"Сравните альтернативы {user_state['alternatives_names'][0]} и {user_state['alternatives_names'][1]} для критерия {user_state['criteria_names'][0]} (введите число):")
                return

            i, j = user_state["criteria_index"]
            await update.message.reply_text(
                f"Сравните критерии: {user_state['criteria_names'][i]} и {user_state['criteria_names'][j]} (введите число):")
        else:
            await update.message.reply_text("Пожалуйста, введите корректное число больше нуля.")

            user_state["err_counter"] += 1
            if user_state["err_counter"] == 3:
                user_state["prev_state"] = "get_criteria_comparisons"
                user_state["stage"] = "stubborn_user"
                user_state["err_counter"] = 0


    elif user_state["stage"] == "get_alternative_comparisons":
        if text.isdigit() and int(text) > 0:
            if "alternative_comparisons" not in user_state:
                user_state["alternative_comparisons"] = {criteria: {} for criteria in user_state["criteria_names"]}

            comparison = float(update.message.text)
            alt_i, alt_j = user_state["alt_index"]
            criteria = user_state["criteria_names"][user_state["current_criteria"]]

            # Сохраняем сравнение альтернатив
            user_state["alternative_comparisons"][criteria][
                (user_state["alternatives_names"][alt_i], user_state["alternatives_names"][alt_j])] = comparison
            user_state["alternative_comparisons"][criteria][
                (user_state["alternatives_names"][alt_j], user_state["alternatives_names"][alt_i])] = 1 / comparison

            # Переход к следующему сравнению альтернатив
            if alt_j < len(user_state["alternatives_names"]) - 1:
                user_state["alt_index"] = [alt_i, alt_j + 1]
            elif alt_i < len(user_state["alternatives_names"]) - 2:
                user_state["alt_index"] = [alt_i + 1, alt_i + 2]
            else:
                if user_state["current_criteria"] < len(user_state["criteria_names"]) - 1:
                    user_state["current_criteria"] += 1
                    user_state["alt_index"] = [0, 1]
                else:
                    user_state["stage"] = "calculate_ahp"
                    await update.message.reply_text("Все данные введены. Начинаем расчет AHP...")
                    await calculate_ahp(update, context)
                    return

            alt_i, alt_j = user_state["alt_index"]
            criteria = user_state["criteria_names"][user_state["current_criteria"]]
            await update.message.reply_text(
                f"Сравните альтернативы {user_state['alternatives_names'][alt_i]} и {user_state['alternatives_names'][alt_j]} для критерия {criteria} (введите число):")
        else:
            await update.message.reply_text("Пожалуйста, введите корректное число больше нуля.")

            user_state["err_counter"] += 1
            if user_state["err_counter"] == 3:
                user_state["prev_state"] = "get_alternative_comparisons"
                user_state["stage"] = "stubborn_user"
                user_state["err_counter"] = 0

    elif user_state["stage"] == "stubborn_user":
        user_state["meet_counter"] += 1
        if user_state["meet_counter"] == 1:
            await update.message.reply_text(
                "Пожалуйста, вводите корректно\n\n"

            )
            user_state["stage"] = user_state["prev_state"]

        if user_state["meet_counter"] == 2:
            await update.message.reply_text(
                "Некорректно\n\n"
            )
            user_state["stage"] = user_state["prev_state"]

        if user_state["meet_counter"] == 3:
            await update.message.reply_text(
                "И снова мимо\n\n"
            )
            user_state["stage"] = user_state["prev_state"]

        if user_state["meet_counter"] == 4:
            await update.message.reply_text(
                "Предупреждаю\n"
            )
            user_state["stage"] = user_state["prev_state"]

        if user_state["meet_counter"] == 5:
            await update.message.reply_text(
                "Доигрались?\n\n"
                "Работа бота прекращена...\n"
            )
            await update.message.reply_text(
                "Алгоритм остановлен...\n\n"
            )
            return


async def calculate_ahp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_chat.id
    user_state = user_data[user_id]

    # Выполнение расчета AHP
    criteria_obj = ahpy.Compare('criteria', user_state['criteria_comparisons'], precision=3, random_index='saaty')

    criteria_objects = {}
    for criteria_name in user_state["criteria_names"]:
        criteria_objects[criteria_name] = ahpy.Compare(criteria_name,
                                                       user_state['alternative_comparisons'][criteria_name],
                                                       precision=3, random_index='saaty')

    criteria_obj.add_children(list(criteria_objects.values()))

    # Выводим результаты
    await update.message.reply_text(f"Локальные веса для критериев: {criteria_obj.local_weights}")
    await update.message.reply_text(f"Целевые веса для альтернатив: {criteria_obj.target_weights}")

    for criteria_name in user_state["criteria_names"]:
        await update.message.reply_text(
            f"Отчет для критерия '{criteria_name}':\n{criteria_objects[criteria_name].report(show=False)}")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Чтобы начать, используйте команду /start. Я проведу вас через процесс многокритериального анализа.\n"
        "Если у вас возникли вопросы, просто следуйте инструкциям или задайте вопрос в чате."
    )


def main():
    TOKEN = "SECRET DATA"

    application = ApplicationBuilder().token(TOKEN).build()

    # Отправляем вступительное сообщение при запуске бота
    application.job_queue.run_once(send_welcome_message, 0)

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(CommandHandler("help", help_command))

    application.run_polling()


if __name__ == "__main__":
    main()
