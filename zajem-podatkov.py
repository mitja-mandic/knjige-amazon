import orodja
import re
import requests
import bs4

link = "https://www.nepremicnine.net/"
naslovna = orodja.shrani_spletno_stran(link,"podatki/naslovna.html") #naslovno stran rabimo za regije
vsebina = orodja.vsebina_datoteke("podatki/naslovna.html")
juha = bs4.BeautifulSoup(vsebina, 'html.parser')

#vzorec_linka = re.compile()

#for i in juha.find_all('a', 'href'):
#    print(i)^




stevilo_strani = 5
for stran in range(1,stevilo_strani):
    if stran == 1:
        datoteka = f"podatki/nepremicnine{stran}.html"
        url = f"https://www.nepremicnine.net/oglasi-prodaja/"
        orodja.shrani_spletno_stran(url, datoteka)
        vsebina = orodja.vsebina_datoteke(datoteka)
    else:
        url = f"https://www.nepremicnine.net/oglasi-prodaja/{stran}/"
        datoteka = f"podatki/nepremicnine{stran}.html"
        orodja.shrani_spletno_stran(url, datoteka)
#print(count)


page = orodja.vsebina_datoteke("nepremicnine1.html")
soup = bs4.BeautifulSoup(page, 'html.parser')
with open("test.html",'w', encoding='utf-8') as d:
    d.write(soup.prettify())

for povezava in soup.find_all('h2'):
    link = povezava.get('data-href')
    id = int(re.search(r'\d{7}', link).group(0))
    lokacija = list(povezava.descendants)[-1]
    #print(id, lokacija)

seznam_lokacij = [lokacija.get_text() for lokacija in soup.find_all('span', class_="title")]
