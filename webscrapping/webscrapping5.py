
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
#from selenium.webdriver.support import expected_conditions as EC
#from selenium.webdriver.common.by import By
import pandas as pd
#from openpyxl import Workbook
#import numpy as np
from unidecode import unidecode
pd.set_option('display.max_columns', None)

import time

pd.set_option('display.max_rows', 10)
pd.set_option('display.min_rows', 10)




driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.implicitly_wait(45)

#"https://www.transfermarkt.pl/bundesliga/marktwerteverein/wettbewerb/L1"
#"https://www.transfermarkt.pl/premier-league/marktwerteverein/wettbewerb/GB1"
#"https://www.transfermarkt.pl/ligue-1/marktwerteverein/wettbewerb/FR1"
#"https://www.transfermarkt.pl/laliga/marktwerteverein/wettbewerb/ES1"
#"https://www.transfermarkt.pl/serie-a/marktwerteverein/wettbewerb/IT1"
#"https://www.transfermarkt.pl/liga-nos/marktwerteverein/wettbewerb/PO1"

transfermarkt_df = pd.DataFrame([])


ligi_linki = ["https://www.transfermarkt.pl/bundesliga/marktwerteverein/wettbewerb/L1",
              "https://www.transfermarkt.pl/premier-league/marktwerteverein/wettbewerb/GB1",
              "https://www.transfermarkt.pl/ligue-1/marktwerteverein/wettbewerb/FR1",
              "https://www.transfermarkt.pl/laliga/marktwerteverein/wettbewerb/ES1",
              "https://www.transfermarkt.pl/serie-a/marktwerteverein/wettbewerb/IT1",
              "https://www.transfermarkt.pl/liga-nos/marktwerteverein/wettbewerb/PO1"
              ]

ligi = ["bundesliga", "premier league", "ligue 1", "laliga", "serie a", "liga nos"]



for liga in range(6):
    website = ligi_linki[liga]
    driver.get(website)
    jaka_liga = ligi[liga]
    

    #tworzę listę klubów piłkarskih z wybranej ligi
    clubs_web = driver.find_elements(
        "xpath",'//table[@class="items"]/tbody/tr/td[@class="hauptlink no-border-links"]/a[@title]')
    clubs = []

    for club in clubs_web:
        clubs.append(club.text)
        
    #tworzę listę linków z każdym klubem z danej ligi
    club_web2 = driver.find_elements("xpath",'//table[@class="items"]/tbody/tr/td[@class="hauptlink no-border-links"]/a')
    clubs_links = list()


    for club in club_web2:
        clubs_links.append(club.get_attribute("href"))
        
    #tworzę puste listy do petli nizej
    nazwa =[]
    pozycja = []
    data_urodzenia = []
    wzrost = []
    noga = []
    kontrakt_od = []
    kontrakt_do = []
    wartosc_eur = []
    klub = []
    liga = []
        
        
    ile_zespolow = len(clubs_links)
    # przechodzenie przez linki i klik na szczegoly
    for n in range(ile_zespolow):    
        driver.get(clubs_links[n])
        details_button = driver.find_element("xpath",'//a[@class="tm-tab"][1]')
        details_button.click()
        #powtarzalna sciezka xpath
        tabela = driver.find_elements("xpath",'//table[@class="items"]/tbody/tr')
        len(tabela)
        len(nazwa)
        #petla, ktora pobiera dane zawodnikow
        for i in tabela:
            data_urodzenia.append(i.find_element("xpath",'./td[3]').text)
            wzrost.append(i.find_element("xpath",'./td[5]').text)
            noga.append(i.find_element("xpath",'./td[6]').text)
            kontrakt_od.append(i.find_element("xpath",'./td[7]').text)
            kontrakt_do.append(i.find_element("xpath",'./td[9]').text)
            wartosc_eur.append(i.find_element("xpath",'./td[10]').text)
            pozycja.append(i.find_element("xpath",'./td[2]/table/tbody/tr[2]').text)
            name = (i.find_element("xpath",'./td[2]/table/tbody/tr[1]').text)
            nazwa.append(name)
            print(name) #do sprawdzenia czy ta petla dziala prawidlowo
            klub.append(clubs[n])
            liga.append(jaka_liga)


        

    #umieszczam dane w DataFrame 
    df = pd.DataFrame({'klub': klub, 'pilkarz': nazwa, 'pozycja': pozycja, 'data_urodzenia': data_urodzenia, 'wzrost': wzrost, 
                  'dominujaca_noga': noga, 'kontrakt_od': kontrakt_od, 'kontrakt_do': kontrakt_do, 
                  'wartosc_eur': wartosc_eur, 'liga': liga})

    transfermarkt_df = transfermarkt_df.append(df, ignore_index=True)

    transfermarkt_df.to_csv('transfermarkt.csv', index=True, encoding="utf-8")
    print(transfermarkt_df)
    transfermarkt_df.to_excel('transfermarkt.xlsx')
        

