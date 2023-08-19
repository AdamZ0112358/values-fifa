#This part of the code was written in Python using spyder. The variables have Polish names. 

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

#I used Xpath to locate items on the page. I set the maximum wait time per page to 45 seconds, because with less time not all the data would download.
#I could afford to do this because the data set is not that large.


#My first source of data is a website: https://www.transfermarkt.pl/, which collects data on football players, their value and also transfers between clubs.
#It can be a challenging task not to be able to display all players on one page. To download the details of all players you need to go to the league link.
#If you select the detailed view, general information such as name, position on the pitch, nationality, age, club, highest career value, last update 
#and the most important information - market value - will be displayed.
#When we enter an individual club, information such as date of birth, height, better leg, date of joining, previous club and length of contract additionally appears.
#Although it takes more time and work to click on the links for individual clubs, I think it is worth it because the additional information may prove useful.




driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.implicitly_wait(45)

#I will first look into getting the information from the transfermarkt website. 


transfermarkt_df = pd.DataFrame([])

#In the case of transfermarkt, I generated links to 6 leagues using the page, as you can see below.
#I then wrote a nested loop that first opens the link for the league in question, creates a list of clubs 
#and the associated list of links. Subsequently it goes into each of the links and retrieves the data I indicated.
#Each piece of information goes into a list, which I combine and put into a data frame and save as csv and xlsx.

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
    

    #I create a list of football clubs from a selected league
    clubs_web = driver.find_elements(
        "xpath",'//table[@class="items"]/tbody/tr/td[@class="hauptlink no-border-links"]/a[@title]')
    clubs = []

    for club in clubs_web:
        clubs.append(club.text)
        
    #I create a list of links for each club in a given league.
    club_web2 = driver.find_elements("xpath",'//table[@class="items"]/tbody/tr/td[@class="hauptlink no-border-links"]/a')
    clubs_links = list()


    for club in club_web2:
        clubs_links.append(club.get_attribute("href"))
        
    #I create empty lists for the loop below
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
    # going through the links and clicking on the details in the website
    for n in range(ile_zespolow):    
        driver.get(clubs_links[n])
        details_button = driver.find_element("xpath",'//a[@class="tm-tab"][1]')
        details_button.click()
        #repetitive xpath
        tabela = driver.find_elements("xpath",'//table[@class="items"]/tbody/tr')
        len(tabela)
        len(nazwa)
        #A loop that retrieves player's data.
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
            print(name) # to check if this loop is working correctly.
            klub.append(clubs[n])
            liga.append(jaka_liga)


        

    #I put the data in a DataFrame 
    df = pd.DataFrame({'klub': klub, 'pilkarz': nazwa, 'pozycja': pozycja, 'data_urodzenia': data_urodzenia, 'wzrost': wzrost, 
                  'dominujaca_noga': noga, 'kontrakt_od': kontrakt_od, 'kontrakt_do': kontrakt_do, 
                  'wartosc_eur': wartosc_eur, 'liga': liga})

    transfermarkt_df = transfermarkt_df.append(df, ignore_index=True)

    transfermarkt_df.to_csv('transfermarkt.csv', index=True, encoding="utf-8")
    print(transfermarkt_df)
    transfermarkt_df.to_excel('transfermarkt.xlsx')
        

driver.quit()




#------------------------------------------------------------------------------

transfermarkt_df = pd.read_csv(r'C:\Users\User\transfermarkt.csv', encoding="utf-8")
transfermarkt_df = transfermarkt_df.drop(['Unnamed: 0'], axis = 1)
transfermarkt_df.head()


tf_df = transfermarkt_df.copy()

#I pre-clean some of the data to see if I can work on it:


#The date of birth contains the actual date and age of the footballer, which can be useful for data merging and an
tf_df['wiek'] = tf_df['data_urodzenia'].str.strip().str[-3:]
tf_df['wiek'] = tf_df['wiek'].str.replace(')','')


#the value_eur column contains the € sign, commas and millions and thousands
tf_df['wartosc_eur'] = tf_df['wartosc_eur'].str.replace('€','')
tf_df['wartosc_eur'] = tf_df['wartosc_eur'].str.replace('.','')
tf_df['wartosc_eur'] = tf_df['wartosc_eur'].str.replace(' ','')
tf_df['wartosc_eur'] = tf_df['wartosc_eur'].str.replace(',','')


