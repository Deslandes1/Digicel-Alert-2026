import streamlit as st
from io import BytesIO
import base64

try:
    from gtts import gTTS
    GTTS_AVAILABLE = True
except ImportError:
    GTTS_AVAILABLE = False
    print("⚠️ gTTS not installed. Using browser speech synthesis fallback.")

# ---------- DEBUG ----------
print("✅ app.py is starting...")
print("✅ Python version:", __import__('sys').version)
print("✅ gTTS available:", GTTS_AVAILABLE)

# ---------- Page Config ----------
st.set_page_config(
    page_title="Alert for Digicel Haiti",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="expanded"
)

print("✅ Page config set.")

# ---------- Custom CSS ----------
st.markdown("""
    <style>
    .stApp {
        background: #0a0a0a !important;
    }
    .stSidebar,
    .stSidebar .sidebar-content,
    .css-1d391kg,
    .css-1lcbmhc,
    section[data-testid="stSidebar"] {
        background: #0a0a0a !important;
    }
    .stSidebar .stRadio label,
    .stSidebar .stRadio div,
    .stSidebar .stMarkdown,
    .stSidebar .stCaption,
    .stSidebar .stButton button,
    .stSidebar .stSelectbox label,
    .stSidebar .stTextInput label {
        color: #ffffff !important;
    }
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
        color: #ffffff !important;
        font-weight: 500;
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
    .contact-info * {
        color: #ffffff !important;
    }
    .warning-box {
        background: rgba(255, 0, 0, 0.15);
        border: 2px solid #FF0000;
        border-radius: 10px;
        padding: 20px;
        margin: 20px 0;
    }
    .warning-box * {
        color: #ffffff !important;
    }
    .voice-text {
        background: rgba(255, 0, 0, 0.08);
        padding: 15px;
        border-radius: 10px;
        border-left: 4px solid #FF0000;
        margin: 10px 0;
        color: #ffffff !important;
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
        color: #ffffff !important;
    }
    .footer-text .small {
        font-size: 0.8rem;
        color: #aaaaaa !important;
    }
    .city-heading {
        color: #ffffff !important;
        font-weight: 700;
        margin-bottom: 20px;
    }
    .total-cities {
        color: #ffffff !important;
        font-weight: 600;
        margin-top: 10px;
    }
    .stRadio label {
        color: #ffffff !important;
    }
    .stRadio div {
        color: #ffffff !important;
    }
    .stMarkdown {
        color: #ffffff !important;
    }
    </style>
""", unsafe_allow_html=True)

print("✅ CSS applied.")