driver.quit()




#----------------------------------------------------------

transfermarkt_df = pd.read_csv(r'C:\Users\User\transfermarkt.csv', encoding="utf-8")
transfermarkt_df = transfermarkt_df.drop(['Unnamed: 0'], axis = 1)
transfermarkt_df.head()


tf_df = transfermarkt_df.copy()

#Data urodzenia zawiera faktyczną datę oraz wiek pilkarza, ktory moze sie przydac przy laczeniu danych oraz analizie
tf_df['wiek'] = tf_df['data_urodzenia'].str.strip().str[-3:]
tf_df['wiek'] = tf_df['wiek'].str.replace(')','')


#kolumna wartosc_eur zawiera znak €, przecinki oraz mln i tys
tf_df['wartosc_eur'] = tf_df['wartosc_eur'].str.replace('€','')
tf_df['wartosc_eur'] = tf_df['wartosc_eur'].str.replace('.','')
tf_df['wartosc_eur'] = tf_df['wartosc_eur'].str.replace(' ','')
tf_df['wartosc_eur'] = tf_df['wartosc_eur'].str.replace(',','')


#te wartosci potencjalnie do wyrzucenia, są to zawodnicy zawieszeni, konczacy kariere etc.
pd.unique(tf_df['wartosc_eur'].str[-3:])
tf_df[tf_df['wartosc_eur'].str[-3:] == '-'] 

#zamiana mln
wart = tf_df['wartosc_eur'].str[-3:] == "mln"
tf_df.loc[wart, 'wartosc_eur'] =tf_df.loc[wart, 'wartosc_eur'].str.replace('mln','')
tf_df.loc[wart, 'wartosc_eur'] =tf_df.loc[wart, 'wartosc_eur'].astype(float)
tf_df.loc[wart, 'wartosc_eur'] =tf_df.loc[wart, 'wartosc_eur'].apply(lambda x: x* 10000)


#zamiana tys
wart2 = tf_df['wartosc_eur'].str[-3:] == "tys"
tf_df.loc[wart2, 'wartosc_eur'] =tf_df.loc[wart2, 'wartosc_eur'].str.replace('tys','')
tf_df.loc[wart2, 'wartosc_eur'] =tf_df.loc[wart2, 'wartosc_eur'].astype(float)
tf_df.loc[wart2, 'wartosc_eur'] =tf_df.loc[wart2, 'wartosc_eur'].apply(lambda x: x* 1000)


tf_df

tf_df.to_csv(r'C:\Users\User\tf_df.csv', index=True)





#-------------------------------------------------------------------------------------
#sofifa - statystyki piłkarzy z gry fifa23

#https://sofifa.com/players?type=all&lg%5B%5D=13&lg%5B%5D=16&lg%5B%5D=19&lg%5B%5D=31&lg%5B%5D=53&lg%5B%5D=308
#def document_initialised(driver):
#   return driver.execute_script("return initialised")


website2 ="https://sofifa.com/players?type=all&lg%5B%5D=13&lg%5B%5D=16&lg%5B%5D=19&lg%5B%5D=31&lg%5B%5D=53&lg%5B%5D=308"
driver.get(website2)



#licze ile jest stron
ile_stron = 0
for s in range(100):
    ile_stron += 1
    next_button = driver.find_element("xpath",'//span[@class="bp3-icon bp3-icon-chevron-right"]')
    next_button.click()
    
pilkarze_fifa = []
website2 ="https://sofifa.com/players?type=all&lg%5B%5D=13&lg%5B%5D=16&lg%5B%5D=19&lg%5B%5D=31&lg%5B%5D=53&lg%5B%5D=308"
driver.get(website2)

s = 0
for s in range(ile_stron):
    if s == 0:
        for row in range(60):
            WebDriverWait(driver, timeout=10).until(lambda d:driver.find_element("xpath",
                '//table[@class="table table-hover persist-area"]/tbody/tr['+ str(row+1) +']'))
            temp = driver.find_element("xpath",
                '//table[@class="table table-hover persist-area"]/tbody/tr['+ str(row+1) +']').text
            temp = temp.splitlines()
            #print(temp)
            temp2 = driver.find_element("xpath",
                '//table[@class="table table-hover persist-area"]/tbody/tr['+ str(row+1) +']//a').get_attribute("aria-label")
            temp.append(temp2)
            pilkarze_fifa.append(temp)
        print(s)
    else:
        next_button = driver.find_element("xpath",'//span[@class="bp3-icon bp3-icon-chevron-right"]')
        next_button.click()
        for row in range(60):
            WebDriverWait(driver, timeout=10).until(lambda d:driver.find_element("xpath",
                '//table[@class="table table-hover persist-area"]/tbody/tr['+ str(row+1) +']'))
            temp = driver.find_element("xpath",
                '//table[@class="table table-hover persist-area"]/tbody/tr['+ str(row+1) +']').text
            temp = temp.splitlines()
            #print(temp)
            temp2 = driver.find_element("xpath",
                '//table[@class="table table-hover persist-area"]/tbody/tr['+ str(row+1) +']//a').get_attribute("aria-label")
            temp.append(temp2)
            pilkarze_fifa.append(temp)
        print(s)
        pilkarze_fifa_df = pd.DataFrame(pilkarze_fifa)
        

