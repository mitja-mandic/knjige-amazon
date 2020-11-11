import orodja
import re
import requests 
import os
import locale
locale.setlocale(locale.LC_ALL, '')

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

def zajemi_po_regiji(url, stevilo_oglasov, regija): #shrani po regijah
#    regija = st_oglasov_na_regijo(url)[0]
#    stevilo_strani = st_oglasov_na_regijo(url)[1]
    for stran in range(2, stevilo_oglasov + 1):
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

url_naslovna = r"https://www.nepremicnine.net/oglasi-prodaja/slovenija/"
datoteka_naslovna = r'podatki\strani_z_oglasi\nepremicnine1.html'

seznam = poberi_regije(datoteka_naslovna)

def zajemi_regije(seznam):
    for link in seznam:
        zajemi_po_regiji(link, st_oglasov_na_regijo(link)[1], st_oglasov_na_regijo(link)[0])

#zajemi_regije(seznam) #Datoteke so pobrane

def slovar_iz_oglasa(oglas): #naredi slovar iz seznama oglasov. Sprejme niz, vrne slovar podatkov
    vzorec = re.compile(
        r'<meta itemprop="category" content="oglasi prodaja > (?P<regija>(.+?))[>|"]'
        r'.*?'
        r'<a href=".*?title=.(?P<id>(\d+))"'
        r'.+?'
        r'span class="title">(?P<ime_oglasa>(.*?))<'
        r'.+?'
        r'<span class="vrsta">(?P<vrsta_nepremicnine>(.*?))</'
        r'.*?'
        r'<span class="tipi">(?P<tip_nepremicnine>(.*?))<'
        r'.+?'
        #r'<span class="atribut leto">Leto: <strong>(?P<leto>(\d+))<\strong>'
        #r'.+?'
        #r'(<span class="atribut">Zemljišče: <strong>(?P<zemljisce>(.*?))\s)?'
        #r'.+?'
        r'<span class="velikost" lang="sl">(?P<velikost>(.*?))</'
        r'.+?'
        r'<span class="cena">(?P<cena>(.*?))[\s|<]'
        r'.+?'
        r'<span class="agencija">(?P<agencija>(.*?))</span>',
    re.DOTALL)
    #vsebina = orodja.vsebina_datoteke(oglas)
    rezultat = re.search(vzorec, oglas)
    #rezultat = re.search(vzorec, vsebina)
    
    return rezultat.groupdict()
dat = r'podatki\oglasi\oglas_zasavska_1.html'

vzorec_zemljisce = re.compile(
     r'<span class="atribut">Zemljišče: <strong>(?P<zemljisce>(.*?))\s',
     re.DOTALL
)

vzorec_leto = re.compile(
    r'<span class="atribut leto">Leto: <strong>(?P<leto>(\d+))</',
    re.DOTALL
)

def razbij_na_oglase(datoteka): #razbije datoteko na nize oglasov, vrne seznam nizov
    vzorec_oglasa = re.compile(
    r'<div class="oglas_container oglasbold(.*?)<meta itemprop="priceCurrency" content="EUR" />', 
    re.DOTALL)
    vsebina_datoteke = orodja.vsebina_datoteke(datoteka)
    return re.findall(vzorec_oglasa, vsebina_datoteke)

#oglasi = razbij_na_oglase(dat)
#testni = oglasi[0]

#vz = vzorec_zemljisce.search(oglasi[3])
#print(vz['zemljisce'])
#print([slovar_iz_oglasa(oglas) for oglas in oglasi])


def oglasi_iz_datoteke(datoteka):
    seznam = []
    oglasi = razbij_na_oglase(datoteka)
    for oglas in oglasi:
        nepr = slovar_iz_oglasa(oglas)
        zemljisce = vzorec_zemljisce.search(oglas)
        if zemljisce:
            nepr['zemljisce'] = locale.atof(zemljisce['zemljisce'])
        else:
            nepr['zemljisce'] = None
        leto = vzorec_leto.search(oglas)
        if leto:
            nepr['leto'] = int(leto['leto'])
        else:
            nepr['leto'] = None

        nepr['id'] = int(nepr['id'])
        #if not nepr['zemljisce'] == None:
        #    nepr['zemljisce'] = locale.atof(nepr['zemljisce'])
        
        if not nepr['velikost'] == None and nepr['velikost'] != '':
            #if not nepr['velikost'] != '':
            nepr['velikost'] = nepr['velikost'][:-2]
            nepr['velikost'] = locale.atof(nepr['velikost'])
        if nepr['cena'] != "":
            nepr['cena'] = locale.atof(nepr['cena'])
        else:
            nepr['cena'] = None
        #print(nepr)
        seznam += [nepr]
        #print(len(seznam))
    return seznam

nepremicnine = []
i=0
for stran in os.listdir('podatki/oglasi'):
    #print(os.path.join('podatki/oglasi', stran))
    datoteka = os.path.join('podatki/oglasi', stran)
    print(datoteka)
    nepremicnine += oglasi_iz_datoteke(datoteka)

#print(nepremicnine[0])
##print(i)
orodja.zapisi_json(nepremicnine, r"podatki\obdelani_podatki\nepremicnine.json")
orodja.zapisi_csv(nepremicnine,['regija','id','ime_oglasa','vrsta_nepremicnine',"tip_nepremicnine","zemljisce","velikost","cena","agencija",'leto'], 
r'podatki\obdelani_podatki\nepremicnine.csv')