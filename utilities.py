import requests
import scrapy
from scrapy.crawler import CrawlerProcess
from spiders.varredorvagas import VarredorVagasSpider
import os
from dotenv import load_dotenv

def validate_username(window, username):
    # API do GitHub para verificar se um nome de usuário existe
    response = requests.get(f"https://api.github.com/users/{username}")
    if response.status_code == 200:
        window.write_event_value('validate_username', {'result' : True,
                                                       'code' : 200,
                                                       'message': 'Usuário encontrado.'})
    elif response.status_code == 404:
        window.write_event_value('validate_username', {'result' : False,
                                                       'code' : 404,
                                                       'message': 'Usuário não encontrado.'})
    else:
        window.write_event_value('validate_username', {'result' : False,
                                                       'code' : response.status_code,
                                                       'message': f'Erro ao verificar o usuário : {response.status_code}'})
        

def init_scrap(window, values):
    descricao = values['description']
    cidade = values['city']
    uf = values['uf']
    modo_presencial = values['presencial_radio']
    diretorio = values['-DIRPATH-']
    
    load_dotenv()
    
    caminho_csv = os.path.join(diretorio,'vagas.csv')
    
    if os.path.exists(caminho_csv):
        os.remove(caminho_csv)
    
    bot = CrawlerProcess(
        settings = {
            "FEEDS": {
                caminho_csv: {"format":"csv","encoding": "utf-8","item_export_kwargs": {
                        "delimiter": ";"
                    }}
            },
            "ROBOTSTXT_OBEY" : False,
            "DOWNLOADER_MIDDLEWARES" : {
                'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
                'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
                'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,
                'scrapy_fake_useragent.middleware.RetryUserAgentMiddleware': 401,
                'scrapeops_scrapy_proxy_sdk.scrapeops_scrapy_proxy_sdk.ScrapeOpsScrapyProxySdk': 725
            },
            "FAKEUSERAGENT_PROVIDERS" : [
                'scrapy_fake_useragent.providers.FakeUserAgentProvider',  # This is the first provider we'll try
                'scrapy_fake_useragent.providers.FakerProvider',  # If FakeUserAgentProvider fails, we'll use faker to generate a user-agent string for us
                'scrapy_fake_useragent.providers.FixedUserAgentProvider'  # Fall back to USER_AGENT value
            ],
            "USER_AGENT" : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.203',
            "SCRAPEOPS_API_KEY": os.getenv('SCRAPEOPS_API_KEY'),
            "CRAPEOPS_PROXY_ENABLED" : True
        }
    )

        
    bot.crawl(VarredorVagasSpider,descricao=descricao,cidade=cidade,uf=uf,modo_presencial=modo_presencial)
    
    
    bot.start()
    
    window.write_event_value('final_bot','')
    
    
    
    
    