#'//a[@class="bp3-button bp3-intent-primary pjax"]'

 

driver.quit()
        
        
pilkarze_fifa_df = pd.DataFrame(pilkarze_fifa)
print(pilkarze_fifa_df)
pilkarze_fifa_df.to_csv('sofifa2.csv', index=True, encoding="utf-8")
pilkarze_fifa_df.to_excel('sofifa2.xlsx')



#----------------------------------------------------------
pilkarze_fifa_df = pd.read_csv(r'C:\Users\User\sofifa2.csv', encoding="utf-8")
#pilkarze_fifa_df = pd.read_excel(r'C:\Users\User\sofifa2.xlsx', sheet_name = "Sheet1")

pilkarze_fifa_df.head() #wygląda na to, że mamy dodatkową kolumnę
pilkarze_fifa_df.iloc[:,22].unique() 
pilkarze_fifa_df[pilkarze_fifa_df.iloc[:,22] == 'João Félix Sequeira'] #dodatkowa informacja - pilkarze na wypozyczeniu

#fifa_columns = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]
fifa_columns = [*range(23)]
pilkarze_fifa_df.columns = fifa_columns #nadaję tymczasowe nazwy kolumn


pilkarze_fifa_df = pilkarze_fifa_df.drop([0], axis = 1) # usuwam pustą kolumnę 
pilkarze_fifa_df[22].unique()
#pilkarze_fifa_df = pilkarze_fifa_df.drop([23], axis = 1) # usuwam pustą kolumnę 

pilkarze_fifa_df.head(5)
pilkarze_fifa_df[7]



pd.unique(pilkarze_fifa_df[22]) # wyglada na to, że w niektórych przypadkach mielismy wiecej wartosci w danej kolumnie
print(pilkarze_fifa_df[~pilkarze_fifa_df[22].isnull()]) 

check = (pilkarze_fifa_df[~pilkarze_fifa_df[22].isnull()])
print(pd.unique(check[7])) # w kolumnie 7 dodala sie wartosc "ON LOAN" u pilkarzy ktorzy sa na wypozyczeniu

fifa_df = pilkarze_fifa_df.copy()
fifa_df = fifa_df.rename(columns={fifa_df.columns[6]: 'value'})
print(fifa_df[fifa_df['value'] == "ON LOAN"])

#trzeba usunac wartosci "ON LOAN" i przesunac te dane o kolumne w lewo

loan = fifa_df['value'] == "ON LOAN"
fifa_df[loan]

fifa_df.loc[loan, 'value':] = fifa_df.loc[loan, 'value':].shift(-1, axis=1)
print(fifa_df[fifa_df['value'] == "ON LOAN"])


print(pd.unique(fifa_df[22]))
non_nan_count = fifa_df[22].count()
print(non_nan_count)
fifa_df = fifa_df.drop([22], axis = 1) # usuwam pustą kolumnę 

fifa_df.info()
fifa_df.head()

#koluma 1 zawiera dane o pozycjach jak i wieku

fifa_df['AGE'] = fifa_df[2].str.strip().str[-2:]
fifa_df[2] = fifa_df[2].str[:-2]

#value zawiera wartosc pilkarza oraz jego zarobki, rozdziele to na dwie kolumny
fifa_df_split = fifa_df['value'].str.split(' ', expand = True)
fifa_df = pd.concat([fifa_df, fifa_df_split], axis=1)
fifa_df = fifa_df.drop(['value'], axis = 1)




#kolumna 2 - niektórzy pilkarze maja przypisane kilka pozycji, z zestawu danych transfermarkt mam dominujaca pozycje,
# prawdopodobnie skorzystam w analizie z tamtych danych, te kolumne zostawiam, gdyby jednak miala sie przydac

