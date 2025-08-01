
0].isupper() and "," in line and len(line.split()) < 20:
                job_title_line = line
                i += 1
                bullet_points = []
                while i < len(sorted_content) and not (sorted_content[i].isupper() and "," in sorted_content[i]):
                    bullet_points.append(sorted_content[i])
                    i += 1
                job_para = doc.add_paragraph()
                job_run = job_para.add_run(job_title_line.strip())
                job_run.bold = True
                job_run.font.name = "Garamond"
                job_run.font.size = Pt(11)
                for bp in bullet_points:
                    bullet = doc.add_paragraph(style='List Bullet')
                    bullet_run = bullet.add_run(bp.strip("• "))
                    bullet_run.font.name = "Garamond"
                    bullet_run.font.size = Pt(11)
            else:
                i += 1

    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

def enhance_text(input_text):
    prompt = (
        "Improve the following resume bullet points to be stronger, more action-oriented, and quantifiable. "
        "Keep them professional and concise:\n\n" + input_text
    )
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

# --- Streamlit App UI ---
st.set_page_config(page_title="Resume AI", page_icon="📄", layout="centered")
st.title("📄 Apollo Society Resume Builder")
st.markdown("""
Build and enhance resumes in seconds. Upload your draft or paste resume bullets, and select the **Apollo Society** template.
""")

format_option = st.selectbox("Choose resume format:", ["Apollo Society", "Custom (coming soon)"])
input_method = st.radio("Input method:", ["Paste text", "Upload .docx"])

raw_text = ""
if input_method == "Paste text":
    raw_text = st.text_area("Paste your resume bullets or content here:", height=300)
elif input_method == "Upload .docx":
    uploaded_file = st.file_uploader("Upload Word Document:", type=["docx"])
    if uploaded_file:
        doc = Document(uploaded_file)
        raw_text = "\n".join([para.text for para in doc.paragraphs])

if raw_text:
    if st.button("✨ Enhance Bullets with AI"):
        improved_text = enhance_text(raw_text)
        st.subheader("Enhanced Resume Bullets:")
        st.text(improved_text)

    if st.button("📁 Format Resume to Apollo Society Template"):
        sections = {}
        current_section = "Other"
        sections[current_section] = []
        for line in raw_text.splitlines():
            if line.strip().isupper() and len(line.strip()) < 40:
                current_section = line.strip()
                sections[current_section] = []
            elif line.strip():
                sections[current_section].append(line.strip("• "))

        resume_docx = format_resume(sections)
        st.download_button(
            label=f"📥 Download {format_option} Resume",
            data=resume_docx,
            file_name=f"{format_option.replace(' ', '_')}_Resume.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
