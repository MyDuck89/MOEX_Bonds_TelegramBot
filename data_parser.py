import requests
from  bs4 import BeautifulSoup
import datetime

bond_code = 'RU000A0ZYNY4'
url = 'https://smart-lab.ru/q/bonds/' + bond_code + '/'


def bond_info(url): 

    headers = {
        'Accept': '*/*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 \
                YaBrowser/23.3.0.2246 Yowser/2.5 Safari/537.36'
    }

    req = requests.get(url, headers=headers)
    src = req.text    

    soup = BeautifulSoup(src, 'lxml')
    params = soup.find_all("td") # [0:64] - 65 элементов с информацией
    

    # Расчёт количества купонных выплат в год
    # на 365 считает некорректно
    ticket_in_year = 370 // int(params[27].text) 


    # Перевод формата записи в вид ДД.ММ.ГГГГ дат погашения, купона и оферты
    redemption_date = '.'.join(str(params[11].text).split('-'))

    ticket_date = '.'.join(str(params[15].text).split('-'))

    
    if str(params[9].text.strip()) != '—':
        offer_date = '.'.join(str(params[9].text).split('-')) # удобное отображение
    
    # И подсчёт лет до оферты
        offer_date_2 = ', '.join((str(params[9].text).split('-'))[::-1])   
        offer_date_ymd = datetime.date(int(offer_date_2.split(', ')[0]), \
                                        int(offer_date_2.split(', ')[1]), \
                                        int(offer_date_2.split(', ')[2]))

        year_to_offer = round(int((str(offer_date_ymd - \
                                       datetime.date.today())).split()[0]) / 365, 2)

    else:
        offer_date = str('Облигация без оферты')
        year_to_offer = str("-")


    # Чистая доходность без реинвестирования - через размер и количество купона.
    #net_profit_on_year = 100 * float(((params[23].text)[0:4]).strip()) * \
    #    ticket_in_year * 0.87 / (float(params[55].text) * 10) + \
    #        ((100 - float(params[55].text)) / float(params[13].text)) * 0.87

    #round_net_profit = round(net_profit_on_year, 2)


    # Чистая доходность - через ставку купона от номинала облигации
    net_profit_2 = 100 * float(params[21].text.strip('%')) * 0.87 / float(params[55].text) + \
                ((100 - float(params[55].text)) / float(params[13].text)) * 0.87

    round_net_profit_2 = f'{round(net_profit_2, 2)}% к погашениюю'


    # Выбор вывода доходности (к погашению, либо к оферте, если она есть)
    if str(params[9].text.strip()) == '—' or year_to_offer < 0:
        net_profit = round_net_profit_2
    else:
        net_profit_offer  = 100 * float(params[21].text.strip('%')) * 0.87 / float(params[55].text) + \
                ((100 - float(params[55].text)) / float(year_to_offer)) * 0.87
        net_profit = f'{round(net_profit_offer, 2)}% к оферте'



    # Необходимое кол-во облигаций для получения 1000 купонами
    ticket_value = ((params[23].text).split())[0]
    ticket_thousand = 1000 / (float(ticket_value) * 0.87)
    round_tick_tsd = round(ticket_thousand, 2)

    # Необходимое кол-во облигаций для получения номинала купонами
    ticket_nominal = float(params[17].text) / (float(ticket_value) * 0.87) * (float(params[55].text) / 100)
    round_ticket_nominal = round(ticket_nominal, 2)


    # Выводимые параметры облигации
    about_bond = f'{params[2].text} {params[3].text} \n\
● Наименование облигации:\n{params[1].text} \n\
● Cтоимость:\n{params[55].text}% номинала\nвеличиной {params[17].text} {params[19].text} \n\
● Дата выплаты купона:\n{ticket_date} \n\
● Размер купона / НКД:\n{params[23].text} / {params[25].text} \n\
● Выплат купона в год:\n{ticket_in_year} \n\
● Дата оферты:\n{offer_date} ({year_to_offer} лет) \n\
● Дата погашения:\n{redemption_date} ({params[13].text} лет) \n\
● Эффективная доходность к погашению (оферте):\n{params[53].text} \n\
● Доходность "чистыми" и\nбез реинвестирования:\n{net_profit} \n\
● Кол-во для получения 1000\n{params[19].text} "чистыми" купонами:\n{round_tick_tsd} \n\
● Кол-во для получения\nтекущей цены "чистыми"\nкупонами:\n{round_ticket_nominal} \n\n\
● Начальная информация\n➡️/start⬅️'

    #Дюрация: {params[63].text} дней

    #return(about_bond)

    if 'облигации' or 'Облигации' in params[45].text:
        out_info = about_bond
    else:
        out_info = 'Облигация с данным кодом не найдена'
    return(out_info)
    print(out_info)

    

# Ссылка на облигацию в Тинькофф-инвестиции
def link_creator(bond_code):
    link_tinkoff = 'https://www.tinkoff.ru/invest/bonds/' + bond_code + '/'
    print(link_tinkoff)



if __name__ == '__main__':
    bond_info(url)
    #link_creator(bond_code)



    #for item in params[0:64]:
    #    print(item.text)