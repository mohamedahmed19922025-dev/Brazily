import streamlit as st

st.set_page_config(page_title="Main Menu", layout="centered")

# ========= Display Image =========
st.image("604666275_122204317928499086_8891459876267880658_n.jpg", use_column_width=True)   # غيّر اسم الصورة لو غير كده

# ========= Start Button =========
start = st.button("START")

# ========= Main Menu After Start =========
if start:
    st.subheader("Main Menu")
    st.write("اختر صفحة:")

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

# ========= Page Router =========
if "page" in st.session_state:
    page = st.session_state["page"]

    if page == "suppliers":
        st.title("📦 صفحة الموردين")
        st.write("محتوى صفحة الموردين هنا...")

    elif page == "inventory":
        st.title("🏪 صفحة المخزن")
        st.write("محتوى صفحة المخزن هنا...")

    elif page == "sales":
        st.title("🛒 صفحة المبيعات")
        st.write("محتوى صفحة المبيعات هنا...")

    elif page == "accounts":
        st.title("💰 صفحة الحسابات")
        st.write("محتوى صفحة الحسابات هنا...")