#zmiana nazw kolumn
fifa_columns = ['NAME', 'POSITIONS', 'OVA', 'POT', 'TEAM', 'CONTRACT_LENGTH', 'ATTACKING', 'SKILL', 
                'MOVEMENT', 'POWER', 'MENTALITY', 'DEFENDING', 'TOTAL', 'PAC', 'SHO', 'PAS', 'DRI', 'DEF', 'PHY',
                'FULL_NAME', 'AGE', 'VALUE_EUR', 'SALARY_EUR']
len(fifa_columns)
fifa_df.columns = fifa_columns

#czyszczenie kolumn value_eur i salary_eur
fifa_df['VALUE_EUR'] = fifa_df['VALUE_EUR'].str.replace('€','')

         
pd.unique(fifa_df['VALUE_EUR'].str[-1:])

val = fifa_df['VALUE_EUR'].str[-1:] == "M"

fifa_df.loc[val, 'VALUE_EUR'] = fifa_df.loc[val, 'VALUE_EUR'].str.replace('M','')
fifa_df.loc[val, 'VALUE_EUR'] = fifa_df.loc[val, 'VALUE_EUR'].astype(float)
fifa_df.loc[val, 'VALUE_EUR'] = fifa_df.loc[val, 'VALUE_EUR'].apply(lambda x: x* 1000000)


val2 = fifa_df['VALUE_EUR'].str[-1:] == "K"
fifa_df.loc[val2, 'VALUE_EUR'] = fifa_df.loc[val2, 'VALUE_EUR'].str.replace('K','')
fifa_df.loc[val2, 'VALUE_EUR'] = fifa_df.loc[val2, 'VALUE_EUR'].astype(float)
fifa_df.loc[val2, 'VALUE_EUR'] = fifa_df.loc[val2, 'VALUE_EUR'].apply(lambda x: x* 1000)

fifa_df['VALUE_EUR'] = fifa_df['VALUE_EUR'].astype(float)

# czyszczenie salary_eur
pd.unique(fifa_df['SALARY_EUR'].str[-1:])

val3 = fifa_df['SALARY_EUR'].str[-1:] == "K"

fifa_df['SALARY_EUR'] = fifa_df['SALARY_EUR'].str.replace('K','')
fifa_df['SALARY_EUR'] = fifa_df['SALARY_EUR'].str.replace('€','')
fifa_df['SALARY_EUR'] = fifa_df['SALARY_EUR'].astype(float)
fifa_df['SALARY_EUR'] = fifa_df['SALARY_EUR'].apply(lambda x: x* 1000)




#fifa_df[val, 'VALUE_EUR']
fifa_df['VALUE_EUR']

fifa_df.to_csv('sofifa3.csv', index=True, encoding="utf-8")
fifa_df.to_excel('sofifa3.xlsx')

sf_df = fifa_df.copy()


#---------------------------------------------------------------------------
#web scrapping danych z whoscored
driver = webdriver.Chrome()
driver.implicitly_wait(45)
import time

website3 ="https://www.whoscored.com"
driver.get(website3)


ws_lista = []

for x in range(6):
    website3 ="https://www.whoscored.com"
    driver.get(website3)
    time.sleep(2)
    league_button = driver.find_element("xpath", '(//ul[@id="popular-tournaments-list"])/li['+ str(x+1) +']')
    league_button.click()

    time.sleep(2)
    player_stats_button = driver.find_element("xpath", '(//*[text()="Player Statistics"])')
    player_stats_button.click()

    time.sleep(2)
    all_players_button = driver.find_element("xpath", '(//dl[@class="listbox right"]/dd[2]/a[@class="option "])[1]')
    all_players_button.click()
    
    time.sleep(2)
    page = driver.find_element("xpath", '//b[contains(text(), "Page")]').text
    page_nr = (int(page[7:9])-1)
    i = 0
    for i in range(page_nr):
        if i == 0:
            time.sleep(2)
            for n in range(10):
                
                row = driver.find_element("xpath",
                    '(//table[@id="top-player-stats-summary-grid"])/tbody/tr['+ str(n+1) +']').text
                row = row.splitlines()
                print(row)
                ws_lista.append(row) 
               
            next_button2 = driver.find_element("xpath", '(//a[@id="next"])[1]')
            next_button2.click()
        else:
            time.sleep(2)
            for n in range(10):
                
                row = driver.find_element("xpath",
                    '(//table[@id="top-player-stats-summary-grid"])/tbody/tr['+ str(n+1) +']').text
                row = row.splitlines()
                print(row)
                ws_lista.append(row)
                    
            next_button2 = driver.find_element("xpath", '(//a[@id="next"])[1]')
            next_button2.click()
    

tl_df = pd.DataFrame(ws_lista)
print(tl_df)

tl_df.to_csv('who_scored.csv', index=True, encoding="utf-8")
tl_df.to_excel('who_scored.xlsx')

