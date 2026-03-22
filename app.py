import streamlit as st
import requests
import re

WEBHOOK_URL = "your-n8n-webhook-url-here"

st.set_page_config(page_title="Job Application Assistant", page_icon="💼", layout="centered")

# Custom CSS
st.markdown("""
    <style>
    .main { background-color: #0f1117; }
    .title { text-align: center; font-size: 2.5em; font-weight: bold; color: #ffffff; margin-bottom: 5px; }
    .subtitle { text-align: center; color: #888; margin-bottom: 30px; font-size: 1em; }
    .score-box { background: linear-gradient(135deg, #1a1a2e, #16213e);
        border: 2px solid #4CAF50; border-radius: 15px; padding: 25px;
        text-align: center; margin-bottom: 20px; }
    .score-number { font-size: 3em; font-weight: bold; color: #4CAF50; }
    .score-label { color: #aaa; font-size: 1em; margin-top: 5px; }
    .section-box { background: #1e1e2e; border-radius: 15px; padding: 20px;
        margin-bottom: 20px; border: 1px solid #333; }
    .section-title { font-size: 1.2em; font-weight: bold; margin-bottom: 10px; }
    .skill-tag { display: inline-block; background: #2d2d3f; color: #ff6b6b;
        border: 1px solid #ff6b6b; border-radius: 20px; padding: 4px 12px;
        margin: 4px; font-size: 0.85em; }
    .cover-letter { color: #ccc; line-height: 1.8; white-space: pre-wrap; font-size: 0.95em; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">💼 Job Application Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Paste a job description to analyze it against Nafay\'s CV</div>', unsafe_allow_html=True)

job_description = st.text_area("Job Description", height=220,
                                placeholder="Paste the job description here...")

if st.button("🔍 Analyze", use_container_width=True):
    if job_description.strip() == "":
        st.warning("Please paste a job description first!")
    else:
        with st.spinner("Analyzing your CV against the job description..."):
            try:
                response = requests.post(WEBHOOK_URL, json={"jobDescription": job_description})
                result = response.text

                # Parse Match Score
                score_match = re.search(r'Match Score[:\s]+(\d+)%', result)
                score = int(score_match.group(1)) if score_match else None

                # Parse Missing Skills
                skills_match = re.search(r'Missing Skills[:\s]*(.*?)(?=Cover Letter|$)', result, re.DOTALL)
                skills_text = skills_match.group(1).strip() if skills_match else ""
                skills = [s.strip().lstrip('-*•').strip() for s in skills_text.split('\n') if s.strip() and s.strip() not in ['-', '*', '•']]

                # Parse Cover Letter
                cover_match = re.search(r'Cover Letter[:\s]*(.*)', result, re.DOTALL)
                cover_letter = cover_match.group(1).strip() if cover_match else ""

                st.success("Analysis Complete!")
                st.markdown("---")

                # Score Box
                if score is not None:
                    color = "#4CAF50" if score >= 70 else "#FFA500" if score >= 40 else "#ff6b6b"
                    st.markdown(f"""
                        <div class="score-box" style="border-color: {color}">
                            <div class="score-number" style="color: {color}">{score}%</div>
                            <div class="score-label">Match Score</div>
                        </div>
                    """, unsafe_allow_html=True)

                # Missing Skills
                if skills:
                    st.markdown('<div class="section-box">', unsafe_allow_html=True)
                    st.markdown('<div class="section-title">❌ Missing Skills</div>', unsafe_allow_html=True)
                    tags = "".join([f'<span class="skill-tag">{s}</span>' for s in skills if s])
                    st.markdown(tags, unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)

                # Cover Letter
                if cover_letter:
                    st.markdown('<div class="section-box">', unsafe_allow_html=True)
                    st.markdown('<div class="section-title">📄 Cover Letter</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="cover-letter">{cover_letter}</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                    st.download_button("⬇️ Download Cover Letter", cover_letter,
                                       file_name="cover_letter.txt", use_container_width=True)

            except Exception as e:
                st.error(f"Something went wrong: {str(e)}")
