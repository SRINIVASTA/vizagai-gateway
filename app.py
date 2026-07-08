import streamlit as st
import requests
import base64
import time
import os

# ==============================================================================
# 1. CORE CONFIGURATION & ENVIRONMENTAL SECURITY
# ==============================================================================
BRAND_NAME = "VizagAI Gateway"
BRAND_LOGO = "🤖"

# Streamlit securely extracts these variables from your web settings secrets panel
EVOLUTION_API_BASE_URL = st.secrets["EVOLUTION_API_BASE_URL"]
MASTER_SYSTEM_KEY = st.secrets["EVOLUTION_MASTER_KEY"]
COMMUNITY_PASSWORD = st.secrets["GATEWAY_PASSWORD"]

st.set_page_config(page_title=f"{BRAND_NAME} | Dashboard", page_icon=BRAND_LOGO, layout="wide")

# ==============================================================================
# 2. LIGHTWEIGHT COMMUNITY AUTHENTICATION LAYER
# ==============================================================================
def check_community_access():
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if st.session_state["authenticated"]:
        return True

    st.markdown(f"## {BRAND_LOGO} Welcome to {BRAND_NAME}")
    st.caption("This system provisions isolated automated WhatsApp channels for verified developers.")
    
    user_entry = st.text_input("Enter Community Access Token Key:", type="password")
    
    if st.button("Unlock Developer Workspace", type="primary"):
        if user_entry == COMMUNITY_PASSWORD:
            st.session_state["authenticated"] = True
            st.success("Access authorized successfully!")
            time.sleep(0.5)
            st.rerun()
        else:
            st.error("Invalid token credential configuration string. Please verify inside your community portal.")
    return False

# ==============================================================================
# 3. HELPER FUNCTIONS TO TALK TO THE BACKEND ENGINE
# ==============================================================================
def create_new_instance(instance_name):
    endpoint = f"{EVOLUTION_API_BASE_URL}/instance/create"
    headers = {
        "apiKey": MASTER_SYSTEM_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "instanceName": instance_name,
        "qrcode": True
    }
    try:
        response = requests.post(endpoint, json=payload, headers=headers, timeout=15)
        if response.status_code in:
            return response.json()
        else:
            st.error(f"Backend Engine Error ({response.status_code}): {response.text}")
            return None
    except Exception as e:
        st.error(f"Could not connect to the cloud API server: {e}")
        return None

def check_instance_status(instance_name):
    endpoint = f"{EVOLUTION_API_BASE_URL}/instance/connectionStatus/{instance_name}"
    headers = {"apiKey": MASTER_SYSTEM_KEY}
    try:
        response = requests.get(endpoint, headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, dict):
                return data.get("instance", {}).get("state", "DISCONNECTED")
            return "DISCONNECTED"
        return "DISCONNECTED"
    except:
        return "ERROR"

# ==============================================================================
# 4. PRIMARY USER WORKSPACE INTERFACE
# ==============================================================================
if check_community_access():
    st.title(f"{BRAND_LOGO} {BRAND_NAME} - White Label API Portal")
    st.caption("Provision isolated background automated WhatsApp channels instantly.")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("🛠️ Provision New Channel")
        user_instance_name = st.text_input("Enter Instance Name / Client Name:", placeholder="e.g., client_vizag_1").strip()
        
        if st.button("Generate Activation QR Code", type="primary"):
            if not user_instance_name:
                st.warning("Please enter a valid instance identifier name.")
            else:
                with st.spinner("Spawning container pipeline instances..."):
                    api_data = create_new_instance(user_instance_name)
                    
                    if api_data:
                        instance_root = api_data.get("instance", api_data)
                        hash_root = api_data.get("hash", instance_root)
                        qrcode_root = api_data.get("qrcode", instance_root)
                        
                        st.session_state["active_instance"] = user_instance_name
                        st.session_state["user_token"] = hash_root.get("apikey", hash_root.get("token"))
                        st.session_state["qr_string"] = qrcode_root.get("base64", "")
                        st.success("Instance engine generated successfully!")

    with col2:
        if "active_instance" in st.session_state:
            active_inst = st.session_state['active_instance']
            st.subheader(f"📲 Connection Matrix for: `{active_inst}`")
            st.info(f"**Your Custom API Token:** `{st.session_state['user_token']}`")
            
            current_status = check_instance_status(active_inst).lower()
            st.metric(label="Channel Authorization Status", value=current_status.upper())
            
            if current_status != "connected":
                if st.session_state.get("qr_string"):
                    st.write("👉 Open WhatsApp on your phone -> Linked Devices -> Scan the code below:")
                    try:
                        raw_b64 = st.session_state["qr_string"]
                        if "," in raw_b64:
                            raw_b64 = raw_b64.split(",")[-1]
                        
                        qr_bytes = base64.b64decode(raw_b64)
                        st.image(qr_bytes, width=320)
                    except Exception as decode_err:
                        st.error("Failed to decode visual QR base64 matrix streams.")
                else:
                    st.warning("No live QR token payload discovered for this configuration block. Re-generate session.")
                    
                if st.button("🔄 Refresh Connection Status"):
                    st.rerun()
            else:
                st.balloons()
                st.success("🎉 Channel is authenticated and ready to route automation payload strings!")
                
                st.write("---")
                st.subheader("🚀 Code Generator for Google Colab")
                
                test_phone = st.text_input(
                    "Enter Destination WhatsApp Number (with Country Code) or Group JID:", 
                    value="918897415303"
                )
                
                st.markdown("### 💻 Example Payload Execution Script for your Clients:")
                example_code = f"""import requests

url = "{EVOLUTION_API_BASE_URL}/message/sendText/{active_inst}"
headers = {{
    "apiKey": "{st.session_state['user_token']}",
    "Content-Type": "application/json"
}}
payload = {{
    "number": "{test_phone}",
    "options": {{"delay": 1200, "presence": "composing"}},
    "textMessage": {{
        "text": "Hello from my custom API brand! 🚀"
    }}
}}
response = requests.post(url, json=payload, headers=headers)
print(response.json())"""
                st.code(example_code, language="python")
        else:
            st.info("👈 Enter an instance name and generate a configuration layer to view authentication assets here.")
