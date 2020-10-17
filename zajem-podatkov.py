import orodja
import re
import requests

stevilo_strani = 5

vzorec = re.compile(
    r'<span class="vrsta">Stanovanje', flags=re.DOTALL
)
count = 0

for stran in range(1,stevilo_strani):
    if stran == 1:
        datoteka = f"podatki/nepremicnine{stran}.html"
        url = f"https://www.nepremicnine.net/oglasi-prodaja/"
        orodja.shrani_spletno_stran(url, datoteka)
        vsebina = orodja.vsebina_datoteke(datoteka)
        
        for zadetek in re.finditer(vzorec, vsebina):
            count += 1
            
    else:
        url = f"https://www.nepremicnine.net/oglasi-prodaja/{stran}/"
        datoteka = f"podatki/nepremicnine{stran}.html"
        orodja.shrani_spletno_stran(url, datoteka)
print(count)