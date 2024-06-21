import scrapy

def queryCreator(element):
    elementSplit = element.split(' ')
    elementLen = len(elementSplit)
    
    query = ''
    for i in range (elementLen):
        query = query + elementSplit[i] + '+'
    query = query.rstrip('+')
    
    return query

class VarredorVagasSpider(scrapy.Spider):
    name = 'vagasbot'
    descricao = 'python estagio'
    cidade = 'São Paulo'
    uf = 'SP'
    
    link_descricao = queryCreator(descricao)
    link_cidade = queryCreator(cidade)
    
    def start_requests(self):
        urls = [f'https://br.indeed.com/jobs?q={self.link_descricao}&l={self.link_cidade}%2C+{self.uf}&from=searchOnDesktopSerp&vjk=f0f1efe8d41eb242']
        
        
        for url in urls:
            yield scrapy.Request(url=url, callback= self.parse)
            
    def parse(self,res):
                
        for vaga in res.xpath("//tr/td[@class='resultContent css-1qwrrf0 eu4oa1w0']"):
            if vaga.xpath(".//div[@data-testid='text-location']/span").get() is not None:
                localizacao = vaga.xpath(".//div[@data-testid='text-location']/span/text()").get()
            else:
                localizacao = vaga.xpath(".//div[@data-testid='text-location']/text()").get()         
              
            yield {
                'cargo': vaga.xpath(".//h2/a/span/text()").get(),
                'empresa': vaga.xpath(".//span[@data-testid='company-name']/text()").get(),
                'localizacao': localizacao,
                'link': 'https://br.indeed.com' + vaga.xpath(".//h2/a/@href").get()
            }
        
        try:
            next_page = res.xpath("//a[@aria-label='Next Page']/@href").get()
                                            
            if next_page is not None:
                link_next_page = 'https://br.indeed.com' + next_page
                yield scrapy.Request(url=link_next_page,callback=self.parse)
                
        except Exception as error:
            print("Chegamos na última página!!")
            
            