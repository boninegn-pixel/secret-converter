import streamlit as st
from cryptography.fernet import Fernet

# ገጹን ማስተካከል
st.set_page_config(page_title="Mister Terguami Pro", layout="centered")

# Password መጀመሪያ በ "1234" እንዲጀምር በ memory መያዝ
if 'app_password' not in st.session_state:
    st.session_state.app_password = "1234"

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# --- የመግቢያ ክፍል (Login) ---
if not st.session_state.authenticated:
    st.title("🔐 መግቢያ")
    pwd_input = st.text_input("የአፑን የይለፍ ቃል ያስገቡ:", type="password")
    if st.button("ግባ"):
        if pwd_input == st.session_state.app_password:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("የይለፍ ቃል ተሳስቷል!")
    st.stop() # ትክክለኛ Password እስካልገባ ድረስ ቀሪው ኮድ አይታይም

# --- ዋናው አፕ (ካለፈ በኋላ) ---
st.title("🛡️ ሚስጥራዊ መልዕክት መላኪያ")

# ቁልፍ (Key) ማመንጫ
if 'key' not in st.session_state:
    st.session_state.key = Fernet.generate_key()

cipher_suite = Fernet(st.session_state.key)

# ሶስት ታቦችን (Tabs) መፍጠር
tab1, tab2, tab3 = st.tabs(["እሰር", "ፍታ", "⚙️ ሴቲንግ"])

with tab1:
    user_text = st.text_area("የሚታሰረውን መልዕክት ይጻፉ:")
    if st.button("በኮድ እሰር"):
        if user_text:
            token = cipher_suite.encrypt(user_text.encode())
            st.code(token.decode())
            whatsapp_url = f"https://wa.me/?text={token.decode()}"
            st.markdown(f'<a href="{whatsapp_url}" target="_blank">በ WhatsApp ላክ</a>', unsafe_allow_html=True)

with tab2:
    code_to_decrypt = st.text_area("የታሰረውን ኮድ እዚህ ያስገቡ:")
    input_key = st.text_input("የምስጠራ ቁልፉን (Key) ያስገቡ:")
    if st.button("መልዕክቱን ፍታ"):
        try:
            custom_cipher = Fernet(input_key.encode())
            decrypted = custom_cipher.decrypt(code_to_decrypt.encode()).decode()
            st.success(f"የተፈታ መልዕክት: {decrypted}")
        except:
            st.error("ቁልፉ ወይም ኮዱ ስህተት ነው!")

# --- ሴቲንግ (Password መቀየሪያ) ---
with tab3:
    st.subheader("የአፕ ሴቲንግ")
    st.write("የአፑን መግቢያ የይለፍ ቃል እዚህ መቀየር ይችላሉ።")
    
    current_pwd = st.text_input("የድሮውን Password ያስገቡ:", type="password")
    new_pwd = st.text_input("አዲሱን Password ያስገቡ:", type="password")
    confirm_pwd = st.text_input("አዲሱን Password ድገሙት:", type="password")
    
    if st.button("Password ቀይር"):
        if current_pwd != st.session_state.app_password:
            st.error("የድሮው Password ትክክል አይደለም!")
        elif new_pwd != confirm_pwd:
            st.error("አዲሱ Password እና ድጋሚው አይመሳሰሉም!")
        elif len(new_pwd) < 4:
            st.warning("Password ቢያንስ 4 ፊደል/ቁጥር መሆን አለበት!")
        else:
            st.session_state.app_password = new_pwd
            st.success("የይለፍ ቃል በስኬት ተቀይሯል! በሚቀጥለው ሲገቡ አዲሱን ይጠቀሙ።")

if st.sidebar.button("Log out"):
    st.session_state.authenticated = False
    st.rerun()
