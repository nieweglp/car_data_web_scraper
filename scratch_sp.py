import requests, bs4, csv, datetime

now = datetime.datetime.now()

path = 'https://www.otomoto.pl/osobowe/uzywane' 
fileName = 'otomoto_3' + str(now.date()) + '.csv'

carFile = open(fileName, 'w', newline="")
outputWriter = csv.writer(carFile)

# connection with page
res = requests.get(path)
res.raise_for_status()

carSoup = bs4.BeautifulSoup(res.text)
lastPage = int(carSoup.select('.page')[-1].text)

# iterate through all pages
for i in range(1, lastPage):
    res = requests.get(path + '?page=' + str(i))
    res.raise_for_status()
    currentPage = bs4.BeautifulSoup(res.text)
    carList = currentPage.select('article.offer-item')
    print("parsing page " + str(i))
    for car in carList:
        currentCarData = []
        
        price = car.find('span',class_='offer-price__number').text.strip().replace(" ", "")
        currentCarData.append(price)
        
        title = car.find('a',class_='offer-title__link').text.strip()
        currentCarData.append(title)
        
        pdetails = car.find('span',class_='offer-price__details').text.strip()
        pdetails = " ".join(pdetails.split())
        currentCarData.append(pdetails)
        
        # location = car.find('span',class_='offer-item__location').text.strip().replace(" ","")
        # location = " ".join(location.split())
        # currentCarData.append(location)
        
        # iteration through parameters
        paramList = ["year", "mileage", "engine_capacity", "fuel_type"]
        for param in paramList:
            currentParameter = car.find('li', {"data-code": param})
            if (currentParameter):
                currentCarData.append(currentParameter.text.strip())
            else:
                currentCarData.append("")

        outputWriter.writerow(currentCarData)
