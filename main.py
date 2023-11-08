from bs4 import BeautifulSoup
import requests

request_bs = lambda url: BeautifulSoup(requests.get(url).text, 'html.parser')
base_url = lambda url: 'https://uslugio.com' + url
#-------------------------------------------------------------------
def parse_posts(inp_group, inp_url):
    soup = request_bs(inp_url)
    print(inp_group, inp_url, len(soup.select('#posts-items .items_n')))
    # данные на странице
    for item in soup.select('#posts-items .items_n'):
        # TODO ТУТ САМ ПАРСИНГ
        pass
    # пагинация через группы вверху
    for item in soup.select('h1~.row a'):
        current_group = inp_group+' > '+item.text if inp_group!='' else item.text
        parse_posts(current_group, base_url(item['href']))
    # пагинация через цифры внизу
    pag = soup.select('ul.pagination li.active~li a')
    if len(pag) > 0:
        parse_posts(inp_group, base_url(pag[0]['href']))
#-------------------------------------------------------------------
def parse_main():
    # список всех регионов
    for item_region in request_bs(base_url('/region')).select('.region-list a'):
        print([ 'ОБЛАСТЬ', base_url(item_region['href']), item_region.text ])
        # список городов
        for item_city in request_bs(base_url(item_region['href'])).select('.city-list-home a'):
            print([ 'ГОРОД', base_url(item_city['href']), item_city.text ])
            # объявления по этому городу
            parse_posts(' > '.join([item_region.text, item_city.text]), base_url(item_city['href']))
#-------------------------------------------------------------------
parse_main()
#  parse_posts('' ,'https://uslugio.com/irkutsk')
#  parse_posts('' ,'https://uslugio.com/irkutsk/4/naraschivanie-resnic')
