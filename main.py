import os
import re
import streamlit as st
from dotenv import load_dotenv
from anthropic import Anthropic

# ─────────────────────────────────────────────
# ENVIRONMENT & CLIENT SETUP
# ─────────────────────────────────────────────
load_dotenv()
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
if not ANTHROPIC_API_KEY:
    st.error("❌ Missing ANTHROPIC_API_KEY in environment.")
    st.stop()

# 💡 FIX 1: Initialize Anthropic client using st.session_state.
if "anthropic_client" not in st.session_state:
    try:
        # 🐛 FINAL FIX: Explicitly setting http_client=None to force a clean internal 
        # client creation, bypassing environment-driven configuration (like the 
        # unexpected 'proxies' argument) that triggers the TypeError.
        st.session_state.anthropic_client = Anthropic(
            api_key=ANTHROPIC_API_KEY,
            http_client=None 
        )
    except Exception as e:
        st.error(f"❌ Failed to initialize Anthropic client: {e}")
        st.stop()
        
# Assign the client from session state to a local variable for ease of use
client = st.session_state.anthropic_client

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(page_title="AI Wireframe Generator (Anthropic)", page_icon="🎨", layout="wide")

# ─────────────────────────────────────────────
# SIDEBAR: ABOUT / DISCLAIMER / HOW TO RUN
# ─────────────────────────────────────────────
st.sidebar.title("ℹ️ About This App")
st.sidebar.markdown(
    """
This tool generates **multi-page website wireframes** using **Anthropic Claude 3 models**.

It produces:
- Landing, About, Features, Pricing, Contact sections  
- Responsive HTML + inline CSS  
- Placeholder images for layout visualization
    """
)

st.sidebar.markdown("---")
st.sidebar.markdown(
    """
### ⚙️ Tech Stack
- Streamlit UI  
- Anthropic Claude 3 (Haiku/Sonnet/Opus)  
- Python 3.11+  
- Inline CSS wireframe generation
    """
)

st.sidebar.markdown("---")
st.sidebar.markdown(
    """
### ⚠️ Disclaimer  
This app is for **educational and prototyping purposes only**.  
Generated HTML is **non-production** and should be reviewed before deployment.
    """
)