#these values potentially to be discarded, they are players suspended, ending their careers, etc.
pd.unique(tf_df['wartosc_eur'].str[-3:])
tf_df[tf_df['wartosc_eur'].str[-3:] == '-'] 

#conversion of millions
wart = tf_df['wartosc_eur'].str[-3:] == "mln"
tf_df.loc[wart, 'wartosc_eur'] =tf_df.loc[wart, 'wartosc_eur'].str.replace('mln','')
tf_df.loc[wart, 'wartosc_eur'] =tf_df.loc[wart, 'wartosc_eur'].astype(float)
tf_df.loc[wart, 'wartosc_eur'] =tf_df.loc[wart, 'wartosc_eur'].apply(lambda x: x* 10000)


#conversion of thousands
wart2 = tf_df['wartosc_eur'].str[-3:] == "tys"
tf_df.loc[wart2, 'wartosc_eur'] =tf_df.loc[wart2, 'wartosc_eur'].str.replace('tys','')
tf_df.loc[wart2, 'wartosc_eur'] =tf_df.loc[wart2, 'wartosc_eur'].astype(float)
tf_df.loc[wart2, 'wartosc_eur'] =tf_df.loc[wart2, 'wartosc_eur'].apply(lambda x: x* 1000)


tf_df

tf_df.to_csv(r'C:\Users\User\tf_df.csv', index=True)





#-------------------------------------------------------------------------------------
#sofifa - statistics of football players from fifa23 game

#On the sofifa website we have easy access to a huge amount of data. We can easily select the columns of interest and players from selected national leagues.
#It seems that the data will be easier to download than from transfermarkt.

#After some thought, the decision fell on the following columns:
#['NAME', 'POSITIONS', 'OVA', 'POT', 'TEAM', 'CONTRACT_LENGTH', 'ATTACKING', 'SKILL', 'MOVEMENT', 'POWER', 'MENTALITY', 
#'DEFENDING', 'TOTAL', 'PAC', 'SHO', 'PAS', 'DRI', 'DEF', 'PHY', 'FULL_NAME', 'AGE', 'VALUE_EUR', 'SALARY_EUR']
#It is important to note that we have as much as two pieces of information regarding the player's name in this collection: 
#'NAME' and 'FULL_NAME', this can be useful when the datasets will be combined with each other.

website2 ="https://sofifa.com/players?type=all&lg%5B%5D=13&lg%5B%5D=16&lg%5B%5D=19&lg%5B%5D=31&lg%5B%5D=53&lg%5B%5D=308"
driver.get(website2)

#In this case, there is only one link. In the beginning it was necessary to know the number of pages, 
#unfortunately this could only be done by clicking on 'next', and counting the repetitions in a loop.

#I then created a loop that retrieves the actual data. In this case I'm not assigning each column separately but fetching the whole table row, 
#in addition I'm also separately fetching the "FULL NAME" that was hidden in the data - in the loop it's the temp2 value:

#I count how many pages there are
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
         

driver.quit()
        
        
pilkarze_fifa_df = pd.DataFrame(pilkarze_fifa)
print(pilkarze_fifa_df)
pilkarze_fifa_df.to_csv('sofifa2.csv', index=True, encoding="utf-8")
pilkarze_fifa_df.to_excel('sofifa2.xlsx')



#----------------------------------------------------------
pilkarze_fifa_df = pd.read_csv(r'C:\Users\User\sofifa2.csv', encoding="utf-8")

pilkarze_fifa_df.head() #it looks like we have an additional column
pilkarze_fifa_df.iloc[:,22].unique() 
pilkarze_fifa_df[pilkarze_fifa_df.iloc[:,22] == 'João Félix Sequeira'] #additional information - players on loan


fifa_columns = [*range(23)]
pilkarze_fifa_df.columns = fifa_columns #I give temporary column names


pilkarze_fifa_df = pilkarze_fifa_df.drop([0], axis = 1) # I remove the empty column  
pilkarze_fifa_df[22].unique()

pilkarze_fifa_df.head(5)
pilkarze_fifa_df[7]

