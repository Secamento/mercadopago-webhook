from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "SEU_TELEGRAM_TOKEN"
app = Application.builder().token(TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("Comprar Plano", callback_data='comprar_plano')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Bem-vindo! Clique no botão abaixo para adquirir seu plano.", reply_markup=reply_markup)

async def escolher_plano(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.message.reply_text("Plano selecionado! Aguarde a confirmação de pagamento.")

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(escolher_plano, pattern="comprar_plano"))

if __name__ == "__main__":
    app.run_polling()
