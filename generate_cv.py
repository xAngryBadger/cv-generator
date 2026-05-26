#!/usr/bin/env python3
"""
Generate 2-page layered CV PDFs (PT + EN) for Isaac Nathan — V3.

Jake's Resume style: bold hierarchy, scannable, tech-forward.
Single-column, tight margins, strong section headings,
skills inline with bold labels, experience with role|date inline,
project bullets concise and impact-driven.

ATS-optimized: standard section headings (Skills, Professional Summary,
Education, Projects), Paragraph-based role|date lines so ATS parses
role+date+company as connected text, standard bullet chars.

Page 1 — The Gate:
Name (huge), Objective, Contact, PCD,
Technical Skills (inline labels), Professional Summary,
Professional Experience, Education
Page 2 — The Depth:
Projects (tiered), Certifications, Languages
Portfolio CTA

Footer: portfolio link on every page

Requirements: reportlab (pip install reportlab)
Usage: python generate_cv.py
Output: Isaac-Nathan-CV-PT.pdf, Isaac-Nathan-CV-EN.pdf
"""

from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    HRFlowable, KeepTogether,
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY, TA_RIGHT
import os

PAGE_W, PAGE_H = A4

# ── Colors ──────────────────────────────────────────────────────────────────
DARK = HexColor("#1A1A1A")
ACCENT = HexColor("#456A4B")
AMBER = HexColor("#7A5C1E")
MUTED = HexColor("#6B7280")
BORDER = HexColor("#D1D5DB")
LIGHT_RULE = HexColor("#E5E7EB")

# ── Helpers ─────────────────────────────────────────────────────────────────
def _current_semester() -> int:
    now = datetime.now()
    year, month = now.year, now.month
    total = 0
    for y in range(2024, year + 1):
        start_m = 2 if y == 2024 else 1
        end_m = month if y == year else 12
        for sem_start in [2, 8]:
            if start_m <= sem_start <= end_m:
                total += 1
    return max(total, 1)

SEMESTER = _current_semester()
ORD_PT = {1: "1º", 2: "2º", 3: "3º", 4: "4º", 5: "5º",
           6: "6º", 7: "7º", 8: "8º", 9: "9º", 10: "10º"}
ORD_EN = {1: "1st", 2: "2nd", 3: "3rd", 4: "4th", 5: "5th",
           6: "6th", 7: "7th", 8: "8th", 9: "9th", 10: "10th"}

SEMESTER_PT = f"{ORD_PT.get(SEMESTER, f'{SEMESTER}º')} período — cursando"
SEMESTER_EN = f"{ORD_EN.get(SEMESTER, f'{SEMESTER}th')} semester — in progress"


# ── Custom Flowables ────────────────────────────────────────────────────────



