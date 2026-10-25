import requests

from headers_db import HEADERS, TOTAL_WEIGHT, score_to_grade

TIMEOUT = 10  # segundos


def fetch_headers(url: str) -> requests.structures.CaseInsensitiveDict:
    """Faz um GET na URL e retorna os headers da resposta final.

    Segue redirecionamentos e verifica o certificado SSL (padrões do requests).
    Não captura exceções: erros de rede (requests.exceptions.RequestException)
    sobem para quem chamou decidir como exibi-los.
    """
    response = requests.get(url, timeout=TIMEOUT)
    return response.headers


def analyze(headers: requests.structures.CaseInsensitiveDict) -> dict:
    """Compara os headers recebidos com os headers de segurança esperados.

    Retorna um dicionário com:
      - present: headers encontrados (nome -> valor recebido)
      - missing: nomes dos headers ausentes
      - score:   pontuação de 0 a 100
      - grade:   nota de A a F
    Não faz requisições (função pura), por isso é fácil de testar.
    """
    present = {}
    missing = []

    for name in HEADERS:
        if name in headers:
            present[name] = headers[name]
        else:
            missing.append(name)

    earned = sum(HEADERS[name]["weight"] for name in present)
    score = round(earned / TOTAL_WEIGHT * 100)

    return {
        "present": present,
        "missing": missing,
        "score": score,
        "grade": score_to_grade(score),
    }


print(analyze(fetch_headers("https://github.com")))
