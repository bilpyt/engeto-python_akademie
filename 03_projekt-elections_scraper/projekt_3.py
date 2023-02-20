"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie

author: Jan Hlaváček
e-mail: jan@hlavackovi.net
discord: Jan H.#7413
"""
import sys
import csv
from requests import get
from bs4 import BeautifulSoup as bs


def parsovani_rozcestniku_na_obce(adresa):
    """
    Funkce stáhne stránku z URL zadané do prvního agumentu a provede
    parsování názvu obcí, odkazů na jejich výsledky a jejich ID.
    Vrací slovník "obce" ve formátu:
    {0: ["Alojzov", "https://...", 506761], 1: [...]}
    """
    rozcestnik = get(adresa)
    rozcestnik_rozdeleny = bs(rozcestnik.text, features="html.parser")
    obce = {}
    bunky_s_odkazy = rozcestnik_rozdeleny.find_all("td", {"class": "cislo"})
    bunky_s_nazvy = rozcestnik_rozdeleny.find_all("td", {"class": "overflow_name"})

    for i in range(len(bunky_s_nazvy)):
        obce[i] = [\
            bunky_s_nazvy[i].string, \
            f"{adr}/{bunky_s_odkazy[i].a.get('href')}",\
            int(bunky_s_odkazy[i].string)\
            ]
    return obce


def parsovani_vysledku_obce(poradi_obce_v_seznamu, obce):
    """
    Funkce parsuje výsledky pro danou obec.
    Jako vstup potřebuje slovník "obce" a klíč, která obec bude zpracovávána.

    Nejprve stáhne výsledkové html obce a následně parsuje data:
    "pocet_volicu, odevzdane_obalky, platne hlasy"

    Současně obsahuje vnořenou funkci, která zajišťuje parsování
    stran a počet získaných hlasů u dané obce.

    Funkce následně vrací dva slovníky ve formátu:
    vysledky_obce = {1: ["Občanská demo...", 29], 2: [...]}
    volici_obce = {"registered: 205, "envelopes": 145, "valid": 144}
    """
    vysledky_obce = {}
    volici_obce = {}
    
    #Stažení stránky obce a následné zparsování do objektu bs4
    html_obec = get(obce[poradi_obce_v_seznamu][1])
    html_obec_rozdeleny = bs(html_obec.text, features="html.parser")
    
    #Parsování buněk potřebných pro přehled voličů a odevzdaných hlasů
    pocet_volicu = html_obec_rozdeleny.find_all("td", {"headers": "sa2"})
    odevzdane_obalky = html_obec_rozdeleny.find_all("td", {"headers": "sa3"})
    platne_hlasy = html_obec_rozdeleny.find_all("td", {"headers": "sa6"})

    #Parsování čistých hodnot do slovníku "volici_obce"
    volici_obce["registered"] = int(pocet_volicu[0].string.replace("\xa0", ""))
    volici_obce["envelopes"] = int(odevzdane_obalky[0].string.replace("\xa0", ""))
    volici_obce["valid"] = int(platne_hlasy[0].string.replace("\xa0", ""))

    def parsovani_tabulky_vysledku(j):
        """
        Vnořená funkce pro zparsování jednoho sloupce tabulky s výsledky.
        Funkce vrací část výsledného slovníku "vysledky_obce", která odpovídá
        levé tabulce výsledků v případě argumentu 1 a pravé tabulce výsledků
        v případě argumentu 2.
        """
        #Parsování buněk tabulky s indexem, názvy a výsledky stran
        bunky_s_indexem_stran = html_obec_rozdeleny.find_all("td", {"headers": f"t{j}sb1"})
        bunky_s_nazvy_stran = html_obec_rozdeleny.find_all("td", {"headers": f"t{j}sb2"})
        bunky_s_cisly = html_obec_rozdeleny.find_all("td", {"headers": f"t{j}sb3"} )
        vysledky_obce_cast = {}
        for i in range(len(bunky_s_cisly)):
            #Vynechání prázdných skrytých buněk nakonci stránky
            if bunky_s_cisly[i].string == "-":
                continue
            else:
                #Parsování čistých hodnot do slovníku "vysledky_obce_cast"
                vysledky_obce_cast[int(bunky_s_indexem_stran[i].string)] = [\
                                            bunky_s_nazvy_stran[i].string, \
                                            int(bunky_s_cisly[i].string.replace("\xa0", ""))\
                                            ]
        return vysledky_obce_cast

    #Vytvoření kompletního slovníku s výsledky stran pro danou obec
    vysledky_obce.update(parsovani_tabulky_vysledku(1))
    vysledky_obce.update(parsovani_tabulky_vysledku(2))

    return vysledky_obce, volici_obce


def vytvor_slovnik_s_vysledky(adresa):
    """
    Funkce tvoří slovník se všemi potřebnými daty pro každou obec.
    Nejdříve zavoláním funkce "parsovni_rozscestniku_na_obce" vytvoří
    slovník se základními daty pro každou obec a následně přidá ke každé
    touple se slovníky s výsledky voláním "parsovani_vysledku_obce"

    Vrací pak slovník "obce" ve formátu:
    {0: ["Alojzov", "https://...", 506761,
    ({1: ["Občanská demo...", 29], 2: ...},
    {"registered: 205, "envelopes": 145, "valid": 144})]}
    """
    obce = {}
    obce = parsovani_rozcestniku_na_obce(adresa)
    for i in obce:
        obce[i].append(parsovani_vysledku_obce(i, obce))
    return obce


def vytvor_csv_slovnik(obce):
    """
    Funkce provede rozřazení dat ze slovníku "obce" do nového "csv_dict".
    Klíče tohoto slovníku odpovídají jednotlivým řádkům výsledného CSV souboru.
    Hodnota každé klíče je list hodnot, kdy každý element odpovídá
    jednomu sloupci požadované tabulky.
    Hodnoty prvního (nultého klíče) odpovídají záhlaví tabulky.

    Vrací tedy slovník "csv_dict" ve tvaru:
    {0: ["code", "location", "registred", "envelopes", "valid", "Občan. demo..."...]
    1: [506761, "Alojzov", 205, 145, 144, 29, 0, 0, 9...]}
    """
    csv_dict = {}
    
    #Tvorba prvního klíče(řádku) - záhlaví tabulky
    csv_dict[0] = ["code", "location", "registred", "envelopes", "valid"]
    for id,nazev in obce[0][3][0].items():
        csv_dict[0].append(nazev[0])

    #Tvorba dalšího klíčů(řádků) s výsledky pro jednotlivé obce
    for i in obce:
        csv_dict[i+1] = []
        csv_dict[i+1].append(obce[i][2])
        csv_dict[i+1].append(obce[i][0])
        csv_dict[i+1].append(obce[i][3][1]["registered"])
        csv_dict[i+1].append(obce[i][3][1]["envelopes"])
        csv_dict[i+1].append(obce[i][3][1]["valid"])
        for id,nazev in obce[i][3][0].items():
            csv_dict[i+1].append(nazev[1])
    return csv_dict


def zapis_csv_soubor(csv_dict, soubor):
    """
    Funkce provede zápis dat ze slovníku "csv_dict" do souboru,
    jehož název je zadán jako druhý parametr při spouštění programu.
    Zápis je proveden csv dialektem "excel-tab", kdy jednotlivé
    hodnoty/sloupce jsou odděleny tabelátorem.
    """
    with open(soubor, mode="w") as nove_csv:
        zapisovac = csv.writer(nove_csv, dialect="excel-tab",)
        for i in csv_dict:
            zapisovac.writerow(csv_dict[i])


if __name__ == "__main__":
    #Zpracování vstupních proměnných
    adresa = sys.argv[1]
    soubor = sys.argv[2]
    adr = adresa.rsplit("/", 1)[0]

    #Běh programu
    print(f"Stahuji data z vybraného URL {adresa}")
    obce = vytvor_slovnik_s_vysledky(adresa)
    csv_dict = vytvor_csv_slovnik(obce)
    print(f"Ukládám data do souboru {soubor}")
    zapis_csv_soubor(csv_dict, soubor)
    print("Ukončuji program election-scraper")