import { useState, useEffect, useRef } from 'react'
import { motion } from 'framer-motion'
import { Preloader } from './components/Preloader'
import { useLenis } from './hooks/useLenis'
import { useSmoothContainer } from './hooks/useSmoothContainer'
import { revealVariants, staggerContainer } from './hooks/useScrollReveal'
import { apiUrl } from './lib/api'
import { ApiConfig } from './components/ApiConfig'
import { BetaBanner } from './components/BetaBanner'

const COLAB_URL = 'https://colab.research.google.com/github/xAngryBadger/cv-generator/blob/main/colab-backend.ipynb'

type Language = 'pt' | 'en'
type Template = 'modern' | 'classic' | 'minimal'

interface CVData {
  name: string
  email: string
  phone: string
  location: string
  linkedin: string
  github: string
  portfolio: string
  title: string
  subtitle: string
  profile: string
  experience: string
  projects: string
  education: string
  skills: string
  language: Language
  template: Template
}

const defaultData: CVData = {
  name: 'Isaac Nathan da Silva Barbosa',
  email: 'isaacnathandasilva@gmail.com',
  phone: '+55 (31) 99441-7786',
  location: 'Mariana, MG — Brasil',
  linkedin: 'linkedin.com/in/isaac-nathan',
  github: 'github.com/xAngryBadger',
  portfolio: 'xangrybadger.github.io/isaac-vitae',
  title: 'Desenvolvedor Full-Stack com IA',
  subtitle: 'Engenharia de Computação · IA · Cloud · IoT',
  profile: `Desenvolvedor Full-Stack com IA · Python · FastAPI · React 19 · Azure Cosmos DB · GPT-4.1 · Flutter · PyTorch · 10 meses de experiência profissional. Primeiro contato com Python em 2022 na UFOP (Química Industrial) — Thonny IDE, sem GPT, aulas extras à tarde só para continuar aprendendo.`,
  experience: `Paware Softwares | Desenvolvedor Full-Stack com foco em IA | Out 2025 — Mai 2026
• Migrei datasets legados do Google Drive para Azure Cosmos DB para Meritage Homes (EUA)
• Arquitetei pipeline agentic de geração de imagens para o HelloSocial
• Resolvi problema cross-platform de MIME types`,
  projects: `HarpIA | github.com/xAngryBadger/harpia
• Motor de automação criativa com 7+ modelos de IA
• Pipeline agentic autônomo com GPT-4.1 e schema enforcement

Flora Sensus | github.com/xAngryBadger/flora-sensus
• App Flutter offline-first para inventário florestal
• ~24K LOC com sync custom e UUID remapping`,
  education: `Engenharia de Computação | Cruzeiro do Sul | 2024 — 2029 | 5º período
Engenharia Química | UFSJ | 2022 — 2024 | Período de transição
Química Industrial | UFOP | 2022 | Onde Python começou`,
  skills: 'Python · FastAPI · React 19 · TypeScript · Flutter · Azure · Docker · GPT-4.1 · PyTorch · Azure Cosmos DB · Tailwind CSS · Node.js',
  language: 'pt',
  template: 'modern',
}

