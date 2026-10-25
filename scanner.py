import requests

TIMEOUT = 10 # segundos


def fetch_headers(url: str) -> requests.structures.CaseInsensitiveDict:
    """Faz um GET na URL e retorna os headers da resposta final.

    Segue redirecionamentos e verifica o certificado SSL (padrões do requests).
    Não captura exceções: erros de rede (requests.exceptions.RequestException)
    sobem para quem chamou decidir como exibi-los.
    """
    response = requests.get(url, timeout=TIMEOUT)
    return response.headers


for nome, valor in fetch_headers("https://github.com").items():
    print(nome, "->", valor)