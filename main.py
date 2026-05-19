#!/usr/bin/env python3
import subprocess
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# ============== BOT TOKEN ==============
TELEGRAM_TOKEN = 'YOUR_BOT_TOKEN'
# =======================================

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Bot is active! Send any command to run on this server.")

def run_command(update: Update, context: CallbackContext):
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
                    update.message.reply_text(f"```{output[i:i+4000]}```", parse_mode='Markdown')
            else:
                update.message.reply_text(f"```{output}```", parse_mode='Markdown')
        
        if error:
            update.message.reply_text(f"Error:\n```{error}```", parse_mode='Markdown')
        
        if not output and not error:
            update.message.reply_text("Done (no output)")
            
    except subprocess.TimeoutExpired:
        update.message.reply_text("Timeout! Command took more than 30 seconds.")
    except Exception as e:
        update.message.reply_text(f"Error: {str(e)}")

def main():
    updater = Updater(TELEGRAM_TOKEN)
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, run_command))
    
    print("Bot started...")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
