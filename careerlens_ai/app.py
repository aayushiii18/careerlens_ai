"""
CareerLens AI - AI-Powered Resume, Portfolio & Skill Gap Analyzer
"""

import streamlit as st
import pandas as pd

# ── PyPDF2 (optional) ──────────────────────────────────────────────────────
try:
    import PyPDF2
    PDF_SUPPORT = True
except ImportError:
    PDF_SUPPORT = False

# ── Anthropic client ────────────────────────────────────────────────────────
try:
    import anthropic
    client = anthropic.Anthropic()
    AI_SUPPORT = True
except Exception:
    client = None
    AI_SUPPORT = False

# ═══════════════════════════════════════════════════
# PAGE CONFIG & CUSTOM CSS
# ═══════════════════════════════════════════════════

st.set_page_config(
    page_title="CareerLens AI",
    page_icon="🔭",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Serif+Display&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --bg:      #0D1117;
    --surface: #161B22;
    --border:  #21262D;
    --indigo:  #6366F1;
    --violet:  #8B5CF6;
    --emerald: #10B981;
    --rose:    #F43F5E;
    --text:    #E6EDF3;
    --muted:   #8B949E;
    --radius:  12px;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    color: var(--text);
}
.stApp { background: var(--bg); }

[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border);
}

.hero {
    background: linear-gradient(135deg, #1a1f35 0%, #0f1629 50%, #130f1e 100%);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 40px 48px;
    margin-bottom: 32px;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: "";
    position: absolute;
    inset: 0;
    background: radial-gradient(ellipse 60% 80% at 80% 50%, rgba(99,102,241,0.15) 0%, transparent 70%);
    pointer-events: none;
}
.hero-eyebrow {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    font-weight: 500;
    letter-spacing: 0.18em;
    color: var(--indigo);
    text-transform: uppercase;
    margin-bottom: 12px;
}
.hero-title {
    font-family: 'DM Serif Display', serif;
    font-size: clamp(2rem, 4vw, 3rem);
    font-weight: 400;
    line-height: 1.1;
    color: var(--text);
    margin: 0 0 12px;
}
.hero-title span { color: var(--indigo); }
.hero-sub {
    font-size: 1.05rem;
    color: var(--muted);
    max-width: 520px;
    line-height: 1.6;
}

.card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 28px 32px;
    margin-bottom: 20px;
}
.card-title {
    font-size: 1rem;
    font-weight: 600;
    color: var(--text);
    margin-bottom: 6px;
}
.card-body {
    font-size: 0.92rem;
    color: var(--muted);
    line-height: 1.7;
    white-space: pre-wrap;
}

.metric-row { display: flex; gap: 16px; flex-wrap: wrap; margin-bottom: 24px; }
.metric-pill {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 40px;
    padding: 10px 20px;
    display: flex;
    flex-direction: column;
    align-items: center;
    min-width: 120px;
}
.metric-pill-value {
    font-family: 'DM Serif Display', serif;
    font-size: 1.8rem;
    color: var(--indigo);
    line-height: 1;
}
.metric-pill-label {
    font-size: 0.72rem;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-top: 4px;
}

