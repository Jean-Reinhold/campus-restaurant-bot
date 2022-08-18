import logging
import scrap
import os 
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from telegram.error import NetworkError

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    filename="logs.txt",
    filemode="a+"
)

restaurant_had_no_meals = lambda restaurant: isinstance(scrap.get_menus()[restaurant], str)

async def generic_meal_callback(update: Update, context: ContextTypes.DEFAULT_TYPE, restaurant: str):
  user = update.message.from_user
  logging.info(f"{user['first_name']} {user['last_name']}:  {user['id']}  CONSULTA")
  retries = 0
  while retries < 5:
    try:
      menus = scrap.get_menus()
      if restaurant_had_no_meals(restaurant):
        await context.bot.send_message(chat_id=update.effective_chat.id, text=menus[restaurant])
        return

      for meal in menus[restaurant]:
        resp = scrap.format_meal(title=meal, meal=menus[restaurant][meal])
        await context.bot.send_message(chat_id=update.effective_chat.id, text=resp)    
      return 
  
    except NetworkError as e: 
      logging.error(msg=e)
      retries += 1
    except Exception as e:
      logging.error(msg=e)
      raise(e)

async def capao(update: Update, context: ContextTypes.DEFAULT_TYPE): 
  await generic_meal_callback(update, context, "capao")

async def anglo(update: Update, context: ContextTypes.DEFAULT_TYPE): 
  await generic_meal_callback(update, context, "anglo")

async def ceu(update: Update, context: ContextTypes.DEFAULT_TYPE): 
  await generic_meal_callback(update, context, "ceu")

async def santa(update: Update, context: ContextTypes.DEFAULT_TYPE): 
  await generic_meal_callback(update, context, "santa")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE): 
  user = update.message.from_user
  logging.info(f"{user['first_name']} {user['last_name']}:  {user['id']}   START")

  await context.bot.send_message(
    chat_id=update.effective_chat.id,
    text="""
    Selecione o restaurante para ver o cardápio:
     
    /capao -> RU Capão do Leão
    /anglo -> RU Anglo
    /santa -> RU Santa Cruz
    /ceu   -> Casa do Estudante Universitário

    made by Jean Reinhold
    """
  )


if __name__ == '__main__':
  application = ApplicationBuilder().token(os.getenv("TOKEN")).build()

  application.add_handler(CommandHandler('start', start))

  application.add_handler(CommandHandler('santa', santa))
  application.add_handler(CommandHandler('capao', capao))
  application.add_handler(CommandHandler('anglo', anglo))
  application.add_handler(CommandHandler('ceu', ceu))
  
  application.run_polling()