st.sidebar.markdown("---")
st.sidebar.markdown(
    """
### ▶️ How to Run
1. Save as **`app.py`** 2. Create `.env` file with:
   ```
   ANTHROPIC_API_KEY=your_api_key_here
   ```
3. Install deps:
   ```bash
   pip install streamlit anthropic python-dotenv
   ```
4. Run:
   ```bash
   streamlit run app.py
   ```
5. Click **🚀 Generate Wireframe** → **💾 Download HTML**
    """
)

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.markdown(
    "<h1 style='text-align:center; color:#22C55E;'>🎨 AI Wireframe Generator (Anthropic)</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p style='text-align:center;'>Generate responsive HTML wireframes with placeholder images and adjustable creativity.</p>",
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────
# PAGE MANAGER
# ─────────────────────────────────────────────
st.subheader("🧩 Manage Pages in Your Wireframe")

# Persistent page list
if "pages" not in st.session_state:
    st.session_state.pages = ["Landing", "About", "Features", "Pricing", "Contact"]

col1, col2 = st.columns([3, 1])
with col1:
    new_page = st.text_input("Add a new page (e.g. 'Testimonials')", "")
with col2:
    if st.button("➕ Add Page", key="add_page_btn") and new_page:
        if new_page not in st.session_state.pages:
            st.session_state.pages.append(new_page)
        else:
            st.warning("⚠️ Page already exists.")
        
        # 💡 FIX 2: Use st.rerun() instead of deprecated st.experimental_rerun()
        st.rerun()

# Display and allow deletion
for p in st.session_state.pages:
    cols = st.columns([4, 1])
    cols[0].markdown(f"• **{p}**")
    
    # 💡 FIX 3: Use unique keys for buttons inside a loop
    if cols[1].button(f"🗑️ Delete {p}", key=f"delete_btn_{p}"):
        st.session_state.pages.remove(p)
        
        # 💡 FIX 2: Use st.rerun() instead of deprecated st.experimental_rerun()
        st.rerun()

# ─────────────────────────────────────────────
# CONTROLS FOR THEME & TEMPERATURE
# ─────────────────────────────────────────────
st.sidebar.header("🎨 Customization")
base_color = st.sidebar.color_picker("Pick Base Theme Color", value="#22C55E")
temperature = st.sidebar.slider("🧠 Creativity Level", 0.0, 1.0, 0.7, 0.1)

# ─────────────────────────────────────────────
# STARTUP INFO
# ─────────────────────────────────────────────
st.subheader("🧠 Describe Your Startup")
startup_name = st.text_input("Startup Name", "Apna Grocery Store")
startup_concept = st.text_area(
    "Concept Description",
    "A modern grocery delivery platform offering fresh Indian food and essentials with instant delivery.",
)

# ─────────────────────────────────────────────
# GENERATE BUTTON
# ─────────────────────────────────────────────
if st.button("🚀 Generate Wireframe"):
    with st.spinner("🎨 Generating wireframe with Anthropic Claude 3 Haiku..."):
        try:
            pages_list = ", ".join(st.session_state.pages)
            html_prompt = f"""
                You are a professional front-end designer.

                Generate a complete, responsive, single-page HTML5 website with inline CSS.

                Startup Name: {startup_name}
                Concept: {startup_concept}
                Pages to include: {pages_list}
                Theme Color: {base_color}

                ⚙️ Requirements:
                - Use a **sticky top navigation bar** with links that scroll smoothly to each section.
                - Each section must have a matching `id` (e.g. id="about", id="features", etc.) so links work.
                - Implement `scroll-behavior: smooth;` in CSS.
                - Include **real Unsplash images** for each major section (hero, about, features, pricing, contact).
                - Hero section: full width, large background image with overlay text and CTA button.
                - Use `{base_color}` as the primary color for accents, buttons, and headings.
                - Design should be visually clean, mobile responsive, and balanced.
                - Add light hover effects and consistent padding.
                - Return only valid, complete HTML (<!DOCTYPE html> ... </html>) with inline CSS — no markdown.
                """

            response = client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=4096,
                temperature=temperature,
                messages=[{"role": "user", "content": html_prompt}],
            )

            html_output = response.content[0].text.strip()
            
            # Robust extraction of the HTML content, handling markdown code fences
            if html_output.startswith("```html"):
                html_output = "\n".join(html_output.splitlines()[1:-1])
            html_output = re.sub(r"^```.*?\\n|```$", "", html_output, flags=re.S)

            st.success("✅ Wireframe generated successfully!")
            
            # Display the result in an expander for quick view
            with st.expander("Preview HTML Output"):
                st.code(html_output, language="html")
                
            st.download_button(
                label="💾 Download HTML File",
                data=html_output,
                file_name=f"{startup_name.lower().replace(' ', '_')}_anthropic_wireframe.html",
                mime="text/html",
            )

        except Exception as e:
            st.error(f"❌ Error generating wireframe: {e}")

# ─────────────────────────────────────────────
# FOOTER DISCLAIMER
# ─────────────────────────────────────────────
st.markdown(
    """
<hr>
<div style='text-align:center; font-size:0.9em; line-height:1.6;'>
  <p>© 2025 AI Wireframe Generator (Anthropic) | Developed by <strong>Alhad Bhadekar</strong></p>
  <p style='max-width:680px; margin:auto; font-size:0.85em; color:#6b7280;'>
    <em>Disclaimer: Generated HTML is for demonstration and educational purposes only. Review and refine before real deployment.</em>
  </p>
</div>
""",
    unsafe_allow_html=True,
)