#After saving the data, I noticed that in some cases the values had moved by a column to the right. This was due to the additional value "ON LOAN", in column 6. 
#As the information on whether the footballer is on loan was considered irrelevant, I removed it and moved these values by a column to the left.

#As done in the previous set, I pre-clean the data and then save it to .csv and .xlsx.

pd.unique(pilkarze_fifa_df[22]) # it looks like in some cases we had more values in a given column
print(pilkarze_fifa_df[~pilkarze_fifa_df[22].isnull()]) 

check = (pilkarze_fifa_df[~pilkarze_fifa_df[22].isnull()])
print(pd.unique(check[7])) # in column 7, the value "ON LOAN" has been added in players who are on loan

fifa_df = pilkarze_fifa_df.copy()
fifa_df = fifa_df.rename(columns={fifa_df.columns[6]: 'value'})
print(fifa_df[fifa_df['value'] == "ON LOAN"])

#I need to remove the "ON LOAN" values and move this data by a column to the left

loan = fifa_df['value'] == "ON LOAN"
fifa_df[loan]

fifa_df.loc[loan, 'value':] = fifa_df.loc[loan, 'value':].shift(-1, axis=1)
print(fifa_df[fifa_df['value'] == "ON LOAN"])


print(pd.unique(fifa_df[22]))
non_nan_count = fifa_df[22].count()
print(non_nan_count)
fifa_df = fifa_df.drop([22], axis = 1) # I remove the empty column 

fifa_df.info()
fifa_df.head()

#Column 1 contains data on positions as well as age

fifa_df['AGE'] = fifa_df[2].str.strip().str[-2:]
fifa_df[2] = fifa_df[2].str[:-2]

#value contains the value of the player and his salary, I will split this into two columns
fifa_df_split = fifa_df['value'].str.split(' ', expand = True)
fifa_df = pd.concat([fifa_df, fifa_df_split], axis=1)
fifa_df = fifa_df.drop(['value'], axis = 1)



#column 2 - some players have several positions assigned.I will probably use in the analysis position from transfermarkt set
# I will leave this information as it may prove useful after all


#renaming columns
fifa_columns = ['NAME', 'POSITIONS', 'OVA', 'POT', 'TEAM', 'CONTRACT_LENGTH', 'ATTACKING', 'SKILL', 
                'MOVEMENT', 'POWER', 'MENTALITY', 'DEFENDING', 'TOTAL', 'PAC', 'SHO', 'PAS', 'DRI', 'DEF', 'PHY',
                'FULL_NAME', 'AGE', 'VALUE_EUR', 'SALARY_EUR']
len(fifa_columns)
fifa_df.columns = fifa_columns

#cleaning the value_eur and salary_eur columns
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

# cleaning salary_eur
pd.unique(fifa_df['SALARY_EUR'].str[-1:])

val3 = fifa_df['SALARY_EUR'].str[-1:] == "K"

fifa_df['SALARY_EUR'] = fifa_df['SALARY_EUR'].str.replace('K','')
fifa_df['SALARY_EUR'] = fifa_df['SALARY_EUR'].str.replace('€','')
fifa_df['SALARY_EUR'] = fifa_df['SALARY_EUR'].astype(float)
fifa_df['SALARY_EUR'] = fifa_df['SALARY_EUR'].apply(lambda x: x* 1000)


fifa_df['VALUE_EUR']

fifa_df.to_csv('sofifa3.csv', index=True, encoding="utf-8")
fifa_df.to_excel('sofifa3.xlsx')

sf_df = fifa_df.copy()


#---------------------------------------------------------------------------

#web scraping data from whoscored

#A final source of data is the website https://www.whoscored.com/.
#On the plus side, the data on the page is arranged in a table, but it takes as many as 3 clicks to get to the indicated place(league -> players statistics -> all players). 
#Moving to the next page can also be a problem. When you click on the "next" button, the whole page does not refresh, only the table elements - this can be difficult to handle.


#Retrieving the data from who scored proved to be the most difficult, as when clicking on 'next' the page did not refresh - only the data in the table changed. 
#In this case, the piece of code used on the sofifa page, which made the process wait for all items to load, was not working.
#A workaround turned out to be to non-dynamically put the process to sleep for a period of two seconds. Only this allowed all the desired data to be downloaded (time.sleep(2)).

