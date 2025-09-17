import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit.components.v1 as components

from PIL import Image
import streamlit as st

logo = Image.open("generated-image.png")  # Make sure the filename matches exactly!
st.image(logo, width=150)                   # You can change width to fit your style


if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False

def generate_recommendations(os_type, software, network, sim_result):
    recommendations = []

    if os_type == "Windows":
        recommendations.append("Windows OS is prone to attacks. Keep it updated regularly.")
    elif os_type == "Linux":
        recommendations.append("Linux platforms are generally safer. Apply patches timely.")

    if "outdated" in software.lower():
        recommendations.append("Update your software packages to their latest versions.")

    if network == "Corporate":
        recommendations.append("Use VPN and strong endpoint protection on corporate networks.")
    elif network == "Cloud":
        recommendations.append("Enable multi-factor authentication for cloud services.")

    if sim_result == "breach":
        recommendations.append("Simulation breach detected! Change passwords immediately & enable MFA.")
    elif sim_result == "warning":
        recommendations.append("Simulation showed risky behavior. Review your security settings.")
    else:
        recommendations.append("Your system appears secure based on simulations. Keep it up!")

    return recommendations

def calculate_security_score(os_type, software, network, simulation_result=None):
    score = 100
    
    # Reduce score based on OS
    if os_type == "Windows":
        score -= 20
    elif os_type == "Linux":
        score -= 5
    else:  # MacOS
        score -= 10
    
    # Reduce score if user software list has old versions (demo)
    if "outdated" in software.lower():
        score -= 30
    
    # Network risk
    if network == "Corporate":
        score -= 10
    elif network == "Cloud":
        score -= 5
    
    # Simulation effect
    if simulation_result == "breach":
        score -= 30
    elif simulation_result == "warning":
        score -= 10
    
    if score < 0:
        score = 0
    return score

st.set_page_config(page_title="AegisAI", page_icon="🛡️", layout="wide")

st.title("AegisAI: Adaptive Cyber Defense")
st.write("Welcome to your smart cyber defense dashboard!")

# Sidebar: User inputs and Security Score
st.sidebar.header("Describe Your Setup")

os_type = st.sidebar.selectbox(
    "Select your Operating System",
    ["Windows", "Linux", "MacOS"],
    help="Choose the operating system you use on your device."
)

software = st.sidebar.text_input(
    "Key Software (comma-separated)",
    help="Type important software you use, separated by commas. Mention if any are outdated."
)

network = st.sidebar.selectbox(
    "Network Type",
    ["Home", "Corporate", "Cloud"],
    help="Select the network environment where you connect to the internet."
)

# Simple security score (we'll improve this later)
security_score = 75
# Get simulation result from session state (set after attacks)
sim_result = st.session_state.get("sim_result", None)

security_score = calculate_security_score(os_type, software, network, sim_result)

st.sidebar.markdown("---")
score_color = "#FDE74C" if security_score > 70 else "#FF4B4B"
st.sidebar.markdown(f"<h2 style='color:{score_color}'>Security Score: {security_score}/100</h2>", unsafe_allow_html=True)
st.sidebar.progress(security_score)
if security_score > 70:
    st.sidebar.success("Great job! Keep your system updated and safe.")
else:
    st.sidebar.warning("Your system is at risk! Follow recommendations.")
dark_mode = st.sidebar.checkbox("Dark Mode", value=st.session_state.dark_mode)

if dark_mode != st.session_state.dark_mode:
    st.session_state.dark_mode = dark_mode
    theme = 'dark' if dark_mode else 'light'
    st.experimental_set_query_params(theme=theme)
    st.experimental_rerun()


