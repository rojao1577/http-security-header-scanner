# Scanner Header — Guia do Projeto

## O que é o projeto

HTTP Security Header Scanner: ferramenta que analisa os headers de segurança HTTP
de um site e gera um relatório com nota de A a F, no estilo do securityheaders.com.
É um projeto de portfólio com foco em cybersegurança + cloud (AWS).

O projeto tem duas fases:
- **Fase 1**: script Python local (CLI) que implementa e valida toda a lógica de análise.
- **Fase 2**: migração da lógica para uma arquitetura serverless na AWS
  (Lambda + API Gateway + frontend estático), virando uma ferramenta acessível por link.

Existe um documento de planejamento original: `HTTP_Header_Scanner_Plano.pdf`,
na raiz do projeto.

## Contexto do autor

João, 2º período de Ciência da Computação (UFAPE). Base sólida em C
(estruturas de dados, algoritmos), aprendendo Java/Spring Boot. Participa do
PIBITI com um projeto de cloud computing (AWS, Docker, infraestrutura como código).
Está começando uma trilha DevSecOps (OverTheWire Bandit, PortSwigger, TryHackMe).
Prefere entender o raciocínio por trás de cada decisão técnica em vez de receber
soluções prontas.

## Regras de colaboração (como Claude deve me direcionar)

- **O usuário escreve todo o código do projeto.** Claude explica o raciocínio,
  as opções e o "porquê" de cada decisão técnica, revisa o código depois de
  escrito, mas não escreve os arquivos de código do projeto no lugar do usuário.
- Trabalho passo a passo, com calma, **sem pular etapas**. Uma etapa só avança
  para a próxima depois de concluída e revisada.
- **Antes de qualquer decisão ou ação, Claude avisa antecipadamente o que vai
  fazer e por quê**, e só prossegue após confirmação quando fizer sentido.
  Nenhuma decisão silenciosa.
- Claude não deve assumir que código mencionado em documentos de planejamento
  já existe — sempre verificar o estado real dos arquivos antes de planejar
  os próximos passos.
- Formato que vem funcionando em cada etapa: Claude explica primeiro os
  conceitos e as decisões técnicas (com opções e recomendação); quando o João
  pede, Claude mostra o código completo **no chat**, explicado linha por linha,
  e o João digita no arquivo. Explicar os termos técnicos usados (o João pede
  isso) e usar analogias com C quando ajudar.
- Depois que o João testa, Claude lê o arquivo, revisa, e só então commita e faz push.

## Escopo Fase 1 — CLI local (Python)

Headers de segurança analisados, com peso na pontuação (soma = 100):

| Header | O que protege | Peso |
|---|---|---|
| Strict-Transport-Security | Força HTTPS, previne downgrade/SSL-stripping | 20 |
| Content-Security-Policy | Previne XSS e injeção de conteúdo | 25 |
| X-Frame-Options | Previne clickjacking | 15 |
| X-Content-Type-Options | Previne MIME sniffing | 15 |
| Referrer-Policy | Previne vazamento de dados via header Referer | 10 |
| Permissions-Policy | Restringe acesso a APIs sensíveis do navegador | 15 |

Funcionamento: recebe URL via `argparse` → faz GET com `requests` → compara
headers recebidos com `headers_db.py` → soma pesos dos headers presentes →
converte score 0–100 em nota A–F → exibe relatório formatado com `rich`
(painel com a nota, tabela de headers presentes, tabela de headers ausentes
com risco e sugestão de correção).

Estrutura de arquivos:
```
ScannerHeader/
├── scanner.py        # lógica principal (busca, análise, saída)
├── headers_db.py      # banco de dados dos headers: pesos, riscos, correções
├── requirements.txt
├── README.md
└── tests/             # testes unitários da lógica de pontuação
```

Stack: Python 3, `requests`, `rich`, `argparse` (stdlib).

Próximos passos depois do núcleo funcionando: testes unitários (`pytest`) para
a função de pontuação; flag `--json`; flag `--export-html`; tratamento de
múltiplos redirecionamentos e aviso de redirecionamento HTTP→HTTPS; validação
mais robusta da URL de entrada.

## Escopo Fase 2 — AWS Serverless

**REGRA CRÍTICA — NENHUM RECURSO PAGO: esta fase só pode usar serviços dentro
do Always Free Tier da AWS. Antes de criar qualquer recurso na AWS, Claude
deve explicar exatamente o que será criado, seu custo potencial (mesmo que
teoricamente zero) e esperar confirmação explícita do usuário antes de
prosseguir. Nunca criar, modificar ou destruir recursos AWS sem esse aviso
prévio.**

Arquitetura proposta (todos com camada gratuita perene, "always free"):
- **AWS Lambda** — executa a lógica do scanner sob demanda (1 milhão de
  requisições/mês grátis para sempre).
- **API Gateway** — expõe a Lambda como endpoint HTTP, com rate limiting
  configurado (ex.: 10 req/s) para evitar abuso por bots.
