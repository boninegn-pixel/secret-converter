import streamlit as st
from datetime import datetime
import random

# የፊደላት ዝርዝር
keys = "ሀሁሂሃሄህሆለሉሊላሌልሎሐሑሒሓሔሕሖመሙሚማሜምሞሠሡሢሣሤሥሦረሩሪራሬርሮሰሱሲሳሴስሶሸሹሺሻሼሽሾቀቁቂቃቄቅቆበቡቢባቤብቦተቱቲታቴትቶቸቹቺቻቼችቾነኑኒናኔንኖአኡኢኣኤእኦከኩኪካኬክኮወዉዊዋዌውዎዘዙዚዛዜዝዞየዩዪያዬይዮደዱዲዳዴድዶጀጁጂጃጄጅጆገጉጊጋጌግጎጠጡጢጣጤጥጦጨጩጪጫጬጭጮፈፉፊፋፌፍፎፐፑፒፓፔፕፖ "

st.set_page_config(page_title="ምስጢር ተርጓሚ", page_icon="🔐")

def get_daily_mapping():
    today = datetime.now().strftime("%Y-%m-%d")
    random.seed(today)
    all_numbers = [str(i).zfill(3) for i in range(100, 100 + len(keys))]
    random.shuffle(all_numbers)
    mapping = {char: num for char, num in zip(keys, all_numbers)}
    reverse_mapping = {num: char for char, num in mapping.items()}
    return mapping, reverse_mapping

st.title("🔐 ምስጢር ተርጓሚ")
st.write(f"ዛሬ፦ {datetime.now().strftime('%Y-%m-%d')}")
st.info("ይህ አፕ በየቀኑ ኮዱን ስለሚቀይር፣ መልእክቱ የሚፈታው በዕለቱ ብቻ ነው።")

mapping, reverse_mapping = get_daily_mapping()
option = st.radio("ምን ማድረግ ይፈልጋሉ?", ("መመሰጠር", "መተርጎም"))

if option == "መመሰጠር":
    user_text = st.text_area("አማርኛ ጽሁፍ ያስገቡ፦")
    if user_text:
        result = "".join([mapping.get(c, "000") for c in user_text])
        st.subheader("የተመሰጠረ ውጤት፦")
        st.code(result)

else:
    user_code = st.text_area("የምስጢር ቁጥሩን ያስገቡ፦")
    if user_code:
        result = "".join([reverse_mapping.get(user_code[i:i+3], "?") for i in range(0, len(user_code), 3)])
        st.subheader("የተፈታ መልእክት፦")
        st.success(result)