#-------------------------------------------------------

#tl_df = pd.read_csv(r'C:\Users\User\who_scored.csv', encoding="utf-8")
tl_df = pd.read_excel(r'C:\Users\User\who_scored.xlsx', sheet_name = "Sheet1")

tl_df.head()

tl_df.info()
tl_df['Unnamed: 0']

tl_df = tl_df.drop(['Unnamed: 0'], axis = 1)
tl_df = tl_df.drop([0], axis = 1)

ws_df = tl_df.copy()


    


df_split = ws_df[2].str.split(',', expand=True) #kolumna zawiera info o klubie, wieku i pozycji - rozdzielam
print(df_split)

#dodaję do każdej nazwy kolumny przedrostek 'ws_', żeby być pewnym, z którego zestawu danych pochodzi informacja
ws_col = ['ws_klub', 'ws_wiek', 'ws_pozycja1', 'ws_pozycja2', 'ws_pozycja3']
df_split.columns = ws_col


df_split2 = ws_df[3].str.split(' ', expand=True) #kolumna zawiera info o różnych statystykach - rozdzielam
print(df_split2)

ws_col2 = ['ws_wystepy', 'ws_minuty', 'ws_bramki', 'ws_asysty', 'ws_zolte_kartki', 'ws_czerwone_kartki', 
           'ws_strzaly_na_mecz', 'ws_skutecznosc_podan', 'ws_wygrane_pojedynki_na_mecz', 'ws_MotM', 'ws_srednia_ocena']
df_split2.columns = ws_col2

ws_df = ws_df.drop([2], axis = 1)
ws_df = ws_df.drop([3], axis = 1)

ws_df.columns.values[0] = 'ws_nazwa_pilkarza'

ws_df = pd.concat([ws_df, df_split], axis=1)
ws_df = pd.concat([ws_df, df_split2], axis=1)


ws_df.head()

ws_df['ws_wystepy']

ws_df.to_csv(r'C:\Users\User\ws_df.csv', index=True)



#--------------------------------------------------------------------------
#proba polaczania zestawow danych

tf_df = pd.read_csv(r'C:\Users\User\tf_df.csv', index_col=(0))
ws_df = pd.read_csv(r'C:\Users\User\ws_df.csv', index_col=(0))

tf2_df = tf_df.copy()
ws2_df = ws_df.copy()

#ws_wystepy zawiera tez info o wejsciach z lawki rezerwowych. Do sortowania uzyje jedynie wystepow od poczatku
ws2_df["ws_wystepy_poczatek"] = ws2_df["ws_wystepy"].str.replace(')','').str.partition('(')[0].astype(float)
ws2_df.sort_values(by=['ws_nazwa_pilkarza', 'ws_wiek', 'ws_wystepy_poczatek'], ascending=False, inplace=True)
#po posortowaniu wzgledem wystepow moge usunac duplikaty, zostana wiersze z wieksza iloscia wystepow 
#ta akcja jest wymagana, poniewaz dane zostaly pobrane podczas okienka transferowego i pilkarz moze miec kilka wystepow w innej druzynie
duplicates_ws = ws2_df.duplicated(subset=['ws_nazwa_pilkarza', 'ws_wiek'], keep = False)
print(ws2_df[duplicates_ws])

ws2_df.drop_duplicates(subset=['ws_nazwa_pilkarza', 'ws_wiek'], inplace = True)


tf2_df.sort_values(by=['pilkarz', 'wiek', 'klub'], ascending=True, inplace=True)
duplicates_tf = tf2_df.duplicated(subset=['pilkarz', 'wiek', 'klub'], keep = False)
print(tf2_df[duplicates_tf]) #brak duplikatow w zbiorze tf



tf2_df.count()
ws2_df.count()
# w zestawie tranfsermarkt widac wiecej danych, wynika to z faktu,ze nie kazdy pilkarz jest w kadrze musial zagrac 
# dodatkowo niektorzy gracze mogli zagrac mecz, a nastepnie odejsc do innego zespolu (spoza 6 wybranych lig)


# wyglada na to, ze niektore wartosci w ts maja dodatkowa spacje na koncu, usuwam spacje

tf2_df['pilkarz']

pd.unique(tf2_df['pilkarz'].str[-1:])
pd.unique(ws2_df['ws_nazwa_pilkarza'].str[-1:]) # tutaj jest ok


tf2_df['pilkarz'] = tf2_df.pilkarz.str.replace(r'\b $', '', regex=True).str.strip()


#wyglada na to, ze usuniecie znakow specjalnych powinno poprawic dopasowanie zbiorow
#jesli to nie przyniesie skutku, sprobuje uspojnic kluby w obu zestawach, a nastepnie wyszukac po kluczu (nazwisko&klub&wiek)

