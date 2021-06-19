import random
import requests
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles


app = FastAPI()
templates = Jinja2Templates(directory='templates')
app.mount("/static", StaticFiles(directory="static"), name="static")


# colleagues_db ---------------------------------------------------------------------------------------
colleagues_db = {
    'mariam': {
        'department': 'Management',
        'age': 21,
    },
    'ali': {
        'department': 'IT',
        'age': 25
    },
    'sergey': {
        'department': 'IT',
        'age': 26
    }

}

# quotes RequestAPI -----------------------------------------------------------------------------------
class RequestAPI:
    url = 'https://api.quotable.io/random'
    url2 = 'https://api.covid19api.com/summary'

    # get quote -------------------------------------------------------------------------------------
    def get_quote(self):
        response = requests.get(self.url)


        if response.status_code == 200:
            quote = response.json()

            print(quote)

            return quote

    # get content from get quote-----------------------------------------------------------------------------------
    def get_content(self):
        quote = self.get_quote()
        return quote['content']


    # get text with quote for name from get content ------------------------------------------------------
    def get_text_with_quote_for_name(self, name):
        result = 'Досым %s. Мынау менің саған кеңесім: %s' % (name.capitalize(), self.get_content())

        return result



    # get info about covid19 statistics -----------------------------------------------------------------
    def get_info2(self):
        response2 = requests.get(self.url2)


        if response2.status_code == 200:
            info2 = response2.json()

            return info2


    # info statistics route ------------------------------------------------------------------------
    def get_content2(self):
        info2 = self.get_info2()
        info2_result1 = 'Всего подтвержденных: %s' % info2['Global']['TotalConfirmed']
        info2_result2 = 'Всего смертность: %s' %info2['Global']['TotalDeaths']
        info2_result3 = 'Всего выздоровивших: %s' %info2['Global']['TotalRecovered']
        return info2_result1, info2_result2, info2_result3


# base route --------------------------------------------------------------------------------
@app.get('/')
def home(request: Request):
    return templates.TemplateResponse('index.html', {
        'request': request,
        'name': 'Gauhar'
    })

# quotes route ---------------------------------------------------------------------------------
@app.get('/quotes')
def quotes(request: Request):
    quotes = [
        '... арман деген көп белес. Біріне шықсаң, бірі бар',
        'Сөздің ең ұлысы – тарих',
        'Адам көркі – ақыл',
        'Өмір - бұл қазір. Ол «кеше» немесе «ертең» емес',
        'Досты біз таңдаймыз, нағыз досты уақыт таңдап береді'

    ]

    result = random.choice(quotes)

    return templates.TemplateResponse('quotes.html', {
        'request': request,
        'name': result
    })


# personal quote
@app.get('/quotes/{name}')
def personal_quotes(request: Request, name):
    my_request = RequestAPI()
    return templates.TemplateResponse('quotes.html', {
        'request': request,
        'name': my_request.get_text_with_quote_for_name(name)
    })



# quotes route ---------------------------------------------------------------------------------
@app.get('/covid-statistics')
def get_info(request: Request):
    my_request = RequestAPI()
    return templates.TemplateResponse('covid-statistics.html', {
        'request': request,
        'name': my_request.get_content2()
    })


# colleagues route -----------------------------------------------------------------------------------
@app.get('/colleagues')
def colleagues(request: Request):
    for i in colleagues_db:
        return templates.TemplateResponse('colleagues.html', {
            'request': request,
            'colleagues': colleagues_db
        })

# pesonal colleagues route ----------------------------------------------------------------------
@app.get('/colleagues/{name}')
def colleagues(request: Request, name):
    if name in colleagues_db:
        return templates.TemplateResponse('colleagues.html', {
            'request': request,
            'name': name,
            'info': colleagues_db[name]
        })
    else:
        return 'Qate'