# ---------- Sidebar ----------
with st.sidebar:
    st.markdown('<div class="sidebar-title">🚨 AI Voice Alert</div>', unsafe_allow_html=True)
    
    lang_tab = st.radio(
        "Select Language / Choisissez la langue / Seleccione el idioma",
        ["🇺🇸 English", "🇫🇷 Français", "🇪🇸 Español"],
        index=0
    )
    
    # ---------- Base alert texts (displayed in sidebar) ----------
    english_alert = """This alert is for the Digicel telecommunication phone company. Users with Digicel SIM cards complain that when they do any internet plan on their phone, it never works and they lose money on their account making these plans. They cannot use WhatsApp, Facebook, or any social media. The Digicel company must fix this issue that has been going on for three years and a few months till 2026. Old Digicel users plan to change internet phone company if this issue persists. This message alert was brought to you by Gesner Deslandes, software engineer at GlobalInternet.py."""
    
    french_alert = """Cette alerte concerne la compagnie de télécommunications Digicel. Les utilisateurs avec des cartes SIM Digicel se plaignent que lorsqu'ils font un forfait internet sur leur téléphone, cela ne fonctionne jamais et ils perdent de l'argent sur leur compte en faisant ces forfaits. Ils ne peuvent pas utiliser WhatsApp, Facebook ou aucun réseau social. La compagnie Digicel doit résoudre ce problème qui dure depuis trois ans et quelques mois jusqu'en 2026. Les anciens utilisateurs de Digicel prévoient de changer de compagnie de téléphone internet si ce problème persiste. Ce message d'alerte vous a été présenté par Gesner Deslandes, ingénieur logiciel chez GlobalInternet.py."""
    
    spanish_alert = """Esta alerta es para la compañía de telecomunicaciones Digicel. Los usuarios con tarjetas SIM Digicel se quejan de que cuando contratan un plan de internet en su teléfono, nunca funciona y pierden dinero en su cuenta al hacer estos planes. No pueden usar WhatsApp, Facebook ni ninguna red social. La compañía Digicel debe solucionar este problema que ha estado ocurriendo durante tres años y algunos meses hasta 2026. Los usuarios antiguos de Digicel planean cambiar de compañía de teléfono internet si este problema persiste. Este mensaje de alerta fue presentado por Gesner Deslandes, ingeniero de software en GlobalInternet.py."""
    
    # ---------- Extended voice scripts (include invitation to view the city list) ----------
    english_voice = english_alert + " You can view the full list of affected cities in Southern Haiti on the main page of this alert."
    
    french_voice = french_alert + " Vous pouvez consulter la liste complète des villes touchées dans le Sud d'Haïti sur la page principale de cette alerte."
    
    spanish_voice = spanish_alert + " Puede ver la lista completa de ciudades afectadas en el Sur de Haití en la página principal de esta alerta."
    
    if lang_tab == "🇺🇸 English":
        displayed_text = english_alert
        voice_text = english_voice
        lang_code = 'en'
    elif lang_tab == "🇫🇷 Français":
        displayed_text = french_alert
        voice_text = french_voice
        lang_code = 'fr'
    else:
        displayed_text = spanish_alert
        voice_text = spanish_voice
        lang_code = 'es'
    
    st.markdown(f'<div class="voice-text">{displayed_text}</div>', unsafe_allow_html=True)
    
    # ---------- Voice Alert: gTTS with robust HTML5 audio ----------
    if st.button("🔊 Play Voice Alert (Female)", use_container_width=True):
        if GTTS_AVAILABLE:
            with st.spinner("🔊 Generating voice with gTTS... Please wait."):
                try:
                    # Generate speech
                    tts = gTTS(text=voice_text, lang=lang_code, slow=False)
                    audio_bytes = BytesIO()
                    tts.write_to_fp(audio_bytes)
                    audio_bytes.seek(0)
                    
                    # Encode to base64
                    audio_base64 = base64.b64encode(audio_bytes.read()).decode()
                    
                    # Create a robust HTML5 audio player with preload, autoplay, and fallback
                    audio_html = f"""
                    <div style="margin: 10px 0;">
                        <audio id="myAudio" controls preload="auto" style="width: 100%;">
                            <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
                            Your browser does not support the audio element.
                        </audio>
                        <p style="color: #aaaaaa; font-size: 0.8rem;">
                            💡 If the audio doesn't play automatically, click the play button above.
                        </p>
                        <script>
                            var audio = document.getElementById('myAudio');
                            audio.addEventListener('canplaythrough', function() {{
                                audio.play();
                            }});
                            // If autoplay is blocked, user can still press play.
                        </script>
                    </div>
                    """
                    st.markdown(audio_html, unsafe_allow_html=True)
                    st.success("✅ Audio loaded. It will play once fully loaded.")
                except Exception as e:
                    st.error(f"❌ gTTS error: {e}")
                    st.info("💡 Falling back to browser speech synthesis...")
                    # Fallback: browser TTS
                    escaped_text = voice_text.replace("`", "\\`").replace("'", "\\'")
                    js_code = f"""
                    <script>
                    const utterance = new SpeechSynthesisUtterance(`{escaped_text}`);
                    utterance.lang = '{lang_code}';
                    utterance.rate = 0.9;
                    utterance.pitch = 1.1;
                    function findFemaleVoice() {{
                        const voices = speechSynthesis.getVoices();
                        for (let v of voices) {{
                            if (v.lang.startsWith('{lang_code}') && v.name.toLowerCase().includes('female')) {{
                                return v;
                            }}
                        }}
                        return voices.find(v => v.lang.startsWith('{lang_code}')) || null;
                    }}
                    function speak() {{
                        const voice = findFemaleVoice();
                        if (voice) utterance.voice = voice;
                        speechSynthesis.speak(utterance);
                    }}
                    if (speechSynthesis.getVoices().length > 0) speak();
                    else speechSynthesis.onvoiceschanged = speak;
                    </script>
                    """
                    st.components.v1.html(js_code, height=0)
                    st.success("🔊 Voice playing via browser fallback!")
        else:
            # gTTS not available – use browser TTS directly
            st.info("💡 gTTS not available. Using browser speech synthesis.")
            escaped_text = voice_text.replace("`", "\\`").replace("'", "\\'")
            js_code = f"""
            <script>
            const utterance = new SpeechSynthesisUtterance(`{escaped_text}`);
            utterance.lang = '{lang_code}';
            utterance.rate = 0.9;
            utterance.pitch = 1.1;
            function findFemaleVoice() {{
                const voices = speechSynthesis.getVoices();
                for (let v of voices) {{
                    if (v.lang.startsWith('{lang_code}') && v.name.toLowerCase().includes('female')) {{
                        return v;
                    }}
                }}
                return voices.find(v => v.lang.startsWith('{lang_code}')) || null;
            }}
            function speak() {{
                const voice = findFemaleVoice();
                if (voice) utterance.voice = voice;
                speechSynthesis.speak(utterance);
            }}
            if (speechSynthesis.getVoices().length > 0) speak();
            else speechSynthesis.onvoiceschanged = speak;
            </script>
            """
            st.components.v1.html(js_code, height=0)
            st.success("🔊 Voice playing via browser!")
    
    st.markdown("---")
    
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
    st.caption("🚨 Alert System v3.0")
    st.caption("Brought to you by GlobalInternet.py")

