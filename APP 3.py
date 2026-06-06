import streamlit as st
from PIL import Image
import google.generativeai as genai
import json

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="Inspiration Based Prompt Engine",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# CSS — MINIMAL ORANGE / WHITE THEME
# =========================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');

:root {
    --orange:       #E85D04;
    --orange-light: #FFF0E8;
    --orange-mid:   #FFDCCA;
    --white:        #FFFFFF;
    --off-white:    #FAFAF9;
    --border:       #E8E3DE;
    --text:         #1A1A1A;
    --text-soft:    #6B6560;
    --text-muted:   #A8A09A;
    --radius:       6px;
}

html, body, .stApp {
    background-color: var(--white) !important;
    color: var(--text) !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 14px !important;
}

#MainMenu, footer, header, .stDeployButton { display: none !important; }

.block-container {
    max-width: 1400px !important;
    padding: 2rem 2.5rem 4rem !important;
}

/* ----- Top bar ----- */
.topbar {
    display: flex;
    align-items: baseline;
    gap: 1rem;
    border-bottom: 2px solid var(--orange);
    padding-bottom: 1rem;
    margin-bottom: 2.5rem;
}
.topbar-title {
    font-size: 1.25rem;
    font-weight: 600;
    color: var(--text);
    letter-spacing: -0.01em;
}
.topbar-sub {
    font-size: 12px;
    color: var(--text-muted);
    font-weight: 400;
}
.topbar-badge {
    margin-left: auto;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--orange);
    background: var(--orange-light);
    border: 1px solid var(--orange-mid);
    border-radius: 4px;
    padding: 3px 10px;
}

/* ----- Section labels ----- */
.sec {
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--orange);
    display: block;
    margin-bottom: 0.75rem;
}

/* ----- Rule line ----- */
.rule {
    height: 1px;
    background: var(--border);
    margin: 1.6rem 0;
}

/* ----- Info box ----- */
.info-box {
    background: var(--orange-light);
    border: 1px solid var(--orange-mid);
    border-radius: var(--radius);
    padding: 0.85rem 1rem;
    font-size: 12px;
    color: var(--text-soft);
    line-height: 1.7;
    margin-bottom: 1rem;
}
.info-box strong { color: var(--orange); }

/* ----- API status ----- */
.api-status-ok {
    display: flex;
    align-items: center;
    gap: 6px;
    margin-top: 0.5rem;
    font-size: 11px;
    color: #2D7A3A;
}
.api-status-empty {
    display: flex;
    align-items: center;
    gap: 6px;
    margin-top: 0.5rem;
    font-size: 11px;
    color: var(--text-muted);
}

