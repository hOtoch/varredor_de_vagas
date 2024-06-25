import scrapy
from ..items import VagaItem, filtro_presencial

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
    
    '''
    CASO QUEIRA UTILIZAR O VARREDOR SEM A INTERFACE
    COMENTE A FUNÇÃO ABAIXO __init__ E INFORME OS 
    DADOS NAS VARIAVEIS A SEGUIR : 
    
    descricao = 'COLOQUE AQUI A DESCRIÇÃO'
    cidade = 'COLOQUE AQUI A CIDADE OU HOME OFFICE'
    uf = 'COLOQUE AQUI A UF'
    modo_presencial = COLOQUE TRUE CASO QUEIRA APENAS VAGAS PRESENCIAIS OU FALSE CASO CONTRARIO
    link_descricao = queryCreator(descricao)
    link_cidade = queryCreator(cidade)
    
    exemplo:
    
    descricao = 'python estagio'
    cidade = 'Vitória'
    uf = 'ES'
    modo_presencial = False
    link_descricao = queryCreator(descricao)
    link_cidade = queryCreator(cidade)
    
    '''
    
    def __init__(self, descricao, cidade, uf, modo_presencial = False, *args, **kwargs):
        super(VarredorVagasSpider,self).__init__(*args,**kwargs)
        self.descricao = descricao
        self.cidade = cidade
        self.uf = uf
        self.modo_presencial = modo_presencial
        self.link_descricao = queryCreator(descricao)
        self.link_cidade = queryCreator(cidade)
        
        if(self.cidade == 'Home Office'):
            self.uf = ''
    
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
              
            item = VagaItem()
            
            item['cargo'] = vaga.xpath(".//h2/a/span/text()").get(),
            item['empresa'] = vaga.xpath(".//span[@data-testid='company-name']/text()").get(),
            item['localizacao'] = localizacao,
            item['link'] = 'https://br.indeed.com' + vaga.xpath(".//h2/a/@href").get()
            
            
            if filtro_presencial(item, self.modo_presencial):           
                yield item         
        
        try:
            next_page = res.xpath("//a[@aria-label='Next Page']/@href").get()
                                            
            if next_page is not None:
                link_next_page = 'https://br.indeed.com' + next_page
                yield scrapy.Request(url=link_next_page,callback=self.parse)
                
        except Exception as error:
            print("Chegamos na última página!!")
            
    
            