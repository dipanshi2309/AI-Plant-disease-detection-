# import os
# import numpy as np
# import tensorflow as tf
# import streamlit as st
# from PIL import Image
# import matplotlib.pyplot as plt
# from datetime import datetime, timedelta
# from disease_info import disease_info
# from streamlit_option_menu import option_menu

# # Set page configuration
# st.set_page_config(
#     page_title="PlantAI - Smart Detection",
#     page_icon="🌱",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # ================= STATE MANAGEMENT & INITIALIZATION =================
# if "theme" not in st.session_state:
#     st.session_state.theme = "Dark Mode"
# if "username" not in st.session_state:
#     st.session_state.username = "Dipanshi"
# if "location" not in st.session_state:
#     st.session_state.location = "New Delhi, IN"
# if "notif_count" not in st.session_state:
#     st.session_state.notif_count = 3
# if "notif_show" not in st.session_state:
#     st.session_state.notif_show = False

# if "history" not in st.session_state:
#     st.session_state.history = [
#         {"disease": "Tomato - Rust", "confidence": 96.0, "time": "2 min ago"},
#         {"disease": "Potato - Early Blight", "confidence": 89.0, "time": "1 hour ago"},
#         {"disease": "Tomato - Leaf Spot", "confidence": 78.0, "time": "2 hours ago"},
#         {"disease": "Healthy Leaf", "confidence": 98.0, "time": "Yesterday"},
#         {"disease": "Tomato - Mosaic Virus", "confidence": 65.0, "time": "2 days ago"}
#     ]

# if "current_result" not in st.session_state:
#     st.session_state.current_result = None

# if "processed_file_id" not in st.session_state:
#     st.session_state.processed_file_id = None


# # ================= THEME STYLING CONFIGURATION =================
# if st.session_state.theme == "Light Mode":
#     bg_app = "#f8fafc"
#     bg_sidebar = "#f1f5f9"
#     border_color = "rgba(15, 23, 42, 0.08)"
#     text_primary = "#0f172a"
#     text_secondary = "#475569"
#     card_bg = "#ffffff"
#     scrollbar_track = "#f1f5f9"
#     scrollbar_thumb = "#cbd5e1"
#     box_shadow = "0 4px 20px rgba(15, 23, 42, 0.05)"
#     card_shadow = "rgba(15, 23, 42, 0.04) 0px 4px 12px"
#     # FIX 1: matplotlib-compatible colors (tuples, not CSS rgba strings)
#     chart_grid_color_mpl = (0.06, 0.09, 0.16, 0.05)
# else:
#     bg_app = "#060c14"
#     bg_sidebar = "#0b121f"
#     border_color = "rgba(255, 255, 255, 0.05)"
#     text_primary = "#cbd5e1"
#     text_secondary = "#94a3b8"
#     card_bg = "#0b121f"
#     scrollbar_track = "#060c14"
#     scrollbar_thumb = "#1e293b"
#     box_shadow = "0 4px 30px rgba(0, 0, 0, 0.4)"
#     card_shadow = "rgba(0, 0, 0, 0.3) 0px 4px 20px"
#     # FIX 1: matplotlib-compatible colors (tuples, not CSS rgba strings)
#     chart_grid_color_mpl = (1.0, 1.0, 1.0, 0.05)

# chart_txt_color = "#cbd5e1" if st.session_state.theme == "Dark Mode" else "#475569"

# st.markdown(f"""
# <style>
# /* Base Theme Overrides */
# [data-testid="stAppViewContainer"] {{
#     background-color: {bg_app} !important;
#     color: {text_primary} !important;
#     font-family: 'Outfit', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
# }}
# [data-testid="stSidebar"] {{
#     background-color: {bg_sidebar} !important;
#     border-right: 1px solid {border_color} !important;
# }}
# [data-testid="stHeader"] {{
#     background-color: {bg_app} !important;
#     opacity: 0.8;
# }}

# /* Hide Streamlit default markers */
# footer {{visibility: hidden;}}
# #MainMenu {{visibility: hidden;}}
# [data-testid="stHeader"] {{visibility: hidden;}}

# /* Custom Scrollbar */
# ::-webkit-scrollbar {{
#     width: 6px;
#     height: 6px;
# }}
# ::-webkit-scrollbar-track {{
#     background: {scrollbar_track};
# }}
# ::-webkit-scrollbar-thumb {{
#     background: {scrollbar_thumb};
#     border-radius: 3px;
# }}
# ::-webkit-scrollbar-thumb:hover {{
#     background: #10b981;
# }}

# /* Native Border Wrapper styling (st.container(border=True)) */
# div[data-testid="stBorderWrapper"] {{
#     background-color: {card_bg} !important;
#     border: 1px solid {border_color} !important;
#     border-radius: 16px !important;
#     box-shadow: {card_shadow} !important;
# }}
# div[data-testid="stBorderWrapper"] > div {{
#     padding: 18px !important;
# }}

# /* Standard text typography colors */
# h1, h2, h3, h4, p, span, table, td, tr, li, ul {{
#     color: inherit !important;
# }}

# .card-title {{
#     font-size: 15px;
#     font-weight: 600;
#     color: {text_secondary} !important;
#     margin-bottom: 15px;
#     display: flex;
#     align-items: center;
#     gap: 8px;
#     border-bottom: 1px solid {border_color};
#     padding-bottom: 8px;
# }}

# /* Styled buttons */
# .stButton>button {{
#     border-radius: 10px !important;
#     background: linear-gradient(135deg, #10b981, #059669) !important;
#     color: white !important;
#     font-size: 14px !important;
#     font-weight: 600 !important;
#     border: none !important;
#     padding: 8px 16px !important;
#     transition: all 0.3s !important;
#     width: 100%;
# }}
# .stButton>button:hover {{
#     background: linear-gradient(135deg, #34d399, #10b981) !important;
#     box-shadow: 0 0 15px rgba(16, 185, 129, 0.4) !important;
#     transform: translateY(-1px);
# }}

# /* Custom Header specific buttons overrides */
# div.header-section div[data-testid="column"]:nth-child(2) button {{
#     border-radius: 50% !important;
#     width: 36px !important;
#     height: 36px !important;
#     background-color: rgba(30, 41, 59, 0.2) !important;
#     color: #fbbf24 !important;
#     border: 1px solid {border_color} !important;
#     display: flex !important;
#     align-items: center !important;
#     justify-content: center !important;
#     padding: 0 !important;
#     min-width: 36px !important;
# }}
# div.header-section div[data-testid="column"]:nth-child(3) button {{
#     border-radius: 50% !important;
#     width: 36px !important;
#     height: 36px !important;
#     background-color: rgba(30, 41, 59, 0.2) !important;
#     color: #10b981 !important;
#     border: 1px solid {border_color} !important;
#     display: flex !important;
#     align-items: center !important;
#     justify-content: center !important;
#     padding: 0 !important;
#     min-width: 36px !important;
# }}
# div.header-section div[data-testid="column"]:nth-child(4) button {{
#     border-radius: 20px !important;
#     height: 36px !important;
#     background-color: rgba(30, 41, 59, 0.2) !important;
#     color: {text_primary} !important;
#     border: 1px solid {border_color} !important;
#     padding: 5px 15px !important;
#     font-size: 13px !important;
#     font-weight: 500 !important;
#     text-align: center !important;
#     min-width: 100px !important;
# }}

# /* Warning/Red Button Override */
# div.clear-btn-container button {{
#     background: transparent !important;
#     color: #ef4444 !important;
#     border: 1px solid rgba(239, 68, 68, 0.2) !important;
#     font-size: 13px !important;
#     padding: 6px 12px !important;
# }}
# div.clear-btn-container button:hover {{
#     background: rgba(239, 68, 68, 0.1) !important;
#     border-color: #ef4444 !important;
#     box-shadow: none !important;
# }}

# /* File Uploader styling */
# [data-testid="stFileUploader"] {{
#     background-color: rgba(30, 41, 59, 0.15);
#     border: 1px dashed {border_color};
#     border-radius: 12px;
#     padding: 8px;
# }}

# /* Custom badges */
# .badge {{
#     display: inline-block;
#     padding: 3px 10px;
#     border-radius: 20px;
#     font-size: 11px;
#     font-weight: bold;
#     text-align: center;
# }}
# .badge-green {{ background-color: rgba(16, 185, 129, 0.15) !important; color: #10b981 !important; }}
# .badge-orange {{ background-color: rgba(245, 158, 11, 0.15) !important; color: #f59e0b !important; }}
# .badge-red {{ background-color: rgba(239, 68, 68, 0.15) !important; color: #ef4444 !important; }}
# .badge-blue {{ background-color: rgba(59, 130, 246, 0.15) !important; color: #3b82f6 !important; }}
# .badge-purple {{ background-color: rgba(139, 92, 246, 0.15) !important; color: #8b5cf6 !important; }}
# </style>
# """, unsafe_allow_html=True)


# # ================= DISEASE DATABASE & METADATA =================
# DISEASE_METADATA = {
#     "Pepper__bell___Bacterial_spot": {
#         "display_name": "Pepper Bell - Bacterial Spot",
#         "category": "Bacterial Disease",
#         "scientific_name": "Xanthomonas campestris pv. vesicatoria",
#         "affects": "Pepper Plants",
#         "severity": "Moderate to High",
#         "description": "Bacterial disease causing dark, water-soaked spots on pepper leaves, which eventually turn brown, dry up, and fall off.",
#         "treatment": [
#             "Apply copper-based bactericides early in the disease cycle.",
#             "Remove and destroy heavily infected leaves and plants.",
#             "Avoid overhead watering to minimize bacterial splash and spread."
#         ],
#         "prevention": [
#             "Use certified disease-free seeds and transplants.",
#             "Practice crop rotation with non-solanaceous crops.",
#             "Space plants properly to improve canopy air circulation."
#         ]
#     },
#     "Pepper__bell___healthy": {
#         "display_name": "Pepper Bell - Healthy",
#         "category": "Healthy Plant",
#         "scientific_name": "Capsicum annuum",
#         "affects": "Pepper Plants",
#         "severity": "None",
#         "description": "The pepper plant shows no signs of bacterial or fungal infection. Leaves are vibrant green and healthy.",
#         "treatment": [
#             "No chemical or disease treatment required.",
#             "Maintain standard fertilization and watering schedule.",
#             "Inspect foliage regularly for early signs of pests."
#         ],
#         "prevention": [
#             "Provide regular watering at the base of the plant.",
#             "Ensure full sun exposure (6-8 hours daily).",
#             "Maintain soil nutrient balance with organic compost."
#         ]
#     },
#     "Potato___Early_blight": {
#         "display_name": "Potato - Early Blight",
#         "category": "Fungal Disease",
#         "scientific_name": "Alternaria solani",
#         "affects": "Potato Plants",
#         "severity": "Moderate",
#         "description": "A common fungal disease characterized by dark brown spots with concentric rings (target-board pattern) on older leaves.",
#         "treatment": [
#             "Apply protective fungicides containing chlorothalonil or mancozeb.",
#             "Remove lower infected leaves to reduce spore splash.",
#             "Ensure balanced fertilization to keep plants vigorous."
#         ],
#         "prevention": [
#             "Rotate crops annually with non-host families.",
#             "Use drip irrigation to keep leaf surfaces dry.",
#             "Destroy crop residues after harvest."
#         ]
#     },
#     "Potato___Late_blight": {
#         "display_name": "Potato - Late Blight",
#         "category": "Fungal/Oomycete Disease",
#         "scientific_name": "Phytophthora infestans",
#         "affects": "Potato Plants",
#         "severity": "High",
#         "description": "A highly destructive disease causing dark, water-soaked lesions on leaves and stems, which can kill plants rapidly in cool, wet weather.",
#         "treatment": [
#             "Apply systemic fungicides immediately upon detection.",
#             "Remove and destroy infected plants to prevent field-wide outbreak.",
#             "Avoid harvesting tubers until vines have been dead for two weeks."
#         ],
#         "prevention": [
#             "Plant only certified disease-free seed tubers.",
#             "Choose resistant potato cultivars.",
#             "Ensure proper spacing for ventilation and quick drying."
#         ]
#     },
#     "Potato___healthy": {
#         "display_name": "Potato - Healthy",
#         "category": "Healthy Plant",
#         "scientific_name": "Solanum tuberosum",
#         "affects": "Potato Plants",
#         "severity": "None",
#         "description": "The potato plant is healthy, showing vigorous leaf and stem development with no leaf lesions.",
#         "treatment": [
#             "No treatment necessary.",
#             "Continue standard watering hilling practices.",
#             "Apply organic mulches to protect soil moisture."
#         ],
#         "prevention": [
#             "Ensure proper soil drainage to avoid root rot.",
#             "Rotate crops regularly to maintain soil health.",
#             "Monitor regularly for pests like potato beetles."
#         ]
#     },
#     "Tomato_Bacterial_spot": {
#         "display_name": "Tomato - Bacterial Spot",
#         "category": "Bacterial Disease",
#         "scientific_name": "Xanthomonas perforans",
#         "affects": "Tomato Plants",
#         "severity": "Moderate to High",
#         "description": "Bacterial infection causing small, dark, circular spots on leaves and stems, often surrounded by a yellow halo.",
#         "treatment": [
#             "Apply copper-based sprays mixed with mancozeb.",
#             "Prune infected lower branches to improve ventilation.",
#             "Do not work in the garden when the plants are wet."
#         ],
#         "prevention": [
#             "Use disease-free seeds and certified transplants.",
#             "Avoid overhead watering and irrigate at the soil level.",
#             "Practice a 2-3 year crop rotation sequence."
#         ]
#     },
#     "Tomato_Early_blight": {
#         "display_name": "Tomato - Early Blight",
#         "category": "Fungal Disease",
#         "scientific_name": "Alternaria solani",
#         "affects": "Tomato Plants",
#         "severity": "Moderate",
#         "description": "Dark concentric rings on older leaves that can cause early leaf drop, exposing fruit to sunscald.",
#         "treatment": [
#             "Apply copper-based fungicides or bio-fungicides.",
#             "Prune lower leaves to prevent soil-borne spores from splashing up.",
#             "Mulch around the base of plants to create a barrier."
#         ],
#         "prevention": [
#             "Provide consistent base watering.",
#             "Maintain space between plants for airflow.",
#             "Clean up all garden debris at the end of the season."
#         ]
#     },
#     "Tomato_Late_blight": {
#         "display_name": "Tomato - Late Blight",
#         "category": "Fungal/Oomycete Disease",
#         "scientific_name": "Phytophthora infestans",
#         "affects": "Tomato Plants",
#         "severity": "High",
#         "description": "Causes rapid foliage decay and dark, greasy lesions on tomato fruits, leading to complete plant collapse.",
#         "treatment": [
#             "Remove and destroy infected plants immediately.",
#             "Apply preventive copper fungicides to surrounding plants.",
#             "Avoid composting infected plant material."
#         ],
#         "prevention": [
#             "Plant resistant tomato cultivars.",
#             "Space plants widely and prune suckers to improve drying.",
#             "Water early in the day so foliage dries quickly."
#         ]
#     },
#     "Tomato_Leaf_Mold": {
#         "display_name": "Tomato - Leaf Mold",
#         "category": "Fungal Disease",
#         "scientific_name": "Passalora fulva",
#         "affects": "Tomato Plants",
#         "severity": "Low to Moderate",
#         "description": "Yellow patches on upper leaf surfaces with olive-green velvety growth underneath, typically under high humidity.",
#         "treatment": [
#             "Reduce greenhouse or canopy humidity below 85%.",
#             "Apply protective fungicides containing copper or sulfur.",
#             "Prune lower foliage to enhance air movement."
#         ],
#         "prevention": [
#             "Improve greenhouse ventilation using fans.",
#             "Space plants widely and avoid overhead watering.",
#             "Grow resistant tomato cultivars."
#         ]
#     },
#     "Tomato_Septoria_leaf_spot": {
#         "display_name": "Tomato - Septoria Leaf Spot",
#         "category": "Fungal Disease",
#         "scientific_name": "Septoria lycopersici",
#         "affects": "Tomato Plants",
#         "severity": "Moderate",
#         "description": "Fungal disease causing numerous small, circular leaf spots with dark borders and grey/white centers.",
#         "treatment": [
#             "Remove infected leaves immediately to contain spread.",
#             "Apply copper-based fungicides or chlorothalonil.",
#             "Apply organic mulch around the plant base."
#         ],
#         "prevention": [
#             "Irrigate at ground level using drip lines.",
#             "Rotate crops annually to avoid overwintering spores.",
#             "Clean stakes, cages, and tools after use."
#         ]
#     },
#     "Tomato_Spider_mites_Two_spotted_spider_mite": {
#         "display_name": "Tomato - Spider Mites",
#         "category": "Pest Infestation",
#         "scientific_name": "Tetranychus urticae",
#         "affects": "Tomato Plants",
#         "severity": "Moderate to High",
#         "description": "Tiny spider-like pests causing fine white/yellow stippling on leaves and webbing under leaves, leading to leaf drop.",
#         "treatment": [
#             "Spray plants with insecticidal soaps or neem oil.",
#             "Introduce natural predators like predatory mites.",
#             "Wash foliage with a strong stream of water to dislodge mites."
#         ],
#         "prevention": [
#             "Monitor foliage regularly, especially during dry, hot weather.",
#             "Keep plants well-hydrated to reduce stress.",
#             "Maintain humidity around plants."
#         ]
#     },
#     "Tomato__Target_Spot": {
#         "display_name": "Tomato - Target Spot",
#         "category": "Fungal Disease",
#         "scientific_name": "Corynespora cassiicola",
#         "affects": "Tomato Plants",
#         "severity": "Moderate",
#         "description": "Concentric circle lesions similar to early blight but spots are smaller and can spread to stems and fruits.",
#         "treatment": [
#             "Apply fungicides like chlorothalonil or mancozeb.",
#             "Remove and destroy infected lower foliage.",
#             "Avoid overhead irrigation."
#         ],
#         "prevention": [
#             "Maintain proper spacing and airflow.",
#             "Rotate crops with non-host species.",
#             "Ensure weed management around the garden."
#         ]
#     },
#     "Tomato__Tomato_YellowLeaf__Curl_Virus": {
#         "display_name": "Tomato - Yellow Leaf Curl",
#         "category": "Viral Disease",
#         "scientific_name": "Tomato yellow leaf curl virus (TYLCV)",
#         "affects": "Tomato Plants",
#         "severity": "High",
#         "description": "Viral disease transmitted by whiteflies causing severe stunting, yellowing, and upward leaf curling.",
#         "treatment": [
#             "No chemical cure; control the whitefly vector population.",
#             "Use yellow sticky cards to trap whiteflies.",
#             "Spray with neem oil or systemic insecticides to control whiteflies."
#         ],
#         "prevention": [
#             "Plant resistant tomato cultivars.",
#             "Use row covers or insect netting on young plants.",
#             "Destroy virus-infected plants immediately to prevent spread."
#         ]
#     },
#     "Tomato__Tomato_mosaic_virus": {
#         "display_name": "Tomato - Mosaic Virus",
#         "category": "Viral Disease",
#         "scientific_name": "Tomato mosaic virus (ToMV)",
#         "affects": "Tomato Plants",
#         "severity": "High",
#         "description": "Highly contagious viral disease causing mottled dark green and yellow patterns, distorted leaf shapes, and stunted growth.",
#         "treatment": [
#             "No chemical cure exists; pull out and burn infected plants.",
#             "Do not touch healthy plants after handling infected ones.",
#             "Wash hands and tools with soap and hot water."
#         ],
#         "prevention": [
#             "Purchase certified virus-free seeds.",
#             "Avoid planting in soil where infected plants grew recently.",
#             "Do not smoke near tomato plants as tobacco can carry mosaic viruses."
#         ]
#     },
#     "Tomato_healthy": {
#         "display_name": "Tomato - Healthy",
#         "category": "Healthy Plant",
#         "scientific_name": "Solanum lycopersicum",
#         "affects": "Tomato Plants",
#         "severity": "None",
#         "description": "The tomato plant is healthy. Leaves are robust, green, and free of any fungal, bacterial, or viral spots.",
#         "treatment": [
#             "No treatment required.",
#             "Continue standard watering, pruning, and staking.",
#             "Apply slow-release fertilizer for continuous nutrition."
#         ],
#         "prevention": [
#             "Ensure full sun exposure (6-8 hours daily).",
#             "Maintain base watering schedule to avoid leaf moisture.",
#             "Inspect leaf undersides weekly for pests."
#         ]
#     }
# }

