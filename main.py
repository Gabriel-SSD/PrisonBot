from os import getenv
import interactions as ity

bot = ity.Client(token=getenv('DSTOKEN'))


@ity.listen()
async def on_ready():
    print("PrisonBotV1 está online!")

bot.load_extension("ext.lore_ext")
bot.load_extension("ext.weather_ext")
bot.load_extension("ext.clash_ext")

bot.start()