# ── Styles ──────────────────────────────────────────────────────────────────
def make_styles() -> dict:
    s = {}
    s["name"] = ParagraphStyle(
        "Name", fontName="Helvetica-Bold", fontSize=22,
        leading=26, textColor=DARK, alignment=TA_CENTER,
        spaceAfter=0,
    )
    s["title_line"] = ParagraphStyle(
        "TitleLine", fontName="Helvetica", fontSize=9,
        leading=11, textColor=ACCENT, alignment=TA_CENTER,
        spaceAfter=0.5*mm,
    )
    s["objective"] = ParagraphStyle(
        "Objective", fontName="Helvetica-Oblique", fontSize=8,
        leading=11, textColor=ACCENT, alignment=TA_CENTER,
        spaceAfter=0.5*mm,
    )
    s["contact"] = ParagraphStyle(
        "Contact", fontName="Helvetica", fontSize=7.5,
        leading=10, textColor=MUTED, alignment=TA_CENTER,
        spaceAfter=0,
    )
    s["pcd"] = ParagraphStyle(
        "PCD", fontName="Helvetica", fontSize=6.5,
        leading=8, textColor=MUTED, alignment=TA_CENTER,
        spaceAfter=0,
    )
    s["section_head"] = ParagraphStyle(
        "SectionHead", fontName="Helvetica-Bold", fontSize=10.5,
        leading=13, textColor=DARK, alignment=TA_LEFT,
        spaceBefore=4*mm, spaceAfter=0,
    )
    s["body"] = ParagraphStyle(
        "Body", fontName="Helvetica", fontSize=7.5,
        leading=10.5, textColor=DARK, alignment=TA_JUSTIFY,
        spaceAfter=0,
    )
    s["body_small"] = ParagraphStyle(
        "BodySmall", fontName="Helvetica", fontSize=7,
        leading=9, textColor=MUTED, alignment=TA_LEFT,
        spaceAfter=0,
    )
    s["bullet"] = ParagraphStyle(
        "Bullet", fontName="Helvetica", fontSize=7.5,
        leading=10.5, textColor=DARK, alignment=TA_JUSTIFY,
        leftIndent=6, bulletIndent=0,
        spaceAfter=0.5*mm,
    )
    s["skills_line"] = ParagraphStyle(
        "SkillsLine", fontName="Helvetica", fontSize=7.5,
        leading=10.5, textColor=DARK, alignment=TA_LEFT,
        spaceAfter=0.3*mm,
    )
    s["project_title"] = ParagraphStyle(
        "ProjectTitle", fontName="Helvetica-Bold", fontSize=8.5,
        leading=11, textColor=DARK, alignment=TA_LEFT,
        spaceAfter=0,
    )
    s["project_tech"] = ParagraphStyle(
        "ProjectTech", fontName="Helvetica-Oblique", fontSize=7,
        leading=9, textColor=MUTED, alignment=TA_LEFT,
        spaceAfter=0.2*mm,
    )
    s["cert_item"] = ParagraphStyle(
        "CertItem", fontName="Helvetica", fontSize=7.5,
        leading=10, textColor=DARK, alignment=TA_LEFT,
        leftIndent=6, bulletIndent=0,
        spaceAfter=0.2*mm,
    )
    s["cert_context"] = ParagraphStyle(
        "CertContext", fontName="Helvetica-Oblique", fontSize=6.5,
        leading=8.5, textColor=MUTED, alignment=TA_LEFT,
        leftIndent=8, spaceAfter=0.3*mm,
    )
    s["edu_degree"] = ParagraphStyle(
        "EduDegree", fontName="Helvetica-Bold", fontSize=8.5,
        leading=10.5, textColor=DARK, alignment=TA_LEFT,
        spaceAfter=0,
    )
    s["edu_detail"] = ParagraphStyle(
        "EduDetail", fontName="Helvetica", fontSize=7,
        leading=9, textColor=MUTED, alignment=TA_LEFT,
        spaceAfter=0.1*mm,
    )
    s["role_date"] = ParagraphStyle(
        "RoleDate", fontName="Helvetica-Bold", fontSize=8.5,
        leading=11, textColor=DARK, alignment=TA_LEFT,
        spaceAfter=0, spaceBefore=0.5*mm,
    )
    s["subhead"] = ParagraphStyle(
        "Subhead", fontName="Helvetica-Oblique", fontSize=7.5,
        leading=10, textColor=AMBER, alignment=TA_LEFT,
        spaceAfter=0.5*mm,
    )
    s["footer_link"] = ParagraphStyle(
        "FooterLink", fontName="Helvetica", fontSize=7,
        leading=9, textColor=ACCENT, alignment=TA_CENTER,
    )
    return s


# ── Data ────────────────────────────────────────────────────────────────────

PERSONAL = {
    "name": "Isaac Nathan da Silva Barbosa",
    "email": "isaacnathandasilva@gmail.com",
    "phone": "+55 (31) 99441-7786",
    "linkedin": "linkedin.com/in/isaac-nathan-da-silva-barbosa-815b212ab",
    "github": "github.com/xAngryBadger",
    "portfolio": "xangrybadger.github.io/isaac-vitae",
    "personalSite": "xangrybadger.github.io/nathan",
    "location": {"pt": "Mariana, MG — Brasil", "en": "Mariana, MG — Brazil"},
    "title": {
        "pt": "Desenvolvedor Full-Stack com IA",
        "en": "Full-Stack AI Engineer",
    },
    "subtitle": {
        "pt": "Full-Stack · Python · React · Cloud",
        "en": "Full-Stack · Python · React · Cloud",
    },
}

OBJECTIVE = {
    "pt": "Construir sistemas inteligentes que conectam IA, cloud e produto — do pipeline orquestrado por LLM ao deploy em produção.",
    "en": "Build intelligent systems that connect AI, cloud, and product — from LLM-orchestrated pipelines to production deploy.",
}

PROFILE = {
    "pt": (
        "De Química Industrial para Computação: primeiro Python em 2022 (Thonny IDE, sem GPT, "
        "aulas extras à tarde). Construí o ForestAI do zero anotando manualmente "
        "imagens de drone da Fundação Renova. Na Paware, migrei centenas de GB para Azure Cosmos DB "
        "(Meritage Homes, EUA) e arquitetei pipelines orquestrados por LLM para o HelloSocial "
        "(GPT-4.1, DALL-E 3, Flux). Aprendo resolvendo problemas reais — "
        "de MIME type cross-platform a agentes ReAct com schema enforcement."
    ),
    "en": (
        "From Industrial Chemistry to Computer Engineering: first Python in 2022 (Thonny IDE, no GPT, "
        "extra afternoon classes). Built ForestAI from scratch, manually annotating "
        "drone images from Fundação Renova. At Paware, migrated hundreds of GB to Azure Cosmos DB "
        "(Meritage Homes, USA) and architected LLM-orchestrated pipelines for HelloSocial "
        "(GPT-4.1, DALL-E 3, Flux). I learn by solving real problems — "
        "from cross-platform MIME types to ReAct agents with schema enforcement."
    ),
}