- **S3 + CloudFront** (ou alternativa já usada pelo autor, como Netlify) —
  hospeda o frontend estático (formulário simples).
- **AWS Budgets** — alerta de orçamento (ex.: US$1) configurado **antes** de
  criar qualquer recurso, com notificação por e-mail.
- **AWS Free Tier Alerts** — ativado em Billing Preferences para monitorar uso
  próximo dos limites da camada gratuita.

Serviços a evitar totalmente nesta fase, por serem cobrados por hora de
existência (não por uso) e serem causa comum de cobranças inesperadas:
**EC2, NAT Gateway, RDS**.

Ordem de execução recomendada:
1. Configurar alerta de AWS Budget + Free Tier Alerts na conta (antes de criar
   qualquer recurso).
2. Adaptar `scanner.py` para rodar como handler de Lambda.
3. Criar a função Lambda e testar via console da AWS.
4. Criar API Gateway apontando para a Lambda, configurar rate limiting.
5. Testar o endpoint via curl/Postman antes de construir o frontend.
6. Construir um frontend simples (HTML/JS) que consome o endpoint.
7. Hospedar o frontend e documentar tudo no README.

## Narrativa sugerida para o README (portfólio)

Estruturar o README em torno da evolução do projeto: começou como script CLI
para validar a lógica de análise de segurança, depois migrou para arquitetura
serverless na AWS para se tornar acessível via web. Incluir: motivação do
projeto, screenshot do relatório no terminal, diagrama simples da arquitetura
AWS (Lambda + API Gateway + S3), link para a ferramenta funcionando.

## Estado atual do projeto (última verificação: 25/10/2026)

**Repositório:** https://github.com/rojao1577/http-security-header-scanner
(público, branch `main`, local e remoto sincronizados).

**Fase 1: em andamento.** O núcleo lógico já funciona (busca → análise → nota).

| Etapa | Status |
|---|---|
| venv + `requirements.txt` (`requests`, `rich`) | ✅ concluída |
| `headers_db.py`: `HEADERS` (peso, descrição, risco, correção), `TOTAL_WEIGHT`, `score_to_grade()` | ✅ concluída |
| Git + GitHub + `.gitignore` + `README.md` (motivação, ferramentas, roadmap) | ✅ concluída |
| **3a** `fetch_headers(url)` em `scanner.py` | ✅ concluída e commitada |
| **3b** `analyze(headers)` em `scanner.py` | ✅ concluída e commitada (GitHub → 85, nota B, falta só Permissions-Policy) |
| **3c** CLI: `argparse` + `if __name__ == "__main__":` + `try/except RequestException` com mensagem amigável | ⏭️ **PRÓXIMA ETAPA** |
| **3d** relatório com `rich` (painel da nota, tabela de presentes, tabela de ausentes com risco/correção) | ⏳ pendente |
| Testes `pytest`, `--json`, `--export-html`, aviso HTTP→HTTPS, validação de URL | ⏳ pendente |
| Fase 2 (AWS) | ⏳ não iniciada |

**Estado do `scanner.py`:** termina com um `print(analyze(fetch_headers("https://github.com")))`
**temporário**, que deve ser substituído pelo `argparse` + `main` na 3c.

**Decisões técnicas já tomadas (não reabrir sem motivo):**
- `fetch_headers` usa GET (não HEAD), `timeout=TIMEOUT` (constante = 10s) passado
  por nome, segue redirecionamentos, mantém `verify=True`, **não** usa
  `raise_for_status()` (sites 4xx/5xx ainda têm headers analisáveis) e **não captura
  exceções**: elas sobem para a camada de apresentação (CLI agora, Lambda na Fase 2).
- `analyze` é função pura; percorre o `HEADERS` do DB (não os headers do site);
  retorna `dict` com chaves `present` (nome → valor), `missing` (lista de nomes),
  `score` (normalizado por `TOTAL_WEIGHT`, `round`) e `grade`. O dict foi escolhido
  por virar JSON direto (`--json` e Lambda).
- Nomes no código em inglês; comentários/docstrings em português.
- O arquivo foi renomeado `Scanner.py` → `scanner.py` (Linux da Lambda diferencia maiúsculas/minúsculas).
- O PDF de planejamento fica fora do Git (`.gitignore`).

**Ideias registradas para o futuro:** validar o *conteúdo* dos headers (ex.: HSTS
com `max-age=0`, CSP com `'unsafe-inline'`); analisar flags de cookies
(`HttpOnly`, `Secure`, `SameSite`); configurar um formatador no VS Code.

## Convenções de Git

- Commits em português, padrão Conventional Commits (`feat:`, `docs:`, `chore:`, `style:`).
- Um commit por etapa concluída e revisada; push logo em seguida.
- **Sem linha `Co-Authored-By: Claude`** em nenhum commit (decisão do João).
