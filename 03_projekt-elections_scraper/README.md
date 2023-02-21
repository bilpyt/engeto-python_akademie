# Engeto - 3. projekt - elections scraper

Třetí projekt do Engeto Python Akademie.

## Popis projektu

Program slouží k extrahování výsledků okresů z parlamentních voleb v roce 2017 do formátu CSV.

## Instalace prostředí a knihoven
* Nejříve si v místním adresáři vytvoříme z prostředí CLI nové virtuální prostředí:
   ```
   python3 -m menv elections-scraper
   ```
* Provedeme jeho aktivaci
   ```
   source elections-scraper/bin/activate
   ```
* Můžeme si zkontrolovat, verzi pip a že náleží našemu virtuálnímu prostředí:
   ```
   pip3 --version
   ```
* A nainstalujeme potřebné knihovny dle souboru ```requirements.txt```
   ```
   pip3 install -r requirements.txt
   ```

## Spuštění projektu
Program spustíme z CLI pomocí souboru ```projekt_3.py``` a dvou povinných argumentů:
* URL adresa územního celku, jehož výsledky chceme scrapovat.
* Název výsledného souboru, do kterého budou data uložena.

```
python3 projekt_3.py <odkaz-uzemniho-celku> <vysledky-soubor.csv>
```
## Ukázka projektu

Výsledky hlasování pro okres Vyškov:

1. argument ```https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=11&xnumnuts=6206```
2. argument ```vysledky_vyskov.csv```

### Spuštění programu:
```
python3 projekt_3.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=11&xnumnuts=6206" "vysledky_vyskov.csv"
```

### Průběh stahování

```
Stahuji data z vybraného URL https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=11&xnumnuts=6206
Ukládám data do souboru vysledky_vyskov.csv
Ukončuji program election-scraper
```

### Částečný výstup

```
code	location	registred	envelopes	valid	Občanská demokratická strana	Řád národa - Vlastenecká unie	...
592897	Bohaté Málkovice	200	111	111	4	0	0	14	0	2	9	0	1	0	0	0	3	0	1	48	1	0	16	0	0	0	0	10	2	0
592901	Bohdalice-Pavlovice	687	426	422	25	0	0	36	0	19	42	3	0	6	1	1	21	4	6	112	0	1	54	0	3	0	1	87	0	0
...
```
