import scrapy
from datetime import datetime

class AgendaSpider(scrapy.Spider):
    name = "wheyprotein"
    start_urls = [
        # Max Titatnium Top Whey 3W 900g
        "https://www.mercadolivre.com.br/suplemento-em-po-max-titanium-top-whey-3w-proteinas-top-whey-3w-sabor-baunilha-em-pote-de-900g/p/MLB6091177?pdp_filters=item_id:MLB2963216994"
        , "https://www.netshoes.com.br/whey-protein-top-whey-3w-mais-performance-900-g-max-titanium-vitamina+de+frutas-A05-0901-C20"
        , "https://www.maxtitanium.com.br/top-whey-3w-mais-performance-900g/p?idsku=106"
        # Dux Whey Protein Concentrado 900g
        , "https://www.mercadolivre.com.br/suplemento-em-po-dux-nutrition-whey-protein-concentrado-proteinas-whey-protein-concentrado-sabor-baunilha-em-pote-de-900g/p/MLB15067109?pdp_filters=category:MLB264201#searchVariation=MLB15067109"
        , "https://www.netshoes.com.br/whey-protein-concentrado-dux-nutrition-900g-cookies-AUF-1268-037"
        , "https://www.duxnutrition.com/wheyproteinconcentrado-pote900g/p?skuId=2967"
        # Integral Médica Whey 3W Super 907g
        , "https://produto.mercadolivre.com.br/MLB-2652411790-super-whey-protein-3w-pote-907g-integralmedica-_JM?searchVariation=174551860029"
        , "https://www.netshoes.com.br/whey-3w-super-907g-integralmedica-baunilha-MNH-1170-963"
        , "https://www.integralmedica.com.br/superwhey-3w/p"
        # Probiótica 3 Whey Protein 900g
        , "https://produto.mercadolivre.com.br/MLB-2783564400-whey-3w-whey-protein-900g-probiotica-_JM?searchVariation=175166709480"
        , "https://www.netshoes.com.br/whey-protein-3w-900-g-probiotica-baunilha-168-0064-963"
        , "https://www.probiotica.com.br/3-whey-protein-pote-900g/p?skuId=57"
    ]

    def parse(self, response):
        mydate = datetime.today()
        WheyProteinFile = open(f"{mydate.strftime('%Y-%m-%d')}/WheyProtein {mydate.strftime('%H:%M')}.txt", "a")
        site = response.url

        if "mercadolivre" in site:
            geral = response.css('table.andes-table')
            geral = geral.css('tbody tr td span.andes-table__column--value::text').getall()
            marca = geral[0]
            peso = geral[9]
            produto = geral[2]
            valor = response.css('div.ui-pdp-price__second-line span meta::attr(content)').get()

        elif "netshoes" in site:
            geral = response.css('section#features')
            marca = geral.css('ul li a::text').get()
            peso = response.css('title::text').get()
            produto = geral.css('ul li::text').get()
            valor = response.css('div.default-price span strong::text').get()
        
        elif "maxtitanium" in site:
            marca = 'Max Titanium'
            peso = 900
            produto = response.xpath('/html/body/div[2]/div/div[1]/div/div/div/div[3]/div/div[2]/div[3]/section/div/div/div/div[8]/div/div/div[1]/div/div[1]/div/div/div/div/div[2]/div/div/div/div/table/tbody/tr/td[2]/div/p[1]/b/text()').get()
            valor = response.xpath('/html/body/div[2]/div/div[1]/div/div/div/div[3]/div/div[1]/div[9]/section/div/div/div/div[1]/div/div/div/div/div[1]/div/div/div/span/span/span')
            valor = ''.join(valor.css("span::text").getall()[2:5])  # ['R$', '\xa0', '169', ',', '15'] >> '169,15'

        elif "duxnutrition" in site:
            marca = 'Dux Nutrition'
            peso = 900
            produto = response.xpath('/html/body/div[2]/div/div[1]/div/div/div/div[4]/div/div/div/section/div/div/div/div[2]/div/div/div[2]/div/div[2]/div/div/div/h1/span/text()').get()
            valor = response.xpath('/html/body/div[2]/div/div[1]/div/div/div/div[4]/div/div/div/section/div/div/div/div[2]/div/div/div[2]/div/div[4]/div/div/div/div/div[1]/div/div[2]/span/span')
            valor = ''.join(valor.css("span::text").getall()[2:5])  # ['R$', '\xa0', '209', ',', '90'] >> '209,90'

        elif "integralmedica" in site:
            marca = 'Integral Medica'
            peso = 907
            produto = response.xpath('/html/body/main/div[1]/div/div/div[1]/section[2]/div[3]/div/text()').get()
            valor = response.css('p.descricao-preco')
            valor = valor.css('strong.skuBestPrice::text').get()  # ['R$ 162,20', ...]

        elif "probiotica" in site:
            marca = 'Probiotica'
            peso = 900
            produto = response.css('title::text').get()
            valor = response.xpath('/html/body/div[2]/div/div[1]/div/div/div/div[3]/div/div[2]/div[2]/section/div/div/div/div[2]/div/div/div[2]/div/div/div/div/div[1]/div/div/div/div/div[1]/div/div/div/span/span/span')
            valor = ''.join(valor.css("span::text").getall()[2:5])  # ['R$', '\xa0', '203', ',', '90'] >> '203,90'

        else:
            marca = response.css('title::text').get()
            peso = 0
            produto = "Quotes"
            valor = 1

        WheyProteinFile.write(f'{mydate};{marca};{peso};{produto};{valor};{site}\n')
        WheyProteinFile.close()

