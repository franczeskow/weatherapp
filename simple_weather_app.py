import requests
import sys
from matplotlib import pyplot as plt


def get_atrributes():
    """Gets argument/s from command line"""

    try:
        city = sys.argv[1]
        days = sys.argv[2]
        if not days.isnumeric():
            return city
        return city, int(days)*8        #if user enters two arguments
    except IndexError:
        try:
            city = sys.argv[1]
            return city                 #if user enters one argument
        except IndexError:
            raise Exception("Musisz podać przynajmniej 1 argument. Użycie: simple_weather_app.py miasto liczba_dni , lub simple_weather_app.py miasto") #if user enters no argument


def make_request_link():

    try:
        city, days = get_atrributes()
        api_link = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&" \
                   f"appid=d44e7f7aa89ce8910ce865324840365d&units=metric&lang=pl&cnt={days}" # Link for weather forecast
        return api_link
    except ValueError:
        city = get_atrributes()
        api_link = f"http://api.openweathermap.org/data/2.5/weather?q={city}" \
                   f"&appid=d44e7f7aa89ce8910ce865324840365d&units=metric&lang=pl"  # Link for weather now
        return api_link


def parse_one_day_data(api_response):
    """ Prints entered data"""

    print(f"Pogoda w {api_response.json()['name']} to:")
    print(f"Temperatura: {api_response.json()['main']['temp']}°")
    print(f"Temperatura Odczuwalna: {api_response.json()['main']['feels_like']}°")
    print(f"Maksymalna temperatura dzisiaj: {api_response.json()['main']['temp_max']}°")
    print(f"Aura: {api_response.json()['weather'][0]['description']}")


def parse_multi_days_data(dates_list,temp_list):
    """ Plots entered data"""

    plt.rcParams["figure.figsize"] = [15, 9]  # Window size
    plt.plot(dates_list,temp_list,"r-o")
    plt.title(f"Wykres temparatur dla {int(len(dates_list)/8)} dni")
    plt.xticks(rotation="vertical")  # Making labels vertical
    plt.xlabel("Dzień i godzina")
    plt.ylabel("Temperatura w celcjuszach")
    plt.show()


def get_show_data():
    """ Main function, checks if request is ok, then depending if user entered one or two arguments,
     choses way of showing data"""

# Getting request
    api_response = requests.get(make_request_link())

# Check if request correct
    if api_response.status_code == 404:
        print(f"Nie znaleziono miasta! Http Error code:{api_response.status_code}")
        return -1
    elif api_response.status_code != 200:
        print(f"Cos poszło nie tak! Http Error code:{api_response.status_code}")
        return -1

# Makes lists for plot, or show one day data
    try:
        temp_list = []
        dates_list = []

        for dict in api_response.json()["list"]:
            temp_list.append(dict["main"]["temp"])
            dates_list.append(dict["dt_txt"][5:16])

        parse_multi_days_data(dates_list,temp_list)
    except KeyError:
        parse_one_day_data(api_response)


if __name__=="__main__":
    get_show_data()