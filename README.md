# CV PDF Generator

Gere seu currículo profissional em PDF em segundos.

## Features

- ✅ Preencha seus dados uma vez, gere múltiplas versões
- ✅ Templates ATS-friendly
- ✅ Suporte PT/EN
- ✅ Exportação imediata em PDF
- ✅ Interface moderna e responsiva

## Instalação

### Backend (Python)

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend (React)

```bash
cd frontend
npm install
npm run dev
```

Acesse `http://localhost:5173`

## Deploy

### Frontend (Vercel)

```bash
cd frontend
npm run build
# Deploy na Vercel
```

### Backend (Render/Railway)

```bash
# requirements.txt já está pronto
# Procfile:
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

## Tech Stack

- **Frontend:** React 19 + TypeScript + Vite + Tailwind CSS v4
- **Backend:** Python FastAPI
- **PDF:** ReportLab

## License

MIT
