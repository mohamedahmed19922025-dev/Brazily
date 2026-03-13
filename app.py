import streamlit as st

st.set_page_config(page_title="Main Menu", layout="centered")

# ======= Custom Button Style =======
button_style = """
<style>
div.stButton > button {
    background-color: black;
    color: white;
    padding: 15px 40px;
    font-size: 22px;
    border-radius: 10px;
    width: 100%;
}
div.stButton > button:hover {
    background-color: #333333;
    color: white;
}
</style>
"""
st.markdown(button_style, unsafe_allow_html=True)

# ======= If user already pressed START → show menu only =======
if st.session_state.get("started", False):

    st.title("Main Menu")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("📦 صفحة الموردين"):
            st.session_state["page"] = "suppliers"

        if st.button("💰 صفحة الحسابات"):
            st.session_state["page"] = "accounts"

    with col2:
        if st.button("🏪 صفحة المخزن"):
            st.session_state["page"] = "inventory"

        if st.button("🛒 صفحة المبيعات"):
            st.session_state["page"] = "sales"

else:
    # ======= Show Image + Start Button (before starting) =======
    st.image("604666275_122204317928499086_8891459876267880658_n.jpg", use_column_width=True)

    col1, col2, col3 = st.columns(3)
    with col2:
        if st.button("START"):
            st.session_state["started"] = True
            st.rerun()

# ======= Page Content =======
if "page" in st.session_state:
    if st.session_state["page"] == "suppliers":
        st.title("📦 صفحة الموردين")
    elif st.session_state["page"] == "inventory":
        st.title("🏪 صفحة المخزن")
    elif st.session_state["page"] == "sales":
        st.title("🛒 صفحة المبيعات")
    elif st.session_state["page"] == "accounts":
        st.title("💰 صفحة الحسابات")
