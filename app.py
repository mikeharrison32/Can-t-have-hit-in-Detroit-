from bot.main_bot import MainBot
import os
from dotenv import load_dotenv

load_dotenv()


TOKEN = os.getenv('TOKEN')


try: 
    main_bot = MainBot()
    main_bot.run(TOKEN)
except Exception as e:
    print(e)