/* ----- Image upload panels ----- */
.img-panel {
    border: 1px dashed var(--border);
    border-radius: var(--radius);
    padding: 1rem;
    background: var(--off-white);
    min-height: 80px;
}
.img-label {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--text-muted);
    margin-bottom: 6px;
    display: block;
}
.img-label-pre  { color: #5B6EE8; }
.img-label-inspo { color: var(--orange); }

/* ----- Inputs ----- */
.stSelectbox label,
.stTextArea label,
.stTextInput label,
.stCheckbox label,
.stFileUploader label,
.stSlider label,
.stNumberInput label {
    font-size: 11px !important;
    font-weight: 500 !important;
    color: var(--text-soft) !important;
    letter-spacing: 0.04em !important;
    text-transform: uppercase !important;
    margin-bottom: 4px !important;
}

.stSelectbox > div > div {
    background: var(--off-white) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    color: var(--text) !important;
    font-size: 13px !important;
}
.stSelectbox > div > div:focus-within {
    border-color: var(--orange) !important;
    box-shadow: 0 0 0 3px rgba(232,93,4,0.1) !important;
}

.stTextArea textarea {
    background: var(--off-white) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    color: var(--text) !important;
    font-size: 13px !important;
    line-height: 1.6 !important;
}
.stTextArea textarea:focus {
    border-color: var(--orange) !important;
    box-shadow: 0 0 0 3px rgba(232,93,4,0.1) !important;
    outline: none !important;
}

.stTextInput input {
    background: var(--off-white) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    color: var(--text) !important;
    font-size: 13px !important;
}
.stTextInput input:focus {
    border-color: var(--orange) !important;
    box-shadow: 0 0 0 3px rgba(232,93,4,0.1) !important;
    outline: none !important;
}

.stCheckbox span {
    font-size: 13px !important;
    color: #1A1A1A !important;
    font-weight: 500 !important;
    text-transform: none !important;
    letter-spacing: normal !important;
}
.stCheckbox > div > label {
    text-transform: none !important;
    font-size: 13px !important;
    letter-spacing: normal !important;
    color: #1A1A1A !important;
}
.stCheckbox p {
    color: #1A1A1A !important;
    font-weight: 500 !important;
}

.stFileUploader > div {
    background: var(--orange-light) !important;
    border: 1px dashed var(--orange-mid) !important;
    border-radius: var(--radius) !important;
}
.stFileUploader > div:hover {
    border-color: var(--orange) !important;
}
.stFileUploader p, .stFileUploader span {
    color: var(--text-soft) !important;
    font-size: 14px !important;
}

/* ----- Slider ----- */
.stSlider [data-testid="stSliderThumb"] {
    background: var(--orange) !important;
}
.stSlider [data-baseweb="slider"] div[role="progressbar"] {
    background: var(--orange) !important;
}

/* ----- Buttons ----- */
.stButton > button {
    width: 100% !important;
    background: var(--orange) !important;
    color: #fff !important;
    border: none !important;
    border-radius: var(--radius) !important;
    font-size: 11px !important;
    font-weight: 600 !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    padding: 0.75rem 1.25rem !important;
    transition: background 0.15s !important;
    margin-top: 0.5rem !important;
}
.stButton > button:hover {
    background: #C94E00 !important;
}
.stButton > button:disabled {
    background: var(--border) !important;
    color: var(--text-muted) !important;
}

.stDownloadButton > button {
    width: 100% !important;
    background: transparent !important;
    color: var(--orange) !important;
    border: 1px solid var(--orange) !important;
    border-radius: var(--radius) !important;
    font-size: 11px !important;
    font-weight: 600 !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    padding: 0.7rem 1.25rem !important;
    transition: background 0.15s !important;
    margin-top: 0.4rem !important;
}
.stDownloadButton > button:hover {
    background: var(--orange-light) !important;
}

/* ----- Image ----- */
.stImage img {
    border-radius: var(--radius) !important;
    border: 1px solid var(--border) !important;
}

/* ----- Output textarea ----- */
.stTextArea textarea[readonly] {
    background: var(--off-white) !important;
    color: var(--text-soft) !important;
    font-family: 'Courier New', monospace !important;
    font-size: 12px !important;
    line-height: 1.65 !important;
    border-color: var(--border) !important;
}

/* ----- Scrollbar ----- */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 4px; }

[data-testid="column"] { padding: 0 0.6rem !important; }
[data-testid="column"]:first-child { padding-left: 0 !important; }
[data-testid="column"]:last-child  { padding-right: 0 !important; }

/* strength badge */
.strength-tag {
    display: inline-block;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--orange);
    background: var(--orange-light);
    border: 1px solid var(--orange-mid);
    border-radius: 4px;
    padding: 2px 8px;
    margin-left: 8px;
    vertical-align: middle;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# TOPBAR
# =========================================================

# Encode logo as base64 to embed inline
import base64
from pathlib import Path

logo_path = Path("LOGO_BLACK.png")
logo_b64 = base64.b64encode(logo_path.read_bytes()).decode()

st.markdown(f"""
<div class="topbar">
    <div style="display:flex; flex-direction:column; gap:2px;">
        <span class="topbar-title">Inspiration Based Prompt Engine</span>
        <span class="topbar-sub">Inspiration-specific prompts for architectural AI rendering</span>
    </div>
    <div style="margin-left:auto;">
        <img src="data:image/png;base64,{logo_b64}"
             style="height:65px; width:auto; display:block;" />
    </div>
</div>
""", unsafe_allow_html=True)