SKILLS = {
    "pt": [
        ("IA / ML", "GPT-4.1 · Azure OpenAI · PyTorch · DeepForest · OpenCV · Ollama · DALL-E 3 · Flux · Sora · Veo 3.1 · Gemini SDK · scikit-learn"),
        ("Backend", "Python · FastAPI · Node.js · Express · Java · Azure Cosmos DB · PocketBase · SQL"),
        ("Frontend", "React 19 · TypeScript · JavaScript · Flutter · Tailwind CSS v4 · Vite · React Native (Expo 54)"),
        ("Cloud & Infra", "Azure · Docker · Git / GitHub · PocketBase · Linux (CachyOS/Hyprland) · PyInstaller / Inno Setup"),
        ("Integrações", "Mercado Pago PIX · Canva Connect API · Placid API · Templated.io · Pexels API · NVIDIA NIM API"),
        ("Outros", "Inglês Fluente · Cibersegurança · Metodologias Ágeis · Testes de API · FastAPI + Jinja2 · Rich CLI · xlwings/COM"),
    ],
    "en": [
        ("AI / ML", "GPT-4.1 · Azure OpenAI · PyTorch · DeepForest · OpenCV · Ollama · DALL-E 3 · Flux · Sora · Veo 3.1 · Gemini SDK · scikit-learn"),
        ("Backend", "Python · FastAPI · Node.js · Express · Java · Azure Cosmos DB · PocketBase · SQL"),
        ("Frontend", "React 19 · TypeScript · JavaScript · Flutter · Tailwind CSS v4 · Vite · React Native (Expo 54)"),
        ("Cloud & Infra", "Azure · Docker · Git / GitHub · PocketBase · Linux (CachyOS/Hyprland) · PyInstaller / Inno Setup"),
        ("Integrations", "Mercado Pago PIX · Canva Connect API · Placid API · Templated.io · Pexels API · NVIDIA NIM API"),
        ("Other", "Fluent English · Cybersecurity · Agile Methodologies · API Testing · FastAPI + Jinja2 · Rich CLI · xlwings/COM"),
    ],
}

EXPERIENCE = {
    "pt": [
        {
            "company": "Paware Softwares",
            "role": "Desenvolvedor Full-Stack com foco em IA",
            "period": "Out 2025 — Mai 2026",
            "location": "Remoto",
            "bullets": [
                "Migrei centenas de GB de datasets legados do Google Drive para Azure Cosmos DB (Meritage Homes, EUA) — pipeline com extração automatizada, compressão e injeção em painéis para agente WhatsApp. Docker + validação de schema com rollback automático.",
                "Resolvi problema cross-platform de MIME types (Android vs iOS) — validação que virou o backbone da migração Cosmos DB, com testes extensivos em dispositivos iOS.",
                "Arquitetei pipeline de geração de imagens para o HelloSocial — pipeline multi-etapa com GPT-4.1 (geração, curadoria, composição, validação), Flux Kontext Pro + DALL-E 3 + Placid/Canva, fallback SQLite/PIL local.",
            ],
        },
        {
            "company": "SuperNerds",
            "role": "Instrutor de Robótica",
            "period": "Set 2025 — Out 2025",
            "location": "Mariana, MG",
            "bullets": [
                "Aprendi Arduino e LEGO em <2 semanas e ministrei aulas de robótica para crianças/adolescentes.",
                "Conciliei manhãs aqui com trabalho noturno na Paware — disciplina e adaptabilidade.",
            ],
        },
    ],
    "en": [
        {
            "company": "Paware Softwares",
            "role": "Full-Stack Developer with AI focus",
            "period": "Oct 2025 — May 2026",
            "location": "Remote",
            "bullets": [
                "Migrated hundreds of GB of legacy datasets from Google Drive to Azure Cosmos DB (Meritage Homes, USA) — automated extraction, compression, injection into panels for WhatsApp agent. Docker + schema validation with auto-rollback.",
                "Resolved cross-platform MIME type issue (Android vs iOS) — validation layer that became the backbone of the Cosmos DB migration, with extensive testing on iOS devices.",
                "Architected image-generation pipeline for HelloSocial — multi-step pipeline with GPT-4.1 (generation, curation, composition, validation), Flux Kontext Pro + DALL-E 3 + Placid/Canva, local SQLite/PIL fallback.",
            ],
        },
        {
            "company": "SuperNerds",
            "role": "Robotics Instructor",
            "period": "Sep 2025 — Oct 2025",
            "location": "Mariana, MG",
            "bullets": [
                "Learned Arduino and LEGO in under 2 weeks and taught robotics to children/teens.",
                "Balanced mornings here with evening work at Paware — discipline and adaptability.",
            ],
        },
    ],
}

