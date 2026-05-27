# Cegonha

Gerador de curriculo profissional em PDF com formulario estruturado, suporte biligue (PT/EN), renderizacao server-side via ReportLab e preview ao vivo. Preencha seus dados uma vez, gere multiplas versoes.

## O que faz?

O Cegonha recebe dados pessoais e profissionais via formulario web, envia ao backend FastAPI que renderiza o PDF com ReportLab usando templates ATS-friendly. O resultado e exibido em preview e baixado automaticamente. Suporta saida em portugues e ingles.

## Funcionalidades

- Formulario estruturado com 6 secoes: Dados Pessoais, Titulo/Perfil, Experiencia, Projetos, Educacao/Habilidades, Configuracoes
- Suporte biligue: Portugues (PT) e Ingles (EN)
- Selecao de template: Modern, Classic, Minimal
- Geracao server-side de PDF via ReportLab (`SimpleDocTemplate`)
- Preview do PDF gerado em iframe
- Download automatico com padrao `CV-{Nome}-{IDIOMA}.pdf`
- Layout ATS-friendly: secoes padrao, layout baseado em paragrafos (sem colunas/tabelas complexas que confundem parsers ATS)
- Modelo Pydantic `CVData` com schema tipado (nome, email, telefone, localizacao, linkedin, github, portfolio, titulo, subtitulo, perfil, experiencia, projetos, educacao, habilidades, idioma, template)
- Script standalone `generate_cv.py` para geracao offline de CV pessoal
- Backend via Google Colab + tunnel Cloudflare (sem servidor proprio)

## Tecnologias

**Frontend:** React 19, TypeScript, Vite 8, Tailwind CSS v4, Framer Motion, Lenis

**Backend:** Python 3.12, FastAPI, ReportLab, Pydantic, uvicorn, cloudflared

**Deploy:** Render (free plan), Vercel (frontend), Google Colab + cloudflared tunnel

## Pre-requisitos

**Frontend:**
- Node.js 22+
- npm

**Backend (local):**
- Python 3.12+

**Backend (Colab -- recomendado):**
- Conta Google
- Navegador moderno

## Instalacao

**Frontend:**

```bash
cd frontend
npm install
```

**Backend (Colab -- metodo recomendado):**

1. Abra `colab-backend.ipynb` no Google Colab
2. Execute as celulas em sequencia
3. Copie a URL `trycloudflare.com` exibida na saida

**Backend (local):**

```bash
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Gerador standalone (offline):**

```bash
python generate_cv.py
# Gera Isaac-Nathan-CV-PT.pdf e Isaac-Nathan-CV-EN.pdf
```

## Uso

1. Inicie o backend (Colab ou local)
2. Inicie o frontend: `cd frontend && npm run dev`
3. No header do Cegonha, clique em "Sem API" e cole a URL do backend
4. Preencha o formulario com seus dados
5. Selecione o idioma (PT/EN) e template
6. Clique em "Gerar PDF" para visualizar e baixar

## Comandos

| Comando | Diretorio | Descricao |
|---------|-----------|-----------|
| `npm run dev` | `frontend/` | Servidor de desenvolvimento Vite |
| `npm run build` | `frontend/` | Build de producao |
| `npm run preview` | `frontend/` | Preview do build |
| `npm run lint` | `frontend/` | Lint com ESLint |
| `python generate_cv.py` | raiz | Gerador standalone de CV offline |

## Estrutura

```
cegonha/
├── main.py                Backend FastAPI (geracao de CV PDF)
├── generate_cv.py         Gerador standalone offline (775 linhas)
├── colab-backend.ipynb    Notebook Colab com backend + tunnel
├── frontend/
│   ├── src/
│   │   ├── App.tsx
│   │   ├── components/    ApiConfig, BetaBanner, Preloader
│   │   ├── hooks/         useLenis, useScrollReveal, useSmoothContainer
│   │   └── lib/           api.ts
│   └── package.json
├── requirements.txt
├── render.yaml
├── Isaac-Nathan-CV-EN.pdf   CV gerado (ingles)
├── NATHAN-VITAE.pdf          CV gerado (versao anterior)
└── .github/workflows/     Deploy do frontend
```

## Arquitetura

O Cegonha segue a arquitetura desacoplada frontend/backend:

- **Frontend (React + Vite):** Formulario com 6 secoes e preview em iframe. Modelo de dados tipado via Pydantic (`CVData`).
- **Backend (FastAPI + ReportLab):** Recebe os dados via POST em `/api/generate-cv`, renderiza o PDF com `SimpleDocTemplate` e retorna como stream. DejaVu Sans com fallback Helvetica.
- **Tunnel Cloudflare:** O notebook Colab inicia o Uvicorn na porta 8000 e expoe via `cloudflared tunnel`.
- **Gerador standalone:** `generate_cv.py` e um script V3 estilo "Jake's Resume" com dados hardcoded, gera CVs de 2 paginas (PT + EN) sem necessidade de backend.

Fluxo: `Formulario (dados CVData) -> POST /api/generate-cv -> ReportLab (renderizacao) -> Preview + Download`.

## API Endpoints

| Endpoint | Metodo | Descricao |
|----------|--------|-----------|
| `/api/generate-cv` | POST | Gera CV PDF a partir de JSON (schema CVData) |
| `/` | GET | Health check |

## Configuracao

| Variavel | Onde | Descricao |
|----------|------|-----------|
| `badger-api-url` | localStorage (frontend) | URL base do backend |

Nao ha arquivo `.env`. A URL da API e configurada pela interface no header.

## Testes

O projeto nao possui suite de testes automatizados no momento.

## Troubleshooting

| Problema | Solucao |
|----------|---------|
| "Configure a URL da API primeiro" | Clique no header e cole a URL do tunnel Cloudflare |
| PDF sem formatacao | Verifique se o backend esta rodando (template CSS e aplicado server-side) |
| Caracteres especiais quebrados | O backend usa DejaVu Sans com amplo suporte Unicode; para fontes customizadas, registre no ReportLab |
| Tunnel Cloudflare nao gera URL | Aguarde ate 30 segundos; reexecute a celula |
| Porta 8000 ocupada | Altere a porta no comando `uvicorn` e na celula do tunnel |

## Relacionamento com outros projetos

- **Predecessor do isaac-vitae:** O `generate_cv.py` e uma versao standalone anterior do que se tornou o portfolio pessoal [isaac-vitae](https://github.com/xAngryBadger/isaac-vitae). O Cegonha generalizou isso em uma ferramenta web onde qualquer pessoa pode gerar um CV.
- **Complementar ao Capivara:** Cegonha gera PDFs de CV do zero; Capivara manipula PDFs existentes.
- Compartilha o padrao arquitetural (`api.ts`, `ApiConfig`, `BetaBanner`) com Anta e Capivara.

## Contribuindo

1. Fork o repositorio em [github.com/xAngryBadger/cegonha](https://github.com/xAngryBadger/cegonha)
2. Crie uma branch: `git checkout -b minha-feature`
3. Commit: `git commit -m "Adiciona minha-feature"`
4. Push: `git push origin minha-feature`
5. Abra um Pull Request

## Licenca

MIT
