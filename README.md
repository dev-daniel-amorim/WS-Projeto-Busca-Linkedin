# Web Scraping - Projeto busca Linkedin

Este é um projeto de Web Scraping utilizando Selenium e tem objetivo de criar uma busca automatizada na página do linkedin, 
nele vamos preencher na página principal da busca alguns filtros:

- País: Brasil
- Nome da vaga: (Nome da vaga no código)
- Tipo de vaga: Tempo integral
- Nível de experiância: Estágio

Depois iremos navegar entre as páginas do linkedin e ir salvando em um arquivos CSV as informações coletadas abaixo:

1. URL da vaga
2. Nome da vaga
3. Nome da Empresa contratante
4. URL da empresa contratante
5. Modelo de contratação (hibrido, presencial ou remoto)
6. Tipo de contratação (tempo integral ou estágio)
7. Nivel de experiência
8. Número de candidaturas para vaga
9. Data da postagem da vaga (dia, mês e ano)
10. Horário da realização do Scraping (minuto/hora/dia/mês/ano)
11. Número exato de funcionários da empresa (pode ser necessário
navegar para página da empresa para obter esse valor)
12. Número exato de seguidores da empresa
13. Local sede da empresa contratante
14. URL da candidatura (pode ser simplificada pelo Linkedin, ou um link
externode direcionamento da vaga)

O código deverá estar preparado para queda de energia, desligamento do sistema ou queda da rede de internet, e deverá
continuar a busca de onde parou após ser reiniciado.

### Código fonte do projeto:
- [Clique aqui para ver o código em Python.](https://github.com/dev-daniel-amorim/WS-Projeto-Busca-Linkedin/blob/main/main.py)

<br>
<hr>

[<< Voltar](https://github.com/dev-daniel-amorim/Topico-Selenium_e_WS)
