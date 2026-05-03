import streamlit as st
from datetime import datetime
import random

# 1. የገጹን ስፋትና ርዕስ ማስተካከያ (ሁልጊዜ ከላይ መሆን አለበት)
st.set_page_config(page_title="ምስጢር ተርጓሚ", page_icon="🔐", layout="centered")

# 2. የይለፍ ቃል ማረጋገጫ ተግባር
def check_password():
    """ተጠቃሚው ትክክለኛ የይለፍ ቃል ማስገባቱን ያረጋግጣል"""
    if "password_correct" not in st.session_state:
        st.markdown("<h2 style='text-align: center;'>🔐 ምስጢር ተርጓሚ</h2>", unsafe_allow_html=True)
        st.write("---")
        st.warning("ይህንን አፕ ለመጠቀም እባክዎ የፍቃድ ቁልፍ ያስገቡ።")
        
        pwd = st.text_input("የይለፍ ቃል (Password)", type="password")
        if st.button("ግባ"):
            # እዚህ ጋር "2018" የሚለውን ወደፈለግከው ቁልፍ መቀየር ትችላለህ
            if pwd == "1993": 
                st.session_state["password_correct"] = True
                st.rerun()
            else:
                st.error("የተሳሳተ የይለፍ ቃል ነው! እባክዎ እንደገና ይሞክሩ።")
        return False
    else:
        return True

# 3. የይለፍ ቃሉ ትክክል ከሆነ ብቻ ዋናው አፕ ይከፈታል
if check_password():
    # ቁልፎች
    keys = "ሀሁሂሃሄህሆለሉሊላሌልሎሐሑሒሓሔሕሖመሙሚማሜምሞሠሡሢሣሤሥሦረሩሪራሬርሮሰሱሲሳሴስሶሸሹሺሻሼሽሾቀቁቂቃቄቅቆበቡቢባቤብቦተቱቲታቴትቶቸቹቺቻቼችቾኀኁኂኃኄኅኆነኑኒናኔንኖኘኙኚኛኜኝኞአኡኢአኤእኦከኩኪካኬክኮኸኹኺኻኼኽኾወዉዊዋዌውዎዐዑዒዓዔዕዖዘዙዚዛዜዝዞዠኡዢዣዤዥዦየዩዪያዬይዮደዱዲዳዴድዶጀጁጂጃጄጅጆገጉጊጋጌግጎጠጡጢጣጤጥጦጨጩጪጫጬጭጮጰጱጲጳጴጵጶጸጹጺጻጼጽጾፀፁፂፃፄፅፆፈፉፊፋፌፍፎፐፑፒፓፔፕፖ "

    def get_daily_mapping():
        today = datetime.now().strftime("%Y-%m-%d")
        random.seed(today)
        all_numbers = [str(i).zfill(3) for i in range(100, 100 + len(keys))]
        random.shuffle(all_numbers)
        mapping = {char: num for char, num in zip(keys, all_numbers)}
        reverse_mapping = {num: char for char, num in mapping.items()}
        return mapping, reverse_mapping

    # የዋናው ገጽ ዲዛይን
    st.title("🔐 ምስጢር ተርጓሚ")
    st.write(f"**ዛሬ:-** {datetime.now().strftime('%Y-%m-%d')}")
    st.info("ይህ አፕ በየቀኑ ኮዱ ስለሚቀየር መልእክቱ የሚፈታው በዕለቱ ብቻ ነው።")

    mapping, reverse_mapping = get_daily_mapping()
    option = st.radio("ምን ማድረግ ይፈልጋሉ?", ("መመስጠር", "መተርጎም"))

    if option == "መመስጠር":
        user_text = st.text_area("አማርኛ ጽሁፍ ያስገቡ:-", height=150)
        if user_text:
            result = "".join([mapping.get(c, "000") for c in user_text])
            st.subheader("የተመሰጠረ ውጤት:-")
            st.text_area("ኮፒ ለማድረግ እንዲመችህ እዚህ ጋር ተቀምጧል:-", result, height=200)
    else:
        user_code = st.text_area("የተመሰጠረ ቁጥር ያስገቡ:-", height=150)
        if user_code:
            # ባዶ ቦታዎችን ለማጽዳት
            user_code = user_code.replace(" ", "").replace("\n", "")
            result = "".join([reverse_mapping.get(user_code[i:i+3], "?") for i in range(0, len(user_code), 3)])
            st.subheader("የተፈታ መልእክት:-")
            st.success(result)
            
    # Logout ለማድረግ (አማራጭ)
    if st.sidebar.button("ውጣ (Logout)"):
        del st.session_state["password_correct"]
        st.rerun()