PROJECTS = {
    "pt": [
        {
            "name": "HarpIA",
            "url": "github.com/xAngryBadger/harpia",
            "tech": "Python · GPT-4.1 · DALL-E 3 · Flux 2.0 Pro · Sora · Veo 3.1 · Azure Cosmos DB · SQLite",
            "tier": 1,
            "bullets": [
                "Motor de automação criativa com 7+ modelos de IA — pipeline orquestrado por LLM multi-etapa: copywriting, busca de imagens, composição de designs, geração de vídeo. Stack leve por padrão (SQLite + PIL local) com fallback para APIs pagas.",
                "6.900+ LOC Python async com testes de segurança e zero hardcoded secrets. Backend swap: SQLite local para Azure Cosmos DB + Blob Storage, alternado via env var. Pronto para cron com file-locking e recuperação de lotes travados.",
            ],
        },
        {
            "name": "Urutau",
            "url": "github.com/xAngryBadger/flora-sensus",
            "tech": "Flutter · Dart · Drift/SQLite · React · PocketBase · TypeScript",
            "tier": 1,
            "bullets": [
"App Flutter offline-first para inventário florestal com serviço de sync custom — remapping de UUIDs em cascata pelas tabelas relacionadas e rollback transacional em caso de falha.",
            "Arquitetura e lógica de sync construídas do zero; código gerado com apoio de LLM (web) e revisado manualmente. Painel admin React com auth, fotos, relatórios e exportação XLSX/PDF/CSV.",
            ],
        },
        {
            "name": "ForestAI",
            "url": "github.com/xAngryBadger/forestai",
            "tech": "PyTorch · DeepForest · OpenCV · scikit-learn · TensorBoard",
            "tier": 1,
            "bullets": [
                "Detecção e classificação de espécies florestais com Deep Learning — construído do zero sem IA-assisted coding. Stack Overflow + Thonny IDE apenas.",
                "Anotação manual de imagens de drone da Fundação Renova (bounding boxes), treinamento DeepForest em GPU local, splits estratificadas. Interpretação de curvas no TensorBoard — detectando memorização vs generalização.",
            ],
        },
        {
            "name": "Fennec Excel",
            "url": "github.com/xAngryBadger/Sahara-Fenneck",
            "tech": "Python · Ollama · CustomTkinter · xlwings/COM · PyInstaller · Inno Setup",
            "tier": 1,
            "bullets": [
                "Assistente de IA local para Excel via agente ReAct (Ollama/qwen2.5). Comando em linguagem natural para filtrar, ordenar, renomear abas e manipular planilhas com checkpoint automático antes de cada alteração.",
                "6+ integrações OAuth (Gmail, Teams, Calendar, Drive, Outlook, Trello) com confirmação do usuário antes de modificações. Instalador nativo Windows (Inno Setup + PyInstaller). Interface bilíngue PT/EN.",
            ],
        },
        {
            "name": "Orca",
            "url": "github.com/xAngryBadger/orca",
            "tech": "Python · pandas · FastAPI · Jinja2 · Rich CLI · openpyxl · unittest",
            "tier": 2,
            "bullets": [
                "Motor de planejamento operacional para restauração florestal em larga escala — geração automática de dossiês executivos com alocação de equipes, territórios e cronogramas.",
                "Gerenciamento de tarifas e custos operacionais. Interface FastAPI + Jinja2 + CLI Rich com suite de testes unitários.",
            ],
        },
        {
            "name": "MaineCoon",
            "url": "github.com/xAngryBadger/minepal",
            "tech": "Node.js · mineflayer · NVIDIA NIM API · Reinforcement Learning",
            "tier": 2,
            "bullets": [
                "Bot de Minecraft com comandos em linguagem natural via LLM (NVIDIA NIM API) — minerar, craftar, seguir, navegar e interagir pelo chat. Módulo de reinforcement learning para comportamento autônomo.",
            ],
        },
        {
            "name": "HelloSocial",
            "url": None,
            "tech": "Python · FastAPI · Azure OpenAI · Flux · Canva Connect · React",
            "tier": 2,
            "bullets": [
                "Plataforma de criação e agendamento de posts com IA — projeto na Paware que inspirou o HarpIA. Pipeline de geração de imagens com Flux Kontext Pro e DALL-E 3, agentes de copy e template.",
            ],
        },
        {
            "name": "Capivara",
            "url": "github.com/xAngryBadger/capivara",
            "tech": "React 19 · TypeScript · FastAPI · pypdf · PyMuPDF · cloudflared",
            "tier": 2,
            "bullets": [
                "Suíte PDF completa com 15 ferramentas — DOCX/XLSX→PDF, PDF→DOCX, compressão, merge, split, rotação, marca d'água, numeração, cabeçalho/rodapé, proteção, desbloqueio, OCR, PDF→imagens, PDF/A. Frontend React 19, backend FastAPI com StreamingResponse.",
                "Túnel serverless gratuito via cloudflared + Google Colab — zero conta, zero token. Lazy imports para deps pesadas (PyMuPDF, pytesseract, pikepdf). pypdf 4+ com PdfWriter-based merge.",
            ],
        },
        {
            "name": "Tarsier",
            "url": "github.com/xAngryBadger/tarsier",
            "tech": "React 19 · TypeScript · Vite · Tailwind CSS v4 · Framer Motion",
            "tier": 2,
            "bullets": [
                "Workbench JSON 100% client-side com árvore colapsável, transformações (pretty-print, minify, CSV, tipos TypeScript) e stats. Zero backend — tudo roda no browser.",
            ],
        },
        {
            "name": "Kakapo",
            "url": "github.com/xAngryBadger/kakapo",
            "tech": "React 19 · Canvas API · TypeScript · Vite · Tailwind CSS v4",
            "tier": 2,
            "bullets": [
                "Editor de imagens no navegador — filtros, crop, resize, rotação, text overlay, ajustes. Motor commit-based com undo/redo. 100% client-side, Canvas API nativo.",
            ],
        },
        {
            "name": "Oilbird",
            "url": "github.com/xAngryBadger/oilbird",
            "tech": "React 19 · TypeScript · FastAPI · WeasyPrint · cloudflared",
            "tier": 2,
            "bullets": [
                "Conversor Markdown → PDF com preview live split-pane e renderização WeasyPrint profissional. Backend FastAPI + WeasyPrint com CSS Paged Media (@page, headers/footers), túnel cloudflared gratuito via Google Colab.",
            ],
        },
        {
            "name": "Cegonha",
            "url": "github.com/xAngryBadger/cegonha",
            "tech": "React 19 · TypeScript · FastAPI · reportlab",
            "tier": 2,
            "bullets": [
                "Gerador de currículo com formulários estruturados e exportação PDF server-side via FastAPI + reportlab. Paleta sage green com tipografia editorial. Suporte bilíngue (pt/en).",
            ],
        },
    ],
    "en": [
        {
            "name": "HarpIA",
            "url": "github.com/xAngryBadger/harpia",
            "tech": "Python · GPT-4.1 · DALL-E 3 · Flux 2.0 Pro · Sora · Veo 3.1 · Azure Cosmos DB · SQLite",
            "tier": 1,
            "bullets": [
                "Creative automation engine with 7+ AI models — multi-model pipeline with GPT-4.1: copywriting, image search, design compositing, video generation. Lightweight stack by default (SQLite + local PIL) with fallback to paid APIs.",
                "6,900+ LOC async Python with security tests and zero hardcoded secrets. Backend swap: local SQLite to Azure Cosmos DB + Blob Storage, toggled via env var. Cron-ready with file-locking and stuck batch recovery.",
            ],
        },
        {
            "name": "Urutau",
            "url": "github.com/xAngryBadger/flora-sensus",
            "tech": "Flutter · Dart · Drift/SQLite · React · PocketBase · TypeScript",
            "tier": 1,
            "bullets": [
"Flutter offline-first app for forest inventory with custom sync service — cascading UUID remapping across related tables and transactional rollback on failure.",
            "Architecture and sync logic built from scratch; code generated with LLM assistance (web) and manually reviewed. React admin panel with auth, photos, reports, and XLSX/PDF/CSV export.",
            ],
        },
        {
            "name": "ForestAI",
            "url": "github.com/xAngryBadger/forestai",
            "tech": "PyTorch · DeepForest · OpenCV · scikit-learn · TensorBoard",
            "tier": 1,
            "bullets": [
                "Forest species detection and classification with Deep Learning — built from scratch without AI-assisted coding. Stack Overflow + Thonny IDE only.",
                "Manual annotation of drone images from Fundação Renova (bounding boxes), DeepForest training on local GPU, stratified splits. TensorBoard curve interpretation — detecting memorization vs generalization.",
            ],
        },
        {
            "name": "Fennec Excel",
            "url": "github.com/xAngryBadger/Sahara-Fenneck",
            "tech": "Python · Ollama · CustomTkinter · xlwings/COM · PyInstaller · Inno Setup",
            "tier": 1,
            "bullets": [
                "Local AI assistant for Excel via ReAct agent (Ollama/qwen2.5). Natural language commands to filter, sort, rename sheets and manipulate spreadsheets with auto-checkpoint before every change.",
                "6+ OAuth integrations (Gmail, Teams, Calendar, Drive, Outlook, Trello) with user confirmation before modifications. Native Windows installer (Inno Setup + PyInstaller). Bilingual PT/EN interface.",
            ],
        },
        {
            "name": "Orca",
            "url": "github.com/xAngryBadger/orca",
            "tech": "Python · pandas · FastAPI · Jinja2 · Rich CLI · openpyxl · unittest",
            "tier": 2,
            "bullets": [
                "Operational planning engine for large-scale forest restoration — automatic generation of executive dossiers with crew allocation, territory mapping, and schedules.",
                "Tariff and operational cost management. FastAPI + Jinja2 + Rich CLI interface with unit test suite.",
            ],
        },
        {
            "name": "MaineCoon",
            "url": "github.com/xAngryBadger/minepal",
            "tech": "Node.js · mineflayer · NVIDIA NIM API · Reinforcement Learning",
            "tier": 2,
            "bullets": [
                "Minecraft bot with natural language commands via LLM (NVIDIA NIM API) — mine, craft, follow, navigate, and interact via chat. Reinforcement learning module for autonomous behavior.",
            ],
        },
        {
            "name": "HelloSocial",
            "url": None,
            "tech": "Python · FastAPI · Azure OpenAI · Flux · Canva Connect · React",
            "tier": 2,
            "bullets": [
                "AI-powered social media post creation and scheduling platform — project at Paware that inspired HarpIA. Image generation pipeline with Flux Kontext Pro and DALL-E 3, copy and template agents.",
            ],
        },
        {
            "name": "Capivara",
            "url": "github.com/xAngryBadger/capivara",
            "tech": "React 19 · TypeScript · FastAPI · pypdf · PyMuPDF · cloudflared",
            "tier": 2,
            "bullets": [
                "Full PDF suite with 15 tools — DOCX/XLSX→PDF, PDF→DOCX, compress, merge, split, rotate, watermark, page numbers, header/footer, protect, unlock, OCR, PDF→images, PDF/A. React 19 frontend, FastAPI backend with StreamingResponse.",
                "Free serverless tunneling via cloudflared + Google Colab — zero account, zero token. Lazy imports for heavy deps (PyMuPDF, pytesseract, pikepdf). pypdf 4+ with PdfWriter-based merge.",
            ],
        },
        {
            "name": "Tarsier",
            "url": "github.com/xAngryBadger/tarsier",
            "tech": "React 19 · TypeScript · Vite · Tailwind CSS v4 · Framer Motion",
            "tier": 2,
            "bullets": [
                "100% client-side JSON workbench with collapsible tree, transformations (pretty-print, minify, CSV, TypeScript types) and stats. Zero backend — everything runs in the browser.",
            ],
        },
        {
            "name": "Kakapo",
            "url": "github.com/xAngryBadger/kakapo",
            "tech": "React 19 · Canvas API · TypeScript · Vite · Tailwind CSS v4",
            "tier": 2,
            "bullets": [
                "Browser image editor — filters, crop, resize, rotation, text overlay, adjustments. Commit-based editing engine with undo/redo. 100% client-side, native Canvas API.",
            ],
        },
        {
            "name": "Oilbird",
            "url": "github.com/xAngryBadger/oilbird",
            "tech": "React 19 · TypeScript · FastAPI · WeasyPrint · cloudflared",
            "tier": 2,
            "bullets": [
                "Markdown → PDF converter with live split-pane preview and professional WeasyPrint rendering. FastAPI + WeasyPrint backend with CSS Paged Media (@page, headers/footers), free cloudflared tunnel via Google Colab.",
            ],
        },
        {
            "name": "Cegonha",
            "url": "github.com/xAngryBadger/cegonha",
            "tech": "React 19 · TypeScript · FastAPI · reportlab",
            "tier": 2,
            "bullets": [
                "Resume generator with structured forms and server-side PDF export via FastAPI + reportlab. Sage green palette with editorial typography. Bilingual support (pt/en).",
            ],
        },
    ],
}

