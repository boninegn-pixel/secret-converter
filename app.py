import streamlit as st
from cryptography.fernet import Fernet
import streamlit.components.v1 as components

# ገጹን ማስተካከል
st.set_page_config(page_title="Mister Terguami Pro", layout="centered")

# Password መጀመሪያ በ "1234" እንዲጀምር
if 'app_password' not in st.session_state:
    st.session_state.app_password = "1234"

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# --- የመግቢያ ክፍል ---
if not st.session_state.authenticated:
    st.title("🔐 መግቢያ")
    pwd_input = st.text_input("የአፑን የይለፍ ቃል ያስገቡ:", type="password")
    if st.button("ግባ"):
        if pwd_input == st.session_state.app_password:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("የይለፍ ቃል ተሳስቷል!")
    st.stop()

# --- ዋናው አፕ ---
st.title("🛡️ ሚስጥራዊ መልዕክት መላኪያ")

if 'key' not in st.session_state:
    st.session_state.key = Fernet.generate_key()

cipher_suite = Fernet(st.session_state.key)

# ኮፒ ለማድረግ የሚረዳ የ JavaScript ኮድ
def copy_button(text_to_copy):
    html_code = f"""
    <button onclick="navigator.clipboard.writeText('{text_to_copy}')" 
    style="background-color: #4CAF50; color: white; border: none; padding: 10px 20px; 
    border-radius: 5px; cursor: pointer; width: 100%; font-size: 16px; margin-top: 5px;">
    📋 ኮፒ አድርግ
    </button>
    """
    return components.html(html_code, height=60)

tab1, tab2, tab3 = st.tabs(["መልዕክት እሰር", "መልዕክት ፍታ", "⚙️ ሴቲንግ"])

with tab1:
    # የጽሁፍ ሳጥኑን ለማጽዳት እንዲረዳ "key" ሰጥተነዋል
    user_text = st.text_area("የሚታሰረውን መልዕክት እዚህ ይጻፉ:", height=150, key="encrypt_input")
    
    col1, col2 = st.columns(2)
    with col1:
        process_btn = st.button("🔐 በኮድ እሰር", use_container_width=True)
    with col2:
        # ሳጥኑን የሚያጸዳ ቁልፍ
        if st.button("🗑️ አጽዳ (Delete)", use_container_width=True):
            st.session_state.encrypt_input = ""
            st.rerun()

    if process_btn:
        if user_text:
            token = cipher_suite.encrypt(user_text.encode()).decode()
            st.success("መልዕክቱ በስኬት ታስሯል!")
            st.text_area("የታሰረው ውጤት:", value=token, height=150)
            copy_button(token)
            
            whatsapp_url = f"https://wa.me/?text={token}"
            st.markdown(f'<a href="{whatsapp_url}" target="_blank"><button style="background-color:#25D366; color:white; border:none; padding:12px 24px; border-radius:8px; cursor:pointer; width:100%; font-size:18px; margin-top:10px;">📲 በ WhatsApp ላክ</button></a>', unsafe_allow_html=True)

with tab2:
    code_to_decrypt = st.text_area("የታሰረውን ኮድ እዚህ ያስገቡ:", height=150, key="decrypt_input")
    input_key = st.text_input("የምስጠራ ቁልፉን (Key) ያስገቡ:")
    
    col3, col4 = st.columns(2)
    with col3:
        decrypt_btn = st.button("🔓 መልዕክቱን ፍታ", use_container_width=True)
    with col4:
        if st.button("🗑️ አጽዳ", use_container_width=True):
            st.session_state.decrypt_input = ""
            st.rerun()

    if decrypt_btn:
        try:
            custom_cipher = Fernet(input_key.encode())
            decrypted = custom_cipher.decrypt(code_to_decrypt.encode()).decode()
            st.success("መልዕክቱ ተፈቷል!")
            st.text_area("የተፈታ መልዕክት:", value=decrypted, height=150)
            copy_button(decrypted)
        except:
            st.error("ቁልፉ ወይም ኮዱ ስህተት ነው!")

with tab3:
    st.subheader("የአፕ ሴቲንግ")
    current_key = st.session_state.key.decode()
    st.info(f"የአሁኑ መቆለፊያ ቁልፍ (Key): {current_key}")
    copy_button(current_key)
        
    st.write("---")
    st.write("የመግቢያ Password መቀየሪያ")
    current_pwd = st.text_input("የድሮውን Password ያስገቡ:", type="password")
    new_pwd = st.text_input("አዲሱን Password ያስገቡ:", type="password")
    
    if st.button("Password ቀይር"):
        if current_pwd == st.session_state.app_password:
            st.session_state.app_password = new_pwd
            st.success("Password ተቀይሯል!")
        else:
            st.error("የድሮው Password ስህተት ነው።")

if st.sidebar.button("Log out"):
    st.session_state.authenticated = False
    st.rerun()
