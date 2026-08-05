import streamlit as st

# ---------- Page Config ----------
st.set_page_config(
    page_title="Alert for Digicel Haiti",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- Custom CSS ----------
st.markdown("""
    <style>
    .main-title {
        color: #FF0000;
        font-size: 3.5rem;
        font-weight: 900;
        text-align: center;
        text-shadow: 0 0 30px rgba(255, 0, 0, 0.4);
        animation: pulse 2s ease-in-out infinite;
        padding: 20px 0;
    }
    @keyframes pulse {
        0%, 100% { text-shadow: 0 0 30px rgba(255, 0, 0, 0.4); }
        50% { text-shadow: 0 0 60px rgba(255, 0, 0, 0.8), 0 0 120px rgba(255, 0, 0, 0.3); }
    }
    .sub-title {
        color: #FF4444;
        font-size: 1.5rem;
        text-align: center;
        font-weight: 600;
        margin-bottom: 30px;
    }
    .city-card {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        padding: 10px 15px;
        margin: 5px 0;
        border-left: 4px solid #FF0000;
        transition: 0.3s;
    }
    .city-card:hover {
        background: rgba(255, 0, 0, 0.1);
        transform: translateX(5px);
    }
    .sidebar-title {
        color: #FF6666;
        font-size: 1.2rem;
        font-weight: 700;
        margin-bottom: 15px;
    }
    .contact-info {
        background: rgba(255, 0, 0, 0.1);
        border-radius: 10px;
        padding: 15px;
        margin-top: 20px;
        border: 1px solid rgba(255, 0, 0, 0.3);
    }
    .warning-box {
        background: rgba(255, 0, 0, 0.15);
        border: 2px solid #FF0000;
        border-radius: 10px;
        padding: 20px;
        margin: 20px 0;
    }
    .stApp {
        background: #0a0a0a;
    }
    .stSidebar {
        background: #1a1a2e;
    }
    .voice-text {
        background: rgba(255, 0, 0, 0.08);
        padding: 15px;
        border-radius: 10px;
        border-left: 4px solid #FF0000;
        margin: 10px 0;
        color: #DDDDDD;
        font-size: 0.95rem;
        line-height: 1.6;
    }
    .footer-text {
        text-align: center;
        padding: 20px 0;
        color: #888;
    }
    .footer-text p {
        font-size: 0.9rem;
        color: #666;
    }
    .footer-text .small {
        font-size: 0.8rem;
        color: #555;
    }
    </style>
""", unsafe_allow_html=True)

# ---------- Sidebar ----------
with st.sidebar:
    st.markdown('<div class="sidebar-title">🚨 AI Voice Alert</div>', unsafe_allow_html=True)
    
    # Language Selection
    lang_tab = st.radio(
        "Select Language / Choisissez la langue / Seleccione el idioma",
        ["🇺🇸 English", "🇫🇷 Français", "🇪🇸 Español"],
        index=0
    )
    
    # Multilingual Alert Texts
    english_text = """This alert is for the Digicel telecommunication phone company. Users with Digicel SIM cards complain that when they do any internet plan on their phone, it never works and they lose money on their account making these plans. They cannot use WhatsApp, Facebook, or any social media. The Digicel company must fix this issue that has been going on for three years and a few months till 2026. Old Digicel users plan to change internet phone company if this issue persists. This message alert was brought to you by Gesner Deslandes, software engineer at GlobalInternet.py."""
    
    french_text = """Cette alerte concerne la compagnie de télécommunications Digicel. Les utilisateurs avec des cartes SIM Digicel se plaignent que lorsqu'ils font un forfait internet sur leur téléphone, cela ne fonctionne jamais et ils perdent de l'argent sur leur compte en faisant ces forfaits. Ils ne peuvent pas utiliser WhatsApp, Facebook ou aucun réseau social. La compagnie Digicel doit résoudre ce problème qui dure depuis trois ans et quelques mois jusqu'en 2026. Les anciens utilisateurs de Digicel prévoient de changer de compagnie de téléphone internet si ce problème persiste. Ce message d'alerte vous a été présenté par Gesner Deslandes, ingénieur logiciel chez GlobalInternet.py."""
    
    spanish_text = """Esta alerta es para la compañía de telecomunicaciones Digicel. Los usuarios con tarjetas SIM Digicel se quejan de que cuando contratan un plan de internet en su teléfono, nunca funciona y pierden dinero en su cuenta al hacer estos planes. No pueden usar WhatsApp, Facebook ni ninguna red social. La compañía Digicel debe solucionar este problema que ha estado ocurriendo durante tres años y algunos meses hasta 2026. Los usuarios antiguos de Digicel planean cambiar de compañía de teléfono internet si este problema persiste. Este mensaje de alerta fue presentado por Gesner Deslandes, ingeniero de software en GlobalInternet.py."""
    
    # Set text based on language
    if lang_tab == "🇺🇸 English":
        voice_text = english_text
        lang_code = 'en'
    elif lang_tab == "🇫🇷 Français":
        voice_text = french_text
        lang_code = 'fr'
    else:
        voice_text = spanish_text
        lang_code = 'es'
    
    # Display the voice text
    st.markdown(f'<div class="voice-text">{voice_text}</div>', unsafe_allow_html=True)
    
    # ---------- FALLBACK: Browser Speech Synthesis ----------
    if st.button("🔊 Play Voice Alert (Browser)", use_container_width=True):
        # Escape any backticks or quotes in the text to avoid breaking the JS string
        escaped_text = voice_text.replace("`", "\\`").replace("'", "\\'")
        
        js_code = f"""
        <script>
        const msg = new SpeechSynthesisUtterance(`{escaped_text}`);
        msg.lang = '{lang_code}';
        msg.rate = 0.9;
        msg.pitch = 1.1;
        
        // Wait for voices to load
        function speakWithVoice() {{
            const voices = speechSynthesis.getVoices();
            const voice = voices.find(v => v.lang.startsWith('{lang_code}'));
            if (voice) msg.voice = voice;
            speechSynthesis.speak(msg);
        }}
        
        // Check if voices are already loaded
        if (speechSynthesis.getVoices().length > 0) {{
            speakWithVoice();
        }} else {{
            speechSynthesis.onvoiceschanged = speakWithVoice;
        }}
        </script>
        """
        st.components.v1.html(js_code, height=0)
        st.success("🔊 Voice is playing via your browser!")
        st.info("💡 If you don't hear anything, please check your browser's volume settings.")
    
    st.markdown("---")
    
    # ---------- Contact Information ----------
    st.markdown('<div class="contact-info">', unsafe_allow_html=True)
    st.markdown("### 📱 Contact Information")
    st.markdown("**Gesner Deslandes**")
    st.markdown("*Software Engineer at GlobalInternet.py*")
    st.markdown("---")
    st.markdown("📞 **(509) 4738-5663**")
    st.markdown("📧 **deslandes78@gmail.com**")
    st.markdown("🌐 [GlobalInternet.py](https://globalinternetsitepy-abh7v6tnmskxxnuplrdcgk.streamlit.app/)")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.caption("🚨 Alert System v2.0")
    st.caption("Brought to you by GlobalInternet.py")

# ---------- Main Content ----------
st.markdown('<div class="main-title">🚨 ALERT FOR DIGICEL HAITI</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">⚠️ Internet Connection is NOT Working ⚠️</div>', unsafe_allow_html=True)

# Warning Box
st.markdown("""
<div class="warning-box">
    <h3 style="color: #FF4444; margin: 0;">⚠️ URGENT ALERT</h3>
    <p style="color: #DDDDDD; margin: 10px 0 0 0;">
        Digicel Haiti users in the Southern region are experiencing critical internet connectivity issues.
        Internet plans are not working, causing financial losses and inability to use social media.
        This issue has been ongoing for over 3 years.
    </p>
</div>
""", unsafe_allow_html=True)

# ---------- City List ----------
st.markdown("### 📍 Affected Cities in Southern Haiti")

southern_cities = [
    "Grand Goâve", "Petit-Goâve", "Léogâne", "Jacmel", "Cayes-Jacmel",
    "Marigot", "Kenscoff", "Fonds-Verrettes", "Thiotte", "Bainet",
    "Côte-de-Fer", "Belle-Anse", "Grand-Gosier", "Anse-à-Pitres", "Port-à-Piment",
    "Les Cayes", "Camp-Perrin", "Torbeck", "Chantal", "Maniche",
    "Aquin", "Cavaillon", "Saint-Louis-du-Sud", "Tiburon", "Roche-à-Bateaux",
    "Côtes-de-Fer", "Baradères", "Petit-Trou-de-Nippes", "Anse-à-Veau", "Miragoâne",
    "Fonds-des-Nègres", "Paillant", "Petit-Rivière-de-Nippes", "Arnaud",
    "Cap-Haïtien (South Region)", "Gonaïves (South Region)", "Saint-Marc (South Region)",
    "Les Anglais", "Dame-Marie", "Chambellan", "Moron", "Abricots",
    "Bonbon", "Jérémie", "Roseaux", "Beaumont", "Pestel",
    "Corail", "Trouin", "Miragoâne", "Fonds-Verrettes", "Ganthier",
    "Croix-des-Bouquets (South)", "Thomazeau (South)", "Cornillon (South)"
]

# Display cities in 3 columns
cols = st.columns(3)
for idx, city in enumerate(southern_cities):
    with cols[idx % 3]:
        st.markdown(f'<div class="city-card">📍 {city}</div>', unsafe_allow_html=True)

st.caption(f"📊 Total affected cities: {len(southern_cities)}")

# ---------- Footer ----------
st.markdown("---")
st.markdown("""
<div class="footer-text">
    <p>
        <strong style="color: #FF4444;">⚠️ This is a public alert</strong> for Digicel Haiti users.<br>
        If you are experiencing internet issues, please contact Digicel customer support.
    </p>
    <p class="small">
        © 2026 GlobalInternet.py | Alert System v2.0 | Built with ❤️ in Haiti
    </p>
</div>
""", unsafe_allow_html=True)
