import os
import asyncio
from playwright.async_api import async_playwright
import pandas as pd
from datetime import datetime

async def run():
    async with async_playwright() as p:
        # 1. Abre o navegador (headless=False para ver o robô agindo)
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        # 2. Vai direto para o perfil da Samsung Brasil
        print("Acessando o X da Samsung Brasil...")
        await page.goto("https://x.com/SamsungBrasil?lang=pt")
        await page.wait_for_selector('article')
        await page.wait_for_timeout(2000)
        
        # Espera um tempo para carregar 
        await page.wait_for_timeout(5000)

        # 3. Rola a página para carregar mais posts 
        for _ in range(5): 
            await page.mouse.wheel(0, 1000)
            await page.wait_for_timeout(2000)

        # 4. Seleciona os posts (usando o seletor 'article' que é o padrão do X)
        tweets = await page.query_selector_all('article')
        
        dados_finais = []

        for tweet in tweets:
            try:
                # MODELAGEM: onde cada informação mora no HTML
                texto = await tweet.query_selector('div[data-testid="tweetText"]')
                texto_final = await texto.inner_text() if texto else "Sem texto"
                
                data_elemento = await tweet.query_selector('time')
                #formato ISO 8601 ("2026-03-06T23:15:52.000Z").
                data_iso = await data_elemento.get_attribute('datetime') if data_elemento else None
                if data_iso:
                    #para um padrão mais legível (dd/mm/aaaa hh:mm:ss)
                    dt = datetime.fromisoformat(data_iso.replace("Z", "+00:00"))
                    data_final = dt.strftime("%d/%m/%Y %H:%M:%S")
                else:
                    data_final = "Sem data"

                curtidas = await tweet.query_selector('button[data-testid="like"]')
                curtidas_texto = await curtidas.get_attribute('aria-label') if curtidas else "0"
                #split() para separar a frase em partes e pegar apenas o primeiro elemento [0],o mesmo que = apresentar só número de curtidas, sem frase facilitando a análise dos dados.
                curtidas_numero = curtidas_texto.split()[0] if curtidas_texto else "0"

                reposts = await tweet.query_selector('button[data-testid="retweet"]')
                reposts_texto = await reposts.get_attribute('aria-label') if reposts else "0"
                ## O mesmo processo é aplicado aos reposts para extrair apenas o valor numérico da string retornada pelo atributo "aria-label".
                reposts_numero = reposts_texto.split()[0] if reposts_texto else "0"

                # Guardando como um objeto (Dicionário)
                dados_finais.append({
                    "autor": "SamsungBrasil",
                    "descricao": texto_final.replace('\n', ' '), # Limpa quebras de linha
                    "data": data_final,
                    "curtidas": curtidas_numero,
                    "reposts": reposts_numero

                })
            except Exception as e:
                print(f"Error ao processar tweet: {e}")
                continue

        # 5. Transformação e Saída
         
        pasta_script = os.path.dirname(os.path.abspath(__file__))
        # Define a pasta onde vai ser armazenado os resultados do scrapings
        pasta_destino = os.path.join(pasta_script, "saidas_scrapings")

        #Verifica se a pasta existe, cria ela, caso não.
        if not os.path.exists(pasta_destino):
            os.makedirs(pasta_destino)
            print(f"Pasta criada em: '{pasta_destino} ")

        caminho_csv = os.path.join(pasta_destino, 'relatorio_samsung.csv')   

        #Converte a lista de dicionários (dados_finais) em um DataFrame do pandas
        df = pd.DataFrame(dados_finais)
        #exporta para um arquivo csv. #encoding='utf-8' garante compatibilidade com caracteres especiais
        df.to_csv(caminho_csv, index=False, encoding='utf-8')
        
        #Exibe no terminal a quantidade de posts coletados e salvos
        print(f"Sucesso! {len(dados_finais)} posts modelados e salvos.")
        await browser.close()

asyncio.run(run())