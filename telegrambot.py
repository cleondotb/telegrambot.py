import os
import random
import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# List of allowed Telegram user IDs
ALLOWED_TG_IDS = [6417455742, 6770001600, 6394830022, 1910648163, 6145894406, 7716810621, 7939400507]  # Replace with actual IDs

# Paths for CODM and MLBB files (Updated for mobile)
FILE_DIRECTORY_CODM = '/storage/emulated/0/codmfiles'
FILE_DIRECTORY_MLBB = '/storage/emulated/0/mlbbfiles'

# Ensure directories exist
os.makedirs(FILE_DIRECTORY_CODM, exist_ok=True)
os.makedirs(FILE_DIRECTORY_MLBB, exist_ok=True)

# Global dictionary to track user file forwarding count
user_file_count = {}
user_last_access = {}

# Daily limit for forwarded files per user
FILE_LIMIT_PER_DAY = 5

# Function to check if a user is authorized
def is_user_authorized(chat_id):
    return chat_id in ALLOWED_TG_IDS

# Function to check if a user has exceeded the limit
def can_forward_file(chat_id):
    current_date = datetime.date.today().isoformat()
    
    if chat_id not in user_last_access or user_last_access[chat_id] != current_date:
        user_file_count[chat_id] = 0  # Reset count for new day
        user_last_access[chat_id] = current_date
    
    return user_file_count[chat_id] < FILE_LIMIT_PER_DAY

# Function to update user file count
def increment_file_count(chat_id):
    user_file_count[chat_id] += 1

async def send_random_file(update: Update, context: ContextTypes.DEFAULT_TYPE, file_directory):
    chat_id = update.effective_chat.id

    if not is_user_authorized(chat_id):
        await update.message.reply_text("You do not have VIP access.")
        return

    if not can_forward_file(chat_id):
        await update.message.reply_text("You have reached your daily file limit. Please try again tomorrow.")
        return

    try:
        if not os.path.exists(file_directory):
            await update.message.reply_text("The bot is generating files. Please wait.")
            return

        files = [f for f in os.listdir(file_directory) if os.path.isfile(os.path.join(file_directory, f))]
        if not files:
            await update.message.reply_text("Bot is under maintenance. Please wait.")
            return

        random_file = random.choice(files)
        file_path = os.path.join(file_directory, random_file)

        with open(file_path, 'rb') as file:
            await context.bot.send_document(chat_id=chat_id, document=file)

        os.remove(file_path)
        increment_file_count(chat_id)  # Update file count

        # Send additional message with file details
        file_details_message = (
            f"Generated: {random_file}\n\n"
            f"Telegram Bot: @UCGeneratorBot\n"
            f"Owner: @CleonDoobie\n"
            f"Admin: @Woozie420\n"
            f"Channel: @UmbrellaCorpPH"
        )
        await update.message.reply_text(file_details_message)

    except Exception as e:
        await update.message.reply_text(f"An error occurred. Contact Admin : @Woozie420 : {str(e)}")

async def generate_codm_txt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_random_file(update, context, FILE_DIRECTORY_CODM)

async def generate_mlbb_txt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_random_file(update, context, FILE_DIRECTORY_MLBB)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "Umbrella Corp Generator Help:\n\n"
        "Commands you can use:\n"
        "/codm - Generate Codm Files\n"
        "/mlbb - Generate Mobile Legends Files\n\n"
        "How to use:\n"
        "Simply Use /codm & /mlbb To Generate The Files.\n\n"
        "Note: Only authorized users can use this bot.\n\n"
        "Contact Owner : @CleonDoobie To Buy"
        "Contact Admin : @Woozie420 To Buy"
    )
    await update.message.reply_text(help_text)

def main():
    application = Application.builder().token('7879249621:AAGSQY63QrX3fq-esCPFK4Sl6PNL2OtdwWk').build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("codm", generate_codm_txt))
    application.add_handler(CommandHandler("mlbb", generate_mlbb_txt))
    application.run_polling()

if __name__ == 'main':
    main()
