from PIL import Image
import requests
import io
from interactions import Embed, Color


def dominant_color(url):
    response = requests.get(url)
    img = Image.open(io.BytesIO(response.content))
    colors = img.getcolors(img.size[0] * img.size[1])
    return max(colors, key=lambda x: x[0])[1]


def flore(champ, lore, title, name):
    url = f"https://ddragon.leagueoflegends.com/cdn/img/champion/splash/{champ}_0.jpg"
    r, g, b = dominant_color(url)
    embed = Embed(title=f"{name}, {title}", color=Color.from_rgb(r, g, b))
    embed.set_image(url=url)
    embed.add_field(name=" ", value=lore)
    return embed


def fweather(string, name):
    embed = Embed(title=f"Previsão do tempo em {name}")
    embed.set_thumbnail(url="https://openweathermap.org/themes/openweathermap/assets/img/logo_white_cropped.png")
    embed.add_field(name=" ", value=string)
    embed.set_footer(text="Dados da AccuWeather")
    return embed


def fquiz(champ, skin):
    url = f"https://ddragon.leagueoflegends.com/cdn/img/champion/splash/{champ}_{str(skin)}.jpg"
    r, g, b = dominant_color(url)
    embed = Embed(title="Qual é o campeão da foto?", color=Color.from_rgb(r, g, b))
    embed.set_image(url=url)
    return embed


def fclash(dataset):
    embed = Embed(title=dataset["name"])
    embed.set_thumbnail(dataset["url_league"])
    del dataset["url_league"]
    del dataset["name"]
    string_formatada = "\n".join([f"{chave}: {valor}" for chave, valor in dataset.items()])
    embed.add_field(name=" ", value=string_formatada)
    return embed