# =========================================================
# LAYOUT — 3 columns: controls | images | output
# =========================================================

col_left, col_mid, col_right = st.columns([1, 0.85, 1.1], gap="large")

# =========================================================
# LEFT — CONTROLS
# =========================================================

with col_left:

    # ----- 00 — API Key -----
    st.markdown('<span class="sec">00 — API Configuration</span>', unsafe_allow_html=True)
    GEMINI_API_KEY = st.text_input(
        "Gemini API Key",
        type="password",
        placeholder="AIza...",
        help="Get your key at https://aistudio.google.com/app/apikey",
        label_visibility="collapsed"
    )
    if GEMINI_API_KEY:
        st.markdown('<div class="api-status-ok"><span>●</span><span>Key entered — ready to generate</span></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="api-status-empty"><span>○</span><span>Enter Gemini API key &nbsp;·&nbsp; <a href="https://aistudio.google.com/app/apikey" target="_blank" style="color:#E85D04;text-decoration:none;">Get one free ↗</a></span></div>', unsafe_allow_html=True)

    st.markdown('<div style="margin-top:0.9rem;"></div>', unsafe_allow_html=True)
    st.markdown('<span style="font-size:10px;font-weight:600;letter-spacing:0.12em;text-transform:uppercase;color:var(--text-muted);">Gemini Model</span>', unsafe_allow_html=True)
    gemini_model = st.selectbox(
        "Gemini Model",
        [
            "gemini-2.5-flash",
            "gemini-2.5-pro",
            "gemini-2.0-flash",
            "gemini-2.0-flash-lite",
            "gemini-1.5-pro",
            "gemini-1.5-flash",
        ],
        index=0,
        label_visibility="collapsed",
        help="Select the Gemini model used for image analysis. gemini-2.5-flash is recommended for speed and quality."
    )

    st.markdown('<div class="rule"></div>', unsafe_allow_html=True)

    # ----- 01 — Render Style -----
    st.markdown('<span class="sec">01 — Render Style Objective</span>', unsafe_allow_html=True)
    render_style = st.selectbox(
        "Render Style",
        [
            "Apply Inspiration Style Fully",
            "Blend Inspiration Partially",
            "Lighting & Mood Transfer Only",
            "Material & Texture Transfer Only",
            "Color Palette Transfer Only",
            "Furniture Style Transfer Only",
            "Full Interior Transformation",
            "Subtle Atmospheric Upgrade",
        ],
        label_visibility="collapsed"
    )

    st.markdown('<div class="rule"></div>', unsafe_allow_html=True)

    # ----- 02 — Inspiration Influence Strength -----
    st.markdown('<span class="sec">02 — Inspiration Influence Strength</span>', unsafe_allow_html=True)
    influence_strength = st.select_slider(
        "Strength",
        options=["Very Subtle (10%)", "Subtle (25%)", "Moderate (50%)", "Strong (70%)", "Very Strong (85%)", "Dominant (95%)"],
        value="Moderate (50%)",
        label_visibility="collapsed"
    )

    st.markdown('<div class="rule"></div>', unsafe_allow_html=True)

    # ----- 03 — Camera -----
    st.markdown('<span class="sec">03 — Camera Settings</span>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        camera_type = st.selectbox("Camera Body", ["Sony A7R IV", "Canon EOS R5", "RED Komodo", "Nikon Z8", "Hasselblad X2D"])
    with c2:
        lens_type = st.selectbox("Lens", ["16mm Ultra Wide", "24mm Architectural", "35mm Natural Perspective", "50mm Cinematic", "85mm Portrait"])

    st.markdown('<div class="rule"></div>', unsafe_allow_html=True)

    # ----- 04 — Lighting Transfer -----
    st.markdown('<span class="sec">04 — Lighting</span>', unsafe_allow_html=True)
    lighting_mode = st.selectbox(
        "Lighting Mode",
        [
            "Transfer from Inspiration Image",
            "Natural Daylight",
            "Warm Ambient",
            "Golden Hour",
            "Soft Luxury",
            "Cinematic Moody",
            "Studio Lighting",
            "Evening Atmosphere",
        ],
        label_visibility="collapsed"
    )

    st.markdown('<div class="rule"></div>', unsafe_allow_html=True)

    # ----- 05 — Elements to Transfer -----
    st.markdown('<span class="sec">05 — Elements to Transfer from Inspiration</span>', unsafe_allow_html=True)
    tf1, tf2 = st.columns(2)
    with tf1:
        transfer_materials  = st.checkbox("Materials & Textures",  value=True)
        transfer_lighting   = st.checkbox("Lighting & Mood",        value=True)
        transfer_colors     = st.checkbox("Color Palette",          value=True)
    with tf2:
        transfer_furniture  = st.checkbox("Furniture Style",        value=False)
        transfer_decor      = st.checkbox("Decor & Accessories",    value=False)
        transfer_atmosphere = st.checkbox("Overall Atmosphere",     value=True)

    st.markdown('<div class="rule"></div>', unsafe_allow_html=True)

    # ----- 06 — Preservation Rules -----
    st.markdown('<span class="sec">06 — Preserve from Pre-Render</span>', unsafe_allow_html=True)
    p1, p2 = st.columns(2)
    with p1:
        preserve_geometry  = st.checkbox("Exact Geometry",         value=True)
        preserve_layout    = st.checkbox("Furniture Layout",        value=True)
        preserve_structure = st.checkbox("Architectural Structure", value=True)
    with p2:
        preserve_dimensions = st.checkbox("Room Dimensions",       value=True)
        preserve_perspective = st.checkbox("Camera Perspective",   value=True)
        preserve_identity   = st.checkbox("Scene Identity",        value=True)

    st.markdown('<div class="rule"></div>', unsafe_allow_html=True)

    # ----- 07 — Realism Quality -----
    st.markdown('<span class="sec">07 — Output Quality</span>', unsafe_allow_html=True)
    realism_quality = st.selectbox(
        "Quality",
        ["Ultra Photorealistic", "Architectural Magazine Quality", "Luxury Interior Photography", "Competition Render Quality", "DSLR Realism"],
        label_visibility="collapsed"
    )

    st.markdown('<div class="rule"></div>', unsafe_allow_html=True)

    # ----- 08 — Custom Instructions -----
    st.markdown('<span class="sec">08 — Additional Instructions</span>', unsafe_allow_html=True)
    custom_instructions = st.text_area(
        "Extra",
        placeholder=(
            "Examples:\n"
            "- Replace flooring with Italian marble from inspiration\n"
            "- Keep existing sofa color unchanged\n"
            "- Apply gold accent tones from inspiration to trims"
        ),
        height=110,
        label_visibility="collapsed"
    )

    st.markdown('<div class="rule"></div>', unsafe_allow_html=True)

    # ----- 09 — Negative / Restrictions -----
    st.markdown('<span class="sec">09 — Restrictions</span>', unsafe_allow_html=True)
    custom_negative = st.text_area(
        "Do Not",
        placeholder=(
            "Examples:\n"
            "- Do not add extra furniture\n"
            "- Do not change room layout\n"
            "- Do not add windows that don't exist"
        ),
        height=100,
        label_visibility="collapsed"
    )

    st.markdown('<div class="rule"></div>', unsafe_allow_html=True)

    # ----- Generate Button -----
    if not GEMINI_API_KEY and (True):
        missing = []
    pre_img_ready  = False
    inspo_img_ready = False

    # placeholders — will be set in col_mid
    # We use session state to pass images across columns
    if "pre_render_image" not in st.session_state:
        st.session_state["pre_render_image"] = None
    if "inspo_image" not in st.session_state:
        st.session_state["inspo_image"] = None

    missing_parts = []
    if not GEMINI_API_KEY:
        missing_parts.append("API key")
    if st.session_state["pre_render_image"] is None:
        missing_parts.append("pre-render image")
    if st.session_state["inspo_image"] is None:
        missing_parts.append("inspiration image")

    if missing_parts:
        btn_label    = f"Missing: {', '.join(missing_parts)}"
        btn_disabled = True
    else:
        btn_label    = "Generate Nano Banana Prompt"
        btn_disabled = False

    generate_btn = st.button(btn_label, disabled=btn_disabled)

# =========================================================
# MIDDLE — IMAGE UPLOADS
# =========================================================

with col_mid:

    st.markdown('<span class="sec">Image 1 — Pre-Render / Base Image</span>', unsafe_allow_html=True)
    st.markdown("""
    <div class="info-box">
        <strong>Pre-Render:</strong> Your existing interior render or photo — the base geometry, layout and structure that must be preserved.
    </div>
    """, unsafe_allow_html=True)

    pre_file = st.file_uploader(
        "Upload Pre-Render",
        type=["jpg", "jpeg", "png"],
        key="pre_render_uploader",
        label_visibility="collapsed"
    )
    if pre_file:
        pre_image = Image.open(pre_file)
        st.session_state["pre_render_image"] = pre_image
        st.image(pre_image, use_container_width=True, caption="Pre-Render / Base")
    else:
        st.session_state["pre_render_image"] = None
        st.markdown("""
        <div style="border:1px dashed #E8E3DE; border-radius:6px; padding:2rem 1rem;
                    text-align:center; color:#A8A09A; font-size:12px; background:#FAFAF9;">
            Upload pre-render image<br><span style="font-size:10px; letter-spacing:0.05em;">(JPG / PNG)</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="rule"></div>', unsafe_allow_html=True)

    st.markdown('<span class="sec">Image 2 — Inspiration / Style Reference</span>', unsafe_allow_html=True)
    st.markdown("""
    <div class="info-box">
        <strong>Inspiration:</strong> Your reference image whose style, materials, lighting or mood should be applied to the pre-render.
    </div>
    """, unsafe_allow_html=True)

    inspo_file = st.file_uploader(
        "Upload Inspiration",
        type=["jpg", "jpeg", "png"],
        key="inspo_uploader",
        label_visibility="collapsed"
    )
    if inspo_file:
        inspo_image = Image.open(inspo_file)
        st.session_state["inspo_image"] = inspo_image
        st.image(inspo_image, use_container_width=True, caption="Inspiration / Style Reference")
    else:
        st.session_state["inspo_image"] = None
        st.markdown("""
        <div style="border:1px dashed #FFDCCA; border-radius:6px; padding:2rem 1rem;
                    text-align:center; color:#A8A09A; font-size:12px; background:#FFF0E8;">
            Upload inspiration image<br><span style="font-size:10px; letter-spacing:0.05em;">(JPG / PNG)</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="rule"></div>', unsafe_allow_html=True)

    # Quick status summary
    pre_ok   = st.session_state["pre_render_image"] is not None
    inspo_ok = st.session_state["inspo_image"] is not None
    api_ok   = bool(GEMINI_API_KEY)

    def status_dot(ok): return ("🟠" if ok else "○")

    st.markdown(f"""
    <div style="font-size:11px; color:var(--text-muted); line-height:2.2;">
        {status_dot(pre_ok)} &nbsp; Pre-render image<br>
        {status_dot(inspo_ok)} &nbsp; Inspiration image<br>
        {status_dot(api_ok)} &nbsp; API key
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# RIGHT — OUTPUT
# =========================================================

with col_right:

    st.markdown('<span class="sec">Prompt Output — Nano Banana img2img</span>', unsafe_allow_html=True)

    pre_render_image = st.session_state.get("pre_render_image")
    inspo_img        = st.session_state.get("inspo_image")

    if not pre_render_image or not inspo_img:
        st.markdown("""
        <div style="
            border: 1px dashed #E8E3DE;
            border-radius: 6px;
            padding: 3.5rem 2rem;
            text-align: center;
            color: #A8A09A;
            font-size: 13px;
            line-height: 2;
            background: #FAFAF9;
        ">
            Upload both images in the middle panel<br>and configure parameters on the left.
        </div>
        """, unsafe_allow_html=True)

    elif not GEMINI_API_KEY:
        st.markdown("""
        <div style="
            border: 1px dashed #FFDCCA;
            border-radius: 6px;
            padding: 3.5rem 2rem;
            text-align: center;
            color: #A8A09A;
            font-size: 13px;
            line-height: 2;
            background: #FFF0E8;
        ">
            Both images uploaded ✓<br>
            Enter your <strong style="color:#E85D04;">Gemini API key</strong> in section 00 on the left.
        </div>
        """, unsafe_allow_html=True)

    elif generate_btn:

        genai.configure(api_key=GEMINI_API_KEY)
        vision_model = genai.GenerativeModel(gemini_model)

        # ----- Analyze pre-render -----
        with st.spinner("Analyzing pre-render image..."):
            pre_analysis_prompt = """
You are an expert architectural analyst.

Analyze this PRE-RENDER / BASE interior image with precision.

RULES:
- Be 100% factual — only describe what is visible
- Do NOT hallucinate or assume hidden areas
- Do NOT suggest changes

Report the following clearly:
1. ROOM TYPE: (e.g. living room, bedroom, office)
2. ARCHITECTURAL STYLE: (e.g. contemporary, traditional, minimalist)
3. EXACT SPATIAL LAYOUT: furniture positions and arrangement
4. STRUCTURAL ELEMENTS: walls, columns, ceiling design, windows, doors
5. FLOORING: material, pattern, color
6. WALL SURFACES: material, texture, color
7. CEILING: design, height, features
8. LIGHTING: type, positions, fixtures visible
9. FURNITURE: every item with approximate placement
10. CAMERA PERSPECTIVE: angle, height, focal direction
11. MATERIAL PALETTE: full list of all visible materials and colors
12. ROOM DIMENSIONS FEEL: sense of scale

Be precise and structured. This analysis is critical for preserving exact geometry.
"""
            r1 = vision_model.generate_content([pre_analysis_prompt, pre_render_image])
            pre_analysis = r1.text

        # ----- Analyze inspiration -----
        with st.spinner("Analyzing inspiration image..."):
            inspo_analysis_prompt = """
You are an expert interior designer and art director.

Analyze this INSPIRATION / STYLE REFERENCE image.

RULES:
- Extract style attributes that can be transferred to another interior
- Focus on transferable qualities

Extract and describe:
1. OVERALL AESTHETIC STYLE: (e.g. luxury, Japandi, industrial, Scandinavian)
2. COLOR PALETTE: primary, secondary, accent colors with descriptors
3. MATERIAL PALETTE: all key materials (marble, oak, linen, brass, etc.)
4. LIGHTING MOOD: type, color temperature, dramatic quality, shadow behavior
5. TEXTURE QUALITIES: rough/smooth, matte/gloss, natural/synthetic
6. FURNITURE DESIGN LANGUAGE: organic, geometric, contemporary, etc.
7. SPATIAL ATMOSPHERE: feeling, emotional quality, sensory impression
8. DECORATIVE ELEMENTS: style of accessories, art, plants, etc.
9. SURFACE FINISHES: wall treatments, floor finish, ceiling finish
10. DEFINING STYLE KEYWORDS: 5–10 descriptive words that define this look

This analysis is used to extract stylistic DNA to apply to another space.
"""
            r2 = vision_model.generate_content([inspo_analysis_prompt, inspo_img])
            inspo_analysis = r2.text

        # ----- Build transfer blocks -----
        transfer_elements = []
        if transfer_materials:  transfer_elements.append("Materials and surface textures")
        if transfer_lighting:   transfer_elements.append("Lighting setup, mood, and color temperature")
        if transfer_colors:     transfer_elements.append("Color palette and tonal range")
        if transfer_furniture:  transfer_elements.append("Furniture style and design language")
        if transfer_decor:      transfer_elements.append("Decorative accessories and styling elements")
        if transfer_atmosphere: transfer_elements.append("Overall spatial atmosphere and emotional mood")

        transfer_list = "\n".join([f"- {e}" for e in transfer_elements]) if transfer_elements else "- Overall style and atmosphere"

        preservation_rules = []
        if preserve_geometry:    preservation_rules.append("Preserve exact geometry of all architectural elements")
        if preserve_layout:      preservation_rules.append("Preserve furniture positions and layout exactly")
        if preserve_structure:   preservation_rules.append("Preserve all structural elements (walls, columns, openings)")
        if preserve_dimensions:  preservation_rules.append("Preserve room dimensions and spatial proportions")
        if preserve_perspective:  preservation_rules.append("Preserve the original camera angle and perspective")
        if preserve_identity:    preservation_rules.append("Preserve the fundamental scene identity and spatial logic")

        preservation_list = "\n".join([f"- {r}" for r in preservation_rules])

        final_prompt = f"""NANO BANANA — IMAGE-TO-IMAGE ARCHITECTURAL RENDERING PROMPT

This prompt is designed for use in Nano Banana img2img mode.
Input: [Pre-Render Image] + [Inspiration Image] (both uploaded alongside this prompt)

===================================================
IMAGE ROLES
===================================================

IMAGE 1 — PRE-RENDER (Structure Source):
Use this image as the strict structural and spatial foundation.
Copy its geometry, layout, perspective, and spatial arrangement exactly.

IMAGE 2 — INSPIRATION (Style Source):
Extract the aesthetic, material, lighting, and atmospheric DNA from this image.
Apply the style elements listed below onto the pre-render structure.

===================================================
PRE-RENDER IMAGE ANALYSIS
===================================================

{pre_analysis}

===================================================
INSPIRATION IMAGE ANALYSIS
===================================================

{inspo_analysis}

===================================================
RENDER OBJECTIVE
===================================================

{render_style}

INSPIRATION INFLUENCE STRENGTH: {influence_strength}

===================================================
STYLE TRANSFER INSTRUCTIONS
===================================================

Transfer the following elements FROM the inspiration image
ONTO the pre-render space:

{transfer_list}

TRANSFER BEHAVIOR:
- Extract the stylistic DNA from the inspiration image
- Apply it realistically to the pre-render geometry
- Blend naturally — avoid jarring discontinuities
- Respect physical plausibility of all transferred materials
- Scale textures correctly to the pre-render room size
- Maintain realistic reflections and shadow behavior for new materials

===================================================
STRICT PRESERVATION RULES (FROM PRE-RENDER)
===================================================

{preservation_list}

DO NOT CHANGE:
- Room floor plan or architectural boundaries
- Number or placement of furniture pieces
- Camera viewpoint or angle
- Any structural element not targeted for change
- Room identity — it must remain recognizably the same space

===================================================
CAMERA SETTINGS
===================================================

Camera Body: {camera_type}
Lens: {lens_type}
Behavior: DSLR architectural photography accuracy, realistic depth of field,
consistent vanishing points, physically accurate perspective

===================================================
LIGHTING
===================================================

Lighting Mode: {lighting_mode}

- Physically accurate light behavior
- Realistic shadow casting
- Consistent light sources
- High dynamic range realism
- Accurate ambient occlusion

===================================================
REALISM TARGET
===================================================

{realism_quality}

- Ultra realistic DSLR-quality output
- Photographic accuracy in all surfaces
- Physically based rendering behavior
- Realistic material interactions with light
- Cinematic depth and clarity

===================================================
ADDITIONAL INSTRUCTIONS
===================================================

{custom_instructions if custom_instructions.strip() else "None."}

===================================================
STRICT NEGATIVE PROMPT
===================================================

Do not redesign the architectural structure.
Do not add furniture that does not exist in the pre-render.
Do not remove existing furniture.
Do not change the room floor plan.
Do not invent rooms, windows, or spaces not in the original.
Do not make artistic reinterpretations — stay photorealistic.
Do not distort geometry or proportions.
Do not stylize artificially.
Do not apply cartoon or painterly effects.
Maintain complete spatial coherence with the pre-render.

{custom_negative if custom_negative.strip() else ""}

===================================================
CRITICAL IMG2IMG INSTRUCTION FOR NANO BANANA
===================================================

This is a strict image-to-image transfer task.
Structure = 100% from Pre-Render Image (Image 1).
Style = extracted from Inspiration Image (Image 2) at {influence_strength}.
Result must look like a photographic rendering of the pre-render
space, re-styled with the aesthetic quality of the inspiration image.
Preserve all spatial logic. Apply only the requested style attributes.
"""

        st.text_area("Output", final_prompt, height=820, label_visibility="collapsed")

        escaped_prompt = json.dumps(final_prompt)
        st.markdown(f"""
        <div style="display:flex; align-items:center; justify-content:space-between; margin-top:0.6rem; margin-bottom:0.2rem;">
            <button onclick="
                navigator.clipboard.writeText({escaped_prompt}).then(() => {{
                    this.textContent = '✓ Copied';
                    this.style.background = '#2D7A3A';
                    setTimeout(() => {{
                        this.textContent = 'Copy Prompt';
                        this.style.background = '#E85D04';
                    }}, 2000);
                }});
            " style="
                background: #E85D04;
                color: #fff;
                border: none;
                border-radius: 6px;
                font-size: 11px;
                font-weight: 600;
                letter-spacing: 0.12em;
                text-transform: uppercase;
                padding: 0.6rem 1.1rem;
                cursor: pointer;
                transition: background 0.15s;
                font-family: 'Inter', sans-serif;
            ">Copy Prompt</button>
            <a href="https://www.nanobananai.com" target="_blank" style="
                display: inline-flex;
                align-items: center;
                gap: 6px;
                font-size: 11px;
                font-weight: 600;
                letter-spacing: 0.08em;
                text-transform: uppercase;
                color: #E85D04;
                text-decoration: none;
                border: 1px solid #FFDCCA;
                border-radius: 6px;
                padding: 0.55rem 1rem;
                background: #FFF0E8;
                transition: background 0.15s;
            ">
                Open Nano Banana ↗
            </a>
        </div>
        """, unsafe_allow_html=True)

        st.download_button(
            "Download Prompt as .txt",
            final_prompt,
            file_name="nano_banana_prompt.txt"
        )

        st.markdown('<div class="rule"></div>', unsafe_allow_html=True)

        m1, m2, m3 = st.columns(3)
        word_count  = len(final_prompt.split())
        char_count  = len(final_prompt)
        transfer_count = len(transfer_elements)

        for col, label, val in zip(
            [m1, m2, m3],
            ["Words", "Characters", "Transfer Elements"],
            [word_count, char_count, transfer_count]
        ):
            with col:
                st.markdown(f"""
                <div style="text-align:center; padding:1rem 0.5rem;
                            border:1px solid #E8E3DE; border-radius:6px; background:#FAFAF9;">
                    <div style="font-size:1.5rem; font-weight:600; color:#E85D04; line-height:1;">{val}</div>
                    <div style="font-size:10px; letter-spacing:0.1em; text-transform:uppercase;
                                color:#A8A09A; margin-top:4px;">{label}</div>
                </div>
                """, unsafe_allow_html=True)

    else:
        st.markdown("""
        <div style="
            border: 1px dashed #E8E3DE;
            border-radius: 6px;
            padding: 3.5rem 2rem;
            text-align: center;
            color: #A8A09A;
            font-size: 13px;
            line-height: 2;
            background: #FAFAF9;
        ">
            All set. Press <strong style="color:#E85D04;">Generate Nano Banana Prompt</strong><br>in the left panel.
        </div>
        """, unsafe_allow_html=True)