# ---------- TRANSLATIONS FOR MAIN CONTENT ----------
if lang_tab == "🇺🇸 English":
    title_text = "🚨 ALERT FOR DIGICEL HAITI"
    subtitle_text = "⚠️ Internet Connection is NOT Working ⚠️"
    warning_title = "⚠️ URGENT ALERT"
    warning_text = """Digicel Haiti users in the Southern region are experiencing critical internet connectivity issues. Internet plans are not working, causing financial losses and inability to use social media. This issue has been ongoing for over 3 years."""
    city_heading = "📍 Affected Cities in Southern Haiti"
    footer_alert = "⚠️ This is a public alert for Digicel Haiti users. If you are experiencing internet issues, please contact Digicel customer support."
    footer_copyright = f"© 2026 GlobalInternet.py | Alert System v3.0 | Built with ❤️ in Haiti"

elif lang_tab == "🇫🇷 Français":
    title_text = "🚨 ALERTE POUR DIGICEL HAÏTI"
    subtitle_text = "⚠️ La connexion Internet ne fonctionne PAS ⚠️"
    warning_title = "⚠️ ALERTE URGENTE"
    warning_text = """Les utilisateurs de Digicel Haïti dans la région Sud rencontrent de graves problèmes de connectivité Internet. Les forfaits Internet ne fonctionnent pas, ce qui entraîne des pertes financières et l'impossibilité d'utiliser les réseaux sociaux. Ce problème dure depuis plus de 3 ans."""
    city_heading = "📍 Villes touchées dans le Sud d'Haïti"
    footer_alert = "⚠️ Ceci est une alerte publique pour les utilisateurs de Digicel Haïti. Si vous rencontrez des problèmes Internet, veuillez contacter le service client de Digicel."
    footer_copyright = f"© 2026 GlobalInternet.py | Système d'alerte v3.0 | Construit avec ❤️ en Haïti"

else:  # Spanish
    title_text = "🚨 ALERTA PARA DIGICEL HAITÍ"
    subtitle_text = "⚠️ La conexión a Internet NO funciona ⚠️"
    warning_title = "⚠️ ALERTA URGENTE"
    warning_text = """Los usuarios de Digicel Haití en la región Sur están experimentando problemas críticos de conectividad a Internet. Los planes de Internet no funcionan, lo que provoca pérdidas financieras y la imposibilidad de usar redes sociales. Este problema ha persistido durante más de 3 años."""
    city_heading = "📍 Ciudades afectadas en el Sur de Haití"
    footer_alert = "⚠️ Esta es una alerta pública para los usuarios de Digicel Haití. Si está experimentando problemas de Internet, comuníquese con el servicio al cliente de Digicel."
    footer_copyright = f"© 2026 GlobalInternet.py | Sistema de alerta v3.0 | Hecho con ❤️ en Haití"

# ---------- Main Content ----------
st.markdown(f'<div class="main-title">{title_text}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="sub-title">{subtitle_text}</div>', unsafe_allow_html=True)

st.markdown(f"""
<div class="warning-box">
    <h3 style="color: #FF4444; margin: 0;">{warning_title}</h3>
    <p style="color: #DDDDDD; margin: 10px 0 0 0;">{warning_text}</p>
</div>
""", unsafe_allow_html=True)

st.markdown(f'<h2 class="city-heading">{city_heading}</h2>', unsafe_allow_html=True)

southern_cities = [
    "Grand Goâve", "Jacmel", "Kenscoff", "Bainet", "Grand-Gosier",
    "Les Cayes", "Chantal", "Cavaillon", "Roche-à-Bateaux", "Petit-Trou-de-Nippes",
    "Fonds-des-Nègres", "Arnaud", "Saint-Marc (South Region)", "Chambellan", "Bonbon",
    "Beaumont", "Trouin", "Ganthier", "Cornillon (South)", "Petit-Goâve",
    "Cayes-Jacmel", "Fonds-Verrettes", "Côte-de-Fer", "Anse-à-Pitres", "Camp-Perrin",
    "Maniche", "Saint-Louis-du-Sud", "Côtes-de-Fer", "Anse-à-Veau", "Paillant",
    "Cap-Haïtien (South Region)", "Les Anglais", "Moron", "Jérémie", "Pestel",
    "Miragoâne", "Croix-des-Bouquets (South)", "Léogâne", "Marigot", "Thiotte",
    "Belle-Anse", "Port-à-Piment", "Torbeck", "Aquin", "Tiburon",
    "Baradères", "Miragoâne", "Petit-Rivière-de-Nippes", "Gonaïves (South Region)",
    "Dame-Marie", "Abricots", "Roseaux", "Corail", "Fonds-Verrettes",
    "Thomazeau (South)"
]

cols = st.columns(3)
for idx, city in enumerate(southern_cities):
    with cols[idx % 3]:
        st.markdown(f'<div class="city-card">📍 {city}</div>', unsafe_allow_html=True)

st.markdown(f'<div class="total-cities">📊 Total affected cities: {len(southern_cities)}</div>', unsafe_allow_html=True)

# ---------- Footer ----------
st.markdown("---")
st.markdown(f"""
<div class="footer-text">
    <p>
        <strong style="color: #FF4444;">{footer_alert}</strong>
    </p>
    <p class="small">
        {footer_copyright}
    </p>
</div>
""", unsafe_allow_html=True)

print("✅ app.py loaded completely and rendered successfully.")
st.success("✅ App ready!")