EDUCATION = {
    "pt": [
        {
            "degree": "Engenharia de Computação",
            "institution": "Cruzeiro do Sul",
            "period": "2024 — 2029",
            "status": SEMESTER_PT,
            "active": True,
        },
        {
            "degree": "Engenharia Química",
            "institution": "UFSJ — Campus Alto Paraopeba",
            "period": "2022 — 2024",
            "status": "Transição — estudo autodirigido em IA",
            "active": False,
        },
        {
            "degree": "Química Industrial",
            "institution": "UFOP",
            "period": "2022",
            "status": "Onde Python começou — Thonny IDE",
            "active": False,
        },
    ],
    "en": [
        {
            "degree": "Computer Engineering",
            "institution": "Cruzeiro do Sul",
            "period": "2024 — 2029",
            "status": SEMESTER_EN,
            "active": True,
        },
        {
            "degree": "Chemical Engineering",
            "institution": "UFSJ — Campus Alto Paraopeba",
            "period": "2022 — 2024",
            "status": "Transition — self-directed AI study",
            "active": False,
        },
        {
            "degree": "Industrial Chemistry",
            "institution": "UFOP",
            "period": "2022",
            "status": "Where Python began — Thonny IDE",
            "active": False,
        },
    ],
}

CERTIFICATIONS = {
    "pt": [
        {"name": "Python Essentials 1 & 2", "issuer": "Cisco Networking Academy", "context": "Fundamentos + Python avançado (OOP, bibliotecas, cert prep)."},
        {"name": "Data Science Essentials with Python", "issuer": "Cisco Networking Academy", "context": "Pandas, Matplotlib — aprendizado prático baseado em projetos."},
        {"name": "Data Analytics Essentials", "issuer": "Cisco Networking Academy", "context": "Ferramentas de analytics reconhecidas pelo mercado."},
        {"name": "IA para Otimização de Processos", "issuer": "Escola Virtual Gov · Enap · Serpro (71h)", "context": "Núcleo de IA do Governo (PBIA) — IA na gestão pública e segurança da informação."},
        {"name": "Networking Basics (120h)", "issuer": "Cisco Networking Academy", "context": "Concluído durante Engenharia de Computação."},
        {"name": "Introdução à Cibersegurança", "issuer": "Cisco Networking Academy", "context": "Segurança de redes e ameaças cibernéticas."},
        {"name": "Segurança em TI", "issuer": "Fundação Bradesco", "context": "Proteção de infraestrutura e dados corporativos."},
        {"name": "Inglês Fluente (3 anos)", "issuer": "KUMON", "context": "Documentação técnica e reuniões com equipes internacionais."},
    ],
    "en": [
        {"name": "Python Essentials 1 & 2", "issuer": "Cisco Networking Academy", "context": "Fundamentals + advanced Python (OOP, libraries, cert prep)."},
        {"name": "Data Science Essentials with Python", "issuer": "Cisco Networking Academy", "context": "Pandas, Matplotlib — hands-on project-based learning."},
        {"name": "Data Analytics Essentials", "issuer": "Cisco Networking Academy", "context": "Industry-recognized analytics tools."},
        {"name": "AI for Process Optimization", "issuer": "Escola Virtual Gov · Enap · Serpro (71h)", "context": "Gov AI Nucleus (PBIA) — strategic AI in public management and infosec."},
        {"name": "Networking Basics (120h)", "issuer": "Cisco Networking Academy", "context": "Completed during Computer Engineering."},
        {"name": "Intro to Cybersecurity", "issuer": "Cisco Networking Academy", "context": "Network security and cyber threats."},
        {"name": "IT Security", "issuer": "Bradesco Foundation", "context": "Corporate infrastructure and data protection."},
        {"name": "Fluent English (3 years)", "issuer": "KUMON", "context": "Technical documentation and meetings with international teams."},
    ],
}