#The loop first went to the home page, then to the corresponding league, then clicked on the player statistics, then selected all players. As on the sofifa page, 
#here too the data was taken in rows and then split into columns. The data set was then saved as .csv and .xlsx:


driver = webdriver.Chrome()
driver.implicitly_wait(45)


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


tl_df = pd.read_excel(r'C:\Users\User\who_scored.xlsx', sheet_name = "Sheet1")

tl_df.head()

tl_df.info()
tl_df['Unnamed: 0']

tl_df = tl_df.drop(['Unnamed: 0'], axis = 1)
tl_df = tl_df.drop([0], axis = 1)

ws_df = tl_df.copy()


    


df_split = ws_df[2].str.split(',', expand=True) #column contains information about the club, age and position - I separate this
print(df_split)

#I add the prefix 'ws_' to each column name to be sure which data set the information comes from
ws_col = ['ws_klub', 'ws_wiek', 'ws_pozycja1', 'ws_pozycja2', 'ws_pozycja3']
df_split.columns = ws_col


df_split2 = ws_df[3].str.split(' ', expand=True) #column contains info on various statistics - I separate this
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
#problem of merging data sets.

#This subtask proved to be the most difficult and time-consuming, due to the fact that although the data relates to the same players 
#it does not mean that these players are named the same in each set. Many abbreviations of names, abbreviated surnames, special characters or spaces were some of the problems I encountered. 
#A significant obstacle was also the fact that there were many duplicates in the who_scored set when considering the name of the footballer. 
#This was due to footballers changing clubs during the two transfer windows when the data was collected.

tf_df = pd.read_csv(r'C:\Users\User\tf_df.csv', index_col=(0))
ws_df = pd.read_csv(r'C:\Users\User\ws_df.csv', index_col=(0))

tf2_df = tf_df.copy()
ws2_df = ws_df.copy()

#ws_appearances also contains information about entries from the bench. For sorting I will use only appearances from the beginning
ws2_df["ws_wystepy_poczatek"] = ws2_df["ws_wystepy"].str.replace(')','').str.partition('(')[0].astype(float)
ws2_df.sort_values(by=['ws_nazwa_pilkarza', 'ws_wiek', 'ws_wystepy_poczatek'], ascending=False, inplace=True)

#after sorting by appearances, I can delete duplicates, leaving rows with more appearances 
#this action is required because the data was downloaded during the transfer window and a player may have several appearances in another team

duplicates_ws = ws2_df.duplicated(subset=['ws_nazwa_pilkarza', 'ws_wiek'], keep = False)
print(ws2_df[duplicates_ws])

ws2_df.drop_duplicates(subset=['ws_nazwa_pilkarza', 'ws_wiek'], inplace = True)


tf2_df.sort_values(by=['pilkarz', 'wiek', 'klub'], ascending=True, inplace=True)
duplicates_tf = tf2_df.duplicated(subset=['pilkarz', 'wiek', 'klub'], keep = False)
print(tf2_df[duplicates_tf]) #brak duplikatow w zbiorze tf



tf2_df.count()
ws2_df.count()

# in tranfsermarkt set you can see more data, this is due to the fact that not every player who is on the team had to play a match
# in addition, some players may have played a match and then left for another team (outside the 6 selected leagues)


# it seems that some values in transfermarkt have an extra space at the end, I will remove the spaces

tf2_df['pilkarz']

pd.unique(tf2_df['pilkarz'].str[-1:])
pd.unique(ws2_df['ws_nazwa_pilkarza'].str[-1:]) # no spaces


tf2_df['pilkarz'] = tf2_df.pilkarz.str.replace(r'\b $', '', regex=True).str.strip()


#it seems that removing the special characters should improve the matching of the sets
#if it doesn't work, I'll try to calm down the clubs in both sets, and then search by key (name&club&age)

from unidecode import unidecode

tf2_df['pilkarz'] = tf2_df['pilkarz'].apply(unidecode)
ws2_df['ws_nazwa_pilkarza'] = ws2_df['ws_nazwa_pilkarza'].apply(unidecode)