function App() {
  const [showPreloader, setShowPreloader] = useState(true)
  const [data, setData] = useState<CVData>(defaultData)
  const [loading, setLoading] = useState(false)
  const [previewUrl, setPreviewUrl] = useState<string | null>(null)
  const prevUrlRef = useRef<string | null>(null)

  useLenis()
  const formScrollRef = useSmoothContainer()

  useEffect(() => {
    if (prevUrlRef.current) URL.revokeObjectURL(prevUrlRef.current)
    prevUrlRef.current = previewUrl
  }, [previewUrl])

  const handleChange = (field: keyof CVData, value: string) => {
    setData(prev => ({ ...prev, [field]: value }))
  }

  const handleSubmit = async () => {
    setLoading(true)
    try {
      const response = await fetch(apiUrl('/api/generate-cv'), {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      })
      if (!response.ok) throw new Error('Failed to generate PDF')
      const blob = await response.blob()
      const url = window.URL.createObjectURL(blob)
      setPreviewUrl(url)
      const link = document.createElement('a')
      link.href = url
      link.download = `CV-${data.name.split(' ')[0]}-${data.language.toUpperCase()}.pdf`
      link.click()
  } catch (error) {
    if (error instanceof Error && error.message === 'NO_API_URL') {
      alert('Configure a URL da API primeiro. Clique em "Sem API" no header e cole a URL do ngrok.')
    } else {
      console.error('Error generating PDF:', error)
      alert('Erro ao gerar PDF. Verifique se o backend está online.')
    }
    } finally {
      setLoading(false)
    }
  }

return (
    <>
      {showPreloader && <Preloader title="CV Generator" onComplete={() => setShowPreloader(false)} />}

      <div className="noise-overlay noise-overlay--animated" aria-hidden="true" />

      <motion.div
        initial={{ clipPath: 'inset(0 0 100% 0)' }}
        animate={{ clipPath: 'inset(0 0 0 0)' }}
        transition={{ duration: 0.8, delay: 0.1, ease: [0.16, 1, 0.3, 1] }}
        className="min-h-screen bg-[var(--color-bg)] text-[var(--color-text)]"
      >
      <BetaBanner colabUrl={COLAB_URL} />
      <header className="fixed top-0 left-0 right-0 z-40 fade-border-bottom h-16 flex items-center" style={{ backdropFilter: 'blur(16px)', backgroundColor: 'rgba(13,17,23,0.8)' }}>
      <div className="max-w-7xl mx-auto px-6 w-full flex items-center justify-between">
            <div className="flex items-center gap-3">
              <motion.div
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                transition={{ delay: 0.4, type: 'spring', stiffness: 200, damping: 15 }}
                className="w-8 h-8 flex items-center justify-center"
              >
                <svg className="w-6 h-6 text-[var(--color-primary)]" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </motion.div>
              <div>
                <h1 className="text-lg font-serif font-normal tracking-tight text-[var(--color-cream)]">CV Generator</h1>
              </div>
            </div>
      <div className="flex items-center gap-4">
        <ApiConfig colabUrl={COLAB_URL} />
        <span className="label-mono text-[var(--color-text-muted)]">ATS-friendly</span>
        <span className="label-mono text-[var(--color-primary)]">PT / EN</span>
      </div>
          </div>
        </header>

        <main className="max-w-7xl mx-auto px-6 pt-20 pb-16 lg:px-8">
          <motion.div
            initial="hidden"
            animate="visible"
            variants={staggerContainer}
            className="grid grid-cols-1 lg:grid-cols-12 gap-8 lg:gap-12"
          >
            <div ref={formScrollRef} data-lenis-prevent className="lg:col-span-7 lg:sticky lg:top-24 lg:self-start lg:max-h-[calc(100dvh-8rem)] lg:overflow-y-auto lg:pr-2 [&::-webkit-scrollbar]:w-1 [&::-webkit-scrollbar-thumb]:bg-[var(--color-border)] [&::-webkit-scrollbar-thumb]:rounded-sm [&::-webkit-scrollbar-track]:transparent">
              <motion.div variants={revealVariants} custom={0} className="mb-10">
                <p className="eyebrow text-[var(--color-primary)] mb-3">Currículo Profissional</p>
                <h2 className="text-3xl md:text-4xl font-serif font-normal text-[var(--color-cream)] leading-tight">
                  Gere seu PDF<br />
                  <span className="text-[var(--color-amber-light)]">em segundos</span>
                </h2>
                <p className="mt-4 text-[var(--color-text-muted)] max-w-md">
                  Preencha os campos abaixo e baixe um currículo profissional,
                  otimizado para sistemas ATS.
                </p>
              </motion.div>

              <motion.div variants={revealVariants} custom={0.1} className="space-y-0">
                {[
                  { num: '01', title: 'Dados Pessoais', content: (
                    <div className="space-y-4">
                      <EditorialInput label="Nome Completo" value={data.name} onChange={(v) => handleChange('name', v)} />
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <EditorialInput label="Email" value={data.email} onChange={(v) => handleChange('email', v)} />
                        <EditorialInput label="Telefone" value={data.phone} onChange={(v) => handleChange('phone', v)} />
                      </div>
                      <EditorialInput label="Localização" value={data.location} onChange={(v) => handleChange('location', v)} />
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <EditorialInput label="LinkedIn" value={data.linkedin} onChange={(v) => handleChange('linkedin', v)} />
                        <EditorialInput label="GitHub" value={data.github} onChange={(v) => handleChange('github', v)} />
                      </div>
                      <EditorialInput label="Portfolio" value={data.portfolio} onChange={(v) => handleChange('portfolio', v)} />
                    </div>
                  )},
                  { num: '02', title: 'Título e Perfil', content: (
                    <div className="space-y-4">
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <EditorialInput label="Título" value={data.title} onChange={(v) => handleChange('title', v)} />
                        <EditorialInput label="Subtítulo" value={data.subtitle} onChange={(v) => handleChange('subtitle', v)} />
                      </div>
                      <EditorialTextarea label="Perfil Profissional" value={data.profile} onChange={(v) => handleChange('profile', v)} rows={4} />
                    </div>
                  )},
                  { num: '03', title: 'Experiência', content: (
                    <EditorialTextarea label="Experiência Profissional" value={data.experience} onChange={(v) => handleChange('experience', v)} rows={6} />
                  )},
                  { num: '04', title: 'Projetos', content: (
                    <EditorialTextarea label="Projetos de Engenharia" value={data.projects} onChange={(v) => handleChange('projects', v)} rows={6} />
                  )},
                  { num: '05', title: 'Educação e Skills', content: (
                    <div className="space-y-4">
                      <EditorialTextarea label="Educação" value={data.education} onChange={(v) => handleChange('education', v)} rows={4} />
                      <EditorialTextarea label="Skills" value={data.skills} onChange={(v) => handleChange('skills', v)} rows={2} />
                    </div>
                  )},
                  { num: '06', title: 'Configurações', content: (
                    <div className="grid grid-cols-2 gap-6">
                      <div>
                        <label className="eyebrow text-[var(--color-text-muted)] mb-3 block">Idioma</label>
                        <div className="flex gap-2">
                          {(['pt', 'en'] as Language[]).map((lang) => (
                            <button
                              key={lang}
          onClick={() => handleChange('language', lang)}
          aria-pressed={data.language === lang}
          className={`px-4 py-2 text-sm transition-all duration-200 ${
                                data.language === lang
                                  ? 'bg-[var(--color-primary)] text-[var(--color-cream)]'
                                  : 'bg-[var(--color-bg)] text-[var(--color-text-muted)] border-b border-[var(--color-border)] hover:border-[var(--color-primary)]'
                              }`}
                            >
                              {lang.toUpperCase()}
                            </button>
                          ))}
                        </div>
                      </div>
                      <div>
                        <label className="eyebrow text-[var(--color-text-muted)] mb-3 block">Template</label>
                        <div className="flex gap-2">
                          {(['modern', 'classic', 'minimal'] as Template[]).map((t) => (
                            <button
                              key={t}
          onClick={() => handleChange('template', t)}
          aria-pressed={data.template === t}
          className={`px-4 py-2 text-sm capitalize transition-all duration-200 ${
                                data.template === t
                                  ? 'bg-[var(--color-primary)] text-[var(--color-cream)]'
                                  : 'bg-[var(--color-bg)] text-[var(--color-text-muted)] border-b border-[var(--color-border)] hover:border-[var(--color-primary)]'
                              }`}
                            >
                              {t}
                            </button>
                          ))}
                        </div>
                      </div>
                    </div>
                  )},
                ].map((section) => (
                  <motion.div
                    key={section.num}
                    variants={revealVariants}
                    custom={parseInt(section.num) * 0.1}
                    className="group editorial-divider py-8"
                  >
                    <div className="flex items-baseline gap-4 mb-6">
                      <span className="section-number">{section.num}</span>
                      <h3 className="text-xl font-serif font-normal text-[var(--color-cream)]">{section.title}</h3>
                    </div>
                    {section.content}
                  </motion.div>
                ))}
              </motion.div>

              <motion.div variants={revealVariants} custom={0.6} className="mt-8 mb-12">
                <button
                  onClick={handleSubmit}
                  disabled={loading}
                  className="btn-clipped w-full"
                >
                  <span className="btn-text-back flex items-center justify-center gap-2 font-semibold text-sm tracking-wide">
                    {loading ? (
                      <>
                        <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24">
                          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                        </svg>
                        Gerando PDF...
                      </>
                    ) : (
                      'Baixar PDF'
                    )}
                  </span>
                </button>
              </motion.div>
            </div>

            <div className="lg:col-span-5">
              <div className="lg:sticky lg:top-24">
                <motion.div variants={revealVariants} custom={0.3}>
                  <p className="eyebrow text-[var(--color-text-muted)] mb-4">Preview</p>
    {previewUrl ? (
          <iframe
            title="CV Preview"
            src={previewUrl}
                      className="w-full h-[600px] border border-[var(--color-border-subtle)] bg-white"
                    />
                  ) : (
                    <div className="flex flex-col items-center justify-center h-[600px] bg-[var(--color-bg-alt)] border border-[var(--color-border-subtle)] geometric-bg">
                      <div className="text-center relative z-10">
                        <p className="font-serif text-2xl text-[var(--color-cream)] mb-2">Preview</p>
                        <p className="text-sm text-[var(--color-text-muted)]">Clique em "Baixar PDF" para gerar</p>
                        <p className="label-mono text-[var(--color-primary)] mt-3">ATS-friendly · PT/EN · Grátis</p>
                      </div>
                    </div>
                  )}
                </motion.div>
              </div>
            </div>
          </motion.div>
        </main>

        <footer className="fade-border-top px-6 py-6 mt-8">
          <div className="max-w-7xl mx-auto flex items-center justify-between">
            <p className="font-serif text-sm text-[var(--color-text-muted)]">
              Desenvolvido por Isaac Nathan
            </p>
            <a
              href="https://github.com/xAngryBadger"
              className="link-underline label-mono text-[var(--color-primary)] hover:text-[var(--color-primary-light)]"
            >
              GitHub
            </a>
          </div>
        </footer>
      </motion.div>
    </>
  )
}

