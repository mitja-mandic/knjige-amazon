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


def poberi_regije(datoteka): #dobim linke za posamezne regije
    vsebina = orodja.vsebina_datoteke(datoteka)
    vzorec_regije = re.compile(
        r'<a href="/oglasi-prodaja/slovenija/" class="param_r_all">Vse regije</a>'
        r'<a href="(.*?)".*?>'
        r'<a href="(.*?)".*?>'
        r'<a href="(.*?)".*?>'
        r'<a href="(.*?)".*?>'
        r'<a href="(.*?)".*?>'
        r'<a href="(.*?)".*?>'
        r'<a href="(.*?)".*?>'
        r'<a href="(.*?)".*?>'
        r'<a href="(.*?)".*?>'
        r'<a href="(.*?)".*?>'
        r'<a href="(.*?)".*?>'
        r'<a href="(.*?)".*?>'
        r'<a href="(.*?)".*?>',
        re.DOTALL)
    seznam = re.findall(vzorec_regije, vsebina)
    return ["https://www.nepremicnine.net" + link for link in seznam[0]]

def poberi_linke(st_datotek): #verjetno ne rabim. linki za posamezne oglase
    seznam_linkov = []
    for fajl in range(1,st_datotek):
        dat = f'podatki\\strani_z_oglasi\\nepremicnine{fajl}.html'
        vsebina = orodja.vsebina_datoteke(dat)
        vzorec_linka = re.compile(r'<!--<meta itemprop="url" content="(.*?)"',re.DOTALL)
        seznam_linkov += re.findall(vzorec_linka, vsebina)
    return seznam_linkov

def st_oglasov_na_regijo(url): #koliko strani z oglasi je v vsaki regiji
    ime = url.split('/')[-2]
    datoteka = f'podatki\\oglasi\\oglas_{ime}_{1}.html'
    orodja.shrani_spletno_stran(url, datoteka)
    vsebina = orodja.vsebina_datoteke(datoteka)
    vzorec_st = re.compile(r'<ul data-pages="(.*?)"', re.DOTALL)
    stevilo = re.findall(vzorec_st, vsebina)
    return (ime, int(stevilo[0]))

def zajemi_po_regiji(url): #shrani prvo stran vsake regije
    regija = st_oglasov_na_regijo(url)[0]
    stevilo_strani = st_oglasov_na_regijo(url)[1]
    for stran in range(2, stevilo_strani + 1):
        datoteka = f'podatki\\oglasi\\oglas_{regija}_{stran}.html'
        nov_url = url + f'{stran}/'
        orodja.shrani_spletno_stran(nov_url, datoteka)

def upravne_enote(datoteka_regije): #pobere linke za upravne enote iz prve strani posamezne regije. Nevem če se bom s tem ukvarjal.
    vsebina = orodja.vsebina_datoteke(datoteka_regije)
    vzorec_linka = re.compile(
        r'<h3>Upravne enote</h3>.*?a href="(.*?)".*?\[\d+?\]',
        re.DOTALL
    )
    return re.findall(vzorec_linka, vsebina)


stevilo_strani = 550
url = r"https://www.nepremicnine.net/oglasi-prodaja/slovenija/"

filename = r'podatki\strani_z_oglasi\nepremicnine1.html'
regije = poberi_regije(filename)

def zajemi_regije(seznam):
    for link in seznam:
        zajemi_po_regiji(link)

zajemi_regije(regije)


def slovar_iz_oglasa(oglas): #naredi slovar iz seznama oglasov.
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
