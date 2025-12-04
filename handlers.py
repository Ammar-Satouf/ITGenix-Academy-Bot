from telegram import ReplyKeyboardMarkup, KeyboardButton, Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from resources import resources, channel_ids, exam_schedules_channels, exam_schedules_messages
from datetime import datetime
from db import add_user
from telegram.constants import ParseMode


def main_menu_keyboard():
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton("📚 محاضرات الكلية")],
            [KeyboardButton("📅 برامج الامتحان")],
            [KeyboardButton("🔐 المحتوى الحصري")],
            [KeyboardButton("ℹ️ عن الأكاديمية")],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def year_keyboard():
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton("السنة الأولى"),
             KeyboardButton("السنة الثانية")],
            [KeyboardButton("السنة الثالثة"),
             KeyboardButton("السنة الرابعة")],
            [KeyboardButton("السنة الخامسة")],
            [KeyboardButton("🔙 رجوع"),
             KeyboardButton("🏠 القائمة الرئيسية")],
        ],
        resize_keyboard=True,
    )


def specialization_keyboard():
    return ReplyKeyboardMarkup(
        [
            [
                KeyboardButton("هندسة البرمجيات"),
                KeyboardButton("الشبكات والنظم")
            ],
            [KeyboardButton("الذكاء الاصطناعي")],
            [KeyboardButton("🔙 رجوع"),
             KeyboardButton("🏠 القائمة الرئيسية")],
        ],
        resize_keyboard=True,
    )


def term_keyboard():
    return ReplyKeyboardMarkup(
        [
            [
                KeyboardButton("الفصل الأول ⚡"),
                KeyboardButton("الفصل الثاني 🔥")
            ],
            [KeyboardButton("🔙 رجوع"),
             KeyboardButton("🏠 القائمة الرئيسية")],
        ],
        resize_keyboard=True,
    )


def section_keyboard():
    return ReplyKeyboardMarkup(
        [
            [
                KeyboardButton("📘 القسم النظري"),
                KeyboardButton("🧪 القسم العملي")
            ],
            [KeyboardButton("🔙 رجوع"),
             KeyboardButton("🏠 القائمة الرئيسية")],
        ],
        resize_keyboard=True,
    )


def content_type_keyboard():
    return ReplyKeyboardMarkup(
        [
            [
                KeyboardButton("📚 محاضرات Gate"),
                KeyboardButton("📚 محاضرات الكميت")
            ],
            [KeyboardButton("✍ محاضرات كتابة زميلنا / دكتور المادة")],
            [KeyboardButton("📄 ملخصات"),
             KeyboardButton("❓ أسئلة دورات")],
            [KeyboardButton("📝 ملاحظات المواد")],
            [KeyboardButton("🔙 رجوع"),
             KeyboardButton("🏠 القائمة الرئيسية")],
        ],
        resize_keyboard=True,
    )


def exam_schedules_keyboard():
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton("📝 برنامج الامتحان النظري"),
             KeyboardButton("🧪 برنامج الامتحان العملي")],
            [KeyboardButton("🔙 رجوع"),
             KeyboardButton("🏠 القائمة الرئيسية")],
        ],
        resize_keyboard=True,
    )


def informatics_exam_types_keyboard():
    return ReplyKeyboardMarkup(
        [
            [
                KeyboardButton("📝 برنامج الامتحان النظري"),
                KeyboardButton("🧪 برنامج الامتحان العملي")
            ],
            [KeyboardButton("🔙 رجوع"),
             KeyboardButton("🏠 القائمة الرئيسية")],
        ],
        resize_keyboard=True,
    )