from unidecode import unidecode

tf2_df['pilkarz'] = tf2_df['pilkarz'].apply(unidecode)
ws2_df['ws_nazwa_pilkarza'] = ws2_df['ws_nazwa_pilkarza'].apply(unidecode)


outer_join3 = pd.merge(tf2_df, ws2_df, left_on="pilkarz", right_on="ws_nazwa_pilkarza", how="outer", indicator=True )

outer_join3[outer_join3._merge == "left_only"].shape[0] #614 wierszy z tf nie znalazly dopasowania w ws
outer_join3[outer_join3._merge == "right_only"].shape[0] #298 wiersze z ws nie znazaly dopaswoania w tf


298/2857 #utrata 10% danych 

tf2_df['klub'].unique()
ws2_df['ws_klub'].unique()
#te same kluby w obu zbiorach maja rozne nazwy


#proba stworzenie slownika klubow

slownik = outer_join3.groupby(['klub','ws_klub']).size().reset_index(name='count')
slownik = slownik[slownik['count'] > 10]
slownik = slownik.rename(columns={slownik.columns[0]: 'slownik_klub'})
print(slownik.head(50))

slownik[slownik.duplicated(subset=["ws_klub"])] #udalo sie, brak duplikatow

ws2_df = pd.merge(ws2_df, slownik[["ws_klub" ,"slownik_klub"]], on="ws_klub", how="left" )
(ws2_df["slownik_klub"] == "").value_counts() #udalo sie, kazdy zawodnik z ws ma przypisany aktualny klub z tf



#przez wiek dane nie chca sie polaczyc
print(tf2_df['wiek'].dtypes)
print(ws2_df['ws_wiek'].dtypes)
#ws2_df['ws_wiek'] = ws2_df['ws_wiek'].str.strip() #usuwam dodatkową spacje

tf2_df[tf2_df.duplicated(subset=['pilkarz', 'wiek', 'klub'], keep=False)] #taki klucz nie ma duplikatów
test = pd.merge(tf2_df, ws2_df, left_on=('pilkarz','wiek','klub'), 
                right_on=('ws_nazwa_pilkarza','ws_wiek','slownik_klub'), how='outer', indicator=True)
test[test._merge=='left_only'].shape[0] #690 wierszy z tf nie znalazly dopasowania w ws
test[test._merge=='right_only'].shape[0] #364 wierszy z ws nie znalazly dopasowania w ts



#tworzenie unikalnego klucza (nazwisko&wiek&klub)
tf2_df['tf_klucz'] = tf2_df['pilkarz'].str.split().str[-1] + tf2_df['wiek'].astype(str) + tf2_df['klub']
ws2_df['ws_klucz'] = ws2_df['ws_nazwa_pilkarza'].str.split().str[-1] + ws2_df['ws_wiek'].astype(str) + ws2_df['slownik_klub']

tf2_df[tf2_df.duplicated(subset=["tf_klucz"], keep=False)] #tylko dwa duplikaty moreno(villareal) i silva(guimaraes)
ws2_df[ws2_df.duplicated(subset=["ws_klucz"], keep=False)] #tylko dwa duplikaty moreno(villareal) i silva(guimaraes)


test2 = pd.merge(tf2_df, ws2_df, left_on="tf_klucz", right_on="ws_klucz", how="outer", indicator=True )

test2[test2._merge == "left_only"].shape[0] #615 wierszy z tf nie znalazly dopasowania w ws
test2[test2._merge == "right_only"].shape[0] #289 wiersze z ws nie znazaly dopaswoania w tf

#sposob z kluczem używajacym nazwiska zamiast pelnej nazwy pilkarza jest lepszy
#Mimo dwoch duplikatow dopasowanie jest zdecudowanie wieksze


ws2_df[ws2_df['ws_klucz'] == 'Moreno30Villarreal CF'] #obaj w ws, usuwam obu
ws2_df[ws2_df['ws_klucz'] == 'Silva25Vitoria Guimarães SC'] #obaj w ws, usuwam obu

tf2_df[tf2_df['tf_klucz'] == 'Silva25Vitoria Guimarães SC']
tf2_df[tf2_df['tf_klucz'] == 'Moreno30Villarreal CF']

ws2_df.drop_duplicates(subset=['ws_klucz'], inplace = True, keep=False)
tf2_df.drop_duplicates(subset=['tf_klucz'], inplace = True, keep=False)


outer_join5 = pd.merge(tf2_df, ws2_df, left_on="tf_klucz", right_on="ws_klucz", how="outer", indicator=True )

outer_join5[outer_join5._merge == "left_only"].shape[0] #615 wierszy z tf nie znalazly dopasowania w ws
outer_join5[outer_join5._merge == "right_only"].shape[0] #289 wiersze z ws nie znazaly dopaswoania w tf



