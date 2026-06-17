"""
CareerLens AI v2.0 - Powered by Groq (Free, No Credit Card)
"""

import streamlit as st
import pandas as pd
import re
import os

# ── PyPDF2 ──────────────────────────────────────────
try:
    import PyPDF2
    PDF_SUPPORT = True
except ImportError:
    PDF_SUPPORT = False

# ── Groq AI ─────────────────────────────────────────
try:
    from groq import Groq
    GROQ_KEY   = os.environ.get("GROQ_API_KEY", "")
    AI_SUPPORT = bool(GROQ_KEY)
except Exception:
    AI_SUPPORT = False

# ═══════════════════════════════════════════════════
# PAGE CONFIG
# ═══════════════════════════════════════════════════
st.set_page_config(
    page_title="CareerLens AI",
    page_icon="🔭",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Sora:wght@400;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
:root{--bg:#07090F;--surface:#0F1219;--surface2:#151923;--border:#1E2433;--indigo:#6366F1;--violet:#8B5CF6;--emerald:#10B981;--amber:#F59E0B;--rose:#F43F5E;--text:#E8EDF5;--muted:#7B8599;--radius:14px;}
html,body,[class*="css"]{font-family:'Inter',sans-serif;color:var(--text);}
.stApp{background:var(--bg);}
.block-container{padding:2rem 2.5rem !important;}
[data-testid="stSidebar"]{background:var(--surface) !important;border-right:1px solid var(--border);}
.hero{background:linear-gradient(135deg,#0d1128 0%,#090d1f 60%,#110d1f 100%);border:1px solid var(--border);border-radius:20px;padding:44px 52px;margin-bottom:36px;position:relative;overflow:hidden;}
.hero::after{content:"";position:absolute;top:-60px;right:-60px;width:300px;height:300px;background:radial-gradient(circle,rgba(99,102,241,0.18) 0%,transparent 70%);pointer-events:none;}
.hero-badge{display:inline-flex;align-items:center;gap:6px;background:rgba(99,102,241,0.12);border:1px solid rgba(99,102,241,0.3);border-radius:20px;padding:4px 14px;font-family:'JetBrains Mono',monospace;font-size:0.65rem;letter-spacing:0.12em;color:var(--indigo);text-transform:uppercase;margin-bottom:18px;}
.hero-title{font-family:'Sora',sans-serif;font-size:clamp(2.2rem,4vw,3.2rem);font-weight:700;line-height:1.1;color:var(--text);margin:0 0 14px;}
.hero-title .accent{color:var(--indigo);}
.hero-sub{font-size:1rem;color:var(--muted);max-width:500px;line-height:1.7;}
.card{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:24px 28px;margin-bottom:16px;transition:border-color 0.2s;}
.card:hover{border-color:rgba(99,102,241,0.35);}
.card-icon{font-size:1.4rem;margin-bottom:10px;}
.card-title{font-size:0.95rem;font-weight:600;color:var(--text);margin-bottom:6px;}
.card-body{font-size:0.85rem;color:var(--muted);line-height:1.7;white-space:pre-wrap;}
.output-card{background:var(--surface2);border:1px solid var(--border);border-left:3px solid var(--indigo);border-radius:var(--radius);padding:28px 32px;margin-bottom:20px;font-size:0.9rem;color:var(--text);line-height:1.8;white-space:pre-wrap;}
.metric-row{display:flex;gap:14px;flex-wrap:wrap;margin-bottom:28px;}
.metric-box{background:var(--surface);border:1px solid var(--border);border-radius:12px;padding:18px 24px;min-width:130px;text-align:center;}
.metric-val{font-family:'Sora',sans-serif;font-size:2rem;font-weight:700;color:var(--indigo);line-height:1;}
.metric-lbl{font-size:0.68rem;color:var(--muted);text-transform:uppercase;letter-spacing:0.1em;margin-top:6px;}
.tags{display:flex;flex-wrap:wrap;gap:8px;margin:10px 0;}
.tag{font-size:0.75rem;font-weight:600;padding:5px 13px;border-radius:20px;border:1px solid;letter-spacing:0.02em;}
.tag-green{background:rgba(16,185,129,0.1);color:#10B981;border-color:rgba(16,185,129,0.3);}
.tag-red{background:rgba(244,63,94,0.1);color:#F43F5E;border-color:rgba(244,63,94,0.3);}
.tag-indigo{background:rgba(99,102,241,0.1);color:#6366F1;border-color:rgba(99,102,241,0.3);}
.eyebrow{font-family:'JetBrains Mono',monospace;font-size:0.62rem;letter-spacing:0.14em;text-transform:uppercase;color:var(--muted);margin-bottom:10px;}
.score-green{color:#10B981;}.score-amber{color:#F59E0B;}.score-red{color:#F43F5E;}
div[data-testid="stTextInput"] input,div[data-testid="stTextArea"] textarea,div[data-testid="stSelectbox"]>div>div{background:var(--surface2) !important;border:1px solid var(--border) !important;border-radius:8px !important;color:var(--text) !important;}
.stButton>button{background:linear-gradient(135deg,#6366F1,#8B5CF6) !important;color:white !important;border:none !important;border-radius:10px !important;font-weight:600 !important;font-size:0.88rem !important;padding:0.6rem 1.6rem !important;}
.stButton>button:hover{opacity:0.85 !important;}
div[data-testid="stProgress"]>div>div{background:var(--indigo) !important;}
.stTabs [data-baseweb="tab"]{color:var(--muted) !important;font-weight:500;font-size:0.88rem;}
.stTabs [aria-selected="true"]{color:var(--indigo) !important;border-bottom-color:var(--indigo) !important;}
hr{border-color:var(--border) !important;}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════
# CONSTANTS
# ═══════════════════════════════════════════════════
TARGET_ROLES = ["AI/ML Intern","Web Developer","Data Analyst","IoT Developer","Software Engineer"]
KNOWN_SKILLS = [
    "python","c++","java","sql","machine learning","deep learning","nlp",
    "tensorflow","pytorch","html","css","javascript","react","node.js",
    "mongodb","arduino","iot","cloud","data analysis","pandas","numpy",
    "scikit-learn","power bi","excel","git","docker","aws","flask","django",
]
ROLE_SKILLS = {
    "AI/ML Intern":      ["python","machine learning","numpy","pandas","sql","scikit-learn","data analysis"],
    "Web Developer":     ["html","css","javascript","react","node.js","mongodb"],
    "Data Analyst":      ["python","sql","excel","power bi","pandas","data visualization"],
    "IoT Developer":     ["arduino","iot","nodemcu","sensors","mqtt","cloud","python"],
    "Software Engineer": ["python","java","sql","dsa","oop","git"],
}
LEARNING_RESOURCES = {
    "python":"freeCodeCamp Python · cs50p Harvard",
    "machine learning":"Andrew Ng ML Specialization (Coursera)",
    "sql":"SQLZoo · Mode Analytics SQL Tutorial",
    "javascript":"javascript.info · The Odin Project",
    "react":"React Official Docs · Scrimba React",
    "html":"MDN Web Docs · freeCodeCamp",
    "css":"CSS Tricks · Kevin Powell YouTube",
    "numpy":"NumPy Official Docs · Kaggle Learn",
    "pandas":"Kaggle Pandas · official docs",
    "scikit-learn":"Scikit-learn Docs · Kaggle Learn",
    "power bi":"Microsoft Learn Power BI",
    "docker":"Docker Official Getting Started",
    "git":"Git Handbook · Learn Git Branching",
    "aws":"AWS Skill Builder (free tier)",
    "arduino":"Arduino Official Tutorials",
    "iot":"Coursera IoT Specialization",
    "tensorflow":"TensorFlow Official Tutorials",
    "pytorch":"PyTorch Official 60-min Blitz",
}

# ═══════════════════════════════════════════════════
# UTILITIES
# ═══════════════════════════════════════════════════
def extract_pdf_text(f) -> str:
    if not PDF_SUPPORT: return ""
    try:
        r = PyPDF2.PdfReader(f)
        return "\n".join(p.extract_text() or "" for p in r.pages)
    except Exception as e:
        st.warning(f"PDF error: {e}"); return ""

def detect_skills(text: str) -> list:
    lo = text.lower()
    return [s for s in KNOWN_SKILLS if s in lo]

def compute_gap(user_skills: list, role: str) -> dict:
    req     = ROLE_SKILLS.get(role, [])
    lo      = [s.lower().strip() for s in user_skills]
    matched = [s for s in req if s in lo]
    missing = [s for s in req if s not in lo]
    pct     = round(len(matched)/len(req)*100) if req else 0
    recs = []
    if missing:
        recs.append(f"📚 Learn: {', '.join(missing[:3])}" + (" + more" if len(missing)>3 else ""))
    recs += [
        "🛠️ Build a capstone project using the full role stack",
        "🔑 Add role keywords to your resume headline",
        "🎓 Get 1 relevant certification to boost credibility",
    ]
    return {"required":req,"matched":matched,"missing":missing,"percentage":pct,"recs":recs}

# ═══════════════════════════════════════════════════
# CORE AI — GROQ (Free, Fast)
# ═══════════════════════════════════════════════════
def get_groq_client():
    key = st.session_state.get("groq_key","") or os.environ.get("GROQ_API_KEY","")
    if key:
        try:
            from groq import Groq
            return Groq(api_key=key)
        except Exception:
            return None
    return None

def call_ai(prompt: str) -> str:
    client = get_groq_client()
    if not client:
        return "⚠️ Please enter your Groq API key in the sidebar first."
    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role":"user","content":prompt}],
            max_tokens=2000,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"⚠️ Error: {e}"

def ctx(p: dict) -> str:
    return f"""Name: {p.get('name','N/A')}
Email: {p.get('email','')} | Phone: {p.get('phone','')}
Education: {p.get('education','')}
Skills: {', '.join(p.get('skills',[]))}
Projects: {p.get('projects','')}
Certifications: {p.get('certifications','')}
Target Role: {p.get('role','')}
Company: {p.get('company','a top company')}"""

# ═══════════════════════════════════════════════════
# AI GENERATORS
# ═══════════════════════════════════════════════════
def gen_resume(p):
    return call_ai(f"""You are a senior resume writer. Write a polished ATS-friendly resume.
Sections: Professional Summary | Core Skills | Projects | Education | Certifications
Use clean formatting. No markdown symbols. Make it impactful and keyword-rich.
PROFILE:\n{ctx(p)}""")

def gen_cover(p):
    return call_ai(f"""Write a compelling 3-paragraph cover letter.
Para 1: Hook - why this role excites them.
Para 2: 2-3 specific achievements that prove fit.
Para 3: Confident call to action. Plain text only.
Role: {p.get('role')} at {p.get('company','a top company')}
PROFILE:\n{ctx(p)}""")

def gen_portfolio(p):
    return call_ai(f"""Create portfolio website copy with five labelled sections:
ABOUT ME | SKILLS | PROJECTS | ACHIEVEMENTS | CONTACT
Each: professional, specific, 3-5 sentences. Plain text only.
PROFILE:\n{ctx(p)}""")

def gen_interview_qa(p, extra="", difficulty="Fresher / Entry Level"):
    return call_ai(f"""Generate 10 interview questions WITH detailed model answers.
Role: {p.get('role')} | Skills: {', '.join(p.get('skills',[]))}
Projects: {p.get('projects','')} | Difficulty: {difficulty}
{f'Focus: {extra}' if extra else ''}
Format:
Q[N]: [Question]
A[N]: [STAR method answer specific to their profile]
Mix: 3 technical, 3 behavioral, 2 project-based, 2 HR.""")

def gen_linkedin(p, tone="Professional & Formal"):
    return call_ai(f"""Write a complete LinkedIn profile. Tone: {tone}
1. HEADLINE (under 220 chars)
2. ABOUT SECTION (first-person storytelling)
3. EXPERIENCE BULLETS (3 bullets per project, action verb + metric)
4. TOP 10 SKILLS
5. BANNER TAGLINE
PROFILE:\n{ctx(p)}""")

def gen_jd_match(p, jd_text: str):
    return call_ai(f"""Analyze this job description against the candidate.
JOB DESCRIPTION:\n{jd_text}
CANDIDATE:\n{ctx(p)}
Output:
MATCH SCORE: [X/100]
STRONG MATCHES:
GAPS TO ADDRESS:
KEYWORDS TO ADD:
TAILORED SUMMARY:
TOP 3 INTERVIEW QUESTIONS:""")

def gen_roadmap(p, hours=2):
    gap     = compute_gap(p.get('skills',[]), p.get('role','Software Engineer'))
    missing = gap['missing']
    return call_ai(f"""Create a 12-week learning roadmap.
Target Role: {p.get('role')}
Current Skills: {', '.join(p.get('skills',[]))}
Skills to Learn: {', '.join(missing) if missing else 'Advanced topics'}
Daily hours: {hours}
Format:
WEEK 1-2: [Topic] - [tasks, resources, mini project]
...for all 12 weeks
MILESTONE PROJECTS: 3 projects
CERTIFICATION PATH:
DAILY ROUTINE: {hours}-hour plan""")

def gen_ats_score(p, resume_text=""):
    content = resume_text if resume_text else f"""
Name: {p.get('name')} | Skills: {', '.join(p.get('skills',[]))}
Education: {p.get('education','')}
Projects: {p.get('projects','')}
Certifications: {p.get('certifications','')}"""
    return call_ai(f"""You are an ATS expert. Score this resume for: {p.get('role')}
RESUME:\n{content}
OVERALL ATS SCORE: [X/100]
SECTION SCORES:
- Keywords Match: [X/25]
- Format & Structure: [X/20]
- Skills Section: [X/20]
- Quantified Achievements: [X/20]
- Contact & Header: [X/15]
CRITICAL ISSUES:
IMPROVEMENTS:
MISSING KEYWORDS:
OPTIMIZED HEADLINE:""")

# ═══════════════════════════════════════════════════
# UI HELPERS
# ═══════════════════════════════════════════════════
def hero():
    st.markdown("""
    <div class="hero">
      <div class="hero-badge">🔭 v2.0 · Groq AI · 100% Free · No Credit Card</div>
      <h1 class="hero-title">Career<span class="accent">Lens</span> AI</h1>
      <p class="hero-sub">AI-Powered Resume, Portfolio & Skill Gap Analyzer — built for students ready to stand out.</p>
    </div>""", unsafe_allow_html=True)

def card(icon, title, body):
    st.markdown(f"""<div class="card"><div class="card-icon">{icon}</div>
    <div class="card-title">{title}</div><div class="card-body">{body}</div></div>""",
    unsafe_allow_html=True)

def output_card(text):
    safe = text.replace("<","&lt;").replace(">","&gt;")
    st.markdown(f'<div class="output-card">{safe}</div>', unsafe_allow_html=True)

def tags_html(items, style="indigo"):
    html = "".join(f'<span class="tag tag-{style}">{i}</span>' for i in items)
    st.markdown(f'<div class="tags">{html}</div>', unsafe_allow_html=True)

def eyebrow(text):
    st.markdown(f'<div class="eyebrow">{text}</div>', unsafe_allow_html=True)

def skill_gap_ui(gap, role):
    pct   = gap["percentage"]
    color = "green" if pct>=75 else "amber" if pct>=50 else "red"
    st.markdown(f"""<div class="metric-row">
      <div class="metric-box"><div class="metric-val score-{color}">{pct}%</div><div class="metric-lbl">Match Score</div></div>
      <div class="metric-box"><div class="metric-val">{len(gap['matched'])}</div><div class="metric-lbl">Skills Found</div></div>
      <div class="metric-box"><div class="metric-val">{len(gap['missing'])}</div><div class="metric-lbl">Gaps</div></div>
      <div class="metric-box"><div class="metric-val">{len(gap['required'])}</div><div class="metric-lbl">Required</div></div>
    </div>""", unsafe_allow_html=True)
    st.progress(pct/100)
    if pct>=75: st.success(f"🎯 Strong match for **{role}**!")
    elif pct>=50: st.warning("⚡ Moderate match. Close a few gaps to be competitive.")
    else: st.error("📈 Early stage. Focus on foundational skills first.")
    c1,c2 = st.columns(2)
    with c1:
        eyebrow("✅ skills you have")
        tags_html(gap["matched"] or ["—"],"green")
    with c2:
        eyebrow("❌ skills to learn")
        tags_html(gap["missing"] or ["—"],"red")
    eyebrow("💡 recommendations")
    for r in gap["recs"]: st.markdown(f"- {r}")
    if gap["missing"]:
        st.markdown("---")
        eyebrow("📚 learning resources")
        for sk in gap["missing"]:
            res = LEARNING_RESOURCES.get(sk.lower())
            if res: st.markdown(f"**{sk.title()}** → {res}")

def require_profile():
    p = st.session_state.get("profile")
    if not p:
        st.warning("⚠️ Please complete **Input Profile** first (sidebar).")
        st.stop()
    return p

# ═══════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style="padding:16px 8px 8px">
      <div style="font-family:'Sora',sans-serif;font-size:1.1rem;font-weight:700;color:#E8EDF5">🔭 CareerLens AI</div>
      <div style="font-size:0.7rem;color:#7B8599;margin-top:2px">v2.0 · Groq AI · Free Forever</div>
    </div><hr style="border-color:#1E2433;margin:10px 0 14px">
    """, unsafe_allow_html=True)

    # ── API Key Box ─────────────────────────────────
    st.markdown("#### 🔑 Groq API Key")
    st.caption("Free at [console.groq.com](https://console.groq.com) — no credit card!")

    saved_key = st.session_state.get("groq_key","")
    user_key  = st.text_input(
        "Paste your key",
        value=saved_key,
        type="password",
        placeholder="gsk_...",
        label_visibility="collapsed",
    )

    col1,col2 = st.columns(2)
    with col1:
        if st.button("✅ Activate"):
            if user_key.strip():
                try:
                    from groq import Groq
                    test = Groq(api_key=user_key.strip())
                    test.chat.completions.create(
                        model="llama3-8b-8192",
                        messages=[{"role":"user","content":"hi"}],
                        max_tokens=5
                    )
                    st.session_state["groq_key"] = user_key.strip()
                    st.success("✅ Connected!")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ {e}")
            else:
                st.error("Paste your key first.")
    with col2:
        if st.button("🔄 Clear"):
            st.session_state.pop("groq_key", None)
            st.rerun()

    if st.session_state.get("groq_key"):
        st.success("✅ Groq AI Active — Free!")
    else:
        st.warning("⚠️ Key needed")

    st.markdown("<hr style='border-color:#1E2433;margin:14px 0'>", unsafe_allow_html=True)

    page = st.radio("nav", [
        "🏠  Home",
        "📋  Input Profile",
        "📄  Resume & Cover Letter",
        "🌐  Portfolio Builder",
        "📊  Skill Gap Analyzer",
        "🎤  Interview Prep",
        "💼  LinkedIn Bio",
        "🎯  JD Matcher",
        "🗺️  Learning Roadmap",
        "🏆  ATS Scorer",
    ], label_visibility="collapsed")

    st.markdown("""<hr style="border-color:#1E2433;margin:14px 0 10px">
    <div style="font-size:0.72rem;color:#7B8599;padding:0 8px">
    Streamlit + Groq (Llama 3)<br>100% Free · No billing ever
    </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════
# PAGE: HOME
# ═══════════════════════════════════════════════════
if page == "🏠  Home":
    hero()
    c1,c2,c3 = st.columns(3)
    with c1:
        card("📄","Resume Generator","ATS-optimised resume from your PDF or manual input in seconds.")
        card("🎤","Interview Prep","10 role-specific Q&As with STAR-method model answers.")
        card("🗺️","Learning Roadmap","12-week personalised study plan with daily tasks and resources.")
    with c2:
        card("✉️","Cover Letter","Tailored cover letter for any role and company.")
        card("💼","LinkedIn Bio","Full LinkedIn profile: headline, about, bullets and skills.")
        card("🏆","ATS Scorer","Score your resume against ATS. Find and fix critical gaps.")
    with c3:
        card("🌐","Portfolio Builder","5-section portfolio content ready to paste into any website.")
        card("🎯","JD Matcher","Paste a job posting — get match %, missing keywords and tailored summary.")
        card("📊","Skill Gap Analyzer","Match % vs your target role with curated learning resources.")
    st.markdown("---")
    st.markdown("### ⚡ Quick Start — 3 Steps")
    ca,cb,cc = st.columns(3)
    with ca: card("1️⃣","Get Free Groq Key","Go to console.groq.com → sign up → create API key. Takes 1 minute.")
    with cb: card("2️⃣","Activate in Sidebar","Paste your gsk_... key → click Activate.")
    with cc: card("3️⃣","Fill Profile & Go","Input Profile → fill details → use all 9 AI tools!")

# ═══════════════════════════════════════════════════
# PAGE: INPUT PROFILE
# ═══════════════════════════════════════════════════
elif page == "📋  Input Profile":
    hero()
    st.markdown("## 📋 Your Profile")
    profile = st.session_state.get("profile", {})
    mode = st.radio("Input method",["✍️ Fill manually","📎 Upload PDF"], horizontal=True)

    if mode == "📎 Upload PDF":
        if not PDF_SUPPORT:
            st.error("PyPDF2 not installed. Use manual input.")
        else:
            up = st.file_uploader("Upload Resume PDF", type=["pdf"])
            if up:
                with st.spinner("Reading PDF…"):
                    raw = extract_pdf_text(up)
                if raw:
                    found = detect_skills(raw)
                    st.success(f"✅ Extracted! Found {len(found)} skills.")
                    with st.expander("Preview extracted text"):
                        st.text(raw[:1000]+"…")
                    st.markdown("#### Confirm details")
                    n  = st.text_input("Full Name",  value=profile.get("name",""))
                    em = st.text_input("Email",       value=profile.get("email",""))
                    ph = st.text_input("Phone",       value=profile.get("phone",""))
                    ed = st.text_area("Education",    value=profile.get("education",""), height=80)
                    sk = st.text_input("Skills (pre-filled from PDF)",
                                        value=", ".join(found) or profile.get("skills_raw",""))
                    pr = st.text_area("Projects",     value=profile.get("projects",""), height=100)
                    ce = st.text_input("Certifications", value=profile.get("certifications",""))
                    ro = st.selectbox("Target Role", TARGET_ROLES)
                    co = st.text_input("Company (optional)", value=profile.get("company",""))
                    if st.button("💾 Save Profile"):
                        st.session_state["profile"] = {
                            "name":n,"email":em,"phone":ph,"education":ed,
                            "skills":[s.strip().lower() for s in sk.split(",") if s.strip()],
                            "skills_raw":sk,"projects":pr,"certifications":ce,
                            "role":ro,"company":co,"resume_text":raw
                        }
                        st.success("✅ Profile saved!")
                else:
                    st.error("Could not extract text — try manual input.")
    else:
        with st.form("mf"):
            st.markdown("#### Personal")
            a,b,c_ = st.columns(3)
            n  = a.text_input("Full Name *",  value=profile.get("name",""))
            em = b.text_input("Email *",       value=profile.get("email",""))
            ph = c_.text_input("Phone",        value=profile.get("phone",""))
            st.markdown("#### Academic & Skills")
            ed = st.text_area("Education *",
                placeholder="B.Tech CSE, XYZ University, 2025",
                value=profile.get("education",""), height=70)
            sk = st.text_input("Skills * (comma-separated)",
                placeholder="Python, Machine Learning, SQL, React",
                value=profile.get("skills_raw",""))
            pr = st.text_area("Projects *",
                placeholder="Project 1: Name - description, tech stack, outcome",
                value=profile.get("projects",""), height=120)
            ce = st.text_input("Certifications",
                placeholder="AWS Cloud Practitioner, Google Data Analytics",
                value=profile.get("certifications",""))
            st.markdown("#### Target")
            x,y = st.columns(2)
            ro = x.selectbox("Target Role *", TARGET_ROLES)
            co = y.text_input("Company Name (optional)", value=profile.get("company",""))
            sub = st.form_submit_button("💾 Save Profile")
        if sub:
            if not all([n,em,ed,sk,pr]):
                st.error("Fill all required (*) fields.")
            else:
                st.session_state["profile"] = {
                    "name":n,"email":em,"phone":ph,"education":ed,
                    "skills":[s.strip().lower() for s in sk.split(",") if s.strip()],
                    "skills_raw":sk,"projects":pr,"certifications":ce,
                    "role":ro,"company":co
                }
                st.success("✅ Profile saved! Use any tool from the sidebar.")

# ═══════════════════════════════════════════════════
# PAGE: RESUME & COVER LETTER
# ═══════════════════════════════════════════════════
elif page == "📄  Resume & Cover Letter":
    hero()
    p = require_profile()
    st.markdown(f"## 📄 Resume & Cover Letter — *{p['name']}*")
    t1,t2 = st.tabs(["📄 Resume","✉️ Cover Letter"])
    with t1:
        if st.button("⚡ Generate Resume"):
            with st.spinner("Writing your resume…"):
                st.session_state["resume"] = gen_resume(p)
        if "resume" in st.session_state:
            output_card(st.session_state["resume"])
            st.download_button("⬇️ Download (.txt)", st.session_state["resume"],
                file_name=f"{p['name'].replace(' ','_')}_resume.txt", mime="text/plain")
    with t2:
        if st.button("⚡ Generate Cover Letter"):
            with st.spinner("Writing your cover letter…"):
                st.session_state["cover"] = gen_cover(p)
        if "cover" in st.session_state:
            output_card(st.session_state["cover"])
            st.download_button("⬇️ Download (.txt)", st.session_state["cover"],
                file_name=f"{p['name'].replace(' ','_')}_cover_letter.txt", mime="text/plain")

# ═══════════════════════════════════════════════════
# PAGE: PORTFOLIO
# ═══════════════════════════════════════════════════
elif page == "🌐  Portfolio Builder":
    hero()
    p = require_profile()
    st.markdown(f"## 🌐 Portfolio Builder — *{p['name']}*")
    if st.button("⚡ Generate Portfolio Content"):
        with st.spinner("Building your portfolio…"):
            st.session_state["portfolio"] = gen_portfolio(p)
    if "portfolio" in st.session_state:
        output_card(st.session_state["portfolio"])
        st.download_button("⬇️ Download (.txt)", st.session_state["portfolio"],
            file_name=f"{p['name'].replace(' ','_')}_portfolio.txt", mime="text/plain")

# ═══════════════════════════════════════════════════
# PAGE: SKILL GAP
# ═══════════════════════════════════════════════════
elif page == "📊  Skill Gap Analyzer":
    hero()
    p = require_profile()
    st.markdown(f"## 📊 Skill Gap Analyzer — *{p['role']}*")
    gap = compute_gap(p.get("skills",[]), p.get("role",""))
    skill_gap_ui(gap, p["role"])
    st.markdown("---")
    st.markdown("### Compare vs a different role")
    alt = st.selectbox("Role", TARGET_ROLES, key="alt")
    if alt != p["role"]:
        skill_gap_ui(compute_gap(p.get("skills",[]), alt), alt)
    st.markdown("---")
    st.markdown("### 📈 All Roles Comparison")
    rows = []
    for r in TARGET_ROLES:
        g = compute_gap(p.get("skills",[]), r)
        rows.append({"Role":r,"Match %":g["percentage"],
                     "Matched":len(g["matched"]),"Missing":len(g["missing"])})
    df = pd.DataFrame(rows).sort_values("Match %", ascending=False)
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.success(f"🏆 Strongest fit: **{df.iloc[0]['Role']}**")

# ═══════════════════════════════════════════════════
# PAGE: INTERVIEW PREP
# ═══════════════════════════════════════════════════
elif page == "🎤  Interview Prep":
    hero()
    p = require_profile()
    st.markdown(f"## 🎤 Interview Q&A — *{p['role']}*")
    st.info("10 role-specific questions with detailed STAR-method answers.")
    col1,col2 = st.columns([2,1])
    with col1:
        extra = st.text_input("Specific topic? (optional)", placeholder="e.g. pandas, system design")
    with col2:
        difficulty = st.selectbox("Difficulty",["Fresher / Entry Level","Mid Level","Senior"])
    if st.button("⚡ Generate Interview Q&A"):
        with st.spinner("Preparing questions…"):
            st.session_state["interview"] = gen_interview_qa(p, extra, difficulty)
    if "interview" in st.session_state:
        output_card(st.session_state["interview"])
        st.download_button("⬇️ Download (.txt)", st.session_state["interview"],
            file_name=f"{p['name'].replace(' ','_')}_interview_qa.txt", mime="text/plain")

# ═══════════════════════════════════════════════════
# PAGE: LINKEDIN BIO
# ═══════════════════════════════════════════════════
elif page == "💼  LinkedIn Bio":
    hero()
    p = require_profile()
    st.markdown(f"## 💼 LinkedIn Profile — *{p['name']}*")
    st.info("Complete LinkedIn profile: headline, about, bullets, skills and tagline.")
    tone = st.radio("Tone",["Professional & Formal","Friendly & Conversational","Bold & Ambitious"],horizontal=True)
    if st.button("⚡ Generate LinkedIn Profile"):
        with st.spinner("Crafting your LinkedIn presence…"):
            st.session_state["linkedin"] = gen_linkedin(p, tone)
    if "linkedin" in st.session_state:
        output_card(st.session_state["linkedin"])
        st.download_button("⬇️ Download (.txt)", st.session_state["linkedin"],
            file_name=f"{p['name'].replace(' ','_')}_linkedin.txt", mime="text/plain")

# ═══════════════════════════════════════════════════
# PAGE: JD MATCHER
# ═══════════════════════════════════════════════════
elif page == "🎯  JD Matcher":
    hero()
    p = require_profile()
    st.markdown(f"## 🎯 Job Description Matcher — *{p['name']}*")
    st.info("Paste any job description — get match score, missing keywords and tailored summary.")
    jd = st.text_area("Paste Job Description", height=250,
        placeholder="Copy from LinkedIn, Naukri, Indeed, etc.")
    if st.button("⚡ Analyse JD"):
        if not jd.strip():
            st.error("Please paste a job description first.")
        else:
            with st.spinner("Analysing match…"):
                st.session_state["jd_result"] = gen_jd_match(p, jd)
    if "jd_result" in st.session_state:
        output_card(st.session_state["jd_result"])
        st.download_button("⬇️ Download (.txt)", st.session_state["jd_result"],
            file_name=f"{p['name'].replace(' ','_')}_jd_match.txt", mime="text/plain")

# ═══════════════════════════════════════════════════
# PAGE: LEARNING ROADMAP
# ═══════════════════════════════════════════════════
elif page == "🗺️  Learning Roadmap":
    hero()
    p = require_profile()
    st.markdown(f"## 🗺️ 12-Week Roadmap — *{p['role']}*")
    gap = compute_gap(p.get("skills",[]), p.get("role",""))
    if gap["missing"]:
        st.markdown("**Gaps to cover:**")
        tags_html(gap["missing"],"red")
    else:
        st.success("All core skills present! Roadmap covers advanced topics.")
    hours = st.slider("Daily study hours", 1, 6, 2)
    if st.button("⚡ Generate Roadmap"):
        with st.spinner("Building your 12-week plan…"):
            st.session_state["roadmap"] = gen_roadmap(p, hours)
    if "roadmap" in st.session_state:
        output_card(st.session_state["roadmap"])
        st.markdown("---")
        eyebrow("📚 resources")
        for sk in gap["missing"]:
            res = LEARNING_RESOURCES.get(sk.lower())
            if res: st.markdown(f"**{sk.title()}** → {res}")
        st.download_button("⬇️ Download (.txt)", st.session_state["roadmap"],
            file_name=f"{p['name'].replace(' ','_')}_roadmap.txt", mime="text/plain")

# ═══════════════════════════════════════════════════
# PAGE: ATS SCORER
# ═══════════════════════════════════════════════════
elif page == "🏆  ATS Scorer":
    hero()
    p = require_profile()
    st.markdown(f"## 🏆 ATS Resume Scorer — *{p['role']}*")
    st.info("Score your resume out of 100. Find and fix issues before recruiters see it.")
    ats_mode = st.radio("Score based on",["My saved profile","Paste resume text"],horizontal=True)
    resume_text = ""
    if ats_mode == "Paste resume text":
        resume_text = st.text_area("Paste resume here", height=250)
    if st.button("⚡ Score My Resume"):
        with st.spinner("Running ATS analysis…"):
            st.session_state["ats"] = gen_ats_score(p, resume_text)
    if "ats" in st.session_state:
        raw = st.session_state["ats"]
        m   = re.search(r"OVERALL ATS SCORE[:\s]+(\d+)", raw)
        if m:
            sc    = int(m.group(1))
            color = "green" if sc>=75 else "amber" if sc>=50 else "red"
            st.markdown(f"""<div class="metric-row"><div class="metric-box">
              <div class="metric-val score-{color}">{sc}</div>
              <div class="metric-lbl">ATS Score / 100</div>
            </div></div>""", unsafe_allow_html=True)
            st.progress(sc/100)
        output_card(raw)
        st.download_button("⬇️ Download (.txt)", raw,
            file_name=f"{p['name'].replace(' ','_')}_ats_report.txt", mime="text/plain")
