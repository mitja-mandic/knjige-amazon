import orodja
import re
import requests
import bs4


def zajemi_strani_z_oglasi(st_strani, url):
    
    for stran in range(1,st_strani):
        if stran == 1:
            datoteka = f"strani_z_oglasi\\podatki\\nepremicnine{stran}.html"
            #url = f"https://www.nepremicnine.net/oglasi-prodaja/"
            orodja.shrani_spletno_stran(url, datoteka)
        else:
            novi_url = url + f"{stran}/"
            datoteka = f"strani_z_oglasi\\podatki\\nepremicnine{stran}.html"
            orodja.shrani_spletno_stran(novi_url, datoteka)
            
def poberi_regije(datoteka):
    vzorec_regije = re.compile(
        r'Vse regije</a>.*?>'
        r'(.*?)'
        r'<\a>'
        ,#r'(.*)<\a>',
    re.DOTALL)
    vsebina = orodja.vsebina_datoteke(datoteka)
    return re.findall(vzorec_regije, vsebina)

def poberi_linke(st_datotek):
    seznam_linkov = []
    for fajl in range(1,st_datotek):
        dat = f'podatki\\ strani_z_oglasi\\nepremicnine{fajl}.html'
        vsebina = orodja.vsebina_datoteke(dat)
        vzorec_linka = re.compile(r'<!--<meta itemprop="url" content="(.*?)"',re.DOTALL)
        seznam_linkov += re.findall(vzorec_linka, vsebina)
    return seznam_linkov

def zajemi_oglase(seznam_linkov):
    st = 1
    for url in seznam_linkov:
        datoteka = f'podatki\\oglasi\\oglas{st}.html'
        orodja.shrani_spletno_stran(url, datoteka)
        st += 1


stevilo_strani = 550
url = r"https://www.nepremicnine.net/oglasi-prodaja/slovenija/"
#seznam_linkov = poberi_linke(stevilo_strani)
filename = r'podatki\strani_z_oglasi\nepremicnine1.html'

print(poberi_regije(filename))

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







#def oglasi(datoteka):
#    vzorec_oglasa = re.compile(
#    r'oglasbold(.*?)<meta itemprop="priceCurrency" content="EUR" />', 
#    re.DOTALL)
#    vsebina_datoteke = orodja.vsebina_datoteke(datoteka)
#    return re.findall(vzorec_oglasa, vsebina_datoteke)
#
#
#def oglasi_iz_datoteke(datoteka):
#    return[slovar_iz_oglasa(oglas) for oglas in oglasi(datoteka)]