outer_join3 = pd.merge(tf2_df, ws2_df, left_on="pilkarz", right_on="ws_nazwa_pilkarza", how="outer", indicator=True )

outer_join3[outer_join3._merge == "left_only"].shape[0] #614 rows from transfermarkt found no match in who_scored
outer_join3[outer_join3._merge == "right_only"].shape[0] #298 rows from who_scored found no match in transfermarkt


298/2857 #10% data loss

tf2_df['klub'].unique()
ws2_df['ws_klub'].unique()
#the same clubs in both sets have different names


#creating a dictionary of teams

slownik = outer_join3.groupby(['klub','ws_klub']).size().reset_index(name='count')
slownik = slownik[slownik['count'] > 10]
slownik = slownik.rename(columns={slownik.columns[0]: 'slownik_klub'})
print(slownik.head(50))

slownik[slownik.duplicated(subset=["ws_klub"])] #successful, no duplicates

ws2_df = pd.merge(ws2_df, slownik[["ws_klub" ,"slownik_klub"]], on="ws_klub", how="left" )
(ws2_df["slownik_klub"] == "").value_counts() #It worked, every player from who_scored is assigned a current club from transfermarkt



#because of age, data doesn't want to merge
print(tf2_df['wiek'].dtypes)
print(ws2_df['ws_wiek'].dtypes)
ws2_df['ws_wiek'] = ws2_df['ws_wiek'].str.strip() #remove extra space

tf2_df[tf2_df.duplicated(subset=['pilkarz', 'wiek', 'klub'], keep=False)] #such key has no duplicates
test = pd.merge(tf2_df, ws2_df, left_on=('pilkarz','wiek','klub'), 
                right_on=('ws_nazwa_pilkarza','ws_wiek','slownik_klub'), how='outer', indicator=True)
test[test._merge=='left_only'].shape[0] #690 lines from transfermarkt found no match in who_scored
test[test._merge=='right_only'].shape[0] #364 lines from who_scored found no match in transfermarkt



#creating a unique key (name&age&club)
tf2_df['tf_klucz'] = tf2_df['pilkarz'].str.split().str[-1] + tf2_df['wiek'].astype(str) + tf2_df['klub']
ws2_df['ws_klucz'] = ws2_df['ws_nazwa_pilkarza'].str.split().str[-1] + ws2_df['ws_wiek'].astype(str) + ws2_df['slownik_klub']

tf2_df[tf2_df.duplicated(subset=["tf_klucz"], keep=False)] #only two duplicates moreno(villareal) and silva(guimaraes)
ws2_df[ws2_df.duplicated(subset=["ws_klucz"], keep=False)] #only two duplicates moreno(villareal) and silva(guimaraes)


test2 = pd.merge(tf2_df, ws2_df, left_on="tf_klucz", right_on="ws_klucz", how="outer", indicator=True )

test2[test2._merge == "left_only"].shape[0] #615 rows from transfermarkt found no match in who_scored
test2[test2._merge == "right_only"].shape[0] #289 rows from who_scored found no match in transfermarkt

#the way with the key using the surname instead of the full name of the footballer is better
#Despite two duplicates, the match is devastatingly greater


ws2_df[ws2_df['ws_klucz'] == 'Moreno30Villarreal CF'] #both in who_scored, I remove both of them
ws2_df[ws2_df['ws_klucz'] == 'Silva25Vitoria Guimarães SC'] #both in who_scored, I remove both of them

tf2_df[tf2_df['tf_klucz'] == 'Silva25Vitoria Guimarães SC']
tf2_df[tf2_df['tf_klucz'] == 'Moreno30Villarreal CF']

ws2_df.drop_duplicates(subset=['ws_klucz'], inplace = True, keep=False)
tf2_df.drop_duplicates(subset=['tf_klucz'], inplace = True, keep=False)


outer_join5 = pd.merge(tf2_df, ws2_df, left_on="tf_klucz", right_on="ws_klucz", how="outer", indicator=True )

outer_join5[outer_join5._merge == "left_only"].shape[0] #615 rows from transfermarkt did not find a match in who_scored
outer_join5[outer_join5._merge == "right_only"].shape[0] #289 rows from who_scored found no match in transfermarkt



