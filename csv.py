import datetime
import pycountry

def readfile (filepath): #funkcja otwierająca plik
    try:
        csvf = open(filepath, "r", encoding="utf-8")
        print("the file", filepath, "is open...")
        data=transformdata(csvf)
        csvf.close()
        return data
    except:
        print("File opening error")

# funkcja pobiera dane z pliku w sposób umożliwiający dalszą pracę
def transformdata (data):
    tdata = []
    for i in data.readlines():
        dat= []
        countrycode="XXX"

        date, state, impressions, ctrprecentage = i.split(',')
        month, day, year = date.split('/')
        day, month = day.lstrip("0"), month.lstrip("0")
        dateform = datetime.datetime(year=int(year), month=int(month), day=int(day))
        #zamiana nazwy stanu/refionu na kod kraju
        for t in list(pycountry.subdivisions):
            if state in t.name:
                code = pycountry.subdivisions.get(code=t.code)
                countrycode = code.country.alpha_3
        # obliczenie zaokrąglonej liczby kliknięć
        ctrprecentage = ctrprecentage.rstrip()
        ctrprecentage = ctrprecentage.rstrip("%")
        ctr = round (float(impressions)*float(ctrprecentage)/100)

        dat.append(dateform)
        dat.append(countrycode)
        dat.append(impressions)
        dat.append(ctr)
        tdata.append(dat)
    return tdata

# sortowanie wg dwóch kolumn
def sortdata(data):
    data.sort(key=lambda row: row[1])
    data.sort(key=lambda row: row[0])
    return data

#funkcja tworząca nowy plik csv
def writefile(data):
    try:
        csvresult= open(fileresultname, "w", encoding="utf-8")
        for i in data:
            x = 0
            for j in i:
                if type(j) == datetime.datetime:
                    j=j.strftime("%Y-%m-%d")

                csvresult.write(str(j))
                x = x + 1

                if x < len(i):
                    csvresult.write(',')

            csvresult.write('\n')
        print("the file", fileresultname, " is created...")
        csvresult.close()
    except:
        print("Error in writing")


filepath="file.csv"
fileresultname="result.csv"

t = readfile(filepath)
x = sortdata(t)
writefile(x)