def subjects_keyboard(subjects):
    keyboard = []
    for i in range(0, len(subjects), 2):
        row = [KeyboardButton(subjects[i])]
        if i + 1 < len(subjects):
            row.append(KeyboardButton(subjects[i + 1]))
        keyboard.append(row)

    keyboard.append(
        [KeyboardButton("🔙 رجوع"),
         KeyboardButton("🏠 القائمة الرئيسية")])

    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def get_greeting():
    hour = datetime.now().hour
    if hour < 12:
        return "صباح الخير ☀️"
    elif hour < 18:
        return "مساء النور 🌤️"
    else:
        return "مساء الخير 🌙"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_first_name = update.effective_user.first_name or "صديقي"
    user_id = update.effective_user.id
    first_name = update.effective_user.first_name or ""
    last_name = update.effective_user.last_name or ""
    username = update.effective_user.username or ""
    language_code = update.effective_user.language_code or ""
    greeting = get_greeting()

    await add_user(user_id, first_name, last_name, username, language_code)

    welcome_text = (
        f"🎓 <b>ITGenix Academy</b>\n\n"
        f"{greeting} {user_first_name}! 👋\n\n"
        f"هون رح تلاقي كل يلي بتحتاجو:\n"
        f"📚 محاضرات • ملخصات • دورات\n\n"
        f"اختر من القائمة 👇"
    )

    await update.message.reply_text(
        welcome_text,
        reply_markup=main_menu_keyboard(),
        parse_mode=ParseMode.HTML
    )
    context.user_data.clear()


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "🏠 القائمة الرئيسية":
        await start(update, context)
        return

    if text == "📚 محاضرات الكلية":
        context.user_data.clear()
        context.user_data["current_step"] = "year"
        
        msg = (
            "╔══════════════════════════════╗\n"
            "      📚 <b>محاضرات الكلية</b> 📚\n"
            "╚══════════════════════════════╝\n\n"
            "🎓 اختر السنة الدراسية:"
        )
        await update.message.reply_text(
            msg,
            reply_markup=year_keyboard(),
            parse_mode=ParseMode.HTML
        )
        return

    if text == "📅 برامج الامتحان":
        context.user_data.clear()
        context.user_data["in_exam_schedules"] = True
        context.user_data["selected_branch"] = "informatics"
        
        msg = (
            "╔══════════════════════════════╗\n"
            "   💻 <b>هندسة معلوماتية</b> 💻\n"
            "╚══════════════════════════════╝\n\n"
            "📋 اختر نوع الامتحان:"
        )
        await update.message.reply_text(
            msg,
            reply_markup=exam_schedules_keyboard(),
            parse_mode=ParseMode.HTML
        )
        return

    if text == "🔐 المحتوى الحصري":
        msg = (
            "🔐 <b>المحتوى الحصري</b>\n\n"
            "🔒 قريباً...\n\n"
            "عم نحضر محتوى مميز إلكن!\n"
            "تابعونا 📢"
        )
        await update.message.reply_text(
            msg,
            reply_markup=main_menu_keyboard(),
            parse_mode=ParseMode.HTML
        )
        return

    if text == "ℹ️ عن الأكاديمية":
        msg = (
            "🎓 <b>ITGenix Academy</b>\n\n"
            "منصة أكاديمية لطلاب هندسة المعلوماتية\n"
            "بجامعة تشرين - اللاذقية\n\n"
            "👨‍💻 <b>المطور:</b>\n"
            "<a href='https://t.me/ammarouis'>عمار نضال سطوف</a>\n\n"
            "💡 صُنع بشغف للطلاب"
        )
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("📢 ITGenix Academy", url="https://t.me/ITGenixAcademy")]
        ])
        
        await update.message.reply_text(
            msg,
            reply_markup=keyboard,
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True
        )
        return

    if text == "🔙 رجوع":
        year = context.user_data.get("year")
        specialization = context.user_data.get("specialization")
        term = context.user_data.get("term")
        section = context.user_data.get("section")
        current_step = context.user_data.get("current_step")

        if current_step == "content_type":
            if section:
                context.user_data["current_step"] = "section"
                await update.message.reply_text(
                    "📂 اختر القسم:",
                    reply_markup=section_keyboard())
                return
            else:
                context.user_data["current_step"] = "subject"
                if year in ["السنة الرابعة", "السنة الخامسة"]:
                    subjects_all = []
                    for section_key in ["theoretical", "practical"]:
                        subjects_all += list(
                            resources.get(year, {}).get(term, {}).get(
                                specialization, {}).get(section_key, {}).keys())
                else:
                    subjects_all = []
                    for section_key in ["theoretical", "practical"]:
                        subjects_all += list(
                            resources.get(year, {}).get(term, {}).get(section_key, {}).keys())

                subjects_all_set = set(subjects_all)
                prefix = "⚡ " if term == "الفصل الأول" else "🔥 "
                subjects_with_emoji = [prefix + subj for subj in sorted(subjects_all_set)]

                await update.message.reply_text(
                    "📖 اختر المادة:",
                    reply_markup=subjects_keyboard(subjects_with_emoji))
                return

        if current_step == "section":
            context.user_data["current_step"] = "subject"
            context.user_data.pop("section", None)

            if year in ["السنة الرابعة", "السنة الخامسة"]:
                subjects_all = []
                for section_key in ["theoretical", "practical"]:
                    subjects_all += list(
                        resources.get(year, {}).get(term, {}).get(
                            specialization, {}).get(section_key, {}).keys())
            else:
                subjects_all = []
                for section_key in ["theoretical", "practical"]:
                    subjects_all += list(
                        resources.get(year, {}).get(term, {}).get(section_key, {}).keys())

            subjects_all_set = set(subjects_all)
            prefix = "⚡ " if term == "الفصل الأول" else "🔥 "
            subjects_with_emoji = [prefix + subj for subj in sorted(subjects_all_set)]

            await update.message.reply_text(
                "📖 اختر المادة:",
                reply_markup=subjects_keyboard(subjects_with_emoji))
            return

        if current_step == "subject":
            context.user_data["current_step"] = "term"
            context.user_data.pop("subject", None)
            context.user_data.pop("section", None)

            await update.message.reply_text(
                "📆 اختر الفصل الدراسي:",
                reply_markup=term_keyboard())
            return

        if current_step == "term":
            context.user_data.pop("term", None)

            if year in ["السنة الرابعة", "السنة الخامسة"]:
                context.user_data["current_step"] = "specialization"
                await update.message.reply_text(
                    "🎯 اختر التخصص:",
                    reply_markup=specialization_keyboard())
                return
            else:
                context.user_data["current_step"] = "year"
                msg = (
                    "╔══════════════════════════════╗\n"
                    "      📚 <b>محاضرات الكلية</b> 📚\n"
                    "╚══════════════════════════════╝\n\n"
                    "🎓 اختر السنة الدراسية:"
                )
                await update.message.reply_text(
                    msg,
                    reply_markup=year_keyboard(),
                    parse_mode=ParseMode.HTML)
                return

        if current_step == "specialization":
            context.user_data["current_step"] = "year"
            context.user_data.pop("specialization", None)

            msg = (
                "╔══════════════════════════════╗\n"
                "      📚 <b>محاضرات الكلية</b> 📚\n"
                "╚══════════════════════════════╝\n\n"
                "🎓 اختر السنة الدراسية:"
            )
            await update.message.reply_text(
                msg,
                reply_markup=year_keyboard(),
                parse_mode=ParseMode.HTML)
            return

        if current_step == "year":
            context.user_data.clear()
            await start(update, context)
            return

        if context.user_data.get("in_exam_schedules"):
            context.user_data.clear()
            await start(update, context)
            return

        context.user_data.clear()
        await start(update, context)
        return


    if context.user_data.get("selected_branch") == "informatics":
        if text == "📝 برنامج الامتحان النظري":
            channel_id = exam_schedules_channels.get("informatics_theoretical_exam")
            msg_id = exam_schedules_messages.get("informatics_theoretical_exam")

            if not channel_id or not msg_id:
                await update.message.reply_text(
                    "📝 لا يتوفر برنامج الامتحان النظري حالياً.",
                    reply_markup=informatics_exam_types_keyboard())
                return

            try:
                await context.bot.copy_message(
                    chat_id=update.effective_chat.id,
                    from_chat_id=channel_id,
                    message_id=msg_id,
                    protect_content=True)
                await update.message.reply_text(
                    "✅ تم إرسال برنامج الامتحان النظري.\n💪 بالتوفيق!",
                    reply_markup=informatics_exam_types_keyboard())
            except Exception as e:
                await update.message.reply_text(
                    "❌ حدث خطأ في جلب البرنامج.",
                    reply_markup=informatics_exam_types_keyboard())
            return

        elif text == "🧪 برنامج الامتحان العملي":
            channel_id = exam_schedules_channels.get("informatics_practical_exam")
            msg_id = exam_schedules_messages.get("informatics_practical_exam")

            if not channel_id or not msg_id:
                await update.message.reply_text(
                    "🧪 لا يتوفر برنامج الامتحان العملي حالياً.",
                    reply_markup=informatics_exam_types_keyboard())
                return

            try:
                await context.bot.copy_message(
                    chat_id=update.effective_chat.id,
                    from_chat_id=channel_id,
                    message_id=msg_id,
                    protect_content=True)
                await update.message.reply_text(
                    "✅ تم إرسال برنامج الامتحان العملي.\n💪 بالتوفيق!",
                    reply_markup=informatics_exam_types_keyboard())
            except Exception as e:
                await update.message.reply_text(
                    "❌ حدث خطأ في جلب البرنامج.",
                    reply_markup=informatics_exam_types_keyboard())
            return

    years_map = {
        "السنة الأولى": "السنة الأولى",
        "السنة الثانية": "السنة الثانية",
        "السنة الثالثة": "السنة الثالثة",
        "السنة الرابعة": "السنة الرابعة",
        "السنة الخامسة": "السنة الخامسة",
    }

    if text in years_map:
        year = text
        context.user_data["year"] = year

        if year in ["السنة الرابعة", "السنة الخامسة"]:
            context.user_data["current_step"] = "specialization"
            await update.message.reply_text(
                "🎯 اختر التخصص:",
                reply_markup=specialization_keyboard())
        else:
            context.user_data["current_step"] = "term"
            await update.message.reply_text(
                "📆 اختر الفصل الدراسي:",
                reply_markup=term_keyboard())
        return

    specializations_map = {
        "هندسة البرمجيات": "هندسة البرمجيات",
        "الشبكات والنظم": "الشبكات والنظم",
        "الذكاء الاصطناعي": "الذكاء الاصطناعي",
    }

    if text in specializations_map:
        context.user_data["specialization"] = text
        context.user_data["current_step"] = "term"
        await update.message.reply_text(
            "📆 اختر الفصل الدراسي:",
            reply_markup=term_keyboard())
        return

    term_map = {
        "الفصل الأول ⚡": "الفصل الأول",
        "الفصل الثاني 🔥": "الفصل الثاني"
    }

    if text in term_map:
        year = context.user_data.get("year")
        specialization = context.user_data.get("specialization")
        term = term_map[text]
        context.user_data["term"] = term
        context.user_data["current_step"] = "subject"

        if year in ["السنة الرابعة", "السنة الخامسة"]:
            if (year not in resources or term not in resources[year]
                    or specialization not in resources[year][term]):
                await update.message.reply_text(
                    "⚠️ لا توجد مواد لهذا التخصص والفصل.",
                    reply_markup=term_keyboard())
                return

            theoretical_subjects = list(
                resources[year][term][specialization].get("theoretical", {}).keys())
            practical_subjects = list(
                resources[year][term][specialization].get("practical", {}).keys())
        else:
            if year not in resources or term not in resources[year]:
                await update.message.reply_text(
                    "⚠️ لا توجد مواد لهذا الفصل.",
                    reply_markup=term_keyboard())
                return

            theoretical_subjects = list(resources[year][term].get("theoretical", {}).keys())
            practical_subjects = list(resources[year][term].get("practical", {}).keys())

        all_subjects_set = set(theoretical_subjects + practical_subjects)
        all_subjects = sorted(all_subjects_set)

        if not all_subjects:
            await update.message.reply_text(
                "⚠️ لا توجد مواد لهذا الفصل.",
                reply_markup=term_keyboard())
            return

        await update.message.reply_text(
            "📖 اختر المادة:",
            reply_markup=subjects_keyboard(all_subjects))
        return

    year = context.user_data.get("year")
    specialization = context.user_data.get("specialization")
    term = context.user_data.get("term")

    if year and term:
        subjects_all = []
        if year in ["السنة الرابعة", "السنة الخامسة"] and specialization:
            for section_key in ["theoretical", "practical"]:
                subjects_all += list(
                    resources.get(year, {}).get(term, {}).get(
                        specialization, {}).get(section_key, {}).keys())
        else:
            for section_key in ["theoretical", "practical"]:
                subjects_all += list(
                    resources.get(year, {}).get(term, {}).get(section_key, {}).keys())

        if text in subjects_all:
            context.user_data["subject"] = text
            context.user_data["current_step"] = "section"
            print(f"Subject selected: {text} (Available: {subjects_all})")
            await update.message.reply_text(
                "📂 اختر القسم:",
                reply_markup=section_keyboard())
            return
        else:
            print(f"Subject '{text}' not found. Available: {subjects_all}")

    section_map = {
        "📘 القسم النظري": "theoretical",
        "🧪 القسم العملي": "practical"
    }

    if text in section_map:
        section = section_map[text]
        context.user_data["section"] = section
        context.user_data["current_step"] = "content_type"
        await update.message.reply_text(
            "📚 اختر نوع المحتوى:",
            reply_markup=content_type_keyboard())
        return

    content_types = {
        "📚 محاضرات Gate": "gate",
        "📚 محاضرات الكميت": "komit",
        "✍ محاضرات كتابة زميلنا / دكتور المادة": "student_written",
        "📄 ملخصات": "summaries",
        "❓ أسئلة دورات": "exams",
        "📝 ملاحظات المواد": "notes",
    }

    if text in content_types:
        content_type = content_types[text]
        year = context.user_data.get("year")
        term = context.user_data.get("term")
        subject = context.user_data.get("subject")
        section = context.user_data.get("section")
        specialization = context.user_data.get("specialization")

        if not all([year, term, subject, section]):
            await update.message.reply_text(
                "⚠️ يرجى اختيار المادة والقسم أولاً.",
                reply_markup=main_menu_keyboard())
            return

        year_suffix = ""
        if year == "السنة الأولى":
            year_suffix = "1"
        elif year == "السنة الثانية":
            year_suffix = "2"
        elif year == "السنة الثالثة":
            year_suffix = "3"
        elif year == "السنة الرابعة":
            if specialization == "هندسة البرمجيات":
                year_suffix = "4p"
            elif specialization == "الشبكات والنظم":
                year_suffix = "4n"
            elif specialization == "الذكاء الاصطناعي":
                year_suffix = "4i"
        elif year == "السنة الخامسة":
            if specialization == "هندسة البرمجيات":
                year_suffix = "5p"
            elif specialization == "الشبكات والنظم":
                year_suffix = "5n"
            elif specialization == "الذكاء الاصطناعي":
                year_suffix = "5i"

        content_key = f"{content_type}{year_suffix}"

        try:
            if year in ["السنة الرابعة", "السنة الخامسة"]:
                subject_data = resources.get(year, {}).get(term, {}).get(
                    specialization, {}).get(section, {}).get(subject, {})
                if not subject_data:
                    await update.message.reply_text(
                        "⚠️ لم يتم العثور على المادة.",
                        reply_markup=content_type_keyboard())
                    return
            else:
                subject_data = resources.get(year, {}).get(term, {}).get(
                    section, {}).get(subject, {})
                if not subject_data:
                    await update.message.reply_text(
                        "⚠️ لم يتم العثور على المادة.",
                        reply_markup=content_type_keyboard())
                    return

            message_ids = subject_data.get(content_key, [])

            if not message_ids or message_ids == [0]:
                await update.message.reply_text(
                    "📭 لا يوجد محتوى متاح حالياً لهذا النوع.",
                    reply_markup=content_type_keyboard())
                return

            channel_id = channel_ids.get(year_suffix)
            if not channel_id:
                await update.message.reply_text(
                    "⚠️ حدث خطأ في جلب المحتوى.",
                    reply_markup=content_type_keyboard())
                return

            sent_count = 0
            for msg_id in message_ids:
                if msg_id and msg_id != 0:
                    try:
                        await context.bot.forward_message(
                            chat_id=update.effective_chat.id,
                            from_chat_id=channel_id,
                            message_id=msg_id
                        )
                        sent_count += 1
                        print(f"Message {msg_id} forwarded successfully")
                    except Exception as e:
                        print(f"Error forwarding message {msg_id}: {e}")
                        continue

            if sent_count > 0:
                await update.message.reply_text(
                    f"✅ تم إرسال {sent_count} ملف/ملفات بنجاح!",
                    reply_markup=content_type_keyboard())
            else:
                await update.message.reply_text(
                    "📭 لا يوجد محتوى متاح.",
                    reply_markup=content_type_keyboard())

        except Exception as e:
            print(f"Error: {e}")
            await update.message.reply_text(
                "⚠️ حدث خطأ في جلب المحتوى.",
                reply_markup=content_type_keyboard())
        return

    await update.message.reply_text(
        "🤔 لم أفهم طلبك. اختر من القائمة:",
        reply_markup=main_menu_keyboard())