function EditorialInput({ label, value, onChange }: { label: string; value: string; onChange: (v: string) => void }) {
  return (
    <div className="group/input">
      <label className="eyebrow text-[var(--color-text-muted)] mb-2 block text-xs">{label}</label>
      <input
        type="text"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="w-full bg-transparent border-0 border-b border-[var(--color-border)] px-0 py-2.5 text-sm text-[var(--color-text)] focus:outline-none focus:border-[var(--color-primary)] transition-colors duration-200 placeholder:text-[var(--color-offset)]"
        placeholder={label}
      />
    </div>
  )
}

function EditorialTextarea({ label, value, onChange, rows = 3 }: { label: string; value: string; onChange: (v: string) => void; rows?: number }) {
  return (
    <div className="group/textarea">
      <label className="eyebrow text-[var(--color-text-muted)] mb-2 block text-xs">{label}</label>
      <textarea
        value={value}
        onChange={(e) => onChange(e.target.value)}
        rows={rows}
        className="w-full bg-transparent border-0 border-b border-[var(--color-border)] px-0 py-2.5 text-sm text-[var(--color-text)] focus:outline-none focus:border-[var(--color-primary)] transition-colors duration-200 resize-vertical placeholder:text-[var(--color-offset)]"
        placeholder={label}
      />
    </div>
  )
}

export default App