ws2_df.to_excel("ws5_df.xlsx")
tf2_df.to_excel("tf5_df.xlsx")

289/2866

#join using this key has fewer matches, but the matching is more accurate 
#as the main data set I treat transfermartk, because I am studying the impact on price, so I leave
#all data from transfermarkt and I remove 284 rows from who_scored which is about 10% of this set
#618 players from transfermarkt who did not find an assignment remain, many of them may not have played a single match
#and therefore have no match in who_scored

left_join = pd.merge(tf2_df, ws2_df['ws_klucz'], left_on="tf_klucz", right_on="ws_klucz", how="left" )
left_join.head(5)
left_join_copy = left_join.copy()
tf2_df_copy = tf2_df.copy()



#--------------------------------------------------------------------------------------
#problem to merge left_join(transfermarkt and who_scored) data with sofif data

fifa_df = pd.read_csv(r'C:\Users\User\sofifa3.csv', index_col=(0))

sf_df = fifa_df.copy()

sf_df.head(5)
sf_df.info()
sf_df.describe()
sf_df[sf_df.columns[sf_df.dtypes == object]].describe()


#first I will add the appropriate club names to the sofifa set by creating a dictionary
#I will replace the special characters with those from the Latin alphabet.

sf_df['FULL_NAME'] = sf_df['FULL_NAME'].apply(unidecode)


outer_join7 = pd.merge(tf2_df, sf_df, left_on="pilkarz", right_on="FULL_NAME", how="outer", indicator=True )

outer_join7[outer_join7._merge == "left_only"].shape[0] #1043 rows from transfermarkt  found no match in sofifa
outer_join7[outer_join7._merge == "right_only"].shape[0] #1295 rows from sofifa found no match in transfermarkt

x = outer_join7['_merge'] == "right_only"
y = outer_join7.loc[x, "FULL_NAME"]
y.head(20)

slownik2 = outer_join7.groupby(['klub','TEAM']).size().reset_index(name='count').sort_values(by=['count'])
slownik2 = slownik2[slownik2['count'] > 1]
slownik2 = slownik2.rename(columns={slownik2.columns[0]: 'slownik_klub2'})

slownik2[slownik2.duplicated(subset=["TEAM"])] #successful, no duplicates

sf_df = pd.merge(sf_df, slownik2[["TEAM" ,"slownik_klub2"]], on="TEAM", how="left" )
(sf_df["slownik_klub2"] == "").value_counts() #successful, every player from sofifa is assigned a current club from transfermarkt


tf2_df.head(5)
sf_df.head(5)

#Unfortunately, but sofifa dataset has outdated age of footballers, and the dataset has no date of birth.
#the key must be "name & club", the name can be extracted in two ways

tf2_df['tf_klucz2'] = tf2_df['pilkarz'].str.split().str[-1] + " (" +tf2_df['klub'] +")"

sf_df['NAME'] = sf_df['NAME'].apply(unidecode)
sf_df['sf_klucz'] = sf_df['FULL_NAME'].str.split().str[-1] + " (" + sf_df['slownik_klub2'] +")"
sf_df['sf_klucz2'] = sf_df['NAME'].str.split().str[-1] + " (" + sf_df['slownik_klub2'] +")"


sf_df[sf_df.duplicated(subset=["sf_klucz"], keep=False)] #125 duplicates
sf_df[sf_df.duplicated(subset=["sf_klucz2"], keep=False)] #75 duplicates
tf2_df[tf2_df.duplicated(subset=["tf_klucz2"], keep=False)] #64 duplicates
#looking at the duplicates alone a better key in sofifa is sf_klucz2

#because I fill in the gaps with different keys then I add another key, this time, it must be 100% unique
sf_df[sf_df.duplicated(subset=["FULL_NAME"], keep=False)]
sf_df["sf_unique"] = sf_df["FULL_NAME"] + sf_df["AGE"].astype(str) 


sf_df.to_csv(r'C:\Users\User\sf_df8.csv', index=True)


#I will create a copy of the files to remove duplicates of both keys separately.
sf_df1 = sf_df.copy() #for sf_klucz1
sf_df2 = sf_df.copy() #for sf_klucz2