.tags { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 8px; }
.tag {
    font-size: 0.78rem;
    font-weight: 500;
    padding: 4px 12px;
    border-radius: 20px;
    border: 1px solid;
}
.tag-green  { background: rgba(16,185,129,0.12); color: #10B981; border-color: rgba(16,185,129,0.3); }
.tag-red    { background: rgba(244,63,94,0.12);  color: #F43F5E; border-color: rgba(244,63,94,0.3); }

.section-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 12px;
}

div[data-testid="stTextInput"] input,
div[data-testid="stTextArea"] textarea {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
}
.stButton > button {
    background: linear-gradient(135deg, #6366F1, #8B5CF6);
    color: white;
    border: none;
    border-radius: 8px;
    font-weight: 600;
    font-size: 0.9rem;
    padding: 0.55rem 1.4rem;
}
.stButton > button:hover { opacity: 0.88; border: none; }
div[data-testid="stProgress"] > div > div { background: #6366F1 !important; }
button[data-baseweb="tab"][aria-selected="true"] {
    color: #6366F1 !important;
    border-bottom-color: #6366F1 !important;
}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════
# CONSTANTS
# ═══════════════════════════════════════════════════

TARGET_ROLES = [
    "AI/ML Intern",
    "Web Developer",
    "Data Analyst",
    "IoT Developer",
    "Software Engineer",
]

KNOWN_SKILLS = [
    "python", "c++", "java", "sql", "machine learning", "deep learning",
    "nlp", "tensorflow", "pytorch", "html", "css", "javascript", "react",
    "node.js", "mongodb", "arduino", "iot", "cloud", "data analysis",
    "pandas", "numpy", "scikit-learn", "power bi",
]

ROLE_SKILLS = {
    "AI/ML Intern":      ["python", "machine learning", "numpy", "pandas", "sql", "scikit-learn", "data analysis"],
    "Web Developer":     ["html", "css", "javascript", "react", "node.js", "mongodb"],
    "Data Analyst":      ["python", "sql", "excel", "power bi", "pandas", "data visualization"],
    "IoT Developer":     ["arduino", "iot", "nodemcu", "sensors", "mqtt", "cloud", "python"],
    "Software Engineer": ["python", "java", "sql", "dsa", "oop", "git"],
}

# ═══════════════════════════════════════════════════
# MODULE 2: PDF EXTRACTION
# ═══════════════════════════════════════════════════

def extract_pdf_text(uploaded_file) -> str:
    """Extract raw text from an uploaded PDF file."""
    if not PDF_SUPPORT:
        return ""
    try:
        reader = PyPDF2.PdfReader(uploaded_file)
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    except Exception as e:
        st.warning(f"Could not read PDF: {e}")
        return ""

def detect_skills_from_text(text: str) -> list:
    """Return any known skills found in resume text."""
    lower = text.lower()
    return [s for s in KNOWN_SKILLS if s in lower]

# ═══════════════════════════════════════════════════
# MODULE 6: SKILL GAP ANALYZER
# ═══════════════════════════════════════════════════

def compute_skill_gap(user_skills: list, role: str) -> dict:
    """Compare user skills against target role required skills."""
    required   = ROLE_SKILLS.get(role, [])
    user_lower = [s.lower().strip() for s in user_skills if s.strip()]
    matched    = [s for s in required if s in user_lower]
    missing    = [s for s in required if s not in user_lower]
    pct        = round(len(matched) / len(required) * 100) if required else 0

    recs = []
    if missing:
        recs.append(f"📚 Learn missing skills: {', '.join(missing[:3])}" +
                    (" and more" if len(missing) > 3 else ""))
    recs.append("🛠️ Build 1–2 projects using the required tech stack")
    recs.append("🔑 Add role-specific keywords to your resume summary")
    if pct < 60:
        recs.append("🎓 Consider a short online course or certification in the domain")

    return {
        "required": required,
        "matched":  matched,
        "missing":  missing,
        "percentage": pct,
        "recommendations": recs,
    }

# ═══════════════════════════════════════════════════
# MODULE 3–5: AI CONTENT GENERATORS
# ═══════════════════════════════════════════════════

def call_claude(prompt: str, max_tokens: int = 1200) -> str:
    """Call Claude API and return response text."""
    if not AI_SUPPORT:
        return "⚠️ Anthropic client unavailable. Please check your API key."
    try:
        msg = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=max_tokens,
            messages=[{"role": "user", "content": prompt}],
        )
        return msg.content[0].text.strip()
    except Exception as e:
        return f"⚠️ AI error: {e}"

def build_profile_context(profile: dict) -> str:
    """Convert profile dict to a readable string for AI prompts."""
    return f"""
Name:           {profile.get('name', 'N/A')}
Email:          {profile.get('email', '')}
Phone:          {profile.get('phone', '')}
Education:      {profile.get('education', '')}
Skills:         {', '.join(profile.get('skills', []))}
Projects:       {profile.get('projects', '')}
Certifications: {profile.get('certifications', '')}
Target Role:    {profile.get('role', '')}
Company:        {profile.get('company', 'a leading company')}
""".strip()

def generate_resume(profile: dict) -> str:
    """Module 3: Generate a professional resume."""
    ctx = build_profile_context(profile)
    return call_claude(f"""
You are a professional resume writer.
Create a polished, ATS-friendly resume for the following candidate.
Use clear sections: Professional Summary | Skills | Projects | Education | Certifications.
Keep it concise and impactful. Plain text, no markdown symbols except dashes.

CANDIDATE PROFILE:
{ctx}
""", max_tokens=1400)

def generate_cover_letter(profile: dict) -> str:
    """Module 4: Generate a professional cover letter."""
    ctx = build_profile_context(profile)
    return call_claude(f"""
Write a compelling, personalised cover letter for:
Role:    {profile.get('role')}
Company: {profile.get('company', 'a leading company')}

CANDIDATE PROFILE:
{ctx}

Use a professional yet warm tone. Three paragraphs: hook, body, call-to-action.
No placeholders. Plain text only.
""", max_tokens=900)

def generate_portfolio(profile: dict) -> str:
    """Module 5: Generate portfolio website content."""
    ctx = build_profile_context(profile)
    return call_claude(f"""
Create portfolio website content for a student with this profile:
{ctx}

Output five clearly labelled sections:
ABOUT ME | SKILLS | PROJECTS | ACHIEVEMENTS | CONTACT

Each section should be professional, specific, and concise.
Plain text. No markdown symbols.
""", max_tokens=1100)

# ═══════════════════════════════════════════════════
# UI HELPER FUNCTIONS
# ═══════════════════════════════════════════════════

def render_hero():
    st.markdown("""
    <div class="hero">
        <div class="hero-eyebrow">🔭 v1.0 · Powered by Claude AI</div>
        <h1 class="hero-title">Career<span>Lens</span> AI</h1>
        <p class="hero-sub">AI-Powered Resume, Portfolio & Skill Gap Analyzer — built for students ready to stand out.</p>
    </div>
    """, unsafe_allow_html=True)

def render_card(icon: str, title: str, body: str):
    st.markdown(f"""
    <div class="card">
        <div class="card-title">{icon} {title}</div>
        <div class="card-body">{body}</div>
    </div>
    """, unsafe_allow_html=True)

def render_tags(items: list, style: str):
    tags_html = "".join(f'<span class="tag tag-{style}">{i}</span>' for i in items)
    st.markdown(f'<div class="tags">{tags_html}</div>', unsafe_allow_html=True)

def render_skill_gap(gap: dict, role: str):
    pct = gap["percentage"]

    # Metric pills row
    st.markdown(f"""
    <div class="metric-row">
        <div class="metric-pill">
            <span class="metric-pill-value">{pct}%</span>
            <span class="metric-pill-label">Match Score</span>
        </div>
        <div class="metric-pill">
            <span class="metric-pill-value">{len(gap['matched'])}</span>
            <span class="metric-pill-label">Skills Found</span>
        </div>
        <div class="metric-pill">
            <span class="metric-pill-value">{len(gap['missing'])}</span>
            <span class="metric-pill-label">Gaps</span>
        </div>
        <div class="metric-pill">
            <span class="metric-pill-value">{len(gap['required'])}</span>
            <span class="metric-pill-label">Required</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.progress(pct / 100)

    if pct >= 80:
        st.success(f"🎯 Strong match for **{role}**! You're well-prepared.")
    elif pct >= 50:
        st.warning(f"⚡ Moderate match for **{role}**. Closing a few gaps will make you competitive.")
    else:
        st.error(f"📈 Early stage for **{role}**. Focus on building foundational skills first.")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-label">✅ Skills You Have</div>', unsafe_allow_html=True)
        render_tags(gap["matched"] or ["—"], "green")
    with col2:
        st.markdown('<div class="section-label">❌ Skills to Learn</div>', unsafe_allow_html=True)
        render_tags(gap["missing"] or ["—"], "red")

    st.markdown('<div class="section-label" style="margin-top:20px">💡 Recommendations</div>',
                unsafe_allow_html=True)
    for rec in gap["recommendations"]:
        st.markdown(f"- {rec}")

# ═══════════════════════════════════════════════════
# SIDEBAR NAVIGATION
# ═══════════════════════════════════════════════════

with st.sidebar:
    st.markdown("### 🔭 CareerLens AI")
    st.markdown('<hr style="border-color:#21262D;margin:8px 0 16px">', unsafe_allow_html=True)
    page = st.radio(
        "Navigate",
        ["🏠 Home", "📋 Input Profile", "🤖 Generate Content", "📊 Skill Gap"],
        label_visibility="collapsed",
    )
    st.markdown('<hr style="border-color:#21262D;margin:16px 0 12px">', unsafe_allow_html=True)
    st.caption("Built with Streamlit · Claude AI")

# ═══════════════════════════════════════════════════
# PAGE: HOME
# ═══════════════════════════════════════════════════

if page == "🏠 Home":
    render_hero()

    c1, c2, c3 = st.columns(3)
    with c1:
        render_card("📄", "Resume Generator",
            "Upload your PDF or fill in details manually. Get a polished, ATS-ready resume in seconds.")
    with c2:
        render_card("✉️", "Cover Letter",
            "Auto-generates a tailored cover letter for your target role and company.")
    with c3:
        render_card("🌐", "Portfolio Builder",
            "Get ready-to-paste portfolio content across five professional sections.")

    c4, c5 = st.columns(2)
    with c4:
        render_card("🔍", "Skill Gap Analyzer",
            "See your match percentage for any role, identify gaps, and get personalised action steps.")
    with c5:
        render_card("⚡", "How it works",
            "1. Go to Input Profile\n2. Upload PDF or fill manually\n3. Click Generate Content\n4. Check Skill Gap tab")

# ═══════════════════════════════════════════════════
# PAGE: INPUT PROFILE  (Module 1 & 2)
# ═══════════════════════════════════════════════════

elif page == "📋 Input Profile":
    render_hero()
    st.markdown("## 📋 Your Profile")

    input_mode = st.radio(
        "How would you like to provide your information?",
        ["✍️ Fill manually", "📎 Upload Resume PDF"],
        horizontal=True,
    )

    profile = st.session_state.get("profile", {})

    # ── PDF Upload ──────────────────────────────────
    if input_mode == "📎 Upload Resume PDF":
        if not PDF_SUPPORT:
            st.error("PyPDF2 is not installed. Please use the manual input option.")
        else:
            uploaded = st.file_uploader("Upload your resume (PDF)", type=["pdf"])
            if uploaded:
                with st.spinner("Extracting text from PDF…"):
                    raw_text = extract_pdf_text(uploaded)

                if raw_text:
                    detected = detect_skills_from_text(raw_text)
                    st.success(f"✅ PDF parsed! Detected {len(detected)} skills.")
                    st.text_area("Extracted text (preview)", raw_text[:800] + "…", height=150)

                    st.markdown("#### Confirm / edit your details")
                    name  = st.text_input("Full Name",  value=profile.get("name", ""))
                    email = st.text_input("Email",       value=profile.get("email", ""))
                    phone = st.text_input("Phone",       value=profile.get("phone", ""))
                    edu   = st.text_area("Education",    value=profile.get("education", ""), height=80)
                    skills_str = st.text_input(
                        "Skills (pre-filled from PDF)",
                        value=", ".join(detected) if detected else profile.get("skills_raw", ""),
                    )
                    projects = st.text_area("Projects", value=profile.get("projects", ""), height=100)
                    certs    = st.text_input("Certifications", value=profile.get("certifications", ""))
                    role     = st.selectbox("Target Role", TARGET_ROLES)
                    company  = st.text_input("Company Name (optional)", value=profile.get("company", ""))

                    if st.button("💾 Save Profile"):
                        st.session_state["profile"] = {
                            "name": name, "email": email, "phone": phone,
                            "education": edu,
                            "skills": [s.strip().lower() for s in skills_str.split(",") if s.strip()],
                            "skills_raw": skills_str,
                            "projects": projects, "certifications": certs,
                            "role": role, "company": company,
                            "resume_text": raw_text,
                        }
                        st.success("✅ Profile saved! Head to Generate Content.")
                else:
                    st.error("Could not extract text. Try the manual option.")

    # ── Manual Input ────────────────────────────────
    else:
        with st.form("manual_form"):
            st.markdown("#### Personal Information")
            col1, col2, col3 = st.columns(3)
            name  = col1.text_input("Full Name *",  value=profile.get("name", ""))
            email = col2.text_input("Email *",       value=profile.get("email", ""))
            phone = col3.text_input("Phone",         value=profile.get("phone", ""))

            st.markdown("#### Academic & Professional Details")
            edu = st.text_area("Education *",
                placeholder="e.g. B.Tech CSE, XYZ University, 2025",
                value=profile.get("education", ""), height=80)
            skills_str = st.text_input(
                "Skills * (comma-separated)",
                placeholder="e.g. Python, Machine Learning, SQL, Pandas",
                value=profile.get("skills_raw", ""),
            )
            projects = st.text_area(
                "Projects *",
                placeholder="Describe 2–3 projects with tech stack and impact.",
                value=profile.get("projects", ""), height=120,
            )
            certs = st.text_input(
                "Certifications",
                placeholder="e.g. AWS Cloud Practitioner, Google Data Analytics",
                value=profile.get("certifications", ""),
            )

            st.markdown("#### Target Role")
            col4, col5 = st.columns(2)
            role    = col4.selectbox("Target Role *", TARGET_ROLES)
            company = col5.text_input("Company Name (optional)", value=profile.get("company", ""))

            submitted = st.form_submit_button("💾 Save Profile")

        if submitted:
            if not all([name, email, edu, skills_str, projects]):
                st.error("Please fill in all required fields (marked *).")
            else:
                st.session_state["profile"] = {
                    "name": name, "email": email, "phone": phone,
                    "education": edu,
                    "skills": [s.strip().lower() for s in skills_str.split(",") if s.strip()],
                    "skills_raw": skills_str,
                    "projects": projects, "certifications": certs,
                    "role": role, "company": company,
                }
                st.success("✅ Profile saved! Head to Generate Content.")

# ═══════════════════════════════════════════════════
# PAGE: GENERATE CONTENT  (Module 3, 4, 5 + Dashboard)
# ═══════════════════════════════════════════════════

elif page == "🤖 Generate Content":
    render_hero()
    st.markdown("## 🤖 AI Content Generator")

    profile = st.session_state.get("profile")
    if not profile:
        st.warning("⚠️ No profile found. Please complete Input Profile first.")
        st.stop()

    st.info(f"Generating content for **{profile['name']}** → *{profile['role']}*")

    tab1, tab2, tab3 = st.tabs(["📄 Resume", "✉️ Cover Letter", "🌐 Portfolio"])

    with tab1:
        if st.button("⚡ Generate Resume", key="gen_resume"):
            with st.spinner("Crafting your resume…"):
                result = generate_resume(profile)
                st.session_state["resume"] = result
        if "resume" in st.session_state:
            render_card("📄", "Your AI-Generated Resume", st.session_state["resume"])
            st.download_button(
                "⬇️ Download Resume (.txt)",
                st.session_state["resume"],
                file_name=f"{profile['name'].replace(' ','_')}_resume.txt",
                mime="text/plain",
            )

    with tab2:
        if st.button("⚡ Generate Cover Letter", key="gen_cl"):
            with st.spinner("Writing your cover letter…"):
                result = generate_cover_letter(profile)
                st.session_state["cover_letter"] = result
        if "cover_letter" in st.session_state:
            render_card("✉️", "Your Cover Letter", st.session_state["cover_letter"])
            st.download_button(
                "⬇️ Download Cover Letter (.txt)",
                st.session_state["cover_letter"],
                file_name=f"{profile['name'].replace(' ','_')}_cover_letter.txt",
                mime="text/plain",
            )

    with tab3:
        if st.button("⚡ Generate Portfolio Content", key="gen_port"):
            with st.spinner("Building your portfolio…"):
                result = generate_portfolio(profile)
                st.session_state["portfolio"] = result
        if "portfolio" in st.session_state:
            render_card("🌐", "Your Portfolio Content", st.session_state["portfolio"])
            st.download_button(
                "⬇️ Download Portfolio (.txt)",
                st.session_state["portfolio"],
                file_name=f"{profile['name'].replace(' ','_')}_portfolio.txt",
                mime="text/plain",
            )

# ═══════════════════════════════════════════════════
# PAGE: SKILL GAP  (Module 6 & 7)
# ═══════════════════════════════════════════════════

elif page == "📊 Skill Gap":
    render_hero()
    st.markdown("## 📊 Skill Gap Analyzer")

    profile = st.session_state.get("profile")
    if not profile:
        st.warning("⚠️ No profile found. Please complete Input Profile first.")
        st.stop()

    role   = profile.get("role", TARGET_ROLES[0])
    skills = profile.get("skills", [])

    st.markdown(f"**Target Role:** `{role}` · **Your Skills:** {len(skills)} detected")

    # Primary role analysis
    gap = compute_skill_gap(skills, role)
    render_skill_gap(gap, role)

    # Compare a different role
    st.markdown("---")
    st.markdown("### Compare against a different role")
    alt_role = st.selectbox("Select role to compare", TARGET_ROLES, key="alt_role")
    if alt_role != role:
        alt_gap = compute_skill_gap(skills, alt_role)
        st.markdown(f"#### Results for **{alt_role}**")
        render_skill_gap(alt_gap, alt_role)

    # Cross-role comparison table
    st.markdown("---")
    st.markdown("### 📈 Across-Role Comparison")
    rows = []
    for r in TARGET_ROLES:
        g = compute_skill_gap(skills, r)
        rows.append({
            "Role": r,
            "Match %": g["percentage"],
            "Matched": len(g["matched"]),
            "Missing": len(g["missing"])
        })
    df = pd.DataFrame(rows).sort_values("Match %", ascending=False)
    st.dataframe(df, use_container_width=True, hide_index=True)

    best = df.iloc[0]["Role"]
    st.success(f"🏆 You're the strongest fit for **{best}** based on your current skills.")