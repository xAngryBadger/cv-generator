#!/usr/bin/env python3
"""
Generate 2-page narrative CV PDFs (PT + EN) for Isaac Nathan.

Source of truth: isaac-portfolio/src/data/content.ts
This script embeds the data directly since Python can't import TypeScript.
When content.ts changes, update the corresponding sections below.

Structure:
  Page 1 — The Gate: Profile narrative, Core Stack, Experience (expanded), Current Education
  Page 2 — The Depth: Engineering Projects (7, tiered), Skills with Proof, Full Education,
           Certifications with context, Languages

Requirements: reportlab (pip install reportlab)
Usage: python generate_cv.py
Output: Isaac-Nathan-CV-PT.pdf, Isaac-Nathan-CV-EN.pdf
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    HRFlowable, KeepTogether,
)
from reportlab.lib.enums import TA_LEFT, TA_JUSTIFY
import os

# ── Colors ──────────────────────────────────────────────────────────────────
SAGE = HexColor("#456A4B")
AMBER = HexColor("#8B6914")
DARK = HexColor("#0D1117")
MUTED = HexColor("#8B9481")
BORDER = HexColor("#D4D0C8")

# ── Styles ──────────────────────────────────────────────────────────────────
def make_styles() -> dict:
    s = {}
    s["name"] = ParagraphStyle(
        "Name", fontName="Helvetica-Bold", fontSize=15,
        leading=18, textColor=DARK, alignment=TA_LEFT,
        spaceAfter=1*mm,
    )
    s["title"] = ParagraphStyle(
        "Title", fontName="Helvetica", fontSize=8.5,
        leading=11, textColor=AMBER, alignment=TA_LEFT,
        spaceAfter=0.5*mm,
    )
    s["contact"] = ParagraphStyle(
        "Contact", fontName="Helvetica", fontSize=7,
        leading=9.5, textColor=MUTED, alignment=TA_LEFT,
        spaceAfter=0,
    )
    s["section_head"] = ParagraphStyle(
        "SectionHead", fontName="Helvetica-Bold", fontSize=9.5,
        leading=11.5, textColor=DARK, alignment=TA_LEFT,
        spaceBefore=2.5*mm, spaceAfter=1*mm,
    )
    s["body"] = ParagraphStyle(
        "Body", fontName="Helvetica", fontSize=8,
        leading=11, textColor=DARK, alignment=TA_JUSTIFY,
        spaceAfter=0.3*mm,
    )
    s["body_small"] = ParagraphStyle(
        "BodySmall", fontName="Helvetica", fontSize=7,
        leading=9.5, textColor=MUTED, alignment=TA_LEFT,
        spaceAfter=0.2*mm,
    )
    s["bullet"] = ParagraphStyle(
        "Bullet", fontName="Helvetica", fontSize=8,
        leading=11, textColor=DARK, alignment=TA_JUSTIFY,
        leftIndent=8, bulletIndent=0,
        spaceAfter=0.4*mm,
    )
    s["keyword_label"] = ParagraphStyle(
        "KeywordLabel", fontName="Helvetica-Bold", fontSize=7.5,
        leading=9.5, textColor=SAGE, alignment=TA_LEFT,
        spaceAfter=0.2*mm,
    )
    s["keyword_items"] = ParagraphStyle(
        "KeywordItems", fontName="Helvetica", fontSize=7.5,
        leading=9.5, textColor=DARK, alignment=TA_LEFT,
        leftIndent=8, spaceAfter=0.6*mm,
    )
    s["role"] = ParagraphStyle(
        "Role", fontName="Helvetica-Bold", fontSize=8.5,
        leading=11, textColor=DARK, alignment=TA_LEFT,
        spaceAfter=0,
    )
    s["org"] = ParagraphStyle(
        "Org", fontName="Helvetica", fontSize=7,
        leading=9, textColor=AMBER, alignment=TA_LEFT,
        spaceAfter=0.3*mm,
    )
    s["project_title"] = ParagraphStyle(
        "ProjectTitle", fontName="Helvetica-Bold", fontSize=8.5,
        leading=11, textColor=DARK, alignment=TA_LEFT,
        spaceAfter=0,
    )
    s["project_url"] = ParagraphStyle(
        "ProjectUrl", fontName="Helvetica", fontSize=6.5,
        leading=8.5, textColor=SAGE, alignment=TA_LEFT,
        spaceAfter=0.1*mm,
    )
    s["project_tech"] = ParagraphStyle(
        "ProjectTech", fontName="Helvetica", fontSize=7,
        leading=9, textColor=MUTED, alignment=TA_LEFT,
        spaceAfter=0.2*mm,
    )
    s["cert_item"] = ParagraphStyle(
        "CertItem", fontName="Helvetica", fontSize=7.5,
        leading=10, textColor=DARK, alignment=TA_LEFT,
        leftIndent=8, bulletIndent=0,
        spaceAfter=0.3*mm,
    )
    s["cert_context"] = ParagraphStyle(
        "CertContext", fontName="Helvetica-Oblique", fontSize=6.5,
        leading=8.5, textColor=MUTED, alignment=TA_LEFT,
        leftIndent=8, spaceAfter=0.4*mm,
    )
    s["skill_proof"] = ParagraphStyle(
        "SkillProof", fontName="Helvetica-Oblique", fontSize=7,
        leading=9, textColor=MUTED, alignment=TA_LEFT,
        leftIndent=8, spaceAfter=0.7*mm,
    )
    return s


# ── Data (synced from content.ts) ──────────────────────────────────────────

PERSONAL = {
    "name": "Isaac Nathan da Silva Barbosa",
    "email": "isaacnathandasilva@gmail.com",
    "phone": "+55 (31) 99441-7786",
    "linkedin": "linkedin.com/in/isaac-nathan",
    "github": "github.com/xAngryBadger",
    "portfolio": "xangrybadger.github.io/isaac-vitae",
    "location": {"pt": "Mariana, MG — Brasil", "en": "Mariana, MG — Brazil"},
    "title": {
        "pt": "Desenvolvedor Full-Stack com IA",
        "en": "Full-Stack AI Engineer",
    },
    "subtitle": {
        "pt": "Engenharia de Computação · IA · Cloud · IoT",
        "en": "Computer Engineering · AI · Cloud · IoT",
    },
}

# Narrative profile: keyword lead + trajectory arc
PROFILE = {
    "pt": (
        "Desenvolvedor Full-Stack com IA · Python · FastAPI · React 19 · Azure Cosmos DB · "
        "GPT-4.1 · Flutter · PyTorch · 10 meses de experiência profissional. "
        "Primeiro contato com Python em 2022 na UFOP (Química Industrial) — Thonny IDE, sem GPT, "
        "aulas extras à tarde só para continuar aprendendo. Construí o ForestAI do zero usando "
        "Stack Overflow e Thonny, anotando manualmente centenas de imagens de drone da Fundação Renova. "
        "Na Paware, migrei bases de dados para Azure Cosmos DB (Meritage Homes, EUA) e arquitetei "
        "pipelines de IA para o HelloSocial (Flux, DALL-E 3, Canva Connect). Aprendo resolvendo "
        "problemas reais — de MIME type cross-platform a agentes ReAct com schema enforcement."
    ),
    "en": (
        "Full-Stack AI Engineer · Python · FastAPI · React 19 · Azure Cosmos DB · "
        "GPT-4.1 · Flutter · PyTorch · 10 months of professional experience. "
        "First Python contact in 2022 at UFOP (Industrial Chemistry) — Thonny IDE, no GPT, "
        "extra afternoon classes just to keep learning. Built ForestAI from scratch using "
        "Stack Overflow and Thonny, manually annotating hundreds of drone images from Fundação Renova. "
        "At Paware, migrated databases to Azure Cosmos DB (Meritage Homes, USA) and architected "
        "AI pipelines for HelloSocial (Flux, DALL-E 3, Canva Connect). I learn by solving "
        "real problems — from cross-platform MIME types to ReAct agents with schema enforcement."
    ),
}

CORE_STACK = {
    "pt": {
        "IA / ML": "GPT-4.1 · Azure OpenAI · PyTorch · DeepForest · OpenCV · Ollama · DALL-E 3 · Flux · scikit-learn",
        "Backend": "Python · FastAPI · Node.js · Express · Azure Cosmos DB · PocketBase · SQL",
        "Frontend": "React 19 · TypeScript · Flutter · Dart · Tailwind CSS v4 · Vite · React Native (Expo)",
        "Cloud & Infra": "Azure · Docker · Git / GitHub · Linux (CachyOS/Hyprland) · PyInstaller / Inno Setup",
        "Integrações": "Mercado Pago PIX · Canva Connect API · Placid API · Templated.io · Pexels API · NVIDIA NIM API",
        "Outros": "Inglês Fluente · Cibersegurança · Metodologias Ágeis · Testes de API · NiceGUI · Rich CLI",
    },
    "en": {
        "AI / ML": "GPT-4.1 · Azure OpenAI · PyTorch · DeepForest · OpenCV · Ollama · DALL-E 3 · Flux · scikit-learn",
        "Backend": "Python · FastAPI · Node.js · Express · Azure Cosmos DB · PocketBase · SQL",
        "Frontend": "React 19 · TypeScript · Flutter · Dart · Tailwind CSS v4 · Vite · React Native (Expo)",
        "Cloud & Infra": "Azure · Docker · Git / GitHub · Linux (CachyOS/Hyprland) · PyInstaller / Inno Setup",
        "Integrations": "Mercado Pago PIX · Canva Connect API · Placid API · Templated.io · Pexels API · NVIDIA NIM API",
        "Other": "Fluent English · Cybersecurity · Agile Methodologies · API Testing · NiceGUI · Rich CLI",
    },
}

# Expanded narrative experience bullets (2-3 sentences each)
EXPERIENCE = {
    "pt": [
        {
            "company": "Paware Softwares",
            "role": "Desenvolvedor Full-Stack com foco em IA",
            "period": "Out 2025 — Mai 2026",
            "bullets": [
                "Migrei datasets legados do Google Drive para Azure Cosmos DB destinados à Meritage Homes (EUA) — pipeline com extração automatizada por cookies, compressão, renomeação e injeção em painéis para embedding via agente WhatsApp com limites rígidos de tamanho de arquivo. Containerizei com Docker para ambientes reproduzíveis e escrevi camada de validação de schema com rollback automático.",
                "Resolvi problema cross-platform de MIME types (Android nativo vs iPhone exigindo octet-stream — testei no iPhone dos meus pais, sem Macbook). Essa validação virou o backbone da migração final para Azure Cosmos DB.",
                "Arquitetei pipeline agentic de geração de imagens para o HelloSocial — agente GPT-4.1 com tool calling, até 10 iterações de raciocínio, integração Flux Kontext Pro + DALL-E 3 + Placid/Canva. Fallback SQLite/PIL local quando API paga não era necessária.",
            ],
        },
        {
            "company": "SuperNerds",
            "role": "Instrutor de Robótica",
            "period": "Set 2025 — Out 2025",
            "bullets": [
                "Aprendi Arduino e LEGO em <2 semanas e ministrei aulas de robótica para crianças/adolescentes, conectando teoria a aplicações reais.",
                "Conciliei manhãs aqui com trabalho noturno na Paware.",
            ],
        },
    ],
    "en": [
        {
            "company": "Paware Softwares",
            "role": "Full-Stack Developer with AI focus",
            "period": "Oct 2025 — May 2026",
            "bullets": [
                "Migrated legacy datasets from Google Drive to Azure Cosmos DB for Meritage Homes (USA) — pipeline with automated cookie-based extraction, compression, renaming, and injection into panels for WhatsApp agent embedding with strict file size limits. Containerized with Docker for reproducible environments and wrote schema validation layer with automated rollback.",
                "Resolved cross-platform MIME type issue (Android native vs iPhone requiring octet-stream — tested on my parents' iPhone, no Macbook). This validation layer became the backbone of the final Azure Cosmos DB migration.",
                "Architected agentic image-generation pipeline for HelloSocial — GPT-4.1 agent with tool calling, up to 10 reasoning iterations, integrating Flux Kontext Pro + DALL-E 3 + Placid/Canva APIs. Fallback to SQLite/local PIL when paid APIs weren't needed.",
            ],
        },
        {
            "company": "SuperNerds",
            "role": "Robotics Instructor",
            "period": "Sep 2025 — Oct 2025",
            "bullets": [
                "Learned Arduino and LEGO in under 2 weeks and taught robotics to children/teens, connecting theory to real applications.",
                "Balanced mornings here with evening work at Paware.",
            ],
        },
    ],
}

# Engineering Projects — tiered depth
PROJECTS = {
    "pt": [
        {
            "name": "HarpIA",
            "url": "github.com/xAngryBadger/harpia",
            "tech": "Python · GPT-4.1 · DALL-E 3 · Flux 2.0 Pro · Sora · Veo 3.1 · Azure Cosmos DB · SQLite · PIL",
            "tier": 1,
            "bullets": [
                "Motor de automação criativa com 7+ modelos de IA. Pipeline agentic autônomo: GPT-4.1 orquestra tool calls (geração de imagem, busca Pexels, copywriting, composição de design) com schema enforcement e até 10 iterações de raciocínio (think → call → observe).",
                "Stack leve por padrão: SQLite + PIL local renderizam designs com 8 templates próprios, brand colors e badge overlays; quando necessário, faz fallback para APIs pagas (DALL-E 3, Flux, Sora, Veo 3.1).",
                "Swap de backend: local SQLite para desenvolvimento, Azure Cosmos DB + Blob Storage para produção, toggle via variável de ambiente. Cron-ready com file-locking e recovery de batches órfãos.",
                "6.930+ LOC de Python async com testes de segurança e zero hardcoded secrets.",
            ],
        },
        {
            "name": "Flora Sensus",
            "url": "github.com/xAngryBadger/flora-sensus",
            "tech": "Flutter · Dart · Drift/SQLite · React · PocketBase · TypeScript",
            "tier": 1,
            "bullets": [
                "App Flutter offline-first para inventário florestal com motor de sincronização custom: detecção de conflitos por timestamp, UUID remapping em cascata pela FK chain (Propriedade → UT → Parcela → Planta → Foto) e rollback atômico via transações Drift.",
                "~24K LOC — arquitetura e lógica de sync construídas do zero; código gerado com apoio de LLM (web) e revisado manualmente. Hierarquia 5-tier com exportação XLSX/PDF/CSV.",
                "Painel admin React com auth, fotos, relatórios e exportação. Backoff exponencial com jitter, auth retry wrapper, bypass ngrok para desenvolvimento.",
            ],
        },
        {
            "name": "ForestAI",
            "url": "github.com/xAngryBadger/forestai",
            "tech": "PyTorch · DeepForest · OpenCV · scikit-learn · TensorBoard",
            "tier": 1,
            "bullets": [
                "Detecção e classificação de espécies florestais com Deep Learning — construído do zero sem IA-assisted coding. Stack Overflow + Thonny IDE apenas.",
                "Anotação manual de centenas de imagens de drone da Fundação Renova (bounding boxes), treinamento DeepForest/YOLO em GPU local, splits estratificadas. Interpretação de curvas no TensorBoard — detectando memorização vs generalização. O jeito difícil construiu a intuição que fez cada framework subsequente clicar mais rápido.",
            ],
        },
        {
            "name": "Fennec Excel",
            "url": "github.com/xAngryBadger/Sahara-Fenneck",
            "tech": "Python · Ollama/qwen2.5 · CustomTkinter · xlwings/COM · PyInstaller · Inno Setup",
            "tier": 1,
            "bullets": [
                "Assistente de IA local para Excel via agente ReAct (Ollama/qwen2.5). Comando em linguagem natural para filtrar, ordenar, renomear abas e manipular planilhas com checkpoint automático antes de cada alteração.",
                "6+ integrações OAuth (Gmail, Teams, Calendar, Drive, Outlook, Trello) com confirmação do usuário antes de modificações.",
                "Design visual feito à mão com paleta pastel e mascote original (Fennec). Instalador nativo Windows (Inno Setup + PyInstaller). Interface bilíngue PT/EN.",
            ],
        },
        {
            "name": "SRF System",
            "url": "github.com/xAngryBadger/srf-system",
            "tech": "Python · pandas · openpyxl · NiceGUI · Rich CLI · unittest",
            "tier": 2,
            "bullets": [
                "Motor de planejamento operacional para restauração florestal em larga escala — geração automática de dossiês executivos com alocação de equipes, territórios e cronogramas.",
                "Gerenciamento de tarifas e custos operacionais. Interface NiceGUI + CLI Rich com suite de testes unitários.",
            ],
        },
        {
            "name": "MaineCoon",
            "url": "github.com/xAngryBadger/minepal",
            "tech": "Node.js · mineflayer · NVIDIA NIM API · Reinforcement Learning · pathfinder",
            "tier": 2,
            "bullets": [
                "Bot de Minecraft com comandos em linguagem natural via LLM (NVIDIA NIM API) — minerar, construir, seguir, navegar e interagir pelo chat. Módulo de reinforcement learning para comportamento autônomo.",
            ],
        },
        {
            "name": "HelloSocial",
            "url": None,
            "tech": "Python · FastAPI · Azure OpenAI · Flux · Canva Connect · React · TypeScript",
            "tier": 3,
            "bullets": [
                "Plataforma de criação e agendamento de posts com IA — projeto na Paware que inspirou o HarpIA. Pipeline de geração de imagens com Flux Kontext Pro e DALL-E 3, agentes de copy e template.",
            ],
        },
    ],
    "en": [
        {
            "name": "HarpIA",
            "url": "github.com/xAngryBadger/harpia",
            "tech": "Python · GPT-4.1 · DALL-E 3 · Flux 2.0 Pro · Sora · Veo 3.1 · Azure Cosmos DB · SQLite · PIL",
            "tier": 1,
            "bullets": [
                "Creative automation engine with 7+ AI models. Autonomous agentic pipeline: GPT-4.1 orchestrates tool calls (image generation, Pexels search, copywriting, design compositing) with schema enforcement and up to 10 reasoning iterations (think → call → observe).",
                "Lightweight stack by default: SQLite + local PIL renders designs with 8 custom templates, brand colors, and badge overlays; falls back to paid APIs when needed (DALL-E 3, Flux, Sora, Veo 3.1).",
                "Backend swap: local SQLite for development, Azure Cosmos DB + Blob Storage for production, toggled via environment variable. Cron-ready with file-locking and stuck batch recovery.",
                "6,930+ LOC async Python with security tests and zero hardcoded secrets.",
            ],
        },
        {
            "name": "Flora Sensus",
            "url": "github.com/xAngryBadger/flora-sensus",
            "tech": "Flutter · Dart · Drift/SQLite · React · PocketBase · TypeScript",
            "tier": 1,
            "bullets": [
                "Flutter offline-first app for forest inventory with custom sync engine: timestamp-based conflict detection, cascading UUID remapping through FK chain (Propriedade → UT → Parcela → Planta → Foto), and atomic rollback via Drift transactions.",
                "~24K LOC — architecture and sync logic built from scratch; code generated with LLM assistance (web) and manually reviewed. 5-tier hierarchy with XLSX/PDF/CSV export.",
                "React admin panel with auth, photos, reports, and export. Exponential backoff with jitter, auth retry wrapper, ngrok bypass for development.",
            ],
        },
        {
            "name": "ForestAI",
            "url": "github.com/xAngryBadger/forestai",
            "tech": "PyTorch · DeepForest · OpenCV · scikit-learn · TensorBoard",
            "tier": 1,
            "bullets": [
                "Forest species detection and classification with Deep Learning — built from scratch without AI-assisted coding. Stack Overflow + Thonny IDE only.",
                "Manual annotation of hundreds of drone images from Fundação Renova (bounding boxes), DeepForest/YOLO training on local GPU, stratified splits. TensorBoard curve interpretation — detecting memorization vs generalization. The hard way built the intuition that made every subsequent framework click faster.",
            ],
        },
        {
            "name": "Fennec Excel",
            "url": "github.com/xAngryBadger/Sahara-Fenneck",
            "tech": "Python · Ollama/qwen2.5 · CustomTkinter · xlwings/COM · PyInstaller · Inno Setup",
            "tier": 1,
            "bullets": [
                "Local AI assistant for Excel via ReAct agent (Ollama/qwen2.5). Natural language commands to filter, sort, rename sheets, and manipulate spreadsheets with auto-checkpoint before every change.",
                "6+ OAuth integrations (Gmail, Teams, Calendar, Drive, Outlook, Trello) with user confirmation before modifications.",
                "Hand-crafted visual design with pastel palette and original mascot (Fennec). Native Windows installer (Inno Setup + PyInstaller). Bilingual PT/EN interface.",
            ],
        },
        {
            "name": "SRF System",
            "url": "github.com/xAngryBadger/srf-system",
            "tech": "Python · pandas · openpyxl · NiceGUI · Rich CLI · unittest",
            "tier": 2,
            "bullets": [
                "Operational planning engine for large-scale forest restoration — automatic generation of executive dossiers with crew allocation, territory mapping, and schedule management.",
                "Tariff and operational cost management. NiceGUI + Rich CLI interface with unit test suite.",
            ],
        },
        {
            "name": "MaineCoon",
            "url": "github.com/xAngryBadger/minepal",
            "tech": "Node.js · mineflayer · NVIDIA NIM API · Reinforcement Learning · pathfinder",
            "tier": 2,
            "bullets": [
                "Minecraft bot with natural language commands via LLM (NVIDIA NIM API) — mine, craft, follow, navigate, and interact through chat. Reinforcement learning module for autonomous behavior.",
            ],
        },
        {
            "name": "HelloSocial",
            "url": None,
            "tech": "Python · FastAPI · Azure OpenAI · Flux · Canva Connect · React · TypeScript",
            "tier": 3,
            "bullets": [
                "AI-powered social media post creation and scheduling platform — project at Paware that inspired HarpIA. Image generation pipeline with Flux Kontext Pro and DALL-E 3, copy and template agents.",
            ],
        },
    ],
}

# Skills with proof — connects each category to real projects
SKILLS_PROOF = {
    "pt": [
        {
            "label": "Frontend",
            "items": "React 19 · TypeScript · Flutter · Tailwind CSS v4 · Vite · React Native",
            "proof": "→ HarpIA frontend, Flora Sensus admin panel, Inovesa site institucional, este portfólio.",
        },
        {
            "label": "Backend",
            "items": "Python · FastAPI · Node.js · Express · Azure Cosmos DB · SQL",
            "proof": "→ HarpIA pipeline, AguaQuality IoT backend, HelloSocial (Paware). Python async como linguagem de produção.",
        },
        {
            "label": "Cloud & Infra",
            "items": "Azure · Docker · Git/GitHub · PocketBase · Linux (CachyOS/Hyprland)",
            "proof": "→ Migração para Azure Cosmos DB (Meritage Homes, EUA). Docker para agentes de IA. PocketBase como backend Flora Sensus.",
        },
        {
            "label": "IA / ML",
            "items": "GPT-4.1 · PyTorch · DeepForest · OpenCV · Ollama · DALL-E 3 · Flux · scikit-learn",
            "proof": "→ 7+ modelos de IA integrados no HarpIA. Agente ReAct com Ollama no Fennec. Detecção de espécies com PyTorch + DeepForest no ForestAI.",
        },
        {
            "label": "Integrações",
            "items": "Mercado Pago PIX · Canva Connect · Placid API · Pexels API · NVIDIA NIM",
            "proof": "→ PIX via Mercado Pago (AguaQuality). Canva + Placid (HelloSocial/Paware). Pexels (HarpIA).",
        },
    ],
    "en": [
        {
            "label": "Frontend",
            "items": "React 19 · TypeScript · Flutter · Tailwind CSS v4 · Vite · React Native",
            "proof": "→ HarpIA frontend, Flora Sensus admin panel, Inovesa institutional site, this portfolio.",
        },
        {
            "label": "Backend",
            "items": "Python · FastAPI · Node.js · Express · Azure Cosmos DB · SQL",
            "proof": "→ HarpIA pipeline, AguaQuality IoT backend, HelloSocial (Paware). Python async as production language.",
        },
        {
            "label": "Cloud & Infra",
            "items": "Azure · Docker · Git/GitHub · PocketBase · Linux (CachyOS/Hyprland)",
            "proof": "→ Database migration to Azure Cosmos DB (Meritage Homes, USA). Docker for AI agents. PocketBase as Flora Sensus backend.",
        },
        {
            "label": "AI / ML",
            "items": "GPT-4.1 · PyTorch · DeepForest · OpenCV · Ollama · DALL-E 3 · Flux · scikit-learn",
            "proof": "→ 7+ AI models integrated in HarpIA. ReAct agent with Ollama in Fennec. Species detection with PyTorch + DeepForest in ForestAI.",
        },
        {
            "label": "Integrations",
            "items": "Mercado Pago PIX · Canva Connect · Placid API · Pexels API · NVIDIA NIM",
            "proof": "→ PIX via Mercado Pago (AguaQuality). Canva + Placid (HelloSocial/Paware). Pexels (HarpIA).",
        },
    ],
}

EDUCATION = {
    "pt": [
        {
            "degree": "Engenharia de Computação",
            "institution": "Cruzeiro do Sul",
            "period": "2024 — 2029",
            "status": "5º período — em andamento",
            "active": True,
        },
        {
            "degree": "Engenharia Química",
            "institution": "UFSJ — Campus Alto Paraopeba",
            "period": "2022 — 2024",
            "status": "Período de transição — longe do código, acompanhando IA de perto",
            "active": False,
        },
        {
            "degree": "Química Industrial",
            "institution": "UFOP",
            "period": "2022",
            "status": "Onde Python começou — Thonny IDE, sem GPT",
            "active": False,
        },
    ],
    "en": [
        {
            "degree": "Computer Engineering",
            "institution": "Cruzeiro do Sul",
            "period": "2024 — 2029",
            "status": "5th semester — in progress",
            "active": True,
        },
        {
            "degree": "Chemical Engineering",
            "institution": "UFSJ — Campus Alto Paraopeba",
            "period": "2022 — 2024",
            "status": "Pivot period — away from code, watching AI closely",
            "active": False,
        },
        {
            "degree": "Industrial Chemistry",
            "institution": "UFOP",
            "period": "2022",
            "status": "Where Python began — Thonny IDE, no GPT",
            "active": False,
        },
    ],
}

CERTIFICATIONS = {
    "pt": [
        {"name": "Python Essentials 1", "issuer": "Cisco Networking Academy", "context": "Fundamentos de programação com Python — lógica, estruturas e primeiros scripts."},
        {"name": "Python Essentials 2", "issuer": "Cisco Networking Academy", "context": "Python avançado — orientação a objetos, bibliotecas e preparação para certificação."},
        {"name": "Data Science Essentials with Python", "issuer": "Cisco Networking Academy", "context": "Análise de dados com Pandas e Matplotlib — aprendizado prático e baseado em projetos."},
        {"name": "Data Analytics Essentials", "issuer": "Cisco Networking Academy", "context": "Ferramentas essenciais de analytics reconhecidas pelo mercado."},
        {"name": "Networking Basics", "issuer": "Cisco Networking Academy (120h)", "context": "Concluído durante Engenharia de Computação na Cruzeiro do Sul."},
        {"name": "Introdução à Cibersegurança", "issuer": "Cisco Networking Academy", "context": "Base em segurança de redes e ameaças cibernéticas."},
        {"name": "IA para Otimização de Processos e Tomada de Decisão", "issuer": "Escola Virtual Gov · Enap · Serpro (71h)", "context": "Programa do Núcleo de IA do Governo (PBIA) — uso estratégico de IA na gestão pública e segurança da informação."},
        {"name": "Segurança em TI", "issuer": "Fundação Bradesco", "context": "Complemento em proteção de infraestrutura e dados corporativos."},
        {"name": "Inglês Fluente", "issuer": "KUMON (3 anos)", "context": "Habilitação para documentação técnica e reuniões com equipes internacionais."},
    ],
    "en": [
        {"name": "Python Essentials 1", "issuer": "Cisco Networking Academy", "context": "Programming fundamentals with Python — logic, structures, and first scripts."},
        {"name": "Python Essentials 2", "issuer": "Cisco Networking Academy", "context": "Advanced Python — OOP, libraries, and certification prep."},
        {"name": "Data Science Essentials with Python", "issuer": "Cisco Networking Academy", "context": "Data analysis with Pandas and Matplotlib — hands-on, project-based learning."},
        {"name": "Data Analytics Essentials", "issuer": "Cisco Networking Academy", "context": "Essential analytics tools recognized by the industry."},
        {"name": "Networking Basics", "issuer": "Cisco Networking Academy (120h)", "context": "Completed during Computer Engineering at Cruzeiro do Sul."},
        {"name": "Intro to Cybersecurity", "issuer": "Cisco Networking Academy", "context": "Foundation in network security and cyber threats."},
        {"name": "AI for Process Optimization & Decision-Making", "issuer": "Escola Virtual Gov · Enap · Serpro (71h)", "context": "Program by the Gov AI Nucleus (PBIA) — strategic use of AI in public management and information security."},
        {"name": "IT Security", "issuer": "Bradesco Foundation", "context": "Complement in corporate infrastructure and data protection."},
        {"name": "Fluent English", "issuer": "KUMON (3 years)", "context": "Enables technical documentation and meetings with international teams."},
    ],
}

LANGUAGES = {
    "pt": ["Português — Nativo", "Inglês — Fluente (KUMON, 3 anos)"],
    "en": ["Portuguese — Native", "English — Fluent (KUMON, 3 years)"],
}


# ── PDF Builder ─────────────────────────────────────────────────────────────

def build_pdf(lang: str, output_path: str):
    styles = make_styles()
    story = []

    def s(key: str) -> ParagraphStyle:
        return styles[key]

    def heading(text: str):
        story.append(Paragraph(text.upper(), s("section_head")))
        story.append(HRFlowable(
            width="100%", thickness=0.5, color=BORDER,
            spaceBefore=0, spaceAfter=2*mm,
        ))

    def bullet(text: str):
        story.append(Paragraph(f"<bullet>&bull;</bullet> {text}", s("bullet")))

    # ── PAGE 1: THE GATE ────────────────────────────────────────────────────

    # Name
    story.append(Paragraph(PERSONAL["name"], s("name")))

    # Title
    story.append(Paragraph(
        f'{PERSONAL["title"][lang]} · {PERSONAL["subtitle"][lang]}',
        s("title"),
    ))

    # PCD
    pcd_text = ("PCD — TEA (CID-11: 6A02.2) + TDAH (CID-11: 6A05.2)"
                if lang == "pt" else
                "PWD — ASD (ICD-11: 6A02.2) + ADHD (ICD-11: 6A05.2)")
    story.append(Paragraph(pcd_text, s("body_small")))

    # Contact line
    contact_parts = [
        PERSONAL["email"],
        PERSONAL["phone"],
        PERSONAL["location"][lang],
        f'<a href="https://{PERSONAL["linkedin"]}" color="{SAGE.hexval()}">{PERSONAL["linkedin"]}</a>',
        f'<a href="https://{PERSONAL["github"]}" color="{SAGE.hexval()}">{PERSONAL["github"]}</a>',
        f'<a href="https://{PERSONAL["portfolio"]}" color="{SAGE.hexval()}">{PERSONAL["portfolio"]}</a>',
    ]
    story.append(Paragraph("  ·  ".join(contact_parts), s("contact")))

    story.append(Spacer(1, 1.5*mm))

    # Profile
    heading("Perfil" if lang == "pt" else "Profile")
    story.append(Paragraph(PROFILE[lang], s("body")))

    # Core Stack (keywords + proof)
    heading("Stack Principal" if lang == "pt" else "Core Stack")
    for sp in SKILLS_PROOF[lang]:
        story.append(Paragraph(f"<b>{sp['label']}:</b> {sp['items']}", s("keyword_items")))
        story.append(Paragraph(sp["proof"], s("skill_proof")))

    # Professional Experience
    heading("Experiência Profissional" if lang == "pt" else "Professional Experience")
    for exp in EXPERIENCE[lang]:
        story.append(Paragraph(exp["role"], s("role")))
        story.append(Paragraph(
            f'{exp["company"]} · {exp["period"]}',
            s("org"),
        ))
        for b in exp["bullets"]:
            bullet(b)
        story.append(Spacer(1, 0.8*mm))

    # ── PROJECTS & DEPTH ────────────────────────────────────────────────────

    # Engineering Projects
    heading("Projetos de Engenharia" if lang == "pt" else "Engineering Projects")
    for proj in PROJECTS[lang]:
        proj_block = []
        header_line = proj["name"]
        if proj["url"]:
            header_line += f' · <a href="https://{proj["url"]}" color="{SAGE.hexval()}">{proj["url"]}</a>'
        proj_block.append(Paragraph(header_line, s("project_title")))
        proj_block.append(Paragraph(proj["tech"], s("project_tech")))
        for b in proj["bullets"]:
            proj_block.append(Paragraph(
                f"<bullet>&bull;</bullet> {b}", s("bullet"),
            ))
        proj_block.append(Spacer(1, 0.6*mm))
        story.append(KeepTogether(proj_block))

    # Education
    heading("Formação" if lang == "pt" else "Education")
    for edu in EDUCATION[lang]:
        story.append(Paragraph(edu["degree"], s("role")))
        story.append(Paragraph(
            f'{edu["institution"]} · {edu["period"]}',
            s("org"),
        ))
        story.append(Paragraph(edu["status"], s("body_small")))
        story.append(Spacer(1, 0.5*mm))

    # Certifications with context
    heading("Certificações" if lang == "pt" else "Certifications")
    for cert in CERTIFICATIONS[lang]:
        line = f"<bullet>&bull;</bullet> <b>{cert['name']}</b> — {cert['issuer']}"
        if cert["context"]:
            line += f" — {cert['context']}"
        story.append(Paragraph(line, s("cert_item")))

    # Languages (inline, no separate heading)
    story.append(Spacer(1, 1*mm))
    lang_label = "Idiomas" if lang == "pt" else "Languages"
    lang_items = LANGUAGES[lang]
    lang_text = "  \u00b7  ".join(lang_items)
    story.append(Paragraph(
        "<b>" + lang_label + ":</b> " + lang_text,
        s("keyword_items"),
    ))

    # ── Build ───────────────────────────────────────────────────────────────
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        topMargin=14*mm,
        bottomMargin=12*mm,
        leftMargin=16*mm,
        rightMargin=16*mm,
    )
    doc.build(story)
    print(f"  Generated: {output_path}")


# ── Main ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    out_dir = os.path.dirname(os.path.abspath(__file__))

    pt_path = os.path.join(out_dir, "Isaac-Nathan-CV-PT.pdf")
    en_path = os.path.join(out_dir, "Isaac-Nathan-CV-EN.pdf")

    print("Generating narrative CVs...")
    build_pdf("pt", pt_path)
    build_pdf("en", en_path)
    print("Done.")
