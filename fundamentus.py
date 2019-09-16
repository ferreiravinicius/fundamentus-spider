from scrapy import Spider, Item, Field, Request

BASE_URL_ASSET_DETAIL = 'http://www.fundamentus.com.br/detalhes.php?papel='
BASE_URL_ASSET_LISTING = 'https://www.fundamentus.com.br/detalhes.php'

class FundamentusInfo(Item):
    simbolo = Field()
    nome_comercial = Field()
    razao_social = Field()
    tipo = Field()
    setor = Field()
    subsetor = Field()

class FundamentusSpider(Spider):
    name = 'fundamentus'
    custom_settings = { 'FEED_EXPORT_ENCODING': 'utf-8' } 
    start_urls = [BASE_URL_ASSET_LISTING]

    def parse(self, response):
        lines = response.css('tbody tr')
        for line in lines:
            info = FundamentusInfo()
            info['simbolo'] = line.css('td:nth-child(1) a::text').get()
            info['nome_comercial'] = line.css('td:nth-child(2)::text').get()
            info['razao_social'] = line.css('td:nth-child(3)::text').get()

            url = BASE_URL_ASSET_DETAIL + info.get('simbolo')
            yield Request(url, meta={"info": info}, callback=self.parse_details)

    def parse_details(self, response):
        info = response.meta.get('info')
        info['tipo'] = response.css('div+ .w728 tr:nth-child(2) .data:nth-child(2) .txt::text').get()
        info['setor'] = response.css('tr:nth-child(4) a::text').get()
        info['subsetor'] = response.css('tr:nth-child(5) a::text').get()
        yield info