import requests
import pandas as pd
from bs4 import BeautifulSoup

page=1
max_page=10

url = 'https://www.cybersport.ru/base/match?disciplines=19&page=1&status=past' 
r = requests.get(url)
with open('test.html', 'w') as output_file:
  output_file.write(r.text)
result = pd.DataFrame()

r = requests.get(url) #отправляем HTTP запрос и получаем результат
soup = BeautifulSoup(r.text) #Отправляем полученную страницу в библиотеку для парсинга
tables=soup.find_all('table', {'section class':'"match center"'}) #Получаем все таблицы с вопросами
for item in tables:
    res=parse_table(item)
def parse_table(table):#Функция разбора таблицы с вопросом
    res = pd.DataFrame()

    id_match=0
    link_match=''
    date_match=''
    match=''
    who_win=''
    who_win_id=''
    who_win_link=''
    tournir=''
    who_lose=''
    who_lose_id=''
    who_lose_link=''
    tournir=''
    
    match_tr=table.find('tr',{'div class':'"match-center__teaser"'})
    #Получаем сам вопрос
    match=match_tr.find_all('td')[1].find('div').text.replace('<br />','\n').strip()
    
    widget_info=question_tr.find_all('div', {'class':'widget__info'})
    #Получаем ссылку на сам вопрос
    link_match='https://cyber.sports.ru/cs/match/tournament/csgo-2022-pgl-major-antwerp-2022-05-09/'+widget_info[0].find('a').get('href').strip()
    #Получаем уникальным номер вопроса
    id_match=link_match.split('=')[1]

    #Получаем того кто задал вопрос
    who_win=widget_info[1].find('a').text.strip()
    #Получаем ссылку на профиль
    who_win_link='https://cyber.sports.ru/cs/match/tournament/csgo-2022-pgl-major-antwerp-2022-05-09/'+widget_info[1].find('a').get('href').strip()
    #Получаем уникальный номер профиля
    who_win_id=widget_info[1].find('a').get('href').strip().split('=')[1]

    #Получаем из какого города вопрос
    
    #Получаем дату вопроса
    date_match=widget_info[1].text.split('(')[1].split(')')[1].strip()
    

    
    #Пишем в таблицу и возвращаем
    res=res.append(pd.DataFrame([[id_match,link_match,match,date_match,who_win,who_win_id,who_win_link,]], columns = ['id_match','link_match','match','date_match','who_win','who_win_id','who_win_link',]), ignore_index=True)
    #print(res)
    return(res)
result = pd.DataFrame()

r = requests.get(url) #отправляем HTTP запрос и получаем результат
soup = BeautifulSoup(r.text) #Отправляем полученную страницу в библиотеку для парсинга
tables=soup.find_all('table', {'div class':'"match-center__teaser"'}) #Получаем все таблицы с вопросами
for item in tables:
    res=parse_table(item)
    result=result.append(res, ignore_index=True)

result.to_excel('result.xlsx')