# def get_disease_metadata(class_name):
#     if class_name in DISEASE_METADATA:
#         return DISEASE_METADATA[class_name]
#     elif class_name in disease_info:
#         info = disease_info[class_name]
#         return {
#             "display_name": class_name.replace("_", " "),
#             "category": "Disease Model",
#             "scientific_name": "N/A",
#             "affects": "Plants",
#             "severity": "Moderate",
#             "description": info.get("description", ""),
#             "treatment": [info.get("treatment", "")],
#             "prevention": [info.get("prevention", "")]
#         }
#     else:
#         return {
#             "display_name": class_name.replace("_", " "),
#             "category": "Unknown",
#             "scientific_name": "N/A",
#             "affects": "Plants",
#             "severity": "Unknown",
#             "description": "No details available.",
#             "treatment": ["N/A"],
#             "prevention": ["N/A"]
#         }


# # ================= WEATHER DATA =================
# WEATHER_DATA = {
#     "New Delhi, IN": {
#         "temp": "30°C",
#         "condition": "Partly Cloudy",
#         "humidity": "65%",
#         "wind": "12 km/h",
#         "feels": "33°C",
#         "icon": """
#         <svg width="32" height="32" viewBox="0 0 24 24">
#             <circle cx="10" cy="10" r="4" fill="#f59e0b" />
#             <path d="M12 14.5a3.5 3.5 0 0 1 0-7 3.5 3.5 0 0 1 5.5-2.5 3.5 3.5 0 0 1 1 5 3.5 3.5 0 0 1-6.5 4.5z" fill="#94a3b8" opacity="0.8" />
#         </svg>
#         """
#     },
#     "Mumbai, IN": {
#         "temp": "28°C",
#         "condition": "Heavy Rain",
#         "humidity": "85%",
#         "wind": "22 km/h",
#         "feels": "32°C",
#         "icon": """
#         <svg width="32" height="32" viewBox="0 0 24 24">
#             <path d="M12 14.5a3.5 3.5 0 0 1 0-7 3.5 3.5 0 0 1 5.5-2.5 3.5 3.5 0 0 1 1 5 3.5 3.5 0 0 1-6.5 4.5z" fill="#94a3b8" />
#             <path d="M8 17v3M12 17v3M16 17v3" stroke="#3b82f6" stroke-width="2" stroke-linecap="round" />
#         </svg>
#         """
#     },
#     "London, UK": {
#         "temp": "18°C",
#         "condition": "Light Drizzle",
#         "humidity": "75%",
#         "wind": "15 km/h",
#         "feels": "17°C",
#         "icon": """
#         <svg width="32" height="32" viewBox="0 0 24 24">
#             <path d="M12 14.5a3.5 3.5 0 0 1 0-7 3.5 3.5 0 0 1 5.5-2.5 3.5 3.5 0 0 1 1 5 3.5 3.5 0 0 1-6.5 4.5z" fill="#94a3b8" />
#             <path d="M10 17v2M14 17v2" stroke="#cbd5e1" stroke-width="1.5" stroke-linecap="round" />
#         </svg>
#         """
#     },
#     "New York, US": {
#         "temp": "22°C",
#         "condition": "Clear & Sunny",
#         "humidity": "50%",
#         "wind": "10 km/h",
#         "feels": "22°C",
#         "icon": """
#         <svg width="32" height="32" viewBox="0 0 24 24">
#             <circle cx="12" cy="12" r="6" fill="#f59e0b" />
#             <path d="M12 2v2M12 20v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M2 12h2M20 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42" stroke="#f59e0b" stroke-width="2" />
#         </svg>
#         """
#     }
# }


# # ================= MODEL UTILITIES =================
# @st.cache_resource
# def load_model():
#     model_path = "plant_disease_model.h5"
#     if os.path.exists(model_path):
#         return tf.keras.models.load_model(model_path)
#     return None

# model = load_model()

# # Load labels list
# with open("labels.txt", "r") as f:
#     classes = [line.strip() for line in f.readlines()]


# # ================= SIDEBAR LAYOUT =================
# with st.sidebar:
#     # Sidebar Header
#     st.markdown("""
#     <div style="padding: 10px 0; display: flex; align-items: center; gap: 12px; margin-bottom: 10px;">
#         <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#10b981" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
#             <path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 3.5 1 9.8a7 7 0 0 1-9 8.2z"/>
#             <path d="M9 22v-4H5a2 2 0 0 1-2-2V6"/>
#         </svg>
#         <div>
#             <span style="font-size: 22px; font-weight: bold; color: inherit;">Plant<span style="color: #10b981;">AI</span></span><br>
#             <span style="font-size: 11px; color: #64748b; font-weight: 500;">Smart Detection</span>
#         </div>
#     </div>
#     """, unsafe_allow_html=True)

#     # Sidebar Navigation Menu
#     selected = option_menu(
#         menu_title=None,
#         options=[
#             "Home",
#             "Predict Disease",
#             "Disease Library",
#             "Statistics",
#             "History",
#             "Plant Care Tips",
#             "Settings",
#             "About Us"
#         ],
#         icons=[
#             "house-door-fill",
#             "search",
#             "journal-bookmark-fill",
#             "bar-chart-line-fill",
#             "clock-history",
#             "lightbulb-fill",
#             "gear-fill",
#             "info-circle-fill"
#         ],
#         default_index=0,
#         styles={
#             "container": {"padding": "0!important", "background-color": "transparent"},
#             "icon": {"color": "#64748b", "font-size": "15px"},
#             "nav-link": {"font-size": "14px", "text-align": "left", "margin":"2px 0px", "color": "#94a3b8", "border-radius": "10px", "padding": "10px 15px"},
#             "nav-link-selected": {"background": "linear-gradient(135deg, #10b981, #059669)", "color": "white", "font-weight": "bold"},
#         }
#     )

#     # Recent Predictions Card
#     with st.container(border=True):
#         st.markdown('<div style="font-size: 13px; font-weight: 600; color: inherit; margin-bottom: 12px;">Recent Predictions</div>', unsafe_allow_html=True)

#         for idx, item in enumerate(st.session_state.history[:5]):
#             conf = item['confidence']
#             badge_class = "badge-green" if conf >= 90 else ("badge-orange" if conf >= 75 else "badge-red")

#             st.markdown(f"""
#             <div style="display: flex; justify-content: space-between; align-items: center; background: rgba(30, 41, 59, 0.15); padding: 8px 12px; border-radius: 10px; margin-bottom: 8px; border: 1px solid {border_color};">
#                 <div>
#                     <div style="font-size: 12px; font-weight: bold; color: inherit;">{item['disease']}</div>
#                     <div style="font-size: 10px; color: #64748b;">{item['time']}</div>
#                 </div>
#                 <span class="badge {badge_class}">{conf:.0f}%</span>
#             </div>
#             """, unsafe_allow_html=True)

#         st.markdown('<div class="clear-btn-container" style="margin-top: 10px;">', unsafe_allow_html=True)
#         if st.button("🗑 Clear History", key="clear_history_btn"):
#             st.session_state.history = []
#             st.rerun()
#         st.markdown('</div>', unsafe_allow_html=True)

#     # Plant Care Tip Card
#     with st.container(border=True):
#         st.markdown("""
#         <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
#             <svg width="18" height="18" fill="none" stroke="#10b981" stroke-width="2" viewBox="0 0 24 24"><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41"/></svg>
#             <span style="color: inherit; font-size: 13px; font-weight: bold;">Plant Care Tip</span>
#         </div>
#         <p style="color: inherit; font-size: 11.5px; opacity:0.8; line-height: 1.5; margin: 0 0 10px 0;">
#             Ensure your plants get enough sunlight (6-8 hours daily) and maintain proper soil moisture for healthy growth.
#         </p>
#         <div style="text-align: center;">
#             <svg width="60" height="30" viewBox="0 0 100 50">
#                 <path d="M50 50 L50 20 Q40 10 30 20 Q40 25 50 50" fill="#047857" />
#                 <path d="M50 50 L50 15 Q60 5 70 15 Q60 20 50 50" fill="#10b981" />
#                 <path d="M35 50 L65 50 L60 42 L40 42 Z" fill="#b45309" />
#             </svg>
#         </div>
#         """, unsafe_allow_html=True)

#     # Weather Widget
#     weather = WEATHER_DATA.get(st.session_state.location, WEATHER_DATA["New Delhi, IN"])
#     with st.container(border=True):
#         # FIX 3: Build weather HTML with explicit string concatenation to avoid rendering issues
#         weather_html = (
#             f'<div style="font-size: 11px; color: inherit; font-weight: bold; margin-bottom: 8px; display: flex; align-items: center; gap: 4px;">'
#             f'<svg width="12" height="12" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M12 2a8 8 0 0 0-8 8c0 5.25 8 12 8 12s8-6.75 8-12a8 8 0 0 0-8-8z"/><circle cx="12" cy="10" r="3"/></svg>'
#             f'{st.session_state.location}</div>'
#             f'<div style="display: flex; align-items: center; gap: 15px; margin-bottom: 8px;">'
#             f'{weather["icon"]}'
#             f'<div>'
#             f'<span style="font-size: 22px; font-weight: bold; color: inherit;">{weather["temp"]}</span><br>'
#             f'<span style="font-size: 11px; color: inherit; opacity:0.8;">{weather["condition"]}</span>'
#             f'</div></div>'
#             f'<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 4px; font-size: 10.5px; color: inherit; opacity:0.7; border-top: 1px solid {border_color}; padding-top: 8px;">'
#             f'<div>Humidity: <strong style="color: inherit;">{weather["humidity"]}</strong></div>'
#             f'<div>Wind: <strong style="color: inherit;">{weather["wind"]}</strong></div>'
#             f'<div style="grid-column: span 2; margin-top: 2px;">Feels like: <strong style="color: inherit;">{weather["feels"]}</strong></div>'
#             f'</div>'
#         )
#         st.markdown(weather_html, unsafe_allow_html=True)


# # ================= CORE INTERFACES =================

# # --- HELPER SVG GENERATORS ---
# def get_circular_gauge_svg(confidence, rating):
#     circumference = 439.82
#     offset = circumference * (1 - confidence / 100)
#     color = "rgba(255, 255, 255, 0.1)" if confidence == 0.0 else ("#10b981" if confidence >= 90 else ("#f59e0b" if confidence >= 75 else "#ef4444"))

#     return f"""
#     <svg width="100%" height="160" viewBox="0 0 200 200" style="display: block; margin: auto;">
#         <circle cx="100" cy="100" r="70" fill="none" stroke="rgba(255,255,255,0.03)" stroke-width="12" />
#         <circle cx="100" cy="100" r="70" fill="none" stroke="{color}" stroke-width="12"
#                 stroke-dasharray="{circumference}" stroke-dashoffset="{offset}"
#                 stroke-linecap="round" transform="rotate(-90 100 100)" />
#         <text x="100" y="95" fill="currentColor" font-size="36" font-weight="bold" text-anchor="middle" dominant-baseline="middle">{confidence:.0f}%</text>
#         <text x="100" y="130" fill="{color if confidence > 0.0 else '#64748b'}" font-size="11" font-weight="bold" text-anchor="middle" dominant-baseline="middle">{rating}</text>
#     </svg>
#     """

