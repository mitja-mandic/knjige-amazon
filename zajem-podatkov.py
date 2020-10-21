import orodja
import re
import requests
import bs4

link = "https://www.nepremicnine.net/"
orodja.shrani_spletno_stran(link,"podatki/naslovna.html") #naslovno stran rabimo za regije
vsebina = orodja.vsebina_datoteke("podatki/naslovna.html")
#juha = bs4.BeautifulSoup(vsebina, 'html.parser')

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

filename = r'podatki\nepremicnine1.html'
def oglasi(datoteka):
    vzorec_oglasa = re.compile(
    r'oglasbold(.*?)<meta itemprop="priceCurrency" content="EUR" />', 
    re.DOTALL)
    vsebina_datoteke = orodja.vsebina_datoteke(datoteka)
    return re.findall(vzorec_oglasa, vsebina_datoteke)


def slovar_iz_oglasa(oglas):
    vzorec = re.compile(
        r'a href=".*?title="(?P<id>(\d{7}))' 
        r'.+?'
        r'span class="title">(?P<ime_oglasa>(.*?))<'
        r'.+?'
        r'<span class="vrsta">(?P<vrsta_nepremicnine>(.*?))<',
    re.DOTALL)
    rezultat = re.search(vzorec, oglas)
    return rezultat.groupdict()

def oglasi_iz_datoteke(datoteka):
    return[slovar_iz_oglasa(oglas) for oglas in oglasi(datoteka)]


def zajemi_podrobne_oglase(datoteka):
    seznam_id = oglasi_iz_datoteke(datoteka)
    for slovar in seznam_id:
        stevilka = int(slovar['id'])
        
        vsta = slovar['vrsta_nepremicnine'].split()
        niz_vrste = ''
        for beseda in vrsta:
            if beseda[-1] == ',':
                beseda = beseda[:-1]
            niz_vrste += beseda + '-'
        
        ime = slovar[vrsta_nepremicnine].split().strip()
        url = f'https://www.nepremicnine.net/oglasi-prodaja/{niz_vrste}-{2+2}_{stevilka}/'












#test_vzorec = re.compile(
#        r'a href=".*?title="(?P<id>(\d{7}))' 
#        r'.+?'
#        r'span class="title">(?P<ime_oglasa>(.*?))<'
#        r'.+?'
#        r'<span class="vrsta">(?P<vrsta_nepremicnine>(.*?))<',
#    re.DOTALL)
#
#print(re.search(test_vzorec,"primer_oglasa.html").groupdict())











#print(re.search(vzorec,orodja.vsebina_datoteke(r"podatki\nepremicnine1.html")).groupdict())

#page = orodja.vsebina_datoteke("nepremicnine1.html")
#soup = bs4.BeautifulSoup(page, 'html.parser')
#with open("podatki/test.html",'w', encoding='utf-8') as d:
#    d.write(soup.prettify())
#
#for povezava in soup.find_all('h2'):
#    link = povezava.get('data-href')
#    id = int(re.search(r'\d{7}', link).group(0))
#    lokacija = list(povezava.descendants)[-1]
#    #print(id, lokacija)
#
#seznam_lokacij = [lokacija.get_text() for lokacija in soup.find_all('span', class_="title")]