import orodja
import re
import requests
import bs4


def zajemi_strani_z_oglasi(st_strani, url):
    seznam_linkov = []
    vzorec_linka = re.compile(r'<!--<meta itemprop="url" content="(.*?)"',re.DOTALL)
    for stran in range(1,st_strani):
        if stran == 1:
            datoteka = f"podatki/nepremicnine{stran}.html"
            #url = f"https://www.nepremicnine.net/oglasi-prodaja/"
            orodja.shrani_spletno_stran(url, datoteka)
            seznam_linkov += re.findall(vzorec_linka, orodja.vsebina_datoteke(datoteka))
            print(seznam_linkov)
        else:
            novi_url = url + f"{stran}/"
            datoteka = f"podatki/nepremicnine{stran}.html"
            orodja.shrani_spletno_stran(novi_url, datoteka)
            seznam_linkov += re.findall(vzorec_linka, orodja.vsebina_datoteke(datoteka))
    return seznam_linkov

def zajemi_oglase(seznam_linkov):
    st = 1
    for link in seznam_linkov:
        datoteka = f'oglas{st}.html'
        orodja.shrani_spletno_stran(link, datoteka)
        st += 1


stevilo_strani = 550
url = r"https://www.nepremicnine.net/oglasi-prodaja/slovenija/"
seznam_linkov = zajemi_strani_z_oglasi(stevilo_strani, url)


filename = r'podatki\nepremicnine1.html'
#tega spodi verjetno ne rabiš
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