# def get_donut_chart_svg(data):
#     total = sum(d[1] for d in data)
#     r = 60
#     circumference = 2 * 3.14159265 * r

#     svg_elements = []
#     current_offset = 0

#     for label, count, color in data:
#         percentage = (count / total) * 100 if total > 0 else 0
#         arc_len = circumference * (percentage / 100)
#         dash_array = f"{arc_len} {circumference - arc_len}"

#         svg_elements.append(f"""
#         <circle cx="100" cy="100" r="{r}" fill="none" stroke="{color}" stroke-width="14"
#                 stroke-dasharray="{dash_array}" stroke-dashoffset="{-current_offset}"
#                 transform="rotate(-90 100 100)" />
#         """)
#         current_offset += arc_len

#     return f"""
#     <svg width="100%" height="165" viewBox="0 0 200 200" style="display: block; margin: auto;">
#         {"".join(svg_elements)}
#         <circle cx="100" cy="100" r="48" fill="{card_bg}" />
#         <text x="100" y="92" fill="white" font-size="28" font-weight="bold" text-anchor="middle" dominant-baseline="middle">{total}</text>
#         <text x="100" y="116" fill="#94a3b8" font-size="11" text-anchor="middle" dominant-baseline="middle">Total</text>
#     </svg>
#     """


# # ================= PAGE ROUTING =================

# if selected in ["Home", "Predict Disease"]:
#     # ---------------- HEADER SECTION ----------------
#     st.markdown('<div class="header-section">', unsafe_allow_html=True)
#     head_col1, head_col2, head_col3, head_col4 = st.columns([5, 0.6, 0.6, 1.2])
#     with head_col1:
#         st.markdown(f"""
#         <h1 style='margin: 0; font-size: 28px; font-weight: 700; color: inherit;'>
#             🌿 AI Plant Disease Detection <span style='color: #10b981;'>Dashboard</span>
#         </h1>
#         <p style='color: #94a3b8; font-size: 13.5px; margin: 5px 0 20px 0;'>
#             Upload a leaf image and get instant disease prediction with treatment and prevention tips.
#         </p>
#         """, unsafe_allow_html=True)

#     with head_col2:
#         theme_icon = "☀️" if st.session_state.theme == "Dark Mode" else "🌙"
#         if st.button(theme_icon, key="header_theme_toggle", help="Toggle Light/Dark Theme"):
#             st.session_state.theme = "Light Mode" if st.session_state.theme == "Dark Mode" else "Dark Mode"
#             st.rerun()

#     with head_col3:
#         if st.button("🔔", key="header_notif_btn", help=f"You have {st.session_state.notif_count} notifications"):
#             st.session_state.notif_show = not st.session_state.notif_show
#             st.rerun()

#     with head_col4:
#         if st.button(f"👤 {st.session_state.username}", key="header_user_btn", help="Click to rename in Settings"):
#             pass

#     st.markdown('</div>', unsafe_allow_html=True)

#     # ---------------- NOTIFICATION POPUP ----------------
#     if st.session_state.notif_show:
#         st.markdown("""
#         <div style="background-color: rgba(30, 41, 59, 0.9); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 10px; padding: 15px; margin-bottom: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.5); z-index: 1000; position:relative;">
#             <div style="font-weight: bold; color: #10b981; margin-bottom: 8px; font-size: 14px;">🔔 Notifications</div>
#             <div style="font-size: 12.5px; color: inherit; display:flex; flex-direction:column; gap:8px;">
#                 <div>• <strong>System Update:</strong> PlantAI classification engine updated to v2.0.</div>
#                 <div>• <strong>Weather Alert:</strong> High humidity detected in Mumbai/New Delhi; monitor leaves for early symptoms.</div>
#                 <div>• <strong>History Cleared:</strong> Prediction logs cleared successfully.</div>
#             </div>
#         </div>
#         """, unsafe_allow_html=True)

#     # ---------------- DYNAMIC UPLOADER INTEGRATION ----------------
#     row1_col1, row1_col2 = st.columns([1.2, 1])

#     res = st.session_state.current_result
#     if res is None:
#         res = {
#             "disease": "Waiting for Leaf Scan",
#             "confidence": 0.0,
#             "category": "N/A",
#             "scientific_name": "N/A",
#             "affects": "N/A",
#             "severity": "N/A",
#             "description": "Please upload a leaf image of Pepper, Potato, or Tomato in the upload panel to run the AI diagnosis.",
#             "treatment": ["No treatments recommended yet. Please upload a leaf image."],
#             "prevention": ["No prevention guidelines available. Please upload a leaf image."],
#             "top3": [
#                 ("-", 0.0),
#                 ("-", 0.0),
#                 ("-", 0.0)
#             ]
#         }

#     uploaded_file = None
#     camera_file = None

#     with row1_col1:
#         with st.container(border=True):
#             st.markdown('<div class="card-title"><svg width="16" height="16" fill="none" stroke="#10b981" stroke-width="2" viewBox="0 0 24 24" style="display:inline; margin-right:5px;"><path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"/><circle cx="12" cy="13" r="4"/></svg> Upload Leaf Image</div>', unsafe_allow_html=True)

#             if "image" in res:
#                 st.image(res["image"], caption="Uploaded Leaf Image", use_container_width=True)
#             else:
#                 st.markdown("""
#                 <div style="border: 2px dashed rgba(255, 255, 255, 0.08); border-radius: 12px; padding: 60px 20px; text-align: center; background: rgba(255,255,255,0.01); display:flex; flex-direction:column; align-items:center; justify-content:center; min-height:220px;">
#                     <svg width="48" height="48" fill="none" stroke="#64748b" stroke-width="1.5" viewBox="0 0 24 24" style="margin-bottom:12px; opacity:0.8;"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>
#                     <span style="font-size: 13.5px; color: inherit; display:block; font-weight:500;">Select a leaf image to scan</span>
#                     <span style="font-size: 11px; color: #64748b; display:block; margin-top:2px;">JPEG, JPG, PNG (Max 5MB)</span>
#                 </div>
#                 """, unsafe_allow_html=True)

#             st.markdown("<div style='margin-top:15px;'></div>", unsafe_allow_html=True)

#             ui_btn_col1, ui_btn_col2 = st.columns(2)
#             with ui_btn_col1:
#                 uploaded_file = st.file_uploader("Choose Image", type=["jpg", "jpeg", "png"], label_visibility="collapsed", key="file_upload_input")
#             with ui_btn_col2:
#                 with st.expander("📷 Camera Scan"):
#                     camera_file = st.camera_input("Capture photo", label_visibility="collapsed")

#             st.markdown('<div style="text-align:center; font-size:11px; color:#64748b; margin-top:8px;">JPG, JPEG, PNG (Max. 5MB)</div>', unsafe_allow_html=True)

#     # ---------------- RUN PREDICTION INFERENCE ----------------
#     active_file = uploaded_file if uploaded_file else (camera_file if camera_file else None)

#     if active_file:
#         file_id = f"{active_file.name}_{active_file.size}"

#         if st.session_state.processed_file_id != file_id:
#             try:
#                 image = Image.open(active_file).convert("RGB")
#                 img_pre = image.resize((224, 224))
#                 img_arr = np.array(img_pre) / 255.0
#                 img_arr = np.expand_dims(img_arr, axis=0)

#                 if model is not None:
#                     predictions = model.predict(img_arr, verbose=0)
#                     pred_idx = np.argmax(predictions[0])
#                     pred_label = classes[pred_idx]
#                     conf_val = float(predictions[0][pred_idx]) * 100

#                     metadata = get_disease_metadata(pred_label)

#                     top3_idx = np.argsort(predictions[0])[-3:][::-1]
#                     top3_res = []
#                     for idx in top3_idx:
#                         c_lbl = classes[idx]
#                         c_meta = get_disease_metadata(c_lbl)
#                         c_pct = float(predictions[0][idx]) * 100
#                         top3_res.append((c_meta["display_name"], c_pct))

#                     st.session_state.current_result = {
#                         "disease": metadata["display_name"],
#                         "confidence": conf_val,
#                         "category": metadata["category"],
#                         "scientific_name": metadata["scientific_name"],
#                         "affects": metadata["affects"],
#                         "severity": metadata["severity"],
#                         "description": metadata["description"],
#                         "treatment": metadata["treatment"],
#                         "prevention": metadata["prevention"],
#                         "top3": top3_res,
#                         "image": image
#                     }

#                     history_entry = {
#                         "disease": metadata["display_name"],
#                         "confidence": conf_val,
#                         "time": "Just now"
#                     }
#                     st.session_state.history.insert(0, history_entry)

#                 st.session_state.processed_file_id = file_id
#                 st.rerun()
#             except Exception as e:
#                 st.error(f"Error executing prediction: {e}")
#     else:
#         st.session_state.processed_file_id = None
#         st.session_state.current_result = None

#     conf_score = res["confidence"]
#     conf_rating = "Waiting for Scan" if conf_score == 0.0 else ("High Confidence" if conf_score >= 90 else ("Medium Confidence" if conf_score >= 75 else "Low Confidence"))

#     with row1_col2:
#         with st.container(border=True):
#             st.markdown('<div class="card-title"><svg width="16" height="16" fill="none" stroke="#10b981" stroke-width="2" viewBox="0 0 24 24" style="display:inline; margin-right:5px;"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg> Prediction Result</div>', unsafe_allow_html=True)

#             st.markdown(f"""
#             <div style="text-align: center; margin-bottom: 15px;">
#                 <span style="font-size: 22px; font-weight: bold; color: { '#10b981' if conf_score > 0.0 else text_secondary };">{res['disease']}</span>
#             </div>
#             """, unsafe_allow_html=True)

#             res_col1, res_col2 = st.columns([1, 1.2])
#             with res_col1:
#                 st.markdown(f"<div style='margin-top: -10px; color: {text_secondary}; font-size:12.5px;'>Confidence Score</div>", unsafe_allow_html=True)
#                 # FIX 2: Use st.markdown (not st.write) to render SVG
#                 st.markdown(get_circular_gauge_svg(conf_score, conf_rating), unsafe_allow_html=True)

#             with res_col2:
#                 cat_bg = "rgba(128,128,128,0.06)" if conf_score == 0.0 else ("#064e3b" if "Healthy" in res["category"] else ("#1e3a8a" if "Viral" in res["category"] else ("#78350f" if "Bacterial" in res["category"] else "#581c87")))
#                 cat_fg = "#64748b" if conf_score == 0.0 else ("#34d399" if "Healthy" in res["category"] else ("#93c5fd" if "Viral" in res["category"] else ("#fcd34d" if "Bacterial" in res["category"] else "#c084fc")))
#                 sev_bg = "rgba(128,128,128,0.06)" if conf_score == 0.0 else ("#064e3b" if "None" in res["severity"] else ("#78350f" if "Moderate" in res["severity"] else "#7f1d1d"))
#                 sev_fg = "#64748b" if conf_score == 0.0 else ("#34d399" if "None" in res["severity"] else ("#fcd34d" if "Moderate" in res["severity"] else "#f87171"))

#                 st.markdown(f"""
#                 <table style="width: 100%; border-collapse: collapse; color: inherit; font-size: 13.5px; margin-top: 5px;">
#                     <tr style="border-bottom: 1px solid {border_color};">
#                         <td style="padding: 10px 0; color: {text_secondary};">Category</td>
#                         <td style="padding: 10px 0; text-align: right;">
#                             <span class="badge" style="background-color: {cat_bg} !important; color: {cat_fg} !important; font-size: 11px; font-weight: bold; padding: 3px 8px; border-radius: 20px;">{res['category']}</span>
#                         </td>
#                     </tr>
#                     <tr style="border-bottom: 1px solid {border_color};">
#                         <td style="padding: 10px 0; color: {text_secondary};">Scientific Name</td>
#                         <td style="padding: 10px 0; text-align: right; font-style: italic; color: inherit;">{res['scientific_name']}</td>
#                     </tr>
#                     <tr style="border-bottom: 1px solid {border_color};">
#                         <td style="padding: 10px 0; color: {text_secondary};">Affects</td>
#                         <td style="padding: 10px 0; text-align: right; color: inherit;">{res['affects']}</td>
#                     </tr>
#                     <tr>
#                         <td style="padding: 10px 0; color: {text_secondary};">Severity</td>
#                         <td style="padding: 10px 0; text-align: right;">
#                             <span class="badge" style="background-color: {sev_bg} !important; color: {sev_fg} !important; font-size: 11px; font-weight: bold; padding: 3px 8px; border-radius: 20px;">{res['severity']}</span>
#                         </td>
#                     </tr>
#                 </table>
#                 """, unsafe_allow_html=True)

#     # ---------------- DETAILS SECTION (ROW 2) ----------------
#     det_col1, det_col2, det_col3 = st.columns(3)

#     with det_col1:
#         with st.container(border=True):
#             st.markdown(f"""
#             <div class="card-title">
#                 <svg width="15" height="15" fill="none" stroke="#10b981" stroke-width="2" viewBox="0 0 24 24" style="display:inline; margin-right:5px;"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path></svg> Description
#             </div>
#             <p style="color: inherit; font-size: 13px; line-height: 1.6; margin-bottom:15px; min-height: 80px;">{res['description']}</p>
#             <div style="text-align: center; margin-top: auto;">
#                 <svg width="100%" height="70" viewBox="0 0 100 80" style="display:block; margin:auto; opacity: 0.85;">
#                     <path d="M50 80 Q50 40 50 10" stroke="#047857" stroke-width="3" fill="none" />
#                     <path d="M50 50 Q30 40 25 50 Q35 60 50 50" fill="#10b981" />
#                     <path d="M50 40 Q70 30 75 40 Q65 50 50 40" fill="#64748b" />
#                     <path d="M50 25 Q35 15 30 25 Q40 32 50 25" fill="#64748b" />
#                     <path d="M50 15 Q65 5 70 15 Q60 22 50 15" fill="#64748b" />
#                     <path d="M20 80 Q50 75 80 80 Z" fill="#78350f" />
#                 </svg>
#             </div>
#             """, unsafe_allow_html=True)

#     with det_col2:
#         with st.container(border=True):
#             # FIX 4: Build treatment bullets as plain HTML string, rendered with unsafe_allow_html=True
#             treat_bullets = ""
#             for t in res["treatment"]:
#                 stroke_color = '#10b981' if conf_score > 0.0 else '#64748b'
#                 treat_bullets += (
#                     f"<div style='display:flex; align-items:flex-start; gap:8px; margin-bottom:8px;'>"
#                     f"<svg width='14' height='14' viewBox='0 0 24 24' fill='none' stroke='{stroke_color}' stroke-width='3' stroke-linecap='round' stroke-linejoin='round' style='margin-top:2px; flex-shrink:0;'><polyline points='20 6 9 17 4 12'/></svg>"
#                     f"<span style='font-size:13px; color:inherit;'>{t}</span>"
#                     f"</div>"
#                 )

