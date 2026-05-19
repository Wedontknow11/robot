#!/usr/bin/env python3
import subprocess
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# ============== BOT TOKEN ==============
TELEGRAM_TOKEN = '8032593273:AAFWNJzJzt6pnePry8fhwE8glnWRiSs-ick'
# =======================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot is active! Send any command to run on this server.")

async def run_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    command = update.message.text
    
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            capture_output=True, 
            text=True,
            timeout=30
        )
        
        output = result.stdout
        error = result.stderr
        
        if output:
            if len(output) > 4000:
                for i in range(0, len(output), 4000):
                    await update.message.reply_text(f"```{output[i:i+4000]}```", parse_mode='Markdown')
            else:
                await update.message.reply_text(f"```{output}```", parse_mode='Markdown')
        
        if error:
            await update.message.reply_text(f"Error:\n```{error}```", parse_mode='Markdown')
        
        if not output and not error:
            await update.message.reply_text("Done (no output)")
            
    except subprocess.TimeoutExpired:
        await update.message.reply_text("Timeout! Command took more than 30 seconds.")
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Error: {context.error}")

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, run_command))
    app.add_error_handler(error_handler)
    
    print("Bot started...")
    app.run_polling()

if __name__ == '__main__':
    main()
