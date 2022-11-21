from dobot.bot import Bot

bot = Bot(port="/dev/ttyUSB0")

bot.set_marker_position("red")