LANGUAGES = {
    "pt": "Português — Nativo · Inglês — Fluente (KUMON, 3 anos)",
    "en": "Portuguese — Native · English — Fluent (KUMON, 3 years)",
}


# ── Page footer ─────────────────────────────────────────────────────────────
def _footer(canvas, doc):
    canvas.saveState()
    footer_y = 7 * mm
    canvas.setStrokeColor(LIGHT_RULE)
    canvas.setLineWidth(0.3)
    canvas.line(doc.leftMargin, footer_y + 2.5*mm, PAGE_W - doc.rightMargin, footer_y + 2.5*mm)
    canvas.restoreState()


# ── PDF Builder ─────────────────────────────────────────────────────────────

def build_pdf(lang: str, output_path: str):
    styles = make_styles()
    story = []

    def s(key: str) -> ParagraphStyle:
        return styles[key]

    def section_heading(text: str):
        story.append(Spacer(1, 0.5*mm))
        story.append(Paragraph(text.upper(), s("section_head")))
        story.append(HRFlowable(
            width="100%", thickness=0.8, color=DARK,
            spaceBefore=0.5*mm, spaceAfter=2*mm,
        ))

    def bullet(text: str):
        story.append(Paragraph(f"- {text}", s("bullet")))

    # ══════════════════════════════════════════════════════════════════════
    # PAGE 1 — THE GATE
    # ══════════════════════════════════════════════════════════════════════

    # Name — huge, centered
    story.append(Paragraph(PERSONAL["name"], s("name")))

    # Title line — centered
    story.append(Paragraph(
        f'{PERSONAL["title"][lang]} · {PERSONAL["subtitle"][lang]}',
        s("title_line"),
    ))

    # Objective — centered, italic, green
    story.append(Paragraph(OBJECTIVE[lang], s("objective")))

    # PCD — centered, small
    pcd_text = ("PCD — TEA (CID-11: 6A02.2) + TDAH (CID-11: 6A05.2)"
                if lang == "pt" else
                "PWD — ASD (ICD-11: 6A02.2) + ADHD (ICD-11: 6A05.2)")
    story.append(Paragraph(pcd_text, s("pcd")))

    # Contact — centered, inline
    contact_parts = [
        PERSONAL["email"],
        PERSONAL["phone"],
        PERSONAL["location"][lang],
        f'<a href="https://{PERSONAL["linkedin"]}" color="{ACCENT.hexval()}">{PERSONAL["linkedin"]}</a>',
        f'<a href="https://{PERSONAL["github"]}" color="{ACCENT.hexval()}">{PERSONAL["github"]}</a>',
        f'<a href="https://{PERSONAL["portfolio"]}" color="{ACCENT.hexval()}">{PERSONAL["portfolio"]}</a>',
    f'<a href="https://{PERSONAL["personalSite"]}" color="{ACCENT.hexval()}">{PERSONAL["personalSite"]}</a>',
    ]
    story.append(Paragraph(" · ".join(contact_parts), s("contact")))

    # ── Technical Skills — inline bold labels (Jake's style) ────────────
    section_heading("Technical Skills" if lang == "en" else "Habilidades Técnicas")
    for label, items in SKILLS[lang]:
        story.append(Paragraph(
            f"<b>{label}:</b> {items}",
            s("skills_line"),
        ))

    # ── Profile — narrative ─────────────────────────────────────────────
    section_heading("Professional Summary" if lang == "en" else "Resumo Profissional")
    story.append(Paragraph(PROFILE[lang], s("body")))

    # ── Professional Experience — role|date alignment ───────────────────
    section_heading("Professional Experience" if lang == "en" else "Experiência Profissional")
    for exp in EXPERIENCE[lang]:
        role_date = f'<b>{exp["role"]}</b>&nbsp;&nbsp;|&nbsp;&nbsp;<font color="{MUTED.hexval()}">{exp["period"]}</font>'
        story.append(Paragraph(role_date, s("role_date")))
        sub_text = f'<i>{exp["company"]}</i>'
        if exp.get("location"):
            sub_text += f'&nbsp;&nbsp;|&nbsp;&nbsp;<font color="{MUTED.hexval()}"><i>{exp["location"]}</i></font>'
        story.append(Paragraph(sub_text, s("subhead")))
        for b in exp["bullets"]:
            bullet(b)
        story.append(Spacer(1, 1*mm))

    # ── Education — degree|period alignment ─────────────────────────────
    section_heading("Education" if lang == "en" else "Educação")
    for edu in EDUCATION[lang]:
        edu_line = f'<b>{edu["degree"]}</b>&nbsp;&nbsp;|&nbsp;&nbsp;<font color="{MUTED.hexval()}">{edu["period"]}</font>'
        story.append(Paragraph(edu_line, s("role_date")))
        story.append(Paragraph(edu["institution"], s("edu_detail")))
        story.append(Paragraph(edu["status"], s("edu_detail")))
        story.append(Spacer(1, 0.5*mm))

    # ══════════════════════════════════════════════════════════════════════
    # PAGE 2 — THE DEPTH
    # ══════════════════════════════════════════════════════════════════════
    story.append(PageBreak())

    # ── Engineering Projects ────────────────────────────────────────────
    section_heading("Projects" if lang == "en" else "Projetos")
    for proj in PROJECTS[lang]:
        proj_block = []
        header_line = f'<b>{proj["name"]}</b>'
        if proj["url"]:
            header_line += f' · <a href="https://{proj["url"]}" color="{ACCENT.hexval()}">{proj["url"]}</a>'
        proj_block.append(Paragraph(header_line, s("project_title")))
        proj_block.append(Paragraph(proj["tech"], s("project_tech")))
        for b in proj["bullets"]:
            proj_block.append(Paragraph(
                f"- {b}", s("bullet"),
            ))
        proj_block.append(Spacer(1, 0.8*mm))
        story.append(KeepTogether(proj_block))

    # ── Certifications ──────────────────────────────────────────────────
    section_heading("Certifications" if lang == "en" else "Certificações")
    for cert in CERTIFICATIONS[lang]:
        line = f"- <b>{cert['name']}</b> — {cert['issuer']}"
        if cert["context"]:
            line += f" — {cert['context']}"
        story.append(Paragraph(line, s("cert_item")))

    # ── Languages ───────────────────────────────────────────────────────
    section_heading("Languages" if lang == "en" else "Idiomas")
    story.append(Paragraph(LANGUAGES[lang], s("skills_line")))

    # Portfolio CTA
    story.append(Spacer(1, 5*mm))
    cta_text = (
        "Case studies completos, demos e codigo-fonte -> "
        if lang == "pt" else
        "Full case studies, demos & source code -> "
    )
    story.append(Paragraph(
        f'{cta_text}<a href="https://{PERSONAL["portfolio"]}" color="{ACCENT.hexval()}">{PERSONAL["portfolio"]}</a>',
        s("footer_link"),
    ))

    # ── Build ───────────────────────────────────────────────────────────
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        topMargin=10*mm,
        bottomMargin=12*mm,
        leftMargin=16*mm,
        rightMargin=16*mm,
    )
    doc.lang = lang
    doc.build(story, onFirstPage=_footer, onLaterPages=_footer)
    print(f"  Generated: {output_path}")


# ── Main ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    out_dir = os.path.dirname(os.path.abspath(__file__))

    pt_path = os.path.join(out_dir, "Isaac-Nathan-CV-PT.pdf")
    en_path = os.path.join(out_dir, "Isaac-Nathan-CV-EN.pdf")

    print("Generating V3 layered CVs (Jake's style)...")
    print(f"  Current semester: {SEMESTER} ({SEMESTER_PT} / {SEMESTER_EN})")
    build_pdf("pt", pt_path)
    build_pdf("en", en_path)
    print("Done.")
