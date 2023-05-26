import scrapy
from datetime import datetime

class AgendaSpider(scrapy.Spider):
    name = "wheyprotein"
    start_urls = [
        # Max Titatnium Top Whey 3W 900g
        "https://www.mercadolivre.com.br/suplemento-em-po-max-titanium-top-whey-3w-proteinas-top-whey-3w-sabor-baunilha-em-pote-de-900g/p/MLB6091177?pdp_filters=item_id:MLB2963216994"
        # , "https://www.netshoes.com.br/whey-protein-top-whey-3w-mais-performance-900-g-max-titanium-baunilha-A05-0901-963"
         "https://www.maxtitanium.com.br/top-whey-3w-mais-performance-900g/p?idsku=106"
        # Dux Whey Protein Concentrado 900g
        , "https://www.mercadolivre.com.br/suplemento-em-po-dux-nutrition-whey-protein-concentrado-proteinas-whey-protein-concentrado-sabor-baunilha-em-pote-de-900g/p/MLB15067109?pdp_filters=category:MLB264201#searchVariation=MLB15067109"
        # , "https://www.netshoes.com.br/whey-protein-concentrado-dux-nutrition-900g-cookies-AUF-1268-037"
        , "https://www.duxnutrition.com/wheyproteinconcentrado-pote900g/p?skuId=2967"
        # Integral Médica Whey 3W Super 907g
        # , "https://produto.mercadolivre.com.br/MLB-2652411790-super-whey-protein-3w-pote-907g-integralmedica-_JM?searchVariation=174551860029"
        # , "https://www.netshoes.com.br/whey-3w-super-907g-integralmedica-baunilha-MNH-1170-963"
        , "https://www.integralmedica.com.br/superwhey-3w/p"
        # Probiótica 3 Whey Protein 900g
        # , "https://produto.mercadolivre.com.br/MLB-2783564400-whey-3w-whey-protein-900g-probiotica-_JM?searchVariation=175166709480"
        # , "https://www.netshoes.com.br/whey-protein-3w-900-g-probiotica-baunilha-168-0064-963"
        , "https://www.probiotica.com.br/3-whey-protein-pote-900g/p?skuId=57"
    ]

    def parse(self, response):
        # WheyProteinFile = open(f"WheyProtein.txt", "a")
        site = response.url

        if "mercadolivre" in site:
            geral = response.css('table.andes-table')
            geral = geral.css('tbody tr td span.andes-table__column--value::text').getall()
            marca = geral[0]
            peso = geral[9]
            produto = geral[2]
            valor = response.css('div.ui-pdp-price__second-line')
            valor = valor.css('span span::text').getall()
            valor = response.css('div.ui-pdp-price__second-line span meta')  # content = valor
            print(f'\n\n\n\n\n\n{datetime.today()};{marca};{peso};{produto};{valor};{site}\n\n\n\n\n\n')

        elif "netshoes" in site:
            geral = response.css('section#features')
            marca = geral.css('ul li a::text').get()
            peso = geral.css('ul li::text').getall()[6]
            produto = geral.css('ul li::text').get()
            valor = response.css('div.default-price span strong::text').get()
            print(f'\n\n\n\n\n\n{datetime.today()};{marca};{peso};{produto};{valor};{site}\n\n\n\n\n\n')
        
        elif "maxtitanium" in site:
            marca = 'Max Titanium'
            peso = 900 # response.xpath('/html/body/div[2]/div/div[1]/div/div/div/div[3]/div/div[2]/div[3]/section/div/div/div/div[1]/div/div/div[1]/div/div/div[2]/div/div[5]/div/div/div/div/div[2]/text()')
            produto = response.xpath('/html/body/div[2]/div/div[1]/div/div/div/div[3]/div/div[2]/div[3]/section/div/div/div/div[8]/div/div/div[1]/div/div[1]/div/div/div/div/div[2]/div/div/div/div/table/tbody/tr/td[2]/div/p[1]/b/text()').get()
            valor = response.xpath('/html/body/div[2]/div/div[1]/div/div/div/div[3]/div/div[1]/div[9]/section/div/div/div/div[1]/div/div/div/div/div[1]/div/div/div/span/span/span')
            valor = ''.join(valor.css("span::text").getall()[2:5])  # ['R$', '\xa0', '169', ',', '15'] >> '169,15'
            print(f'\n\n\n\n\n\n{datetime.today()};{marca};{peso};{produto};{valor};{site}\n\n\n\n\n\n')

        elif "duxnutrition" in site:
            marca = 'Dux Nutrition'
            peso = 900 # response.xpath('/html/body/div[2]/div/div[1]/div/div/div/div[4]/div/div/div/section/div/div/div/div[2]/div/div/div[2]/div/div[2]/div/div/div/h1/span/text()')
            produto = response.xpath('/html/body/div[2]/div/div[1]/div/div/div/div[4]/div/div/div/section/div/div/div/div[2]/div/div/div[2]/div/div[2]/div/div/div/h1/span/text()').get()
            valor = response.xpath('/html/body/div[2]/div/div[1]/div/div/div/div[4]/div/div/div/section/div/div/div/div[2]/div/div/div[2]/div/div[4]/div/div/div/div/div[1]/div/div[2]/span/span')
            valor = ''.join(valor.css("span::text").getall()[2:5])  # ['R$', '\xa0', '209', ',', '90'] >> '209,90'
            print(f'\n\n\n\n\n\n{datetime.today()};{marca};{peso};{produto};{valor};{site}\n\n\n\n\n\n')

        elif "integralmedica" in site:
            marca = 'Integral Medica'
            peso = 907 # response.xpath('/html/body/main/div[1]/div/div/div[2]/div/div[1]/div/ul[1]/li[2]/span/label[1]/text()')
            produto = response.xpath('/html/body/main/div[1]/div/div/div[1]/section[2]/div[3]/div/text()').get()
            valor = response.css('p.descricao-preco')
            valor = valor.css('strong.skuBestPrice::text').get()  # ['R$ 162,20', ...]
            print(f'\n\n\n\n\n\n{datetime.today()};{marca};{peso};{produto};{valor};{site}\n\n\n\n\n\n')

        elif "probiotica" in site:
            marca = 'Probiotica'
            peso = 900 # response.xpath('/html/body/div[2]/div/div[1]/div/div/div/div[3]/div/div[2]/div[2]/section/div/div/div/div[2]/div/div/div[1]/div/div/div[2]/div/div[5]/div/div/div/div/div[1]/span/text()')
            produto = response.css('title::text').get()
            valor = response.xpath('/html/body/div[2]/div/div[1]/div/div/div/div[3]/div/div[2]/div[2]/section/div/div/div/div[2]/div/div/div[2]/div/div/div/div/div[1]/div/div/div/div/div[1]/div/div/div/span/span/span')
            valor = ''.join(valor.css("span::text").getall()[2:5])  # ['R$', '\xa0', '203', ',', '90'] >> '203,90'
            print(f'\n\n\n\n\n\n{datetime.today()};{marca};{peso};{produto};{valor};{site}\n\n\n\n\n\n')

        # WheyProteinFile.write(f'{datetime.today()};{marca};{peso};{produto};{valor};{site}\n')
        # WheyProteinFile.close()

