import streamlit as st
import os, sys, json, time
sys.path.insert(0, "/Users/KRISH/Desktop/AI_Study_Squad")
from app import ask_agent, save_log

st.set_page_config(page_title="AI Study Squad", page_icon="🧠", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

* { font-family: 'Inter', sans-serif; }
#MainMenu {visibility:hidden;} footer {visibility:hidden;} header {visibility:hidden;}

.stApp { background: linear-gradient(135deg, #0a0a1a, #0f0c29, #1a1040); }

::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: rgba(255,255,255,0.02); }
::-webkit-scrollbar-thumb { background: rgba(167,139,250,0.3); border-radius: 3px; }

.hero { text-align:center; padding:2.5rem 0 0.5rem 0; }
.hero h1 {
    font-size:3.5rem; font-weight:900;
    background:linear-gradient(90deg,#a78bfa,#60a5fa,#34d399,#a78bfa);
    background-size: 200%;
    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
    animation: shimmer 3s linear infinite;
    margin-bottom: 0.2rem;
}
@keyframes shimmer { 0%{background-position:0%} 100%{background-position:200%} }
.hero p { color:#64748b; font-size:1.05rem; margin-bottom: 0; }

.stats-bar { display:flex; gap:0.8rem; justify-content:center; margin: 1.2rem 0; flex-wrap: wrap; }
.stat-pill {
    background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.08);
    border-radius:30px; padding:0.35rem 1.1rem;
    color:#94a3b8; font-size:0.78rem; font-weight:500;
    backdrop-filter: blur(10px); transition: all 0.2s;
}
.stat-pill:hover { border-color:rgba(167,139,250,0.3); color:#a78bfa; }

.user-msg {
    background: linear-gradient(135deg, rgba(99,102,241,0.15), rgba(139,92,246,0.1));
    border-radius:14px; padding:1rem 1.2rem; margin:1rem 0; color:#e2e8f0;
    border-left:3px solid #a78bfa; font-size:0.95rem;
}

.agent-card {
    border-radius:20px; padding:1.4rem 1.5rem; min-height:280px;
    border:1px solid rgba(255,255,255,0.06); margin-top:0.5rem;
    position: relative; overflow: hidden; transition: transform 0.2s, border-color 0.2s;
}
.agent-card:hover { transform: translateY(-2px); }
.agent-card::before { content:''; position:absolute; top:0; left:0; right:0; height:2px; border-radius:20px 20px 0 0; }
.nerd-card { background: linear-gradient(145deg, rgba(99,102,241,0.12), rgba(67,56,202,0.06)); border-color: rgba(99,102,241,0.25); }
.nerd-card::before { background: linear-gradient(90deg, #6366f1, #a78bfa); }
.simplifier-card { background: linear-gradient(145deg, rgba(16,185,129,0.12), rgba(5,150,105,0.06)); border-color: rgba(16,185,129,0.25); }
.simplifier-card::before { background: linear-gradient(90deg, #10b981, #34d399); }
.challenger-card { background: linear-gradient(145deg, rgba(239,68,68,0.12), rgba(185,28,28,0.06)); border-color: rgba(239,68,68,0.25); }
.challenger-card::before { background: linear-gradient(90deg, #ef4444, #f87171); }

.agent-header { display:flex; align-items:center; gap:10px; margin-bottom:1rem; padding-bottom:0.8rem; border-bottom:1px solid rgba(255,255,255,0.06); }
.agent-emoji { font-size:1.5rem; }
.agent-name { font-weight:700; font-size:0.95rem; letter-spacing:0.03em; }
.nerd-name { color:#a78bfa; }
.simplifier-name { color:#34d399; }
.challenger-name { color:#f87171; }
.agent-role { font-size:0.68rem; color:#475569; margin-left:auto; background: rgba(255,255,255,0.04); padding: 0.2rem 0.6rem; border-radius: 10px; border: 1px solid rgba(255,255,255,0.06); }
.agent-response { color:#cbd5e1; font-size:0.88rem; line-height:1.75; }
.thinking-text { color:#475569; font-style:italic; padding:1rem 0; font-size:0.85rem; }

.custom-divider { border: none; border-top: 1px solid rgba(255,255,255,0.06); margin: 1.5rem 0; }

.metric-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.07); border-radius: 14px; padding: 1rem 1.2rem; text-align: center; }
.metric-value { font-size:2rem; font-weight:800; color:#a78bfa; }
.metric-label { font-size:0.75rem; color:#64748b; margin-top:0.2rem; }

section[data-testid="stSidebar"] { background: linear-gradient(180deg, #0d0b1e, #0f0c29) !important; border-right: 1px solid rgba(255,255,255,0.06) !important; }
section[data-testid="stSidebar"] * { color: #94a3b8 !important; }
section[data-testid="stSidebar"] strong { color: #e2e8f0 !important; }
section[data-testid="stSidebar"] h2, section[data-testid="stSidebar"] h3 { color: #e2e8f0 !important; }

.stChatInput textarea { background: #ffffff !important; border: 2px solid rgba(167,139,250,0.5) !important; border-radius: 14px !important; color: #0a0a1a !important; font-size: 0.95rem !important; font-weight: 500 !important; }
.stChatInput textarea:focus { border-color: #a78bfa !important; box-shadow: 0 0 0 3px rgba(167,139,250,0.2) !important; }
.stChatInput textarea::placeholder { color: #94a3b8 !important; }
.stChatInput button { background: linear-gradient(135deg, #a78bfa, #60a5fa) !important; border-radius: 10px !important; border: none !important; }
.stChatInput button:hover { background: linear-gradient(135deg, #7c3aed, #3b82f6) !important; transform: scale(1.05) !important; }
.stChatInput button svg { fill: white !important; }
.stChatInputContainer { background: linear-gradient(180deg, transparent, rgba(10,10,26,0.95)) !important; padding: 1rem !important; backdrop-filter: blur(10px) !important; }

/* Conversation History expander - Purple */
div[data-testid="stExpander"]:has(summary p:contains("Conversation")) {
    background: rgba(99,102,241,0.06) !important;
    border: 1.5px solid rgba(167,139,250,0.4) !important;
    border-radius: 16px !important;
    margin-bottom: 1rem !important;
}

/* All expanders base style */
div[data-testid="stExpander"] {
    border-radius: 16px !important;
    margin-bottom: 1rem !important;
    overflow: hidden !important;
    border: 1.5px solid rgba(255,255,255,0.08) !important;
    background: rgba(255,255,255,0.02) !important;
}
div[data-testid="stExpander"]:hover {
    border-color: rgba(167,139,250,0.3) !important;
}

/* History expander - Purple theme */
div[data-testid="stExpander"]:nth-of-type(1) {
    border-color: rgba(167,139,250,0.35) !important;
    background: linear-gradient(135deg, rgba(99,102,241,0.08), rgba(139,92,246,0.04)) !important;
}
div[data-testid="stExpander"]:nth-of-type(1) summary {
    background: linear-gradient(135deg, rgba(99,102,241,0.15), rgba(139,92,246,0.08)) !important;
    padding: 0.9rem 1.2rem !important;
}
div[data-testid="stExpander"]:nth-of-type(1) summary p {
    color: #a78bfa !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
}
div[data-testid="stExpander"]:nth-of-type(1):hover {
    border-color: rgba(167,139,250,0.6) !important;
    box-shadow: 0 0 20px rgba(167,139,250,0.1) !important;
}

/* Analytics expander - Green theme */
div[data-testid="stExpander"]:nth-of-type(2) {
    border-color: rgba(52,211,153,0.35) !important;
    background: linear-gradient(135deg, rgba(16,185,129,0.08), rgba(5,150,105,0.04)) !important;
}
div[data-testid="stExpander"]:nth-of-type(2) summary {
    background: linear-gradient(135deg, rgba(16,185,129,0.15), rgba(5,150,105,0.08)) !important;
    padding: 0.9rem 1.2rem !important;
}
div[data-testid="stExpander"]:nth-of-type(2) summary p {
    color: #34d399 !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
}
div[data-testid="stExpander"]:nth-of-type(2):hover {
    border-color: rgba(52,211,153,0.6) !important;
    box-shadow: 0 0 20px rgba(52,211,153,0.1) !important;
}
</style>
""", unsafe_allow_html=True)

# --- Session state ---
if "question_count" not in st.session_state:
    st.session_state.question_count = 0
if "history" not in st.session_state:
    st.session_state.history = []
if "pdf_loaded" not in st.session_state:
    st.session_state.pdf_loaded = False

# =================== SIDEBAR ===================
with st.sidebar:
    st.markdown("## 🧠 Study Squad")
    st.markdown("---")
    st.markdown("### 📚 Textbook Memory")
    st.caption("Upload your PDF so agents answer from your actual textbook.")
    pdf_file = st.file_uploader("Choose PDF", type=["pdf"], label_visibility="collapsed")
    if pdf_file:
        if st.button("📥 Load into Memory", use_container_width=True):
            import tempfile
            from rag import load_pdf
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(pdf_file.read())
                tmp_path = tmp.name
            with st.spinner("📖 Indexing PDF..."):
                count = load_pdf(tmp_path)
            st.success(f"✅ {count} chunks loaded!")
            st.session_state.pdf_loaded = True

    if st.session_state.pdf_loaded:
        st.markdown("🟢 **Textbook active**")
    else:
        st.markdown("🔴 **No textbook loaded**")

    st.markdown("---")
    st.markdown("### 👥 Your Squad")
    st.markdown("🎓 **Nerd** — Technical Expert")
    st.markdown("😊 **Simplifier** — Fun Explainer")
    st.markdown("🤔 **Challenger** — Critical Thinker")
    st.markdown("---")
    st.markdown("### 📊 Your Stats")
    st.markdown(f"**{st.session_state.question_count}** questions asked")
    st.markdown(f"**{len(st.session_state.history)}** sessions saved")
    if st.session_state.pdf_loaded:
        st.markdown("**PDF** memory active ✅")
    st.markdown("---")
    st.caption("Built with Llama 3.3 + Groq")
    st.caption("AI Study Squad v2.0 — 2026")

# =================== MAIN ===================
st.markdown("""
<div class="hero">
    <h1>🧠 AI Study Squad</h1>
    <p>Three AI minds. One question. Infinite understanding.</p>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="stats-bar">
    <span class="stat-pill">📚 {st.session_state.question_count} questions</span>
    <span class="stat-pill">🤖 3 agents active</span>
    <span class="stat-pill">⚡ Llama 3.3 powered</span>
    <span class="stat-pill">{'📖 PDF loaded' if st.session_state.pdf_loaded else '💡 General knowledge'}</span>
</div>
""", unsafe_allow_html=True)

AGENTS = {
    "Nerd": {
        "card": "nerd-card", "name_class": "nerd-name",
        "emoji": "🎓", "role": "Technical Expert",
        "instruction": "You are The Nerd from AI Study Squad. Use formal technical language, precise definitions and formulas. Be thorough and accurate. Structure your answer clearly."
    },
    "Simplifier": {
        "card": "simplifier-card", "name_class": "simplifier-name",
        "emoji": "😊", "role": "Fun Explainer",
        "instruction": "You are The Simplifier from AI Study Squad. Use fun analogies, emojis and simple everyday words. Make learning feel like talking to a friend. Keep it short and memorable."
    },
    "Challenger": {
        "card": "challenger-card", "name_class": "challenger-name",
        "emoji": "🤔", "role": "Critical Thinker",
        "instruction": "You are The Challenger from AI Study Squad. Push the student to think deeper. Ask 1-2 hard follow-up questions starting with: Wait, are you sure... or But what happens when..."
    }
}

prompt = st.chat_input("Ask your Study Squad anything about Data Mining, ML, or AI...")

if prompt:
    st.session_state.question_count += 1
    st.markdown(f'<div class="user-msg">🧑‍🎓 <strong>You asked:</strong> {prompt}</div>', unsafe_allow_html=True)

    if st.session_state.pdf_loaded:
        try:
            from rag import search_context
            context = search_context(prompt)
            final_prompt = f"Context from textbook:\n{context}\n\nQuestion: {prompt}" if context else prompt
        except:
            final_prompt = prompt
    else:
        final_prompt = prompt

    col1, col2, col3 = st.columns(3)
    cols = {"Nerd": col1, "Simplifier": col2, "Challenger": col3}
    placeholders = {}

    for name, col in cols.items():
        d = AGENTS[name]
        with col:
            placeholders[name] = st.empty()
            placeholders[name].markdown(f"""
            <div class="agent-card {d['card']}">
                <div class="agent-header">
                    <span class="agent-emoji">{d['emoji']}</span>
                    <span class="agent-name {d['name_class']}">{name}</span>
                    <span class="agent-role">{d['role']}</span>
                </div>
                <div class="thinking-text">⏳ Consulting knowledge base...</div>
            </div>""", unsafe_allow_html=True)

    collected = {}
    for name, col in cols.items():
        d = AGENTS[name]
        result = ask_agent(name, d["instruction"], final_prompt)
        collected[name] = result
        placeholders[name].markdown(f"""
        <div class="agent-card {d['card']}">
            <div class="agent-header">
                <span class="agent-emoji">{d['emoji']}</span>
                <span class="agent-name {d['name_class']}">{name}</span>
                <span class="agent-role">{d['role']}</span>
            </div>
            <div class="agent-response">{result}</div>
        </div>""", unsafe_allow_html=True)
        time.sleep(0.3)

    save_log(prompt, collected)
    st.session_state.history.append({"query": prompt, "responses": collected})

st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)

if st.session_state.history:
    with st.expander("📜 Conversation History", expanded=False):
        for i, item in enumerate(reversed(st.session_state.history)):
            st.markdown(f"**Q{len(st.session_state.history)-i}:** {item['query']}")
            c1, c2, c3 = st.columns(3)
            for col, name in zip([c1, c2, c3], ["Nerd", "Simplifier", "Challenger"]):
                with col:
                    d = AGENTS[name]
                    resp = item["responses"].get(name, "")
                    st.markdown(f"**{d['emoji']} {name}**")
                    st.caption(resp[:300] + "..." if len(resp) > 300 else resp)
            st.divider()

with st.expander("📊 Study Analytics", expanded=False):
    from analysis import run_analysis
    data = run_analysis()
    if data:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f'<div class="metric-card"><div class="metric-value">{data["total"]}</div><div class="metric-label">Questions Asked</div></div>', unsafe_allow_html=True)
        with col2:
            most_used = max(data["agent_counts"], key=data["agent_counts"].get) if data["agent_counts"] else "N/A"
            st.markdown(f'<div class="metric-card"><div class="metric-value">{most_used}</div><div class="metric-label">Favourite Agent</div></div>', unsafe_allow_html=True)
        with col3:
            st.markdown(f'<div class="metric-card"><div class="metric-value">{len(data["top_topics"])}</div><div class="metric-label">Topics Mined</div></div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("**🔥 Top topics you studied:**")
        for word, count in data["top_topics"]:
            st.progress(min(count/10, 1.0), text=f"{word} — {count} mentions")
        st.markdown("**🤖 Agent usage:**")
        for agent, count in data["agent_counts"].items():
            d = AGENTS.get(agent, {})
            st.markdown(f"{d.get('emoji','🤖')} **{agent}**: {count} responses")
        st.markdown("**🕐 Recent questions:**")
        for q in data["recent"]:
            st.caption(f"→ {q}")
    else:
        st.info("💡 Ask some questions first to see your learning analytics!")
