HEADERS = {
    "Strict-Transport-Security": {
        "weight": 20,
        "description": "Força o navegador a sempre usar HTTPS ao acessar o site, mesmo se o usuário digitar http:// ou clicar num link http://.",
        "risk": "Sem esse header, um atacante na mesma rede (ex: Wi-Fi público) pode forçar a conexão a cair para HTTP e interceptar ou alterar o tráfego (ataque de downgrade / SSL-stripping).",
        "fix": "Configure o servidor para enviar: Strict-Transport-Security: max-age=31536000; includeSubDomains",
    },
    "Content-Security-Policy": {
        "weight": 25,
        "description": "Define de quais origens o navegador pode carregar scripts, estilos, imagens e outros recursos, restringindo o que a página pode executar.",
        "risk": "Sem esse header, um script malicioso injetado na página (via XSS) roda livremente, podendo roubar cookies de sessão, credenciais ou redirecionar o usuário para sites maliciosos.",
        "fix": "Configure o servidor para enviar: Content-Security-Policy: default-src 'self'",
    },
    "X-Frame-Options": {
        "weight": 15,
        "description": "Controla se o site pode ser exibido dentro de um <iframe> em outra página.",
        "risk": "Sem esse header, um atacante pode embutir o site dentro de um iframe invisível em uma página maliciosa e enganar o usuário a clicar em elementos reais do site sem perceber (clickjacking).",
        "fix": "Configure o servidor para enviar: X-Frame-Options: DENY",
    },
    "X-Content-Type-Options": {
        "weight": 15,
        "description": "Impede que o navegador tente adivinhar o tipo de um arquivo diferente do declarado pelo servidor.",
        "risk": "Sem esse header, o navegador pode interpretar um arquivo enviado como texto (ex: upload de usuário) como script executável, abrindo caminho para ataques de MIME sniffing.",
        "fix": "Configure o servidor para enviar: X-Content-Type-Options: nosniff",
    },
    "Referrer-Policy": {
        "weight": 10,
        "description": "Controla quanta informação da URL de origem é enviada no header Referer quando o usuário navega para outro site.",
        "risk": "Sem esse header, URLs internas, tokens ou parâmetros sensíveis presentes na URL podem vazar para sites de terceiros quando o usuário clica em um link externo.",
        "fix": "Configure o servidor para enviar: Referrer-Policy: strict-origin-when-cross-origin",
    },
    "Permissions-Policy": {
        "weight": 15,
        "description": "Restringe quais APIs sensíveis do navegador (câmera, microfone, geolocalização, etc.) a página e seus iframes podem usar.",
        "risk": "Sem esse header, scripts de terceiros carregados na página (ex: anúncios, widgets) podem tentar acessar câmera, microfone ou localização do usuário sem restrição explícita.",
        "fix": "Configure o servidor para enviar: Permissions-Policy: geolocation=(), camera=(), microphone=()",
    },
}

TOTAL_WEIGHT = sum(h["weight"] for h in HEADERS.values())

def score_to_grade(score: int) -> str: 
    if score >= 90:
        return "A"

    if score >= 75:
        return "B"

    if score >= 60:
        return "C"

    if score >= 40:
        return "D"

    return "F"