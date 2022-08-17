import logging
import scrap
from telegram import Update
from asyncio import run
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from telegram.error import NetworkError

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
menus = scrap.get_menus()

restaurant_had_no_meals = lambda restaurant: isinstance(menus[restaurant], str)
async def generic_meal_callback(update: Update, context: ContextTypes.DEFAULT_TYPE, restaurant: str):
  retries = 0
  while retries < 5:
    try:
      if restaurant_had_no_meals(restaurant):
        await context.bot.send_message(chat_id=update.effective_chat.id, text=menus[restaurant])
        return

      for meal in menus[restaurant]:
        resp = scrap.format_meal(title=meal, meal=menus[restaurant][meal])
        await context.bot.send_message(chat_id=update.effective_chat.id, text=resp)    
      return 
  
    except NetworkError as e: 
      logging.log(level=logging.ERROR, msg=e)
      retries += 1
    except Exception as e:
      logging.log(level=logging.ERROR, msg=e)
      raise(e)

async def capao(update: Update, context: ContextTypes.DEFAULT_TYPE): 
  await generic_meal_callback(update, context, "capao")

async def anglo(update: Update, context: ContextTypes.DEFAULT_TYPE): 
  await generic_meal_callback(update, context, "anglo")

async def ceu(update: Update, context: ContextTypes.DEFAULT_TYPE): 
  await generic_meal_callback(update, context, "ceu")

async def santa(update: Update, context: ContextTypes.DEFAULT_TYPE): 
  await generic_meal_callback(update, context, "santa")

if __name__ == '__main__':
  application = ApplicationBuilder().token('5767350490:AAHoNxFbbb41uKP61O9zua9uGeQHKZmK0tk').build()

  application.add_handler(CommandHandler('santa', santa))
  application.add_handler(CommandHandler('capao', capao))
  application.add_handler(CommandHandler('anglo', anglo))
  application.add_handler(CommandHandler('ceu', ceu))
  
  application.run_polling()