#             st.markdown(
#                 f"<div class='card-title'>"
#                 f"<svg width='15' height='15' fill='none' stroke='#10b981' stroke-width='2' viewBox='0 0 24 24' style='display:inline; margin-right:5px;'><path d='M4.8 15h14.4M12 4.8v20.4'/></svg> Treatment"
#                 f"</div>"
#                 f"<div style='min-height: 80px;'>{treat_bullets}</div>"
#                 f"<div style='text-align: center; margin-top: auto;'>"
#                 f"<svg width='100%' height='70' viewBox='0 0 100 80' style='display:block; margin:auto; opacity: 0.85;'>"
#                 f"<rect x='38' y='22' width='24' height='48' rx='4' fill='#1e293b' stroke='#64748b' stroke-width='2.5' />"
#                 f"<rect x='42' y='12' width='16' height='10' rx='1.5' fill='#cbd5e1' />"
#                 f"<line x1='42' y1='18' x2='58' y2='18' stroke='#94a3b8' stroke-width='2' />"
#                 f"<rect x='47' y='40' width='6' height='12' fill='#64748b' />"
#                 f"<rect x='44' y='43' width='12' height='6' fill='#64748b' />"
#                 f"<path d='M28 70 Q35 55 50 65 Q40 75 28 70' fill='#64748b' />"
#                 f"<path d='M72 70 Q65 55 50 65 Q60 75 72 70' fill='#64748b' />"
#                 f"</svg></div>",
#                 unsafe_allow_html=True
#             )

#     with det_col3:
#         with st.container(border=True):
#             # FIX 4: Build prevention bullets as plain HTML string, rendered with unsafe_allow_html=True
#             prev_bullets = ""
#             for p in res["prevention"]:
#                 stroke_color = '#10b981' if conf_score > 0.0 else '#64748b'
#                 prev_bullets += (
#                     f"<div style='display:flex; align-items:flex-start; gap:8px; margin-bottom:8px;'>"
#                     f"<svg width='14' height='14' viewBox='0 0 24 24' fill='none' stroke='{stroke_color}' stroke-width='3' stroke-linecap='round' stroke-linejoin='round' style='margin-top:2px; flex-shrink:0;'><polyline points='20 6 9 17 4 12'/></svg>"
#                     f"<span style='font-size:13px; color:inherit;'>{p}</span>"
#                     f"</div>"
#                 )

#             st.markdown(
#                 f"<div class='card-title'>"
#                 f"<svg width='15' height='15' fill='none' stroke='#10b981' stroke-width='2' viewBox='0 0 24 24' style='display:inline; margin-right:5px;'><path d='M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z'/></svg> Prevention"
#                 f"</div>"
#                 f"<div style='min-height: 80px;'>{prev_bullets}</div>"
#                 f"<div style='text-align: center; margin-top: auto;'>"
#                 f"<svg width='100%' height='70' viewBox='0 0 100 80' style='display:block; margin:auto; opacity: 0.85;'>"
#                 f"<path d='M50 15 L72 23 C72 23 74 50 50 68 C26 50 28 23 28 23 Z' fill='#1e293b' stroke='#64748b' stroke-width='2.5' />"
#                 f"<rect x='47' y='32' width='6' height='14' fill='#64748b' />"
#                 f"<rect x='43' y='36' width='14' height='6' fill='#64748b' />"
#                 f"<path d='M22 65 Q30 50 45 60 Q35 70 22 65' fill='#64748b' />"
#                 f"<path d='M78 65 Q70 50 55 60 Q65 70 78 65' fill='#64748b' />"
#                 f"</svg></div>",
#                 unsafe_allow_html=True
#             )

#     # ---------------- PREDICTIONS & CHARTS (ROW 3) ----------------
#     row3_col1, row3_col2 = st.columns(2)

#     with row3_col1:
#         with st.container(border=True):
#             st.markdown('<div class="card-title"><svg width="16" height="16" fill="none" stroke="#10b981" stroke-width="2" viewBox="0 0 24 24" style="display:inline; margin-right:5px;"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg> Top 3 Predictions</div>', unsafe_allow_html=True)

#             top_colors = ["#10b981", "#fbbf24", "#8b5cf6"]
#             st.markdown('<div style="display: flex; flex-direction: column; gap: 15px; margin-top: 10px;">', unsafe_allow_html=True)
#             for i, (name, val) in enumerate(res["top3"]):
#                 clr = top_colors[i] if conf_score > 0.0 and i < len(top_colors) else "rgba(128,128,128,0.1)"
#                 text_color = "inherit" if conf_score > 0.0 else "#64748b"

#                 st.markdown(f"""
#                 <div>
#                     <div style="display: flex; justify-content: space-between; font-size: 13.5px; color: {text_color}; margin-bottom: 5px;">
#                         <span style="display: flex; align-items: center; gap: 8px;">
#                             <span style="display: inline-flex; width: 22px; height: 22px; border-radius: 50%; background: {clr if conf_score > 0.0 else 'rgba(128,128,128,0.08)'}; color: { 'white' if conf_score > 0.0 else '#64748b' }; justify-content: center; align-items: center; font-size: 11px; font-weight: bold;">{i+1}</span>
#                             <span style="font-weight: 500;">{name}</span>
#                         </span>
#                         <span style="font-weight: 600; color: { 'inherit' if conf_score > 0.0 else '#64748b' };">{val:.0f}%</span>
#                 </div>
#                 <div style="width: 100%; height: 8px; background: rgba(128, 128, 128, 0.08); border-radius: 4px; overflow: hidden;">
#                     <div style="width: {val}%; height: 100%; background: {clr}; border-radius: 4px;"></div>
#                 </div>
#             </div>
#             """, unsafe_allow_html=True)
#             st.markdown('</div>', unsafe_allow_html=True)

#     with row3_col2:
#         with st.container(border=True):
#             st.markdown('<div class="card-title"><svg width="16" height="16" fill="none" stroke="#10b981" stroke-width="2" viewBox="0 0 24 24" style="display:inline; margin-right:5px;"><path d="M21.21 15.89A10 10 0 1 1 8 2.83M22 12A10 10 0 0 0 12 2v10z"/></svg> Prediction Statistics</div>', unsafe_allow_html=True)

#             stats_dataset = [
#                 ("Rust", 45, "#10b981"),
#                 ("Early Blight", 30, "#fbbf24"),
#                 ("Leaf Spot", 25, "#8b5cf6"),
#                 ("Healthy", 18, "#3b82f6"),
#                 ("Other", 10, "#6b7280")
#             ]

#             st_col1, st_col2 = st.columns([1, 1.1])
#             with st_col1:
#                 # FIX 2: Use st.markdown (not st.write) to render SVG
#                 st.markdown(get_donut_chart_svg(stats_dataset), unsafe_allow_html=True)
#             with st_col2:
#                 st.markdown("<div style='display:flex; flex-direction:column; gap:8px; margin-top:10px;'>", unsafe_allow_html=True)
#                 for name, count, color in stats_dataset:
#                     pct = (count / 128) * 100
#                     st.markdown(f"""
#                     <div style='display:flex; justify-content:space-between; align-items:center; font-size:12px; border-bottom: 1px solid {border_color}; padding-bottom:4px;'>
#                         <div style='display:flex; align-items:center; gap:8px;'>
#                             <div style='width:10px; height:10px; border-radius:50%; background-color:{color};'></div>
#                             <span style='color:inherit; font-weight: 500;'>{name}</span>
#                         </div>
#                         <span style='color:{text_secondary}; font-weight:600;'>{count} ({pct:.0f}%)</span>
#                     </div>
#                     """, unsafe_allow_html=True)
#                 st.markdown("</div>", unsafe_allow_html=True)

#     # ---------------- OCCURRENCE LINE CHART (ROW 4) ----------------
#     with st.container(border=True):
#         chart_title_col1, chart_title_col2 = st.columns([3, 1])
#         with chart_title_col1:
#             st.markdown(f'<div class="card-title" style="border:none; margin:0; color:inherit;"><svg width="16" height="16" fill="none" stroke="#10b981" stroke-width="2" viewBox="0 0 24 24" style="display:inline; margin-right:5px;"><path d="M3 3v18h18M18.7 8l-5.1 5.2-2.8-2.7L7 14.3"/></svg> Disease Occurrence (Last 7 Days)</div>', unsafe_allow_html=True)
#         with chart_title_col2:
#             st.selectbox("Filter", ["Last 7 Days", "Last 30 Days", "All Time"], label_visibility="collapsed", key="chart_filter")

#         base = datetime.now()
#         dates = [(base - timedelta(days=x)).strftime("%d %b") for x in range(6, -1, -1)]

#         data_occurrence = {
#             "Rust": [40, 22, 38, 28, 35, 42, 36],
#             "Early Blight": [20, 14, 14, 9, 8, 9, 13],
#             "Leaf Spot": [8, 25, 18, 23, 15, 18, 12],
#             "Healthy": [3, 16, 11, 13, 11, 12, 2],
#             "Other": [1, 3, 5, 2, 4, 5, 7]
#         }
#         colors_map = {
#             "Rust": "#10b981",
#             "Early Blight": "#fbbf24",
#             "Leaf Spot": "#8b5cf6",
#             "Healthy": "#3b82f6",
#             "Other": "#6b7280"
#         }

#         fig, ax = plt.subplots(figsize=(12, 3.8), facecolor='none')
#         ax.set_facecolor('none')

#         for label, y_values in data_occurrence.items():
#             color = colors_map[label]
#             ax.plot(dates, y_values, color=color, linewidth=5, alpha=0.12)
#             ax.plot(dates, y_values, color=color, linewidth=2, label=label, marker='o', markersize=4)

#         ax.set_ylabel("Count", color=chart_txt_color, fontsize=9)
#         ax.tick_params(colors=chart_txt_color, labelsize=8)

#         # FIX 1: Use matplotlib-compatible color tuples, not CSS rgba() strings
#         ax.spines['bottom'].set_color(chart_grid_color_mpl)
#         ax.spines['left'].set_color(chart_grid_color_mpl)
#         ax.spines['top'].set_visible(False)
#         ax.spines['right'].set_visible(False)
#         ax.grid(axis='y', linestyle='--', color=chart_grid_color_mpl, alpha=0.5)

#         legend = ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.15), ncol=5, frameon=False, fontsize=8.5)
#         for text in legend.get_texts():
#             text.set_color(chart_txt_color)

#         plt.tight_layout()
#         st.pyplot(fig, clear_figure=True)

#     # ---------------- METRIC WIDGETS (ROW 5) ----------------
#     m_col1, m_col2, m_col3 = st.columns(3)

#     with m_col1:
#         st.markdown(f"""
#         <div style="background: {card_bg}; border: 1px solid {border_color}; padding: 15px; border-radius: 12px; display: flex; align-items: center; gap: 15px; box-shadow: {card_shadow};">
#             <div style="background: rgba(16, 185, 129, 0.1); padding: 10px; border-radius: 10px; display: flex; align-items: center; justify-content: center;">
#                 <svg width="24" height="24" fill="none" stroke="#10b981" stroke-width="2" viewBox="0 0 24 24"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>
#             </div>
#             <div>
#                 <div style="font-size: 11.5px; color: {text_secondary};">Total Predictions</div>
#                 <div style="font-size: 20px; font-weight: bold; color: inherit; margin: 2px 0;">128</div>
#                 <div style="font-size: 10.5px; color: #10b981; font-weight: 500;">↑ 12% from last 7 days</div>
#             </div>
#         </div>
#         """, unsafe_allow_html=True)

#     with m_col2:
#         st.markdown(f"""
#         <div style="background: {card_bg}; border: 1px solid {border_color}; padding: 15px; border-radius: 12px; display: flex; align-items: center; gap: 15px; box-shadow: {card_shadow};">
#             <div style="background: rgba(245, 158, 11, 0.1); padding: 10px; border-radius: 10px; display: flex; align-items: center; justify-content: center;">
#                 <svg width="24" height="24" fill="none" stroke="#fbbf24" stroke-width="2" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg>
#             </div>
#             <div>
#                 <div style="font-size: 11.5px; color: {text_secondary};">Accuracy</div>
#                 <div style="font-size: 20px; font-weight: bold; color: inherit; margin: 2px 0;">96.2%</div>
#                 <div style="font-size: 10.5px; color: #10b981; font-weight: 500;">↑ 3.5% from last 7 days</div>
#             </div>
#         </div>
#         """, unsafe_allow_html=True)

#     with m_col3:
#         st.markdown(f"""
#         <div style="background: {card_bg}; border: 1px solid {border_color}; padding: 15px; border-radius: 12px; display: flex; align-items: center; gap: 15px; box-shadow: {card_shadow};">
#             <div style="background: rgba(139, 92, 246, 0.1); padding: 10px; border-radius: 10px; display: flex; align-items: center; justify-content: center;">
#                 <svg width="24" height="24" fill="none" stroke="#8b5cf6" stroke-width="2" viewBox="0 0 24 24"><path d="M12 22a10 10 0 1 0 0-20 10 10 0 0 0 0 20z"/><path d="M12 6v6l4 2"/></svg>
#             </div>
#             <div>
#                 <div style="font-size: 11.5px; color: {text_secondary};">Diseases Detected</div>
#                 <div style="font-size: 20px; font-weight: bold; color: inherit; margin: 2px 0;">5</div>
#                 <div style="font-size: 10.5px; color: {text_secondary};">Total unique diseases</div>
#             </div>
#         </div>
#         """, unsafe_allow_html=True)

#     # ---------------- FOOTER ----------------
#     st.markdown(f"""
#     <div style="text-align: center; font-size: 11.5px; color: {text_secondary}; margin-top: 30px; border-top: 1px solid {border_color}; padding-top: 15px;">
#         © 2026 PlantAI - AI Plant Disease Detection System | Developed with ❤️ by {st.session_state.username}
#     </div>
#     """, unsafe_allow_html=True)

# elif selected == "Disease Library":
#     st.markdown("""
#     <h1 style='margin: 0; font-size: 28px; font-weight: 700; color: inherit;'>
#         📚 Disease Library
#     </h1>
#     <p style='color: #94a3b8; font-size: 13.5px; margin: 5px 0 20px 0;'>
#         Browse details about the supported plant diseases, including symptoms, treatments, and prevention tips.
#     </p>
#     """, unsafe_allow_html=True)

#     search_query = st.text_input("🔍 Search Diseases", placeholder="Type plant or disease name...")

#     for key, data in DISEASE_METADATA.items():
#         if search_query.lower() in data["display_name"].lower() or search_query.lower() in data["category"].lower():
#             with st.container(border=True):
#                 st.markdown(f"""
#                 <div style="display:flex; justify-content:space-between; align-items:center;">
#                     <span style="font-size:18px; font-weight:bold; color:#10b981;">{data['display_name']}</span>
#                     <span class="badge badge-purple">{data['category']}</span>
#                 </div>
#                 <div style="font-size:12px; font-style:italic; color:#64748b; margin: 4px 0 10px 0;">Scientific Name: {data['scientific_name']} | Affects: {data['affects']}</div>
#                 <div style="font-size:13px; color:inherit; margin-bottom:12px;"><strong>Description:</strong> {data['description']}</div>
#                 <div style="display:grid; grid-template-columns: 1fr 1fr; gap:20px; border-top:1px solid {border_color}; padding-top:10px;">
#                     <div>
#                         <strong style="color:#fbbf24; font-size:12.5px;">💊 Recommended Treatment:</strong>
#                         <ul style="margin: 5px 0; padding-left: 20px; font-size:12px; color:inherit;">
#                             {"".join([f"<li>{t}</li>" for t in data['treatment']])}
#                         </ul>
#                     </div>
#                     <div>
#                         <strong style="color:#34d399; font-size:12.5px;">🛡 Prevention Guidelines:</strong>
#                         <ul style="margin: 5px 0; padding-left: 20px; font-size:12px; color:inherit;">
#                             {"".join([f"<li>{p}</li>" for p in data['prevention']])}
#                         </ul>
#                     </div>
#                 </div>
#                 """, unsafe_allow_html=True)

