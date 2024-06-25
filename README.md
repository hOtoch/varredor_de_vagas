# Varredor de Vagas

Este projeto é um web scraper que coleta dados de vagas de trabalho disponíveis no site da Indeed e os salva em um arquivo CSV, separando-as pelas colunas: Cargo, Empresa, Link e Localização. Ele oferece uma interface gráfica onde o usuário pode selecionar a descrição da vaga e o local de trabalho desejado. Além disso, há uma validação mínima de login utilizando o usuário do GitHub. Após configurar suas preferências, o usuário pode iniciar a automação para buscar vagas conforme suas especificações.

## Interface Gráfica

O projeto inclui uma interface gráfica simples que permite ao usuário configurar e iniciar o scraper facilmente:

![Configurações da Interface](https://github.com/hOtoch/varredor_de_vagas/assets/71613053/0ff0a33d-8211-4cae-aafb-f7dd91812585)

Após a execução, a interface exibe um resumo das operações realizadas:

![Resumo da Automação](https://github.com/hOtoch/varredor_de_vagas/assets/71613053/636cd347-49f5-4c24-bf96-1edd9834fe32)

Exemplo de resultado utilizando as preferências "Python Júnior" e a localização "Remoto" : 

![Resultado final](https://github.com/hOtoch/varredor_de_vagas/assets/71613053/24d267ac-c2c3-4e09-9a8d-d8b6c7b7ebbe)


## Inicialização do Projeto

Para utilizar o scraper, siga os passos abaixo:

1. **Configuração da Chave de API**

   Antes de iniciar, é necessário configurar sua chave de API ScrapeOps em um arquivo `.env` localizado na raiz do projeto:

   ```SCRAPEOPS_API_KEY = 'AAAAAAAA-BBBB-CCCC-DDDD-EEEEEEEEEEEE'```


2. **Opções de Execução**

Você pode executar o scraper de duas maneiras:

- **Interface Gráfica**:
  Execute o comando `python interface.py` dentro da pasta `varredor_vagas`. Será solicitada uma chave de acesso do PySimpleGUI.

- **Terminal**:
  Se preferir executar sem a interface gráfica, faça as seguintes modificações no código:

  - Altere o import de `from items import VagaItem, filtro_presencial` para `from ..items import VagaItem, filtro_presencial`.
  - Comente a função `__init__` na classe `VarredorVagasSpider`.
  - Informe os dados necessários diretamente no arquivo `varredorvagas.py`.
  - Execute o comando `scrapy crawl vagasbot -o nomedoarquivo.csv` no terminal.

## Conclusão

Este projeto oferece uma solução prática para quem busca automatizar a busca por vagas de emprego específicas no site da Indeed. Com sua interface intuitiva e opções flexíveis de configuração, permite uma experiência personalizada para o usuário.