ws2_df.to_excel("ws5_df.xlsx")
tf2_df.to_excel("tf5_df.xlsx")

289/2866
#join po kluczu ma mniej dopasowan, ale dopasowanie jest dokladniejsze 
#jako glowny zestaw danych tratuje transfermartk, poniewaz badam wplyw na cene, tak wiec zostawiam
#wszystkie dane z transfermarkt i usuwam 284 wiersze z who_scored co stanowi ok 10% tego zbioru
#618 graczy z transfermarkt, ktorzy nie znalezli przypisanie zostaje, wielu z nich moglo nie zagrac ani jednego meczu
#i dlatego nie maja dopasowania w who_scored
left_join = pd.merge(tf2_df, ws2_df['ws_klucz'], left_on="tf_klucz", right_on="ws_klucz", how="left" )
left_join.head(5)
left_join_copy = left_join.copy()
tf2_df_copy = tf2_df.copy()



#--------------------------------------------------------------------------------------
#proba polaczanie danych left_join z danymi sofifa

fifa_df = pd.read_csv(r'C:\Users\User\sofifa3.csv', index_col=(0))

sf_df = fifa_df.copy()

sf_df.head(5)
sf_df.info()
sf_df.describe()
sf_df[sf_df.columns[sf_df.dtypes == object]].describe()


#najpierw dodam odpowiednie nazwy klubow do zestawu sofifa poprzez stworzenie slownika
#zamieniam znaki specjalne na te z alfabetu lacinskiego
sf_df['FULL_NAME'] = sf_df['FULL_NAME'].apply(unidecode)


outer_join7 = pd.merge(tf2_df, sf_df, left_on="pilkarz", right_on="FULL_NAME", how="outer", indicator=True )

outer_join7[outer_join7._merge == "left_only"].shape[0] #1043 wiersze z tf nie znalazly dopasowania w sofifa
outer_join7[outer_join7._merge == "right_only"].shape[0] #1295 wierszy z ws nie znazaly dopaswoania w tf

x = outer_join7['_merge'] == "right_only"
y = outer_join7.loc[x, "FULL_NAME"]
y.head(20)

slownik2 = outer_join7.groupby(['klub','TEAM']).size().reset_index(name='count').sort_values(by=['count'])
slownik2 = slownik2[slownik2['count'] > 1]
slownik2 = slownik2.rename(columns={slownik2.columns[0]: 'slownik_klub2'})

slownik2[slownik2.duplicated(subset=["TEAM"])] #udalo sie, brak duplikatow

sf_df = pd.merge(sf_df, slownik2[["TEAM" ,"slownik_klub2"]], on="TEAM", how="left" )
(sf_df["slownik_klub2"] == "").value_counts() #udalo sie, kazdy zawodnik z ws ma przypisany aktualny klub z tf


tf2_df.head(5)
sf_df.head(5)

#niestety ale zestaw danych sofifa ma nieaktualny wiek pilkarzy, a zestaw nie posiada daty urodzenia
#kluczem musi byc "nazwisko & klub", nazwisko mozna wyciagnac na dwa sposoby

tf2_df['tf_klucz2'] = tf2_df['pilkarz'].str.split().str[-1] + " (" +tf2_df['klub'] +")"

sf_df['NAME'] = sf_df['NAME'].apply(unidecode)
sf_df['sf_klucz'] = sf_df['FULL_NAME'].str.split().str[-1] + " (" + sf_df['slownik_klub2'] +")"
sf_df['sf_klucz2'] = sf_df['NAME'].str.split().str[-1] + " (" + sf_df['slownik_klub2'] +")"


sf_df[sf_df.duplicated(subset=["sf_klucz"], keep=False)] #125 duplikatow
sf_df[sf_df.duplicated(subset=["sf_klucz2"], keep=False)] #75 duplikatow
tf2_df[tf2_df.duplicated(subset=["tf_klucz2"], keep=False)] #64 duplikaty
#patrzac na same duplikaty lepszym kluczem w sofifa jest sf_klucz2

#dlatego, że uzupelniam braki roznymi kluczami to dodaje kolejny klucz, tym razem, musi byc w 100% unikalny
sf_df[sf_df.duplicated(subset=["FULL_NAME"], keep=False)]
sf_df["sf_unique"] = sf_df["FULL_NAME"] + sf_df["AGE"].astype(str) 


sf_df.to_csv(r'C:\Users\User\sf_df8.csv', index=True)


#stworze kopie plikow, zeby usunac duplikaty obu kluczy oddzielnie
sf_df1 = sf_df.copy() #dla klucza1
sf_df2 = sf_df.copy() #dla klucza2