sf_df1.drop_duplicates(subset="sf_klucz" ,keep=False, inplace=True)
sf_df2.drop_duplicates(subset="sf_klucz2" ,keep=False, inplace=True)

tf2_df.drop_duplicates(subset="tf_klucz2" ,keep=False, inplace=True)



#check for now without going into details, which key will give a better fit
temp_join_sf = pd.merge(tf2_df["tf_klucz2"], sf_df1[["sf_klucz","sf_unique"]], left_on="tf_klucz2", right_on="sf_klucz", how="outer", indicator=True )

temp_join_sf[temp_join_sf._merge == "left_only"].shape[0] #694 rows from transfermarkt found no match in sofifa
temp_join_sf[temp_join_sf._merge == "right_only"].shape[0] #888 rows from sofifa found no match in transfermarkt
temp_join_sf[temp_join_sf._merge == "both"].shape[0] #2432 rows from both 



temp_join_sf2 = pd.merge(tf2_df["tf_klucz2"], sf_df2[["sf_klucz2","sf_unique"]], left_on="tf_klucz2", right_on="sf_klucz2", how="outer", indicator=True )

temp_join_sf2[temp_join_sf2._merge == "left_only"].shape[0] #214 rows from transfermarkt found no match in sofifa
temp_join_sf2[temp_join_sf2._merge == "right_only"].shape[0] #458 rows from sofifa found no match in transfermarkt 
temp_join_sf2[temp_join_sf2._merge == "both"].shape[0] #2912 rows from both 

#seems that here, too, tf_kklucz2 is better.


#I will now check if the deficiencies in the case of using sf_klucz2 can be made up using sf_klucz
temp3 = temp_join_sf2[temp_join_sf2._merge == "left_only"]
temp4 = pd.merge(temp3["tf_klucz2"], sf_df1["sf_klucz"], left_on="tf_klucz2", right_on="sf_klucz", how="outer", indicator=True)
temp4[temp4._merge=="left_only"].shape[0]
215-191
#thanks to the use of tf_klucz there will be an additional 24 matches


temp5 = temp_join_sf2[temp_join_sf2._merge!="right_only"]

temp6 = pd.merge(temp5[["tf_klucz2", "sf_klucz2", "sf_unique"]], sf_df1[["sf_klucz", "sf_unique"]], left_on="tf_klucz2", right_on="sf_klucz", how="left")


temp6[temp6["sf_klucz2"].isna()].shape[0]
temp6["sf_klucz2"].fillna(temp6["sf_klucz"], inplace=True)
temp6["sf_unique_x"].fillna(temp6["sf_unique_y"], inplace=True)

temp6[temp6["sf_klucz2"].isna()].shape[0]


temp6[temp6["sf_unique_x"].isna()].shape[0]
temp6.dropna(subset=["sf_unique_x"]).loc[temp6["sf_unique_x"].duplicated(keep=False)]
#before merging gonzalez and miranda are different footballers in the transfermarkt set,
#then in the sofifa set I create two keys sf1 and sf2, the same player depending on the key is called once gonzalez and once miranda 
#when I do the joins, and then fill in the gaps to different players in transfermarkt, the same one from sofifa is assigned
#I must delete these rows 


temp6.drop_duplicates(subset=['sf_unique_x'], inplace = True, keep=False)

temp6.dropna(subset=["sf_klucz2"]).loc[temp6["sf_klucz2"].duplicated(keep=False)]



temp6.rename(columns = {'sf_klucz2':'final_klucz'}, inplace = True)



left_join['tf_klucz2'] = left_join['pilkarz'].str.split().str[-1] + " (" +left_join['klub'] +")"

#similarly, I need to remove duplicates from leftjoin(i.e. tf_df) because I don't know if it will correctly assign the row
left_join.duplicated(subset="tf_klucz2", keep=False).sum() #64 duplicates
left_join[left_join.duplicated(subset="tf_klucz2", keep=False)]
left_join.drop_duplicates(subset="tf_klucz2", keep=False, inplace=True)


#I merge data with the new key
final_df = pd.merge(left_join, temp6[["final_klucz", "sf_unique_x"]], left_on="tf_klucz2", right_on="final_klucz", how="left" )
final_df #3127 rows

final_df.info()

final_df.to_excel("final_df8.xlsx")