# elif selected == "Statistics":
#     st.markdown("""
#     <h1 style='margin: 0; font-size: 28px; font-weight: 700; color: inherit;'>
#         📊 Detailed Prediction Statistics
#     </h1>
#     <p style='color: #94a3b8; font-size: 13.5px; margin: 5px 0 20px 0;'>
#         Analysis of past prediction data, frequency curves, and detection accuracy ratings.
#     </p>
#     """, unsafe_allow_html=True)

#     col1, col2 = st.columns(2)
#     with col1:
#         with st.container(border=True):
#             st.markdown('<div class="card-title">Detection Shares (Distribution)</div>', unsafe_allow_html=True)
#             stats_dataset = [
#                 ("Rust", 45, "#10b981"),
#                 ("Early Blight", 30, "#fbbf24"),
#                 ("Leaf Spot", 25, "#8b5cf6"),
#                 ("Healthy", 18, "#3b82f6"),
#                 ("Other", 10, "#6b7280")
#             ]

#             st_col1, st_col2 = st.columns([1, 1])
#             with st_col1:
#                 # FIX 2: Use st.markdown (not st.write) to render SVG
#                 st.markdown(get_donut_chart_svg(stats_dataset), unsafe_allow_html=True)
#             with st_col2:
#                 st.markdown("<div style='display:flex; flex-direction:column; gap:8px; margin-top:15px;'>", unsafe_allow_html=True)
#                 for name, count, color in stats_dataset:
#                     pct = (count / 128) * 100
#                     st.markdown(f"""
#                     <div style='display:flex; justify-content:space-between; align-items:center; font-size:12.5px;'>
#                         <div style='display:flex; align-items:center; gap:8px;'>
#                             <div style='width:10px; height:10px; border-radius:50%; background-color:{color};'></div>
#                             <span style='color:inherit;'>{name}</span>
#                         </div>
#                         <span style='color:{text_secondary}; font-weight:600;'>{count} ({pct:.0f}%)</span>
#                     </div>
#                     """, unsafe_allow_html=True)
#                 st.markdown("</div>", unsafe_allow_html=True)

#     with col2:
#         with st.container(border=True):
#             st.markdown('<div class="card-title">Model Performance metrics</div>', unsafe_allow_html=True)
#             st.markdown(f"""
#             <table style="width: 100%; border-collapse: collapse; color: inherit; font-size: 13.5px;">
#                 <tr style="border-bottom: 1px solid {border_color};">
#                     <td style="padding: 12px 0; color: {text_secondary};">Average Inference Time</td>
#                     <td style="padding: 12px 0; text-align: right; font-weight:600;">180 ms</td>
#                 </tr>
#                 <tr style="border-bottom: 1px solid {border_color};">
#                     <td style="padding: 12px 0; color: {text_secondary};">Validation Top-1 Accuracy</td>
#                     <td style="padding: 12px 0; text-align: right; font-weight:600; color: #10b981;">96.2%</td>
#                 </tr>
#                 <tr style="border-bottom: 1px solid {border_color};">
#                     <td style="padding: 12px 0; color: {text_secondary};">Validation Top-5 Accuracy</td>
#                     <td style="padding: 12px 0; text-align: right; font-weight:600; color: #10b981;">99.4%</td>
#                 </tr>
#                 <tr>
#                     <td style="padding: 12px 0; color: {text_secondary};">F1-Score (Macro Average)</td>
#                     <td style="padding: 12px 0; text-align: right; font-weight:600;">0.958</td>
#                 </tr>
#             </table>
#             """, unsafe_allow_html=True)

# elif selected == "History":
#     st.markdown("""
#     <h1 style='margin: 0; font-size: 28px; font-weight: 700; color: inherit;'>
#         🕒 Prediction History Log
#     </h1>
#     <p style='color: #94a3b8; font-size: 13.5px; margin: 5px 0 20px 0;'>
#         Chronological logs of scanned plant diseases.
#     </p>
#     """, unsafe_allow_html=True)

#     if not st.session_state.history:
#         st.info("No prediction history recorded yet.")
#     else:
#         with st.container(border=True):
#             table_body = ""
#             for idx, item in enumerate(st.session_state.history):
#                 table_body += f"""
#                 <tr style="border-bottom: 1px solid {border_color};">
#                     <td style="padding: 12px 5px; color:#64748b;">{idx+1}</td>
#                     <td style="padding: 12px 5px; font-weight:600; color:#10b981;">{item['disease']}</td>
#                     <td style="padding: 12px 5px; text-align:center;"><span class="badge badge-green" style="font-size:10px;">{item['confidence']:.0f}%</span></td>
#                     <td style="padding: 12px 5px; text-align:right; color:#94a3b8;">{item['time']}</td>
#                 </tr>
#                 """

#             st.markdown(f"""
#             <table style="width: 100%; border-collapse: collapse; color: inherit; font-size: 13.5px; text-align: left;">
#                 <thead>
#                     <tr style="border-bottom: 2px solid {border_color}; color:{text_secondary};">
#                         <th style="padding: 10px 5px;">#</th>
#                         <th style="padding: 10px 5px;">Diagnosed Disease</th>
#                         <th style="padding: 10px 5px; text-align:center;">Confidence</th>
#                         <th style="padding: 10px 5px; text-align:right;">Timestamp</th>
#                     </tr>
#                 </thead>
#                 <tbody>
#                     {table_body}
#                 </tbody>
#             </table>
#             """, unsafe_allow_html=True)

# elif selected == "Plant Care Tips":
#     st.markdown("""
#     <h1 style='margin: 0; font-size: 28px; font-weight: 700; color: inherit;'>
#         💡 Plant Care Guidelines & Tips
#     </h1>
#     <p style='color: #94a3b8; font-size: 13.5px; margin: 5px 0 20px 0;'>
#         Practical tips to ensure healthy plants and minimize disease onset.
#     </p>
#     """, unsafe_allow_html=True)

#     tips = [
#         {"title": "Watering Wisely", "icon": "💧", "desc": "Irrigate the roots directly rather than splashing foliage. Wet leaves are prime incubation sites for fungal and bacterial spores. Water early in the morning so excess moisture evaporates during the day."},
#         {"title": "Proper Airflow & Spacing", "icon": "💨", "desc": "Overcrowding traps damp air inside the leaf canopy. Keep plants properly spaced and prune inner foliage/suckers to enhance wind circulation and sunlight entry."},
#         {"title": "Soil Sanitation & Mulching", "icon": "🍂", "desc": "Fungal spores overwinter in old plant tissue. Lay down fresh mulch to create a barrier and clean up fallen infected leaves immediately. Sanitize pruners and cages regularly."},
#         {"title": "Nutrition & Stress Management", "icon": "🧪", "desc": "Keep crops vigorous with balanced organic compost. Stressed plants are highly susceptible to infection. Monitor nitrogen feeds, as excess nitrogen can induce soft, leafy growth vulnerable to pests."}
#     ]

#     for t in tips:
#         with st.container(border=True):
#             st.markdown(f"""
#             <div style="font-size:18px; font-weight:bold; color:#10b981; margin-bottom:8px; display:flex; align-items:center; gap:8px;">
#                 <span>{t['icon']}</span>
#                 <span>{t['title']}</span>
#             </div>
#             <p style="color:inherit; font-size:13.5px; line-height:1.6; margin:0;">{t['desc']}</p>
#             """, unsafe_allow_html=True)

# elif selected == "Settings":
#     st.markdown("""
#     <h1 style='margin: 0; font-size: 28px; font-weight: 700; color: inherit;'>
#         ⚙ Application Settings
#     </h1>
#     <p style='color: #94a3b8; font-size: 13.5px; margin: 5px 0 20px 0;'>
#         Configure your dashboard layouts, detection sensitivity, and notification updates.
#     </p>
#     """, unsafe_allow_html=True)

#     with st.container(border=True):
#         st.markdown('<div class="card-title">User Preferences</div>', unsafe_allow_html=True)
#         new_username = st.text_input("Profile Display Name", value=st.session_state.username)
#         if new_username != st.session_state.username and new_username.strip() != "":
#             st.session_state.username = new_username.strip()
#             st.rerun()

#         location_options = list(WEATHER_DATA.keys())
#         selected_loc = st.selectbox("Location / Region", location_options, index=location_options.index(st.session_state.location))
#         if selected_loc != st.session_state.location:
#             st.session_state.location = selected_loc
#             st.rerun()

#         theme_options = ["Dark Mode", "Light Mode"]
#         selected_theme = st.selectbox("Appearance Theme", theme_options, index=theme_options.index(st.session_state.theme))
#         if selected_theme != st.session_state.theme:
#             st.session_state.theme = selected_theme
#             st.rerun()

#     with st.container(border=True):
#         st.markdown('<div class="card-title">Inference Engine settings</div>', unsafe_allow_html=True)
#         st.slider("Minimum Confidence Threshold (%)", 10, 100, 50)
#         st.checkbox("Enable Automatic Vector Database Lookup for Treatments", value=True)
#         st.checkbox("Log Detections Locally for Analytical Tracking", value=True)

#     with st.container(border=True):
#         st.markdown('<div class="card-title">Appearance Configurations</div>', unsafe_allow_html=True)
#         st.checkbox("Show Dashboard SVG Animations", value=True)

# elif selected == "About Us":
#     st.markdown("""
#     <h1 style='margin: 0; font-size: 28px; font-weight: 700; color: inherit;'>
#         🌱 About the Project
#     </h1>
#     <p style='color: #94a3b8; font-size: 13.5px; margin: 5px 0 20px 0;'>
#         Details regarding the technical stack and objectives of the AI Plant Disease Detection system.
#     </p>
#     """, unsafe_allow_html=True)

#     with st.container(border=True):
#         st.markdown(f"""
#         <h3 style="color:#10b981; margin-top:0;">PlantAI Smart Detection System</h3>
#         <p style="font-size:13.5px; line-height:1.6; color:inherit;">
#             PlantAI is a modern deep-learning application powered by a Convolutional Neural Network (CNN) model built using <strong>TensorFlow / Keras</strong>.
#             The system scans foliar images, runs a rapid classification scan against 15 unique plant leaf states, and delivers real-time confidence
#             ratings along with curated descriptions, treatments, and prevention guidelines.
#         </p>

#         <h4 style="color:inherit; margin-bottom:8px;">Core Architecture Features</h4>
#         <ul style="color:inherit; font-size:13px; line-height:1.7;">
#             <li><strong>TensorFlow 2.21 CNN Inference Layer</strong>: High accuracy classification engine optimized for plant leaves.</li>
#             <li><strong>Interactive SVG Visualizations</strong>: Gauge meters and donut shares generated dynamically for layout speed.</li>
#             <li><strong>Glassmorphic Theme Engine</strong>: Support for Light and Dark Modes constructed using native Streamlit containers.</li>
#             <li><strong>Enriched Treatment Database</strong>: Complete agricultural remedies for Solanaceae (tomato, potato, pepper) crops.</li>
#         </ul>

#         <div style="background: rgba(16, 185, 129, 0.05); border: 1px solid rgba(16, 185, 129, 0.1); border-radius: 8px; padding: 12px; text-align: center; margin-top: 20px; font-size: 13px; color:#10b981; font-weight:bold;">
#             Developed by {st.session_state.username} ❤️
#         </div>
#         """, unsafe_allow_html=True)


