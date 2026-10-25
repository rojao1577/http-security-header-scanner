# HTTP Security Header Scanner

Ferramenta que analisa os **headers de segurança HTTP** de um site e gera um
relatório com nota de **A a F**, indicando quais proteções estão presentes,
quais estão faltando, o risco de cada ausência e como corrigi-la.

> 🚧 **Projeto em desenvolvimento**: atualmente na Fase 1 (CLI em Python).

---

## Motivação

Este projeto nasceu com um objetivo duplo: **praticar cibersegurança** e
**computação em nuvem com os serviços da AWS**, unindo as duas áreas em uma
ferramenta real e útil.

Do lado da **segurança**, a proposta é entender na prática como os navegadores
se defendem de ataques comuns na web (XSS, clickjacking, MIME sniffing,
SSL-stripping, vazamento de dados via Referer) e como a configuração dos
headers HTTP de um servidor influencia diretamente essa proteção. Cada header
analisado vem acompanhado do risco que sua ausência representa e da correção
recomendada.

Do lado da **nuvem**, o objetivo é levar essa lógica de um script local para
uma **arquitetura serverless na AWS**, aprendendo a projetar, publicar e
proteger uma aplicação na nuvem com atenção a custo (somente recursos do
*Always Free Tier*) e a abuso (rate limiting).

O projeto evolui em duas fases:

1. **Fase 1: CLI local em Python**: implementa e valida toda a lógica de
   análise e pontuação no terminal.
2. **Fase 2: AWS Serverless**: migra a lógica para AWS Lambda + API Gateway,
   com um frontend estático, tornando a ferramenta acessível por um link.

---

## Características

### Headers analisados

Cada header tem um peso na pontuação final (soma = 100):

| Header | O que protege | Peso |
|---|---|---|
| `Strict-Transport-Security` | Força HTTPS, previne downgrade / SSL-stripping | 20 |
| `Content-Security-Policy` | Previne XSS e injeção de conteúdo | 25 |
| `X-Frame-Options` | Previne clickjacking | 15 |
| `X-Content-Type-Options` | Previne MIME sniffing | 15 |
| `Referrer-Policy` | Previne vazamento de dados via header Referer | 10 |
| `Permissions-Policy` | Restringe acesso a APIs sensíveis do navegador (câmera, microfone, localização) | 15 |

### Sistema de notas

A soma dos pesos dos headers presentes gera um score de 0 a 100, convertido em nota:

| Score | Nota |
|---|---|
| ≥ 90 | **A** |
| ≥ 75 | **B** |
| ≥ 60 | **C** |
| ≥ 40 | **D** |
| < 40 | **F** |

### Relatório

O relatório no terminal (planejado) exibirá:
- um painel com a nota final;
- uma tabela com os headers de segurança encontrados;
- uma tabela com os headers ausentes, o **risco** de cada ausência e a **sugestão de correção**.

---

## Ferramentas utilizadas

### Fase 1: CLI

| Ferramenta | Uso no projeto |
|---|---|
| **Python 3** | Linguagem principal |
| **requests** | Faz a requisição HTTP ao site e obtém os headers da resposta |
| **rich** | Formata o relatório no terminal (painéis, tabelas, cores) |
| **argparse** (stdlib) | Recebe a URL e as opções via linha de comando |
| **pytest** *(planejado)* | Testes unitários da lógica de pontuação |

### Fase 2: AWS Serverless *(planejado)*

| Serviço | Uso no projeto |
|---|---|
| **AWS Lambda** | Executa a lógica do scanner sob demanda |
| **API Gateway** | Expõe a Lambda como endpoint HTTP, com rate limiting contra abuso |
| **S3 + CloudFront** | Hospeda o frontend estático |
| **AWS Budgets / Free Tier Alerts** | Alertas de custo configurados antes de criar qualquer recurso |

Todos os serviços foram escolhidos por fazerem parte do *Always Free Tier* da AWS.
Serviços cobrados por hora de existência (EC2, NAT Gateway, RDS) são evitados de propósito.

---

## Estrutura do projeto

```
├── scanner.py        # lógica principal: busca, análise e saída (em desenvolvimento)
├── headers_db.py     # base de dados dos headers: pesos, riscos e correções
├── requirements.txt  # dependências
└── tests/            # testes unitários (planejado)
```

---

## Como executar

```bash
# clonar o repositório
git clone https://github.com/rojao1577/http-security-header-scanner.git
cd http-security-header-scanner

# criar e ativar o ambiente virtual
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux/macOS

# instalar as dependências
pip install -r requirements.txt

# executar (quando o scanner.py estiver concluído)
python scanner.py https://exemplo.com
```

---

## Roadmap

**Fase 1: CLI**
- [x] Base de dados dos headers com pesos, riscos e correções (`headers_db.py`)
- [x] Conversão de score em nota A–F
- [ ] Requisição HTTP e coleta dos headers
- [ ] Análise e cálculo da pontuação
- [ ] Interface de linha de comando (`argparse`)
- [ ] Relatório formatado com `rich`
- [ ] Testes unitários com `pytest`
- [ ] Flags `--json` e `--export-html`
- [ ] Aviso de redirecionamento HTTP → HTTPS e validação da URL de entrada

**Fase 2: AWS**
- [ ] Alertas de orçamento (AWS Budgets + Free Tier Alerts)
- [ ] Adaptar o scanner como handler de Lambda
- [ ] Criar API Gateway com rate limiting
- [ ] Frontend estático consumindo o endpoint
- [ ] Diagrama da arquitetura e link para a ferramenta online
