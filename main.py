from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.enums import TA_LEFT, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import io
import tempfile
import os

FONT_DIR = "/usr/share/fonts/TTF"
for _name, _file in [
    ("DejaVu", "DejaVuSans.ttf"),
    ("DejaVu-Bold", "DejaVuSans-Bold.ttf"),
]:
    _path = os.path.join(FONT_DIR, _file)
    if os.path.exists(_path):
        pdfmetrics.registerFont(TTFont(_name, _path))

_FONT = "DejaVu" if "DejaVu" in pdfmetrics._fonts else "Helvetica"
_FONT_BOLD = "DejaVu-Bold" if "DejaVu-Bold" in pdfmetrics._fonts else "Helvetica-Bold"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CVData(BaseModel):
    name: str
    email: str
    phone: str
    location: str
    linkedin: str
    github: str
    portfolio: str
    title: str
    subtitle: str
    profile: str
    experience: str
    projects: str
    education: str
    skills: str
    language: str
    template: str

SAGE = HexColor("#456A4B")
AMBER = HexColor("#8B6914")
DARK = HexColor("#0D1117")
MUTED = HexColor("#8B9481")
BORDER = HexColor("#D4D0C8")

def make_styles():
    styles = {}
    styles["name"] = ParagraphStyle(
        "Name", fontName=_FONT_BOLD, fontSize=15,
        leading=18, textColor=DARK, alignment=TA_LEFT,
        spaceAfter=1*mm,
    )
    styles["title"] = ParagraphStyle(
        "Title", fontName=_FONT, fontSize=8.5,
        leading=11, textColor=AMBER, alignment=TA_LEFT,
        spaceAfter=0.5*mm,
    )
    styles["contact"] = ParagraphStyle(
        "Contact", fontName=_FONT, fontSize=7,
        leading=9.5, textColor=MUTED, alignment=TA_LEFT,
        spaceAfter=0,
    )
    styles["section_head"] = ParagraphStyle(
        "SectionHead", fontName=_FONT_BOLD, fontSize=9.5,
        leading=11.5, textColor=DARK, alignment=TA_LEFT,
        spaceBefore=2.5*mm, spaceAfter=1*mm,
    )
    styles["body"] = ParagraphStyle(
        "Body", fontName=_FONT, fontSize=8,
        leading=11, textColor=DARK, alignment=TA_JUSTIFY,
        spaceAfter=0.3*mm,
    )
    styles["body_small"] = ParagraphStyle(
        "BodySmall", fontName=_FONT, fontSize=7,
        leading=9.5, textColor=MUTED, alignment=TA_LEFT,
        spaceAfter=0.2*mm,
    )
    styles["bullet"] = ParagraphStyle(
        "Bullet", fontName=_FONT, fontSize=8,
        leading=11, textColor=DARK, alignment=TA_JUSTIFY,
        leftIndent=8, bulletIndent=0,
        spaceAfter=0.4*mm,
    )
    return styles

def generate_pdf(data: CVData):
    buffer = io.BytesIO()
    styles = make_styles()
    story = []
    
    def s(key):
        return styles[key]
    
    def heading(text):
        story.append(Paragraph(text.upper(), s("section_head")))
        story.append(HRFlowable(
            width="100%", thickness=0.5, color=BORDER,
            spaceBefore=0, spaceAfter=2*mm,
        ))
    
    def bullet(text):
        story.append(Paragraph(f"<bullet>&bull;</bullet> {text}", s("bullet")))
    
    story.append(Paragraph(data.name, s("name")))
    story.append(Paragraph(f'{data.title} · {data.subtitle}', s("title")))
    
    contact_parts = [
        data.email,
        data.phone,
        data.location,
        data.linkedin,
        data.github,
        data.portfolio,
    ]
    story.append(Paragraph(" · ".join(contact_parts), s("contact")))
    story.append(Spacer(1, 1.5*mm))
    
    heading("Perfil" if data.language == 'pt' else "Profile")
    story.append(Paragraph(data.profile, s("body")))
    
    heading("Experiência" if data.language == 'pt' else "Experience")
    for line in data.experience.split('\n'):
        if line.strip():
            if line.startswith('•'):
                bullet(line[1:].strip())
            else:
                story.append(Paragraph(line, s("body")))
    story.append(Spacer(1, 1*mm))
    
    heading("Projetos" if data.language == 'pt' else "Projects")
    for line in data.projects.split('\n'):
        if line.strip():
            if line.startswith('•'):
                bullet(line[1:].strip())
            else:
                story.append(Paragraph(line, s("body")))
    story.append(Spacer(1, 1*mm))
    
    heading("Educação" if data.language == 'pt' else "Education")
    for line in data.education.split('\n'):
        if line.strip():
            story.append(Paragraph(line, s("body")))
    
    heading("Skills")
    story.append(Paragraph(data.skills, s("body")))
    
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        topMargin=14*mm,
        bottomMargin=12*mm,
        leftMargin=16*mm,
        rightMargin=16*mm,
    )
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()

@app.post("/api/generate-cv")
async def generate_cv(cv_data: CVData):
    try:
        pdf_bytes = generate_pdf(cv_data)
        return StreamingResponse(
            io.BytesIO(pdf_bytes),
            media_type="application/pdf",
            headers={"Content-Disposition": f'attachment; filename="CV-{cv_data.name.split()[0]}-{cv_data.language.upper()}.pdf"'},
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "Cegonha API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