import os
import numpy as np
import tensorflow as tf
import streamlit as st
from PIL import Image
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from streamlit_option_menu import option_menu

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="PlantAI - Smart Detection",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────
defaults = {
    "theme": "Dark Mode",
    "username": "Dipanshi",
    "location": "New Delhi, IN",
    "notif_count": 3,
    "notif_show": False,
    "history": [
        {"disease": "Tomato - Rust",          "confidence": 96.0, "time": "2 min ago"},
        {"disease": "Potato - Early Blight",  "confidence": 89.0, "time": "1 hour ago"},
        {"disease": "Tomato - Leaf Spot",     "confidence": 78.0, "time": "2 hours ago"},
        {"disease": "Healthy Leaf",           "confidence": 98.0, "time": "Yesterday"},
        {"disease": "Tomato - Mosaic Virus",  "confidence": 65.0, "time": "2 days ago"},
    ],
    "current_result": None,
    "processed_file_id": None,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ─────────────────────────────────────────────
# THEME TOKENS
# ─────────────────────────────────────────────
IS_DARK = st.session_state.theme == "Dark Mode"

if IS_DARK:
    BG_APP       = "#060c14"
    BG_SIDEBAR   = "#0b121f"
    BORDER       = "rgba(255,255,255,0.05)"
    TEXT_PRI     = "#cbd5e1"
    TEXT_SEC     = "#94a3b8"
    CARD_BG      = "#0b121f"
    SCRL_TRACK   = "#060c14"
    SCRL_THUMB   = "#1e293b"
    SHADOW       = "0 4px 30px rgba(0,0,0,.4)"
    CARD_SHADOW  = "rgba(0,0,0,.3) 0 4px 20px"
    GRID_COLOR   = (1., 1., 1., .05)
else:
    BG_APP       = "#f8fafc"
    BG_SIDEBAR   = "#f1f5f9"
    BORDER       = "rgba(15,23,42,.08)"
    TEXT_PRI     = "#0f172a"
    TEXT_SEC     = "#475569"
    CARD_BG      = "#ffffff"
    SCRL_TRACK   = "#f1f5f9"
    SCRL_THUMB   = "#cbd5e1"
    SHADOW       = "0 4px 20px rgba(15,23,42,.05)"
    CARD_SHADOW  = "rgba(15,23,42,.04) 0 4px 12px"
    GRID_COLOR   = (.06, .09, .16, .05)

CHART_TXT = "#cbd5e1" if IS_DARK else "#475569"

# ─────────────────────────────────────────────
# GLOBAL CSS
# ─────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

[data-testid="stAppViewContainer"] {{
    background-color:{BG_APP} !important;
    color:{TEXT_PRI} !important;
    font-family:'Inter',-apple-system,BlinkMacSystemFont,sans-serif;
}}
[data-testid="stSidebar"] {{
    background-color:{BG_SIDEBAR} !important;
    border-right:1px solid {BORDER} !important;
}}
[data-testid="stHeader"] {{ visibility:hidden; }}
footer {{ visibility:hidden; }}
#MainMenu {{ visibility:hidden; }}

::-webkit-scrollbar {{ width:6px; height:6px; }}
::-webkit-scrollbar-track {{ background:{SCRL_TRACK}; }}
::-webkit-scrollbar-thumb {{ background:{SCRL_THUMB}; border-radius:3px; }}
::-webkit-scrollbar-thumb:hover {{ background:#10b981; }}

div[data-testid="stBorderWrapper"] {{
    background-color:{CARD_BG} !important;
    border:1px solid {BORDER} !important;
    border-radius:16px !important;
    box-shadow:{CARD_SHADOW} !important;
}}
div[data-testid="stBorderWrapper"]>div {{ padding:18px !important; }}

h1,h2,h3,h4,p,span,table,td,tr,li,ul {{ color:inherit !important; }}

.card-title {{
    font-size:14px; font-weight:600; color:{TEXT_SEC} !important;
    margin-bottom:14px; display:flex; align-items:center; gap:8px;
    border-bottom:1px solid {BORDER}; padding-bottom:8px;
}}

.stButton>button {{
    border-radius:10px !important;
    background:linear-gradient(135deg,#10b981,#059669) !important;
    color:white !important; font-size:14px !important; font-weight:600 !important;
    border:none !important; padding:8px 16px !important;
    transition:all .3s !important; width:100%;
}}
.stButton>button:hover {{
    background:linear-gradient(135deg,#34d399,#10b981) !important;
    box-shadow:0 0 15px rgba(16,185,129,.4) !important;
    transform:translateY(-1px);
}}

.clear-btn button {{
    background:transparent !important; color:#ef4444 !important;
    border:1px solid rgba(239,68,68,.25) !important;
    font-size:13px !important; padding:6px 12px !important;
    box-shadow:none !important;
}}
.clear-btn button:hover {{
    background:rgba(239,68,68,.08) !important;
    border-color:#ef4444 !important; box-shadow:none !important;
}}

[data-testid="stFileUploader"] {{
    background:rgba(30,41,59,.12);
    border:1px dashed {BORDER}; border-radius:12px; padding:8px;
}}

.badge {{
    display:inline-block; padding:3px 10px; border-radius:20px;
    font-size:11px; font-weight:700; text-align:center;
}}
.badge-green  {{ background:rgba(16,185,129,.15)!important; color:#10b981!important; }}
.badge-orange {{ background:rgba(245,158,11,.15)!important; color:#f59e0b!important; }}
.badge-red    {{ background:rgba(239,68,68,.15)!important;  color:#ef4444!important; }}
.badge-blue   {{ background:rgba(59,130,246,.15)!important; color:#3b82f6!important; }}
.badge-purple {{ background:rgba(139,92,246,.15)!important; color:#8b5cf6!important; }}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# DISEASE DATABASE
# ─────────────────────────────────────────────
DISEASE_DB = {
    "Pepper__bell___Bacterial_spot": {
        "display_name": "Pepper Bell - Bacterial Spot",
        "category": "Bacterial Disease",
        "scientific_name": "Xanthomonas campestris pv. vesicatoria",
        "affects": "Pepper Plants", "severity": "Moderate to High",
        "description": "Bacterial disease causing dark, water-soaked spots on pepper leaves that eventually turn brown, dry up, and fall off.",
        "treatment": ["Apply copper-based bactericides early in the disease cycle.", "Remove and destroy heavily infected leaves and plants.", "Avoid overhead watering to minimise bacterial splash."],
        "prevention": ["Use certified disease-free seeds and transplants.", "Practice crop rotation with non-solanaceous crops.", "Space plants properly to improve canopy air circulation."],
    },
    "Pepper__bell___healthy": {
        "display_name": "Pepper Bell - Healthy",
        "category": "Healthy Plant", "scientific_name": "Capsicum annuum",
        "affects": "Pepper Plants", "severity": "None",
        "description": "The pepper plant shows no signs of infection. Leaves are vibrant green and healthy.",
        "treatment": ["No chemical treatment required.", "Maintain standard fertilisation and watering.", "Inspect foliage regularly for early signs of pests."],
        "prevention": ["Provide regular watering at the base.", "Ensure 6-8 hours of full sun daily.", "Maintain soil nutrients with organic compost."],
    },
    "Potato___Early_blight": {
        "display_name": "Potato - Early Blight",
        "category": "Fungal Disease", "scientific_name": "Alternaria solani",
        "affects": "Potato Plants", "severity": "Moderate",
        "description": "Common fungal disease with dark brown spots showing concentric rings (target-board pattern) on older leaves.",
        "treatment": ["Apply fungicides containing chlorothalonil or mancozeb.", "Remove lower infected leaves to reduce spore splash.", "Ensure balanced fertilisation."],
        "prevention": ["Rotate crops annually.", "Use drip irrigation to keep leaf surfaces dry.", "Destroy crop residues after harvest."],
    },
    "Potato___Late_blight": {
        "display_name": "Potato - Late Blight",
        "category": "Fungal/Oomycete Disease", "scientific_name": "Phytophthora infestans",
        "affects": "Potato Plants", "severity": "High",
        "description": "Highly destructive disease causing dark, water-soaked lesions on leaves and stems, rapidly killing plants in cool, wet weather.",
        "treatment": ["Apply systemic fungicides immediately upon detection.", "Remove and destroy infected plants.", "Wait two weeks after vine death before harvesting tubers."],
        "prevention": ["Plant certified disease-free seed tubers.", "Choose resistant cultivars.", "Ensure proper spacing for ventilation."],
    },
    "Potato___healthy": {
        "display_name": "Potato - Healthy",
        "category": "Healthy Plant", "scientific_name": "Solanum tuberosum",
        "affects": "Potato Plants", "severity": "None",
        "description": "The potato plant is healthy, showing vigorous leaf and stem development with no lesions.",
        "treatment": ["No treatment necessary.", "Continue standard watering and hilling.", "Apply organic mulches to protect soil moisture."],
        "prevention": ["Ensure proper soil drainage.", "Rotate crops regularly.", "Monitor for potato beetles."],
    },
    "Tomato_Bacterial_spot": {
        "display_name": "Tomato - Bacterial Spot",
        "category": "Bacterial Disease", "scientific_name": "Xanthomonas perforans",
        "affects": "Tomato Plants", "severity": "Moderate to High",
        "description": "Bacterial infection causing small, dark circular spots on leaves and stems, often with a yellow halo.",
        "treatment": ["Apply copper-based sprays mixed with mancozeb.", "Prune infected lower branches.", "Avoid working with plants when wet."],
        "prevention": ["Use disease-free seeds.", "Avoid overhead watering.", "Practice 2-3 year crop rotation."],
    },
    "Tomato_Early_blight": {
        "display_name": "Tomato - Early Blight",
        "category": "Fungal Disease", "scientific_name": "Alternaria solani",
        "affects": "Tomato Plants", "severity": "Moderate",
        "description": "Dark concentric rings on older leaves that cause early leaf drop, exposing fruit to sunscald.",
        "treatment": ["Apply copper-based or bio-fungicides.", "Prune lower leaves to prevent soil-spore splash.", "Mulch around plant base."],
        "prevention": ["Provide consistent base watering.", "Maintain spacing for airflow.", "Clean up garden debris each season."],
    },
    "Tomato_Late_blight": {
        "display_name": "Tomato - Late Blight",
        "category": "Fungal/Oomycete Disease", "scientific_name": "Phytophthora infestans",
        "affects": "Tomato Plants", "severity": "High",
        "description": "Causes rapid foliage decay and dark greasy lesions on fruit, leading to complete plant collapse.",
        "treatment": ["Remove and destroy infected plants immediately.", "Apply preventive copper fungicides to surrounding plants.", "Do not compost infected material."],
        "prevention": ["Plant resistant cultivars.", "Space plants widely and prune suckers.", "Water early so foliage dries quickly."],
    },
    "Tomato_Leaf_Mold": {
        "display_name": "Tomato - Leaf Mold",
        "category": "Fungal Disease", "scientific_name": "Passalora fulva",
        "affects": "Tomato Plants", "severity": "Low to Moderate",
        "description": "Yellow patches on upper leaf surfaces with olive-green velvety growth underneath, typical under high humidity.",
        "treatment": ["Reduce humidity below 85%.", "Apply copper or sulfur fungicides.", "Prune lower foliage for air movement."],
        "prevention": ["Improve ventilation.", "Space plants and avoid overhead watering.", "Grow resistant cultivars."],
    },
    "Tomato_Septoria_leaf_spot": {
        "display_name": "Tomato - Septoria Leaf Spot",
        "category": "Fungal Disease", "scientific_name": "Septoria lycopersici",
        "affects": "Tomato Plants", "severity": "Moderate",
        "description": "Numerous small circular leaf spots with dark borders and grey/white centres.",
        "treatment": ["Remove infected leaves immediately.", "Apply copper or chlorothalonil fungicides.", "Mulch around the plant base."],
        "prevention": ["Irrigate at ground level.", "Rotate crops annually.", "Clean stakes, cages, and tools after use."],
    },
    "Tomato_Spider_mites_Two_spotted_spider_mite": {
        "display_name": "Tomato - Spider Mites",
        "category": "Pest Infestation", "scientific_name": "Tetranychus urticae",
        "affects": "Tomato Plants", "severity": "Moderate to High",
        "description": "Tiny spider-like pests causing fine white/yellow stippling and webbing under leaves, leading to leaf drop.",
        "treatment": ["Spray with insecticidal soaps or neem oil.", "Introduce predatory mites.", "Wash foliage with a strong water stream."],
        "prevention": ["Monitor foliage during dry, hot weather.", "Keep plants well-hydrated.", "Maintain humidity around plants."],
    },
    "Tomato__Target_Spot": {
        "display_name": "Tomato - Target Spot",
        "category": "Fungal Disease", "scientific_name": "Corynespora cassiicola",
        "affects": "Tomato Plants", "severity": "Moderate",
        "description": "Concentric circle lesions similar to early blight; smaller spots that can spread to stems and fruits.",
        "treatment": ["Apply chlorothalonil or mancozeb fungicides.", "Remove and destroy infected foliage.", "Avoid overhead irrigation."],
        "prevention": ["Maintain proper spacing and airflow.", "Rotate crops.", "Manage weeds around the garden."],
    },
    "Tomato__Tomato_YellowLeaf__Curl_Virus": {
        "display_name": "Tomato - Yellow Leaf Curl Virus",
        "category": "Viral Disease", "scientific_name": "Tomato yellow leaf curl virus (TYLCV)",
        "affects": "Tomato Plants", "severity": "High",
        "description": "Viral disease transmitted by whiteflies causing severe stunting, yellowing, and upward leaf curling.",
        "treatment": ["No chemical cure; control whitefly vector populations.", "Use yellow sticky traps.", "Spray neem oil or systemic insecticides."],
        "prevention": ["Plant resistant cultivars.", "Use row covers on young plants.", "Destroy virus-infected plants immediately."],
    },
    "Tomato__Tomato_mosaic_virus": {
        "display_name": "Tomato - Mosaic Virus",
        "category": "Viral Disease", "scientific_name": "Tomato mosaic virus (ToMV)",
        "affects": "Tomato Plants", "severity": "High",
        "description": "Highly contagious virus causing mottled yellow-green patterns, distorted leaves, and stunted growth.",
        "treatment": ["No cure; pull out and burn infected plants.", "Sanitise hands and tools immediately.", "Do not touch healthy plants after infected ones."],
        "prevention": ["Purchase certified virus-free seeds.", "Avoid soil where infected plants recently grew.", "Do not smoke near plants."],
    },
    "Tomato_healthy": {
        "display_name": "Tomato - Healthy",
        "category": "Healthy Plant", "scientific_name": "Solanum lycopersicum",
        "affects": "Tomato Plants", "severity": "None",
        "description": "The tomato plant is healthy. Leaves are robust, green, and free from any disease.",
        "treatment": ["No treatment required.", "Continue standard watering, pruning, and staking.", "Apply slow-release fertiliser."],
        "prevention": ["Ensure 6-8 hours of sun daily.", "Maintain base watering.", "Inspect leaf undersides weekly for pests."],
    },
}

def get_metadata(class_name):
    if class_name in DISEASE_DB:
        return DISEASE_DB[class_name]
    return {
        "display_name": class_name.replace("_", " "),
        "category": "Unknown", "scientific_name": "N/A",
        "affects": "Plants", "severity": "Unknown",
        "description": "No detailed information available.",
        "treatment": ["Consult an agricultural specialist."],
        "prevention": ["Monitor plants regularly."],
    }

# ─────────────────────────────────────────────
# WEATHER DATA
WEATHER = {
    "New Delhi, IN": {"temp":"30°C","condition":"Partly Cloudy","humidity":"65%","wind":"12 km/h","feels":"33°C"},
    "Mumbai, IN": {"temp":"28°C","condition":"Heavy Rain","humidity":"85%","wind":"22 km/h","feels":"32°C"},
    "London, UK": {"temp":"18°C","condition":"Light Drizzle","humidity":"75%","wind":"15 km/h","feels":"17°C"},
    "Akbarpur, Ayodhya": {"temp":"33°C","condition":"intermittent clouds","humidity":"50%","wind":"10 km/h","feels":"22°C"},
}

city = st.selectbox("Select City", list(WEATHER.keys()))
w = WEATHER[city]
# ─────────────────────────────────────────────
# MODEL LOADING
# ─────────────────────────────────────────────
@st.cache_resource
def load_model():
    path = "plant_disease_model.h5"
    if os.path.exists(path):
        return tf.keras.models.load_model(path)
    return None

@st.cache_resource
def load_classes():
    with open("labels.txt", "r") as f:
        return [l.strip() for l in f.readlines()]

model  = load_model()
classes = load_classes()

# ─────────────────────────────────────────────
# SVG HELPERS
# ─────────────────────────────────────────────
def gauge_svg(confidence, rating):
    circ   = 439.82
    offset = circ * (1 - confidence / 100)
    if confidence == 0:
        color = "rgba(255,255,255,0.08)"
    elif confidence >= 90:
        color = "#10b981"
    elif confidence >= 75:
        color = "#f59e0b"
    else:
        color = "#ef4444"

    return (
        f'<svg width="100%" height="160" viewBox="0 0 200 200" style="display:block;margin:auto;">'
        f'<circle cx="100" cy="100" r="70" fill="none" stroke="rgba(255,255,255,0.04)" stroke-width="12"/>'
        f'<circle cx="100" cy="100" r="70" fill="none" stroke="{color}" stroke-width="12"'
        f' stroke-dasharray="{circ}" stroke-dashoffset="{offset}"'
        f' stroke-linecap="round" transform="rotate(-90 100 100)"/>'
        f'<text x="100" y="95" fill="{TEXT_PRI}" font-size="36" font-weight="bold"'
        f' text-anchor="middle" dominant-baseline="middle">{confidence:.0f}%</text>'
        f'<text x="100" y="128" fill="{color}" font-size="11" font-weight="600"'
        f' text-anchor="middle" dominant-baseline="middle">{rating}</text>'
        f'</svg>'
    )

def donut_svg(data):
    total  = sum(d[1] for d in data) or 1
    r      = 60
    circ   = 2 * 3.14159265 * r
    parts  = []
    offset = 0
    for _, count, color in data:
        arc = circ * (count / total)
        parts.append(
            f'<circle cx="100" cy="100" r="{r}" fill="none" stroke="{color}" stroke-width="14"'
            f' stroke-dasharray="{arc} {circ - arc}" stroke-dashoffset="{-offset}"'
            f' transform="rotate(-90 100 100)"/>'
        )
        offset += arc
    inner = "".join(parts)
    return (
        f'<svg width="100%" height="160" viewBox="0 0 200 200" style="display:block;margin:auto;">'
        f'{inner}'
        f'<circle cx="100" cy="100" r="48" fill="{CARD_BG}"/>'
        f'<text x="100" y="94" fill="{TEXT_PRI}" font-size="28" font-weight="bold"'
        f' text-anchor="middle" dominant-baseline="middle">{total}</text>'
        f'<text x="100" y="116" fill="{TEXT_SEC}" font-size="11"'
        f' text-anchor="middle" dominant-baseline="middle">Total</text>'
        f'</svg>'
    )

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        '<div style="padding:10px 0 12px;display:flex;align-items:center;gap:12px;">'
        '<svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#10b981"'
        ' stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">'
        '<path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 3.5 1 9.8a7 7 0 0 1-9 8.2z"/>'
        '<path d="M9 22v-4H5a2 2 0 0 1-2-2V6"/>'
        '</svg>'
        '<div><span style="font-size:22px;font-weight:700;">Plant<span style="color:#10b981;">AI</span></span>'
        '<br><span style="font-size:11px;color:#64748b;font-weight:500;">Smart Detection</span></div>'
        '</div>',
        unsafe_allow_html=True,
    )

    selected = option_menu(
        menu_title=None,
        options=["Home","Predict Disease","Disease Library","Statistics","History","Plant Care Tips","Settings","About Us"],
        icons=["house-door-fill","search","journal-bookmark-fill","bar-chart-line-fill",
               "clock-history","lightbulb-fill","gear-fill","info-circle-fill"],
        default_index=0,
        styles={
            "container":       {"padding":"0!important","background-color":"transparent"},
            "icon":            {"color":"#64748b","font-size":"15px"},
            "nav-link":        {"font-size":"14px","text-align":"left","margin":"2px 0","color":"#94a3b8",
                                "border-radius":"10px","padding":"10px 15px"},
            "nav-link-selected":{"background":"linear-gradient(135deg,#10b981,#059669)","color":"white","font-weight":"bold"},
        },
    )

    # Recent predictions
    with st.container(border=True):
        st.markdown('<div style="font-size:13px;font-weight:600;margin-bottom:10px;">Recent Predictions</div>', unsafe_allow_html=True)
        for item in st.session_state.history[:5]:
            c   = item["confidence"]
            cls = "badge-green" if c >= 90 else ("badge-orange" if c >= 75 else "badge-red")
            st.markdown(
                f'<div style="display:flex;justify-content:space-between;align-items:center;'
                f'background:rgba(30,41,59,.15);padding:8px 12px;border-radius:10px;'
                f'margin-bottom:7px;border:1px solid {BORDER};">'
                f'<div><div style="font-size:12px;font-weight:700;">{item["disease"]}</div>'
                f'<div style="font-size:10px;color:#64748b;">{item["time"]}</div></div>'
                f'<span class="badge {cls}">{c:.0f}%</span></div>',
                unsafe_allow_html=True,
            )
        st.markdown('<div class="clear-btn">', unsafe_allow_html=True)
        if st.button("🗑 Clear History"):
            st.session_state.history = []
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # Weather widget
    w = WEATHER.get(st.session_state.location, WEATHER["New Delhi, IN"])
    with st.container(border=True):
        st.markdown(
            f'<div style="font-size:11px;font-weight:700;margin-bottom:8px;">'
            f'📍 {st.session_state.location}</div>'
            f'<div style="font-size:22px;font-weight:700;margin-bottom:4px;">{w["temp"]}</div>'
            f'<div style="font-size:12px;color:{TEXT_SEC};margin-bottom:8px;">{w["condition"]}</div>'
            f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:4px;font-size:11px;'
            f'border-top:1px solid {BORDER};padding-top:8px;">'
            f'<div>Humidity: <strong>{w["humidity"]}</strong></div>'
            f'<div>Wind: <strong>{w["wind"]}</strong></div>'
            f'<div style="grid-column:span 2;">Feels like: <strong>{w["feels"]}</strong></div>'
            f'</div>',
            unsafe_allow_html=True,
        )

# ─────────────────────────────────────────────
# HELPERS: build bullet list HTML
# ─────────────────────────────────────────────
def bullet_html(items, active=True):
    color = "#10b981" if active else "#64748b"
    rows = ""
    for item in items:
        rows += (
            f'<div style="display:flex;align-items:flex-start;gap:8px;margin-bottom:8px;">'
            f'<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="{color}"'
            f' stroke-width="3" stroke-linecap="round" stroke-linejoin="round"'
            f' style="margin-top:2px;flex-shrink:0;"><polyline points="20 6 9 17 4 12"/></svg>'
            f'<span style="font-size:13px;">{item}</span></div>'
        )
    return rows

# ─────────────────────────────────────────────
# HOME / PREDICT DISEASE PAGE
# ─────────────────────────────────────────────
if selected in ("Home", "Predict Disease"):

    # ── Header ──────────────────────────────
    hc1, hc2, hc3, hc4 = st.columns([5, 0.6, 0.6, 1.2])
    with hc1:
        st.markdown(
            '<h1 style="margin:0;font-size:28px;font-weight:700;">'
            '🌿 AI Plant Disease Detection <span style="color:#10b981;">Dashboard</span></h1>'
            f'<p style="color:#94a3b8;font-size:13.5px;margin:5px 0 20px;">Upload a leaf image '
            'and get instant disease prediction with treatment and prevention tips.</p>',
            unsafe_allow_html=True,
        )
    with hc2:
        icon = "☀️" if IS_DARK else "🌙"
        if st.button(icon, key="theme_toggle", help="Toggle theme"):
            st.session_state.theme = "Light Mode" if IS_DARK else "Dark Mode"
            st.rerun()
    with hc3:
        if st.button("🔔", key="notif_btn"):
            st.session_state.notif_show = not st.session_state.notif_show
            st.rerun()
    with hc4:
        st.button(f"👤 {st.session_state.username}", key="user_btn")

    # Notifications
    if st.session_state.notif_show:
        st.markdown(
            '<div style="background:rgba(30,41,59,.9);border:1px solid rgba(16,185,129,.3);'
            'border-radius:10px;padding:15px;margin-bottom:20px;">'
            '<div style="font-weight:700;color:#10b981;margin-bottom:8px;font-size:14px;">🔔 Notifications</div>'
            '<div style="font-size:12.5px;display:flex;flex-direction:column;gap:8px;">'
            '<div>• <strong>System Update:</strong> PlantAI engine updated to v2.0.</div>'
            '<div>• <strong>Weather Alert:</strong> High humidity — monitor leaves for early symptoms.</div>'
            '<div>• <strong>History:</strong> Prediction logs available in the History tab.</div>'
            '</div></div>',
            unsafe_allow_html=True,
        )

    # ── Upload + Result row ──────────────────
    col_up, col_res = st.columns([1.2, 1])

    # Default empty result
    res = st.session_state.current_result or {
        "disease": "Waiting for Leaf Scan",
        "confidence": 0.0,
        "category": "N/A", "scientific_name": "N/A",
        "affects": "N/A", "severity": "N/A",
        "description": "Upload a leaf image of Pepper, Potato, or Tomato to run the AI diagnosis.",
        "treatment": ["No treatments recommended yet. Please upload a leaf image."],
        "prevention": ["No prevention guidelines yet. Please upload a leaf image."],
        "top3": [("-", 0.0), ("-", 0.0), ("-", 0.0)],
    }

    with col_up:
        with st.container(border=True):
            st.markdown(
                '<div class="card-title">📷 Upload Leaf Image</div>',
                unsafe_allow_html=True,
            )

            # Show uploaded image preview if available
            if "image" in res and res["image"] is not None:
                st.image(res["image"], caption="Uploaded Leaf", use_container_width=True)
            else:
                st.markdown(
                    f'<div style="border:2px dashed {BORDER};border-radius:12px;padding:50px 20px;'
                    'text-align:center;min-height:200px;display:flex;flex-direction:column;'
                    'align-items:center;justify-content:center;">'
                    '<svg width="44" height="44" fill="none" stroke="#64748b" stroke-width="1.5"'
                    ' viewBox="0 0 24 24" style="margin-bottom:12px;opacity:.75;">'
                    '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>'
                    '<polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>'
                    f'<span style="font-size:13.5px;font-weight:500;color:{TEXT_SEC};">Select a leaf image to scan</span>'
                    f'<span style="font-size:11px;color:#64748b;margin-top:4px;">JPG, JPEG, PNG · Max 5 MB</span>'
                    '</div>',
                    unsafe_allow_html=True,
                )

            st.markdown("<div style='margin-top:14px;'></div>", unsafe_allow_html=True)
            uploaded_file = st.file_uploader(
                "Choose Image", type=["jpg", "jpeg", "png"],
                label_visibility="collapsed", key="leaf_uploader",
            )

    # ── Run inference ────────────────────────
    if uploaded_file:
        file_id = f"{uploaded_file.name}_{uploaded_file.size}"
        if st.session_state.processed_file_id != file_id:
            try:
                image = Image.open(uploaded_file).convert("RGB")
                if model is not None:
                    img_arr = np.expand_dims(np.array(image.resize((224, 224))) / 255.0, 0)
                    preds   = model.predict(img_arr, verbose=0)[0]
                    idx     = int(np.argmax(preds))
                    label   = classes[idx]
                    conf    = float(preds[idx]) * 100
                    meta    = get_metadata(label)
                    top3    = [(get_metadata(classes[i])["display_name"], float(preds[i]) * 100)
                               for i in np.argsort(preds)[-3:][::-1]]

                    st.session_state.current_result = {**meta,
                        "confidence": conf, "top3": top3, "image": image}
                    st.session_state.history.insert(0, {
                        "disease": meta["display_name"], "confidence": conf, "time": "Just now"})
                else:
                    # Model not found — show placeholder with uploaded image
                    st.session_state.current_result = {
                        **get_metadata(""), "confidence": 0.0,
                        "top3": [("-", 0.0), ("-", 0.0), ("-", 0.0)],
                        "image": image,
                        "description": "Model file not found. Place plant_disease_model.h5 and labels.txt in the app directory.",
                    }

                st.session_state.processed_file_id = file_id
                st.rerun()
            except Exception as e:
                st.error(f"Prediction error: {e}")
    else:
        if st.session_state.processed_file_id is not None:
            st.session_state.processed_file_id = None
            st.session_state.current_result    = None
            st.rerun()

    # Refresh res after potential update
    res = st.session_state.current_result or res
    conf  = res["confidence"]
    rating = ("Waiting for Scan" if conf == 0
              else "High Confidence" if conf >= 90
              else "Medium Confidence" if conf >= 75
              else "Low Confidence")

    # ── Result card ─────────────────────────
    with col_res:
        with st.container(border=True):
            st.markdown('<div class="card-title">🛡 Prediction Result</div>', unsafe_allow_html=True)

            name_color = "#10b981" if conf > 0 else TEXT_SEC
            st.markdown(
                f'<div style="text-align:center;margin-bottom:14px;">'
                f'<span style="font-size:20px;font-weight:700;color:{name_color};">'
                
                 
             f'{res.get("disease", "Unknown Disease")}</span></div>',
                unsafe_allow_html=True,
            )

            rc1, rc2 = st.columns([1, 1.2])
            with rc1:
                st.markdown(f'<div style="font-size:12px;color:{TEXT_SEC};margin-bottom:4px;">Confidence Score</div>', unsafe_allow_html=True)
                st.markdown(gauge_svg(conf, rating), unsafe_allow_html=True)

            with rc2:
                def cat_colors(cat, sev, active):
                    if not active:
                        return "#1e293b", "#64748b", "#1e293b", "#64748b"
                    cb = "#064e3b" if "Healthy" in cat else ("#1e3a8a" if "Viral" in cat else ("#78350f" if "Bacterial" in cat else "#3b1f6b"))
                    cf = "#34d399" if "Healthy" in cat else ("#93c5fd" if "Viral" in cat else ("#fcd34d" if "Bacterial" in cat else "#c084fc"))
                    sb = "#064e3b" if "None" in sev else ("#78350f" if "Moderate" in sev else "#7f1d1d")
                    sf = "#34d399" if "None" in sev else ("#fcd34d" if "Moderate" in sev else "#f87171")
                    return cb, cf, sb, sf

                cb, cf, sb, sf = cat_colors(res["category"], res["severity"], conf > 0)
                st.markdown(
                    f'<table style="width:100%;border-collapse:collapse;font-size:13.5px;margin-top:6px;">'
                    f'<tr style="border-bottom:1px solid {BORDER};">'
                    f'<td style="padding:10px 0;color:{TEXT_SEC};">Category</td>'
                    f'<td style="padding:10px 0;text-align:right;">'
                    f'<span style="background:{cb};color:{cf};padding:3px 8px;border-radius:20px;font-size:11px;font-weight:700;">'
                    f'{res["category"]}</span></td></tr>'
                    f'<tr style="border-bottom:1px solid {BORDER};">'
                    f'<td style="padding:10px 0;color:{TEXT_SEC};">Scientific</td>'
                    f'<td style="padding:10px 0;text-align:right;font-style:italic;">{res["scientific_name"]}</td></tr>'
                    f'<tr style="border-bottom:1px solid {BORDER};">'
                    f'<td style="padding:10px 0;color:{TEXT_SEC};">Affects</td>'
                    f'<td style="padding:10px 0;text-align:right;">{res["affects"]}</td></tr>'
                    f'<tr><td style="padding:10px 0;color:{TEXT_SEC};">Severity</td>'
                    f'<td style="padding:10px 0;text-align:right;">'
                    f'<span style="background:{sb};color:{sf};padding:3px 8px;border-radius:20px;font-size:11px;font-weight:700;">'
                    f'{res["severity"]}</span></td></tr>'
                    f'</table>',
                    unsafe_allow_html=True,
                )

    # ── Description / Treatment / Prevention ─
    dc1, dc2, dc3 = st.columns(3)

    with dc1:
        with st.container(border=True):
            st.markdown('<div class="card-title">📖 Description</div>', unsafe_allow_html=True)
            st.markdown(f'<p style="font-size:13px;line-height:1.65;min-height:80px;">{res["description"]}</p>', unsafe_allow_html=True)

    with dc2:
        with st.container(border=True):
            st.markdown('<div class="card-title">💊 Treatment</div>', unsafe_allow_html=True)
            st.markdown(bullet_html(res["treatment"], conf > 0), unsafe_allow_html=True)

    with dc3:
        with st.container(border=True):
            st.markdown('<div class="card-title">🛡 Prevention</div>', unsafe_allow_html=True)
            st.markdown(bullet_html(res["prevention"], conf > 0), unsafe_allow_html=True)

    # ── Top 3 + Statistics ───────────────────
    tc1, tc2 = st.columns(2)
    TOP_COLORS = ["#10b981", "#fbbf24", "#8b5cf6"]

    with tc1:
        with st.container(border=True):
            st.markdown('<div class="card-title">⭐ Top 3 Predictions</div>', unsafe_allow_html=True)
            for i, (name, val) in enumerate(res["top3"]):
                clr      = TOP_COLORS[i] if conf > 0 else "rgba(128,128,128,.12)"
                txt_clr  = "inherit" if conf > 0 else "#64748b"
                num_bg   = clr if conf > 0 else "rgba(128,128,128,.1)"
                num_clr  = "white" if conf > 0 else "#64748b"
                st.markdown(
                    f'<div style="margin-bottom:14px;">'
                    f'<div style="display:flex;justify-content:space-between;font-size:13.5px;color:{txt_clr};margin-bottom:5px;">'
                    f'<span style="display:flex;align-items:center;gap:8px;">'
                    f'<span style="width:22px;height:22px;border-radius:50%;background:{num_bg};color:{num_clr};'
                    f'display:inline-flex;align-items:center;justify-content:center;font-size:11px;font-weight:700;">{i+1}</span>'
                    f'<span style="font-weight:500;">{name}</span></span>'
                    f'<span style="font-weight:700;">{val:.1f}%</span></div>'
                    f'<div style="width:100%;height:8px;background:rgba(128,128,128,.1);border-radius:4px;overflow:hidden;">'
                    f'<div style="width:{val}%;height:100%;background:{clr};border-radius:4px;"></div></div></div>',
                    unsafe_allow_html=True,
                )

    STATS = [("Rust",45,"#10b981"),("Early Blight",30,"#fbbf24"),("Leaf Spot",25,"#8b5cf6"),("Healthy",18,"#3b82f6"),("Other",10,"#6b7280")]

    with tc2:
        with st.container(border=True):
            st.markdown('<div class="card-title">📊 Prediction Statistics</div>', unsafe_allow_html=True)
            sc1, sc2 = st.columns([1, 1.1])
            with sc1:
                st.markdown(donut_svg(STATS), unsafe_allow_html=True)
            with sc2:
                rows = ""
                for name, count, color in STATS:
                    pct = count / 128 * 100
                    rows += (
                        f'<div style="display:flex;justify-content:space-between;align-items:center;'
                        f'font-size:12px;border-bottom:1px solid {BORDER};padding:5px 0;">'
                        f'<div style="display:flex;align-items:center;gap:8px;">'
                        f'<div style="width:10px;height:10px;border-radius:50%;background:{color};"></div>'
                        f'<span style="font-weight:500;">{name}</span></div>'
                        f'<span style="color:{TEXT_SEC};font-weight:600;">{count} ({pct:.0f}%)</span></div>'
                    )
                st.markdown(f'<div style="margin-top:10px;">{rows}</div>', unsafe_allow_html=True)

    # ── Occurrence chart ─────────────────────
    with st.container(border=True):
        ch1, ch2 = st.columns([3, 1])
        with ch1:
            st.markdown('<div class="card-title" style="border:none;margin:0;">📈 Disease Occurrence (Last 7 Days)</div>', unsafe_allow_html=True)
        with ch2:
            st.selectbox("Filter", ["Last 7 Days","Last 30 Days","All Time"], label_visibility="collapsed", key="occ_filter")

        base  = datetime.now()
        dates = [(base - timedelta(days=x)).strftime("%d %b") for x in range(6,-1,-1)]
        series = {
            "Rust":        [40,22,38,28,35,42,36],
            "Early Blight":[20,14,14, 9, 8, 9,13],
            "Leaf Spot":   [ 8,25,18,23,15,18,12],
            "Healthy":     [ 3,16,11,13,11,12, 2],
            "Other":       [ 1, 3, 5, 2, 4, 5, 7],
        }
        cmap = {"Rust":"#10b981","Early Blight":"#fbbf24","Leaf Spot":"#8b5cf6","Healthy":"#3b82f6","Other":"#6b7280"}

        fig, ax = plt.subplots(figsize=(12, 3.8), facecolor="none")
        ax.set_facecolor("none")
        for label, vals in series.items():
            c = cmap[label]
            ax.plot(dates, vals, color=c, linewidth=2, label=label, marker="o", markersize=4)
            ax.fill_between(dates, vals, alpha=0.06, color=c)
        ax.set_ylabel("Count", color=CHART_TXT, fontsize=9)
        ax.tick_params(colors=CHART_TXT, labelsize=8)
        for spine in ("top","right"): ax.spines[spine].set_visible(False)
        for spine in ("bottom","left"): ax.spines[spine].set_color(GRID_COLOR)
        ax.grid(axis="y", linestyle="--", color=GRID_COLOR, alpha=0.5)
        leg = ax.legend(loc="upper center", bbox_to_anchor=(.5,1.15), ncol=5, frameon=False, fontsize=8.5)
        for t in leg.get_texts(): t.set_color(CHART_TXT)
        plt.tight_layout()
        st.pyplot(fig, clear_figure=True)

    # ── Metric cards ────────────────────────
    mc1, mc2, mc3 = st.columns(3)
    metrics = [
        ("#10b981","rgba(16,185,129,.1)","Total Predictions","128","↑ 12% from last 7 days","#10b981"),
        ("#fbbf24","rgba(245,158,11,.1)","Model Accuracy","96.2%","↑ 3.5% from last 7 days","#10b981"),
        ("#8b5cf6","rgba(139,92,246,.1)","Diseases Detected","5","Total unique diseases",TEXT_SEC),
    ]
    for col, (stroke, bg, label, val, sub, sub_color) in zip((mc1,mc2,mc3), metrics):
        with col:
            st.markdown(
                f'<div style="background:{CARD_BG};border:1px solid {BORDER};padding:15px;'
                f'border-radius:12px;display:flex;align-items:center;gap:15px;box-shadow:{CARD_SHADOW};">'
                f'<div style="background:{bg};padding:10px;border-radius:10px;">'
                f'<svg width="24" height="24" fill="none" stroke="{stroke}" stroke-width="2" viewBox="0 0 24 24">'
                f'<circle cx="12" cy="12" r="10"/></svg></div>'
                f'<div><div style="font-size:11.5px;color:{TEXT_SEC};">{label}</div>'
                f'<div style="font-size:20px;font-weight:700;margin:2px 0;">{val}</div>'
                f'<div style="font-size:10.5px;color:{sub_color};">{sub}</div></div></div>',
                unsafe_allow_html=True,
            )

    st.markdown(
        f'<div style="text-align:center;font-size:11.5px;color:{TEXT_SEC};margin-top:30px;'
        f'border-top:1px solid {BORDER};padding-top:15px;">'
        f'© 2026 PlantAI · Developed with ❤️ by {st.session_state.username}</div>',
        unsafe_allow_html=True,
    )

# ─────────────────────────────────────────────
# DISEASE LIBRARY
# ─────────────────────────────────────────────
elif selected == "Disease Library":
    st.markdown(
        '<h1 style="margin:0;font-size:28px;font-weight:700;">📚 Disease Library</h1>'
        f'<p style="color:#94a3b8;font-size:13.5px;margin:5px 0 20px;">Browse supported plant diseases with symptoms, treatments, and prevention tips.</p>',
        unsafe_allow_html=True,
    )
    q = st.text_input("🔍 Search Diseases", placeholder="Type plant or disease name…")
    for key, d in DISEASE_DB.items():
        if q.lower() in d["display_name"].lower() or q.lower() in d["category"].lower():
            with st.container(border=True):
                treat_li = "".join(f"<li>{t}</li>" for t in d["treatment"])
                prev_li  = "".join(f"<li>{p}</li>" for p in d["prevention"])
                st.markdown(
                    f'<div style="display:flex;justify-content:space-between;align-items:center;">'
                    f'<span style="font-size:18px;font-weight:700;color:#10b981;">{d["display_name"]}</span>'
                    f'<span class="badge badge-purple">{d["category"]}</span></div>'
                    f'<div style="font-size:12px;font-style:italic;color:#64748b;margin:4px 0 10px;">'
                    f'Scientific: {d["scientific_name"]} · Affects: {d["affects"]}</div>'
                    f'<p style="font-size:13px;margin-bottom:12px;">{d["description"]}</p>'
                    f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:20px;'
                    f'border-top:1px solid {BORDER};padding-top:10px;">'
                    f'<div><strong style="color:#fbbf24;font-size:12.5px;">💊 Treatment</strong>'
                    f'<ul style="margin:5px 0;padding-left:20px;font-size:12px;">{treat_li}</ul></div>'
                    f'<div><strong style="color:#34d399;font-size:12.5px;">🛡 Prevention</strong>'
                    f'<ul style="margin:5px 0;padding-left:20px;font-size:12px;">{prev_li}</ul></div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )

# ─────────────────────────────────────────────
# STATISTICS
# ─────────────────────────────────────────────
elif selected == "Statistics":
    st.markdown(
        '<h1 style="margin:0;font-size:28px;font-weight:700;">📊 Detailed Statistics</h1>'
        f'<p style="color:#94a3b8;font-size:13.5px;margin:5px 0 20px;">Analysis of prediction data, accuracy ratings, and frequency curves.</p>',
        unsafe_allow_html=True,
    )
    STATS = [("Rust",45,"#10b981"),("Early Blight",30,"#fbbf24"),("Leaf Spot",25,"#8b5cf6"),("Healthy",18,"#3b82f6"),("Other",10,"#6b7280")]
    col1, col2 = st.columns(2)
    with col1:
        with st.container(border=True):
            st.markdown('<div class="card-title">Detection Share</div>', unsafe_allow_html=True)
            dc1, dc2 = st.columns([1,1])
            with dc1:
                st.markdown(donut_svg(STATS), unsafe_allow_html=True)
            with dc2:
                rows = ""
                for n, c, clr in STATS:
                    rows += (f'<div style="display:flex;justify-content:space-between;font-size:12.5px;padding:4px 0;">'
                             f'<div style="display:flex;align-items:center;gap:8px;">'
                             f'<div style="width:10px;height:10px;border-radius:50%;background:{clr};"></div>'
                             f'<span>{n}</span></div>'
                             f'<span style="color:{TEXT_SEC};font-weight:600;">{c} ({c/128*100:.0f}%)</span></div>')
                st.markdown(f'<div style="margin-top:15px;">{rows}</div>', unsafe_allow_html=True)
    with col2:
        with st.container(border=True):
            st.markdown('<div class="card-title">Model Performance</div>', unsafe_allow_html=True)
            st.markdown(
                f'<table style="width:100%;border-collapse:collapse;font-size:13.5px;">'
                f'<tr style="border-bottom:1px solid {BORDER};"><td style="padding:12px 0;color:{TEXT_SEC};">Avg Inference Time</td><td style="text-align:right;font-weight:600;">180 ms</td></tr>'
                f'<tr style="border-bottom:1px solid {BORDER};"><td style="padding:12px 0;color:{TEXT_SEC};">Top-1 Accuracy</td><td style="text-align:right;font-weight:600;color:#10b981;">96.2%</td></tr>'
                f'<tr style="border-bottom:1px solid {BORDER};"><td style="padding:12px 0;color:{TEXT_SEC};">Top-5 Accuracy</td><td style="text-align:right;font-weight:600;color:#10b981;">99.4%</td></tr>'
                f'<tr><td style="padding:12px 0;color:{TEXT_SEC};">F1-Score (Macro)</td><td style="text-align:right;font-weight:600;">0.958</td></tr>'
                f'</table>',
                unsafe_allow_html=True,
            )

# ─────────────────────────────────────────────
# HISTORY
# ─────────────────────────────────────────────
elif selected == "History":
    st.markdown(
        '<h1 style="margin:0;font-size:28px;font-weight:700;">🕒 Prediction History</h1>'
        f'<p style="color:#94a3b8;font-size:13.5px;margin:5px 0 20px;">Chronological log of scanned plant diseases.</p>',
        unsafe_allow_html=True,
    )
    if not st.session_state.history:
        st.info("No prediction history recorded yet.")
    else:
        with st.container(border=True):
            rows = ""
            for i, item in enumerate(st.session_state.history):
                rows += (
                    f'<tr style="border-bottom:1px solid {BORDER};">'
                    f'<td style="padding:12px 5px;color:#64748b;">{i+1}</td>'
                    f'<td style="padding:12px 5px;font-weight:600;color:#10b981;">{item["disease"]}</td>'
                    f'<td style="padding:12px 5px;text-align:center;">'
                    f'<span class="badge badge-green" style="font-size:10px;">{item["confidence"]:.0f}%</span></td>'
                    f'<td style="padding:12px 5px;text-align:right;color:#94a3b8;">{item["time"]}</td></tr>'
                )
            st.markdown(
                f'<table style="width:100%;border-collapse:collapse;font-size:13.5px;text-align:left;">'
                f'<thead><tr style="border-bottom:2px solid {BORDER};color:{TEXT_SEC};">'
                f'<th style="padding:10px 5px;">#</th>'
                f'<th style="padding:10px 5px;">Disease</th>'
                f'<th style="padding:10px 5px;text-align:center;">Confidence</th>'
                f'<th style="padding:10px 5px;text-align:right;">Time</th>'
                f'</tr></thead><tbody>{rows}</tbody></table>',
                unsafe_allow_html=True,
            )

# ─────────────────────────────────────────────
# PLANT CARE TIPS
# ─────────────────────────────────────────────
elif selected == "Plant Care Tips":
    st.markdown(
        '<h1 style="margin:0;font-size:28px;font-weight:700;">💡 Plant Care Tips</h1>'
        f'<p style="color:#94a3b8;font-size:13.5px;margin:5px 0 20px;">Practical guidelines to keep plants healthy and minimise disease onset.</p>',
        unsafe_allow_html=True,
    )
    tips = [
        ("💧","Watering Wisely","Irrigate at the roots rather than splashing foliage. Wet leaves are prime incubation sites for fungal and bacterial spores. Water early in the morning so excess moisture evaporates during the day."),
        ("💨","Airflow & Spacing","Overcrowding traps damp air inside the leaf canopy. Keep plants properly spaced and prune inner foliage to enhance wind circulation and sunlight penetration."),
        ("🍂","Soil Sanitation & Mulching","Fungal spores overwinter in old plant tissue. Lay fresh mulch as a barrier and clean up fallen infected leaves immediately. Sanitise pruners and cages regularly."),
        ("🧪","Nutrition & Stress Management","Keep crops vigorous with balanced organic compost. Stressed plants are highly susceptible to infection. Monitor nitrogen feeds, as excess can induce soft growth vulnerable to pests."),
    ]
    for icon, title, desc in tips:
        with st.container(border=True):
            st.markdown(
                f'<div style="font-size:18px;font-weight:700;color:#10b981;margin-bottom:8px;">{icon} {title}</div>'
                f'<p style="font-size:13.5px;line-height:1.65;margin:0;">{desc}</p>',
                unsafe_allow_html=True,
            )

# ─────────────────────────────────────────────
# SETTINGS
# ─────────────────────────────────────────────
elif selected == "Settings":
    st.markdown(
        '<h1 style="margin:0;font-size:28px;font-weight:700;">⚙ Settings</h1>'
        f'<p style="color:#94a3b8;font-size:13.5px;margin:5px 0 20px;">Configure your dashboard, theme, and detection preferences.</p>',
        unsafe_allow_html=True,
    )
    with st.container(border=True):
        st.markdown('<div class="card-title">User Preferences</div>', unsafe_allow_html=True)
        new_name = st.text_input("Display Name", value=st.session_state.username)
        if new_name.strip() and new_name.strip() != st.session_state.username:
            st.session_state.username = new_name.strip(); st.rerun()

        locs = list(WEATHER.keys())
        sel_loc = st.selectbox("Location", locs, index=locs.index(st.session_state.location))
        if sel_loc != st.session_state.location:
            st.session_state.location = sel_loc; st.rerun()

        themes = ["Dark Mode","Light Mode"]
        sel_theme = st.selectbox("Theme", themes, index=themes.index(st.session_state.theme))
        if sel_theme != st.session_state.theme:
            st.session_state.theme = sel_theme; st.rerun()

    with st.container(border=True):
        st.markdown('<div class="card-title">Detection Settings</div>', unsafe_allow_html=True)
        st.slider("Minimum Confidence Threshold (%)", 10, 100, 50)
        st.checkbox("Log detections for analytics", value=True)

# ─────────────────────────────────────────────
# ABOUT
# ─────────────────────────────────────────────
elif selected == "About Us":
    st.markdown(
        '<h1 style="margin:0;font-size:28px;font-weight:700;">🌱 About PlantAI</h1>'
        f'<p style="color:#94a3b8;font-size:13.5px;margin:5px 0 20px;">Technical overview and objectives of the AI Plant Disease Detection system.</p>',
        unsafe_allow_html=True,
    )
    with st.container(border=True):
        st.markdown(
            '<h3 style="color:#10b981;margin-top:0;">PlantAI Smart Detection System</h3>'
            '<p style="font-size:13.5px;line-height:1.65;">PlantAI is powered by a Convolutional Neural Network (CNN) built with <strong>TensorFlow / Keras</strong>. '
            'It scans foliar images, runs classification across 15 plant leaf states, and delivers real-time confidence scores '
            'with curated treatments and prevention guidelines.</p>'
            '<h4 style="margin-bottom:8px;">Core Features</h4>'
            '<ul style="font-size:13px;line-height:1.7;">'
            '<li><strong>TensorFlow 2.x CNN</strong> — high-accuracy classification optimised for plant leaves.</li>'
            '<li><strong>SVG Visualisations</strong> — gauge meters and donut charts rendered dynamically.</li>'
            '<li><strong>Dual Theme Engine</strong> — Light and Dark modes with full sidebar support.</li>'
            '<li><strong>Treatment Database</strong> — agricultural remedies for Solanaceae crops.</li>'
            '</ul>'
            f'<div style="background:rgba(16,185,129,.05);border:1px solid rgba(16,185,129,.12);'
            f'border-radius:8px;padding:12px;text-align:center;margin-top:20px;'
            f'font-size:13px;color:#10b981;font-weight:700;">'
            f'Developed with ❤️ by {st.session_state.username}</div>',
            unsafe_allow_html=True,
        )