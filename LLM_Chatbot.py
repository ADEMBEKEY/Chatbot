import streamlit as st
import requests

def inject_css():
    st.markdown("""
        <style>
        body {
            background-color: #eafae1;
        }
        .stApp {
            background: linear-gradient(145deg, #eafae1, #f6fff2);
        }
        .css-1cpxqw2 {
            background-color: #ffffffcc;
            border-radius: 10px;
            padding: 10px;
        }
        .css-1v0mbdj {
            background-color: #ffffffd9;
        }
        .stButton>button {
            background-color: #88c57f;
            color: white;
        }
        .stButton>button:hover {
            background-color: #6dae67;
        }
        </style>
    """, unsafe_allow_html=True)

# Sidebar for API Key
with st.sidebar:
    groq_api_key = st.text_input("Groq API Key", key="chatbot_api_key", type="password")
    "[Get a Groq API key](https://console.groq.com/)"

    # Hyperparameter Controls
    st.subheader("Model Hyperparameters 🌿")
    temperature = st.slider("Temperature", min_value=0.0, max_value=1.5, value=0.7, step=0.1)
    max_tokens = st.slider("Max Tokens", min_value=50, max_value=1000, value=500, step=50)
    top_p = st.slider("Top-p (Nucleus Sampling)", min_value=0.0, max_value=1.0, value=1.0, step=0.05)
    frequency_penalty = st.slider("Frequency Penalty", min_value=0.0, max_value=2.0, value=0.0, step=0.1)

# UI Header
st.title("🌱 AI Agriculture Assistant 🌱")

# Display image from URL
st.image("https://www.euractiv.fr/wp-content/uploads/sites/3/2020/02/shutterstock_700890880-800x450.jpg", use_column_width=True)

st.caption("🚜 A Streamlit chatbot powered by Groq (LLaMA model)")

st.markdown("""
# 🌾 Welcome to your AI Agriculture Assistant 🌱  
Ask me anything about crops, soils, irrigation, or pest control.  
I'm here to help you boost your yields sustainably 💧🌿
""")

# System message
system_message = {
    "role": "system",
    "content": (
        "You are an AI agriculture assistant, offering expert support in farming, crop management, soil health, irrigation, pest control, and sustainable agriculture techniques. "
        "Your responses should be practical, science-based, and tailored to specific agricultural contexts (crop type, climate, region, etc.). "
        "You should use agronomic principles, weather considerations, and soil data when advising.\n\n"

        "**Behavior Guidelines:**\n"
        "- Maintain a helpful, knowledgeable, and neutral tone.\n"
        "- Provide precise recommendations for different types of crops and conditions.\n"
        "- Reference best practices in sustainable agriculture.\n"
        "- Explain reasoning clearly (e.g., why a certain fertilizer or pesticide is advised).\n"
        "- Suggest tools, methods, or schedules when relevant.\n\n"

        "**Example Interactions:**\n\n"

        "🌾 *Crop Advice:*\n"
        "_User: What is the best fertilizer for wheat during early growth?_\n"
        "**AI:** 'During the tillering stage of wheat, nitrogen-rich fertilizers such as urea or DAP are recommended to promote leaf development and root strength. "
        "Apply around 40-50 kg/ha depending on soil nitrogen levels. Always check with a soil test before application.'\n\n"

        "🐛 *Pest Management:*\n"
        "_User: How to protect tomatoes from whiteflies?_\n"
        "**AI:** 'Whiteflies are best controlled through integrated pest management: Use yellow sticky traps, introduce natural predators like *Encarsia formosa*, and apply neem oil spray every 7–10 days. "
        "Avoid overuse of chemical insecticides to prevent resistance.'\n\n"

        "💧 *Irrigation Tips:*\n"
        "_User: How often should I water my maize crops in sandy soil?_\n"
        "**AI:** 'Sandy soils have low water retention, so maize should be watered more frequently — typically every 2–3 days during dry spells. "
        "Use drip irrigation if possible to reduce water loss and improve efficiency.'"
    )
}

# Reset conversation
if st.sidebar.button("🔁 Reset conversation"):
    st.session_state.messages = [system_message]
    st.experimental_rerun()

# Initialize session state
if "messages" not in st.session_state:
    st.session_state["messages"] = [system_message]

# Display chat history
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"**User:** {msg['content']}")
    elif msg["role"] == "assistant":
        st.markdown(f"**AI:** {msg['content']}")

# User input
prompt = st.text_input("Ask your question here:")
if prompt:
    if not groq_api_key:
        st.info("Please add your Groq API key to continue.")
        st.stop()

    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})

    # API request
    headers = {"Authorization": f"Bearer {groq_api_key}", "Content-Type": "application/json"}
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": st.session_state.messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "top_p": top_p,
        "frequency_penalty": frequency_penalty
    }

    response = requests.post("https://api.groq.com/openai/v1/chat/completions", json=payload, headers=headers)

    if response.status_code == 200:
        msg = response.json()["choices"][0]["message"]["content"]
        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.markdown(f"**AI:** {msg}")
    else:
        st.error(f"Error: Unable to get a response from Groq API. (Status Code: {response.status_code})")

# Inject CSS
inject_css()