sf_df1.drop_duplicates(subset="sf_klucz" ,keep=False, inplace=True)
sf_df2.drop_duplicates(subset="sf_klucz2" ,keep=False, inplace=True)

tf2_df.drop_duplicates(subset="tf_klucz2" ,keep=False, inplace=True)



#sprawdzę narazie bez wchodzenia w szczegoly, ktory klucz da lepsze dopasowanie
temp_join_sf = pd.merge(tf2_df["tf_klucz2"], sf_df1[["sf_klucz","sf_unique"]], left_on="tf_klucz2", right_on="sf_klucz", how="outer", indicator=True )

temp_join_sf[temp_join_sf._merge == "left_only"].shape[0] #694 wiersze z tf nie znalazly dopasowania w sofifa
temp_join_sf[temp_join_sf._merge == "right_only"].shape[0] #888 wierszy z sofifa nie znazaly dopaswoania w tf
temp_join_sf[temp_join_sf._merge == "both"].shape[0] #2432 wiersze z obu 



temp_join_sf2 = pd.merge(tf2_df["tf_klucz2"], sf_df2[["sf_klucz2","sf_unique"]], left_on="tf_klucz2", right_on="sf_klucz2", how="outer", indicator=True )

temp_join_sf2[temp_join_sf2._merge == "left_only"].shape[0] #214 wiersze z tf nie znalazly dopasowania w sofifa
temp_join_sf2[temp_join_sf2._merge == "right_only"].shape[0] #458 wierszy z sofifa nie znazaly dopaswoania w tf
temp_join_sf2[temp_join_sf2._merge == "both"].shape[0] #2912 wiersze z obu 
#wyglada na to, ze tutaj rowniez lepszy jest tf_klucz2


#sprawdze teraz czy braki w przypadku uzycia sf_klucz2 mozna uzupelnic przy uzyciu sf_klucz
temp3 = temp_join_sf2[temp_join_sf2._merge == "left_only"]
temp4 = pd.merge(temp3["tf_klucz2"], sf_df1["sf_klucz"], left_on="tf_klucz2", right_on="sf_klucz", how="outer", indicator=True)
temp4[temp4._merge=="left_only"].shape[0]
215-191
#dzieki zastosowaniu tf_klucz dojda dodatkowe 24 dopasowania


temp5 = temp_join_sf2[temp_join_sf2._merge!="right_only"]

temp6 = pd.merge(temp5[["tf_klucz2", "sf_klucz2", "sf_unique"]], sf_df1[["sf_klucz", "sf_unique"]], left_on="tf_klucz2", right_on="sf_klucz", how="left")


temp6[temp6["sf_klucz2"].isna()].shape[0]
temp6["sf_klucz2"].fillna(temp6["sf_klucz"], inplace=True)
temp6["sf_unique_x"].fillna(temp6["sf_unique_y"], inplace=True)

temp6[temp6["sf_klucz2"].isna()].shape[0]


temp6[temp6["sf_unique_x"].isna()].shape[0]
temp6.dropna(subset=["sf_unique_x"]).loc[temp6["sf_unique_x"].duplicated(keep=False)]
#przed łączeniem gonzalez i miranda to inni pilkarze w zestawie tf,
#nastepnie w zestawie sf tworze dwa klucze sf1 i sf2, ten sam pilkarz w zaleznosci od klucza nazywa sie raz gonzalez a raz miranda 
#przy joinie, a potem uzupelnianiu brakow do roznych pilkarzy w tf przypisuje sie ten sam z sf
#muszę usunąć te wiersze 


temp6.drop_duplicates(subset=['sf_unique_x'], inplace = True, keep=False)

temp6.dropna(subset=["sf_klucz2"]).loc[temp6["sf_klucz2"].duplicated(keep=False)]



temp6.rename(columns = {'sf_klucz2':'final_klucz'}, inplace = True)



left_join['tf_klucz2'] = left_join['pilkarz'].str.split().str[-1] + " (" +left_join['klub'] +")"

#podobnie musze usunac duplikaty z leftjoin(czyli tf_df), poniewaz nie wiem czy prawidlowo sie przypisze wiersz
left_join.duplicated(subset="tf_klucz2", keep=False).sum() #64 duplikaty
left_join[left_join.duplicated(subset="tf_klucz2", keep=False)]
left_join.drop_duplicates(subset="tf_klucz2", keep=False, inplace=True)


#lacze dane po nowym kluczu
final_df = pd.merge(left_join, temp6[["final_klucz", "sf_unique_x"]], left_on="tf_klucz2", right_on="final_klucz", how="left" )
final_df #3127 wierszy

final_df.info()

final_df.to_excel("final_df8.xlsx")















