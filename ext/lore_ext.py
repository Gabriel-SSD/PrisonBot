import interactions as ity
from sender import flore
import requests
from util import to_pascal_case


def fix_champion(champion):
    champion_mapping = {
        'wukong': 'MonkeyKing',
        'renataglasc': 'Renata',
        'jarvaniv': 'JarvanIV',
        'jarvan': 'JarvanIV'
    }
    lowercase_champion = champion.lower()
    if lowercase_champion in champion_mapping:
        return champion_mapping[lowercase_champion]
    else:
        return champion


class Poppy:
    def __init__(self):
        self.version = "13.1.1"
        self.region = "pt_BR"
        self.URL_BASE = "https://ddragon.leagueoflegends.com/cdn"

    def get_lore(self, champion):
        champion = fix_champion(to_pascal_case(champion))
        api_url = "{}/{}/data/{}/champion/{}.json".format(self.URL_BASE, self.version, self.region, champion)

        try:
            response = requests.get(api_url)
            response.raise_for_status()  # Verifica se ocorreu um erro na requisição
            lore_json = response.json()
            champion_data = lore_json['data'].get(champion)
            if champion_data:
                lore_dict = {
                    "lore": champion_data.get('lore'),
                    "title": champion_data.get('title'),
                    "name": champion_data.get('name'),
                    "champ": champion_data.get('id'),
                }
                return lore_dict
            else:
                print("Dados do campeão não encontrados na resposta JSON.")
        except requests.exceptions.RequestException as e:
            print("Erro na requisição HTTP:", e)
        return None


class LoreCog(ity.Extension):
    @ity.slash_command(name="lore", description="Descubra a lora de qualquer campeão!")
    @ity.slash_option(name="champion", description="Digite o nome do campeão", required=True, opt_type=ity.OptionType.STRING)
    async def lore_function(self, ctx: ity.SlashContext, champion: str):
        try:
            lore = Poppy().get_lore(champion=champion)
            if lore is not None:
                embed = flore(lore['champ'], lore['lore'], lore['title'], lore['name'])
                await ctx.send(embeds=embed)
            else:
                await ctx.send("Campeão não encontrado.")
        except Exception as err:
            await ctx.send("Ocorreu um erro inesperado =(\nContate o mestre Prison para verificar o ocorrido.")
            print(f"Lore error: {err}")


def setup(client):
    LoreCog(client)
