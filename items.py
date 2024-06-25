# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class VagaItem(scrapy.Item):
    cargo = scrapy.Field()
    empresa = scrapy.Field()
    localizacao = scrapy.Field()
    link = scrapy.Field()
    
    
def filtro_presencial(item, modo_presencial):
    
    for loc in item['localizacao']:
        if modo_presencial and 'Home Office' in loc:
            return False
    
    return True