# Tabs for main content
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🕒 Attack Forecast",
    "🧮 Config Analyzer",
    "💣 Attack Simulator",
    "🌍 Global Defense",
    "🔍 Recommendations"
])
with tab1:
    st.header("🕒 Attack Forecast Timeline")
    st.write("These are the predicted threats for the next few days (demo data):")
    
    # Create some fake prediction data
    forecast = pd.DataFrame({
        "Threat": ["Ransomware", "Phishing", "Brute Force", "Malware"],
        "Predicted Date": ["2025-09-18", "2025-09-19", "2025-09-20", "2025-09-21"],
        "Risk Level": [85, 62, 45, 39]
    })
    
    fig = px.bar(
        forecast, 
        x="Threat", 
        y="Risk Level", 
        color="Risk Level", 
        color_continuous_scale="redor", 
        text="Predicted Date"
    )
    fig.update_traces(textposition='outside')
    fig.update_layout(yaxis=dict(title="Risk Level (0-100)"), xaxis=dict(title="Threat"))
    st.plotly_chart(fig, use_container_width=True)

    st.info("⚠️ Highest alert: Ransomware expected soon! Patch and back up your data.")

with tab2:
    st.header("🧮 Configuration Analyzer")
    st.write("Upload your config file (txt or json), or just enter system details in the sidebar!")
config_file = st.file_uploader("Upload a configuration file", type=["txt", "json"])
if config_file:
    st.success("✅ File uploaded successfully!")
    # Your existing pretend scan or analysis here
else:
    st.info("Please upload a config file for analysis.")


with tab3:
    st.header("💣 Simulated Attack")
    st.write("Choose an attack scenario to test your defense (demo logic):")
    
    scenario = st.selectbox("Attack scenario", ["Brute Force", "Phishing", "Malware"])
    simulate = st.button("Run Simulation", key="simulate_button")
    if simulate:
    # After simulation code
        st.success("Simulation Completed Successfully!")

    # Initialize flags in session state if not present
    if "balloons_shown" not in st.session_state:
        st.session_state["balloons_shown"] = False
    if "snow_shown" not in st.session_state:
        st.session_state["snow_shown"] = False

    if simulate:
        # Reset flags every time simulation button is clicked to allow re-showing effects
        st.session_state["balloons_shown"] = False
        st.session_state["snow_shown"] = False

        if scenario == "Brute Force":
                st.warning("Attacker is trying to guess your password...")
        st.success("Result: Password is strong! Attack failed. 😊")
        if not st.session_state["balloons_shown"]:
            st.balloons()
            st.session_state["balloons_shown"] = True
        st.info("Brute Force attack simulation completed successfully.")
        st.session_state["sim_result"] = "safe"

    elif scenario == "Phishing":
        st.info("You receive a suspicious email...")
        st.success("Result: You did NOT click the fake link—defense success!")
        if not st.session_state["snow_shown"]:
                st.snow()
                st.session_state["snow_shown"] = True
        st.info("Phishing attack simulation completed successfully.")
        st.session_state["sim_result"] = "safe"

    else:
        st.error("Attacker uploaded malware...")
        with st.spinner('Analyzing malware...'):
            import time
            time.sleep(3)
        st.success("Malware neutralized successfully!")
        # Show both balloons and snow but only once each
        if not st.session_state["balloons_shown"]:
            st.balloons()
            st.session_state["balloons_shown"] = True
        if not st.session_state["snow_shown"]:
            st.snow()
            st.session_state["snow_shown"] = True
        st.info("Malware attack simulation completed successfully.")
        st.session_state["sim_result"] = "safe"

with tab4:
    st.header("🌍 Global Defense Dashboard")
    st.write("Overview of blocked cyber attacks by country")

    # Sample data - replace with real feed later
    data = pd.DataFrame({
        "Country": ["USA", "India", "UK", "Germany", "France"],
        "Blocked Attacks": [1200, 950, 300, 400, 250]
    })

    fig = px.pie(data, names='Country', values='Blocked Attacks', hole=0.4, 
                 color_discrete_sequence=px.colors.sequential.OrRd)
    
    st.plotly_chart(fig, use_container_width=True)

    st.write("The pie chart above shows estimated blocked attacks per country.")

with tab5:
    st.header("🔍 Actionable Recommendations")
    recs = generate_recommendations(os_type, software, network, sim_result)
    for r in recs:
        st.write(f"• {r}")
        st.markdown("""
    <footer style='text-align: center; padding: 10px; color: gray; font-size: small;'>
        © 2025 AegisAI • All rights reserved.
    </footer>
""", unsafe_allow_html=True)
