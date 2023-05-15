import interactions as ity
from sender import fweather
import requests
from os import getenv
import util


class Weather:
    def __init__(self, city, uf):
        self.city = city
        self.uf = uf
        self.locationid = self.get_location()

    def get_location(self):
        try:
            api_url = "http://dataservice.accuweather.com/locations/v1/cities/search"
            params = {
                "apikey": getenv('ACCUTOKEN'),
                "q": self.city
            }
            response = requests.get(api_url, params=params).json()
            for dicionario in response:
                if dicionario["AdministrativeArea"]["ID"] == self.uf:
                    return dicionario["Key"]
        except (requests.exceptions.RequestException, ValueError, KeyError) as e:
            print(f"Error getting location: {e}")

    def daily_forecast(self):
        try:
            api_url = f"http://dataservice.accuweather.com/forecasts/v1/daily/1day/{self.locationid}"
            params = {
                "apikey": getenv("ACCUTOKEN"),
                "language": "pt-br",
                "details": "true"
            }
            response = requests.get(api_url, params=params).json()
            data = response["DailyForecasts"][0]
            fmax, fmin = data["Temperature"]["Maximum"]["Value"], data["Temperature"]["Minimum"]["Value"]
            cmax = str(util.f_to_c(fmax)) + "°"
            cmin = str(util.f_to_c(fmin)) + "°"
            forecast = f"""Temperatura máxima de {cmax}
                           Temporatura mínima de {cmin}
                           Previsão para o dia: {data['Day']['IconPhrase']}
                           Previsão para a noite: {data['Night']['IconPhrase']}"""
            return forecast
        except (requests.exceptions.RequestException, ValueError, KeyError) as e:
            print(f"Error getting daily forecast: {e}")
        return None


class WeatherCog(ity.Extension):
    @ity.slash_command(name="weather", description="Digite o nome da sua cidade e a sigla do seu estado"
                                                   " para saber a previsão do tempo para hoje!")
    @ity.slash_option(name="cidade", description="Digite o nome da cidade desejada",
                      required=True, opt_type=ity.OptionType.STRING)
    @ity.slash_option(name="estado",
                      description="Digite a sigla do estado que essa cidade pertence. Ex: (RJ)",
                      required=True, opt_type=ity.OptionType.STRING, max_length=2)
    async def weather_func(self, ctx: ity.SlashContext, cidade: str, estado: str):
        try:
            weather = Weather(cidade, estado)
            if weather.locationid is None:
                await ctx.send("Localização não encontrada.")
                return

            forecast = weather.daily_forecast()
            if forecast is not None:
                embeds = fweather(forecast, cidade)
                await ctx.send(embeds=embeds)
            else:
                await ctx.send("Erro ao obter a previsão do tempo.")
        except Exception as e:
            print(f"weather error: {e}")
            await ctx.send("Ocorreu um erro ao prever o tempo\nContate o Mestre Prison para mais informações")


def setup(client):
    WeatherCog(client)
