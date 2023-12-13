'''
This scraper is to be used only with link "https://www.carsensor.net/usedcar/spK/index1.html?YMIN=2014", 
the index inside link represent pages of the site.
'''

from bs4 import BeautifulSoup
import pandas as pd
import requests

def get_car_data(url):
    response = requests.get(url)
    html_content = response.content

    soup = BeautifulSoup(html_content, 'html.parser')

    h3_ele = soup.findAll('div', class_='cassetteMain__carInfoContainer')
    places_handle = soup.findAll("div", class_="cassetteSub__area")
    trim_colors_handle = soup.findAll("ul",class_="carBodyInfoList")

    # Set column names
    columns = [
        "maker","car_name", "prices","base_price","trim", "color","year",
        "milage","permit_validity","repair_history","guarantee","engine_size",
        "city","prefecture"
               ]
    
    makers = []
    car_names = []
    prices = []
    base_prices = []
    trims = []
    colors = []
    years = []
    milages = []
    permit_valids = []
    repair_histories = []
    guarantees = []
    engine_size = []
    cities = []
    prefectures = []


    # Loop to get trim and color of car, trim is eg: hatchback, sedan, SUV etc
    for trim_color in trim_colors_handle:
        trim = trim_color.findAll("li")[0].text
        trims.append(trim)

        color = trim_color.findAll("li")[1].text
        colors.append(color)
    
    #Loop to get car location, city and prefecture
    for places in places_handle:
        # Get cities
        city = places.findAll("p")[1].text
        cities.append(city)

        # Get Prefectures
        prefecture = places.findAll("p")[0].text
        prefectures.append(prefecture)

    '''
        Loop to get a few things:
        1. car maker
        2. car name
        3. car total price
        4. car base price
        5. years
        6. milage
        7. permit validity
        8. repair history
        9. guarantees
        10. engine size
        11. city name 
        12. prefecture name
    '''
    for h3 in h3_ele:
        #Get maker name
        maker = h3.findChildren("p")[2].text
        makers.append(maker)

        # Get car name
        car_name = h3.find("h3", class_="cassetteMain__title").find("a").text
        car_names.append(car_name)

        # Get car total price
        price_p = h3.find("p", class_="totalPrice__content").findAll("span")
        try:
            price = float(f"{price_p[0].text}" + f"{price_p[1].text}")
        except :
            price = f"{price_p[0].text}"
        prices.append(price)

        # Get car base price
        basePrice_p = h3.find("p", class_="basePrice__content").findAll("span")
        try:
            base_price = float(f"{basePrice_p[0].text}" + f"{basePrice_p[1].text}")
        except TypeError:
            base_price = float(f"{basePrice_p[0].text}")
        base_prices.append(base_price)

        #car Year, milage, permit validity period, history, include guarantee ? engine size
        detail= h3.findAll("dd", class_="specList__data")



        year = detail[0].text[:4]
        years.append(year)
        
        milage = detail[1].text
        milages.append(milage)

        permit_valid = detail[2].text
        permit_valids.append(permit_valid)

        repair_history = detail[3].text
        repair_histories.append(repair_history)

        guarantee = detail[4].text
        guarantees.append(guarantee)

        engine = detail[6].text
        engine_size.append(engine)

    data = [
            makers,
            car_names, 
            prices, 
            base_prices, 
            trims,
            colors,
            years, 
            milages,
            permit_valids,
            repair_histories, 
            guarantees, 
            engine_size,
            cities,
            prefectures
            ]    
    df = pd.concat([pd.Series(df) for df in data], axis=1, ignore_index=True)
    df.columns = columns

    return df

all_df = []
pages = int(input("How many pages of the link you wolud like to get data ? \n"))


for i in range(1,pages+1):
    url = f"https://www.carsensor.net/usedcar/spK/index{i}.html?YMIN=2014"
    print(f"creating df no {i}...")
    all_df.append(get_car_data(url))
    print(f"df no {i} done !")

print()

df = pd.concat(all_df, axis=0, ignore_index=True)
print("concatinating all together....")

print()

df.to_csv("japan_used_cars.csv")
print("done! ")




    
