import os
import interactions as ity
import requests
from sender import fclash
from urllib.parse import quote


class Clash:
    def __init__(self, tag):
        self.tag = tag

    def raw_data(self):
        url = f"https://api.clashofclans.com/v1/players/{quote(self.tag)}"
        header = {
            "Authorization": f"Bearer {os.getenv('CLASHTOKEN')}"
        }
        raw_data = requests.get(url=url, headers=header).json()
        if raw_data["reason"]:
            return None
        filtered_data = {
            "name": raw_data["name"],
            "CV": raw_data["townHallLevel"],
            "Clã": raw_data["clan"]["name"],
            "Liga": raw_data["league"]["name"],
            "Troféus": raw_data["trophies"],
            "Max. Troféus": raw_data["bestTrophies"],
            "url_league": raw_data["league"]["iconUrls"]["medium"],
            # "BH": raw_data["builderHallLevel"],
            # "Versus Troféus": raw_data["versusTrophies"],
            # "Max. Versus Troféus": raw_data["bestVersusTrophies"]
        }
        return filtered_data


class ClashCog(ity.Extension):
    @ity.slash_command(name="clash", description="Veja informações de um jogador no COC")
    @ity.slash_option(name="tag", description="Digite sua tag", required=True, opt_type=ity.OptionType.STRING)
    async def clash_function(self, ctx: ity.SlashContext, tag: str):
        try:
            filtered_data = Clash(tag=tag).raw_data()
            if filtered_data is None:
                await ctx.send(f"Jogador não encontrado.\nVerifique se a tag **{tag}** está correta")
            else:
                embed = fclash(filtered_data)
                await ctx.send(embeds=embed)
        except Exception as e:
            print(e)

# tag = "#2Y9RCRR0R"
