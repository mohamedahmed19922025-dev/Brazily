# ============================================================================
# نظام إدارة المبيعات والمخزون والمحاسبة - POS System
# ملف واحد شامل مع قواعد بيانات إكسيل
# ============================================================================

import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta
import hashlib
from PIL import Image
import io

# ============================================================================
# إعدادات الصفحة والتنسيق
# ============================================================================
st.set_page_config(
    page_title="نظام المبيعات والمخزون",
    page_icon="🏪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# تنسيقات CSS مخصصة
# ============================================================================
st.markdown("""
<style>
    /* إخفاء عناصر Streamlit الافتراضية */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* تنسيق الأزرار */
    .stButton > button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        font-weight: bold;
    }
    
    /* تنسيق الصناديق */
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        margin: 10px 0;
    }
    
    /* تنسيق الجداول */
    .dataframe {
        font-size: 14px;
    }
    
    /* تنسيق القائمة الجانبية */
    .sidebar-content {
        padding: 20px;
    }
    
    /* ألوان مخصصة */
    .success-box {
        background-color: #d4edda;
        padding: 15px;
        border-radius: 5px;
        border: 1px solid #c3e6cb;
    }
    
    .warning-box {
        background-color: #fff3cd;
        padding: 15px;
        border-radius: 5px;
        border: 1px solid #ffeeba;
    }
    
    .danger-box {
        background-color: #f8d7da;
        padding: 15px;
        border-radius: 5px;
        border: 1px solid #f5c6cb;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# ثوابت ومسارات الملفات
# ============================================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
IMAGES_DIR = os.path.join(BASE_DIR, "products_images")

# ملفات الإكسيل
USERS_FILE = os.path.join(DATA_DIR, "users.xlsx")
PRODUCTS_FILE = os.path.join(DATA_DIR, "products.xlsx")
CUSTOMERS_FILE = os.path.join(DATA_DIR, "customers.xlsx")
SUPPLIERS_FILE = os.path.join(DATA_DIR, "suppliers.xlsx")
SALES_FILE = os.path.join(DATA_DIR, "sales.xlsx")
EXPENSES_FILE = os.path.join(DATA_DIR, "expenses.xlsx")
MANUAL_INCOME_FILE = os.path.join(DATA_DIR, "manual_income.xlsx")
LEDGER_FILE = os.path.join(DATA_DIR, "ledger.xlsx")

# ============================================================================
# دوال إنشاء المجلدات والملفات
# ============================================================================
def create_directories():
    """إنشاء المجلدات اللازمة"""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    if not os.path.exists(IMAGES_DIR):
        os.makedirs(IMAGES_DIR)

def create_excel_files():
    """إنشاء ملفات الإكسيل إذا لم تكن موجودة"""
    create_directories()
    
    # ملف المستخدمين
    if not os.path.exists(USERS_FILE):
        df_users = pd.DataFrame({
            'username': ['admin', 'seller1'],
            'password': [hash_password('admin123'), hash_password('seller123')],
            'role': ['admin', 'seller'],
            'name': ['المدير', 'البائع']
        })
        df_users.to_excel(USERS_FILE, index=False)
    
    # ملف المنتجات
    if not os.path.exists(PRODUCTS_FILE):
        df_products = pd.DataFrame(columns=[
            'product_code', 'product_name', 'price', 'cost', 
            'quantity', 'min_quantity', 'image_name', 'category'
        ])
        df_products.to_excel(PRODUCTS_FILE, index=False)
    
    # ملف العملاء
    if not os.path.exists(CUSTOMERS_FILE):
        df_customers = pd.DataFrame(columns=[
            'customer_code', 'customer_name', 'phone', 'email', 'address'
        ])
        df_customers.to_excel(CUSTOMERS_FILE, index=False)
    
    # ملف الموردين
    if not os.path.exists(SUPPLIERS_FILE):
        df_suppliers = pd.DataFrame(columns=[
            'supplier_code', 'supplier_name', 'phone', 'email', 'address'
        ])
        df_suppliers.to_excel(SUPPLIERS_FILE, index=False)
    
    # ملف المبيعات
    if not os.path.exists(SALES_FILE):
        df_sales = pd.DataFrame(columns=[
            'sale_id', 'date', 'customer_code', 'customer_name',
            'total_amount', 'payment_method', 'user_id', 'items'
        ])
        df_sales.to_excel(SALES_FILE, index=False)
    
    # ملف المصروفات
    if not os.path.exists(EXPENSES_FILE):
        df_expenses = pd.DataFrame(columns=[
            'expense_id', 'date', 'description', 'amount', 'category', 'user_id'
        ])
        df_expenses.to_excel(EXPENSES_FILE, index=False)
    
    # ملف الإيرادات اليدوية
    if not os.path.exists(MANUAL_INCOME_FILE):
        df_income = pd.DataFrame(columns=[
            'income_id', 'date', 'description', 'amount', 'customer_code', 'user_id'
        ])
        df_income.to_excel(MANUAL_INCOME_FILE, index=False)
    
    # ملف سجل الحسابات (Ledger)
    if not os.path.exists(LEDGER_FILE):
        df_ledger = pd.DataFrame(columns=[
            'ledger_id', 'date', 'party_type', 'party_code', 'party_name',
            'debit', 'credit', 'description', 'reference_id', 'user_id'
        ])
        df_ledger.to_excel(LEDGER_FILE, index=False)

# ============================================================================
# دوال مساعدة
# ============================================================================
def hash_password(password):
    """تشفير كلمة المرور"""
    return hashlib.sha256(password.encode()).hexdigest()

def generate_id(prefix):
    """توليد معرف فريد"""
    return f"{prefix}{datetime.now().strftime('%Y%m%d%H%M%S')}"

def format_currency(amount):
    """تنسيق العملة"""
    return f"{amount:,.2f} ج.م"

def get_current_date():
    """الحصول على التاريخ الحالي"""
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def read_excel(file_path):
    """قراءة ملف إكسيل بأمان"""
    try:
        if os.path.exists(file_path):
            return pd.read_excel(file_path)
        return pd.DataFrame()
    except Exception as e:
        st.error(f"خطأ في قراءة الملف: {str(e)}")
        return pd.DataFrame()

def save_excel(df, file_path):
    """حفظ ملف إكسيل بأمان"""
    try:
        df.to_excel(file_path, index=False)
        return True
    except Exception as e:
        st.error(f"خطأ في حفظ الملف: {str(e)}")
        return False

def save_product_image(uploaded_file, product_code):
    """حفظ صورة المنتج"""
    if uploaded_file is not None:
        image_name = f"{product_code}_{uploaded_file.name}"
        image_path = os.path.join(IMAGES_DIR, image_name)
        
        # حفظ الصورة
        with open(image_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        return image_name
    return None

def load_product_image(image_name):
    """تحميل صورة المنتج"""
    if image_name and os.path.exists(os.path.join(IMAGES_DIR, image_name)):
        return Image.open(os.path.join(IMAGES_DIR, image_name))
    return None

def add_ledger_entry(party_type, party_code, party_name, debit, credit, description, reference_id, user_id):
    """إضافة قيد في سجل الحسابات"""
    df_ledger = read_excel(LEDGER_FILE)
    
    new_entry = {
        'ledger_id': generate_id('L'),
        'date': get_current_date(),
        'party_type': party_type,
        'party_code': party_code,
        'party_name': party_name,
        'debit': debit if debit else 0,
        'credit': credit if credit else 0,
        'description': description,
        'reference_id': reference_id,
        'user_id': user_id
    }
    
    df_ledger = pd.concat([df_ledger, pd.DataFrame([new_entry])], ignore_index=True)
    save_excel(df_ledger, LEDGER_FILE)

def get_party_balance(party_type, party_code):
    """حساب رصيد العميل أو المورد (مدين - دائن)"""
    df_ledger = read_excel(LEDGER_FILE)
    
    if df_ledger.empty:
        return 0
    
    party_entries = df_ledger[
        (df_ledger['party_type'] == party_type) & 
        (df_ledger['party_code'] == party_code)
    ]
    
    total_debit = party_entries['debit'].sum()
    total_credit = party_entries['credit'].sum()
    
    # إذا كان المدين > الدائن = العميل مدين (له علينا)
    # إذا كان الدائن > المدين = العميل دائن (علينا له)
    return total_debit - total_credit

# ============================================================================
# صفحة تسجيل الدخول
# ============================================================================
def login_page():
    """صفحة تسجيل الدخول"""
    st.markdown("<h1 style='text-align: center; color: #1f77b4;'>🏪 نظام إدارة المبيعات</h1>", unsafe_allow_html=True)
    
    # عرض اللوجو
    logo_path = os.path.join(BASE_DIR, "logo.png")
    if os.path.exists(logo_path):
        try:
            logo = Image.open(logo_path)
            logo = logo.resize((200, 200))
            st.image(logo, use_container_width=False)
        except:
            st.markdown("<div style='text-align: center; font-size: 100px;'>🏪</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div style='text-align: center; font-size: 100px;'>🏪</div>", unsafe_allow_html=True)
    
    st.markdown("<h3 style='text-align: center;'>تسجيل الدخول</h3>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        username = st.text_input("اسم المستخدم", placeholder="أدخل اسم المستخدم", key="login_user")
        password = st.text_input("كلمة المرور", type="password", placeholder="أدخل كلمة المرور", key="login_pass")
        
        if st.button("تسجيل الدخول", use_container_width=True, key="login_btn"):
            df_users = read_excel(USERS_FILE)
            
            if not df_users.empty:
                user_row = df_users[df_users['username'] == username]
                
                if not user_row.empty:
                    stored_password = user_row['password'].values[0]
                    
                    if hash_password(password) == stored_password:
                        st.session_state['logged_in'] = True
                        st.session_state['username'] = username
                        st.session_state['role'] = user_row['role'].values[0]
                        st.session_state['name'] = user_row['name'].values[0]
                        st.success("تم تسجيل الدخول بنجاح!")
                        st.rerun()
                    else:
                        st.error("كلمة المرور غير صحيحة")
                else:
                    st.error("اسم المستخدم غير موجود")
            else:
                st.error("لا يوجد مستخدمين مسجلين. يرجى الاتصال بالمدير.")
        
        # معلومات الدخول الافتراضية
        st.markdown("---")
        st.markdown("**معلومات الدخول الافتراضية:**")
        st.markdown("- المدير: `admin` / `admin123`")
        st.markdown("- البائع: `seller1` / `seller123`")

# ============================================================================
# صفحة نقطة البيع (POS)
# ============================================================================
def pos_page():
    """صفحة نقطة البيع"""
    st.markdown("<h1>🛒 نقطة البيع</h1>", unsafe_allow_html=True)
    
    # تهيئة سلة المشتريات
    if 'cart' not in st.session_state:
        st.session_state['cart'] = []
    
    # تقسيم الصفحة
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### المنتجات")
        
        # بحث عن منتج
        search_query = st.text_input("🔍 بحث عن منتج (بالاسم أو الكود)", placeholder="اكتب للبحث...", key="pos_search")
        
        # عرض المنتجات
        df_products = read_excel(PRODUCTS_FILE)
        
        if not df_products.empty:
            # فلترة المنتجات حسب البحث
            if search_query:
                df_products = df_products[
                    df_products['product_name'].str.contains(search_query, case=False, na=False) |
                    df_products['product_code'].str.contains(search_query, case=False, na=False)
                ]
            
            # عرض المنتجات في بطاقات
            num_products = len(df_products)
            num_cols = 3
            cols = st.columns(num_cols)
            
            for idx, row in df_products.iterrows():
                col_idx = idx % num_cols
                with cols[col_idx]:
                    with st.container(border=True):
                        # عرض الصورة
                        if row.get('image_name'):
                            img = load_product_image(row['image_name'])
                            if img:
                                st.image(img.resize((150, 150)), use_container_width=True)
                        else:
                            st.markdown("<div style='text-align: center; font-size: 50px;'>📦</div>", unsafe_allow_html=True)
                        
                        st.markdown(f"**{row['product_name']}**")
                        st.markdown(f"كود: `{row['product_code']}`")
                        st.markdown(f"السعر: **{format_currency(row['price'])}**")
                        st.markdown(f"المتوفر: {row['quantity']}")
                        
                        if row['quantity'] > 0:
                            qty = st.number_input(
                                "الكمية", 
                                min_value=1, 
                                max_value=int(row['quantity']), 
                                value=1,
                                key=f"qty_{row['product_code']}"
                            )
                            
                            if st.button("➕ إضافة", key=f"add_{row['product_code']}", use_container_width=True):
                                # إضافة للسلة
                                cart_item = {
                                    'product_code': row['product_code'],
                                    'product_name': row['product_name'],
                                    'price': row['price'],
                                    'quantity': qty,
                                    'total': row['price'] * qty
                                }
                                
                                # التحقق من وجود المنتج في السلة
                                existing_item = next((item for item in st.session_state['cart'] 
                                                     if item['product_code'] == row['product_code']), None)
                                
                                if existing_item:
                                    existing_item['quantity'] += qty
                                    existing_item['total'] = existing_item['quantity'] * existing_item['price']
                                else:
                                    st.session_state['cart'].append(cart_item)
                                
                                st.success("تمت الإضافة للسلة!")
                        else:
                            st.warning("نفذت الكمية")
        else:
            st.info("لا توجد منتجات مسجلة. يرجى إضافة منتجات من صفحة المخزن.")
    
    with col2:
        st.markdown("### 🧾 الفاتورة الحالية")
        
        if len(st.session_state['cart']) > 0:
            # عرض عناصر السلة
            cart_df = pd.DataFrame(st.session_state['cart'])
            st.dataframe(cart_df[['product_name', 'quantity', 'total']], use_container_width=True)
            
            # حساب الإجمالي
            total_amount = sum(item['total'] for item in st.session_state['cart'])
            st.markdown(f"### الإجمالي: {format_currency(total_amount)}")
            
            st.markdown("---")
            
            # اختيار العميل
            df_customers = read_excel(CUSTOMERS_FILE)
            customer_options = ["عميل نقدي"] + list(df_customers['customer_name'].values) if not df_customers.empty else ["عميل نقدي"]
            selected_customer = st.selectbox("العميل", customer_options, key="pos_customer")
            
            # طريقة الدفع
            payment_method = st.selectbox("طريقة الدفع", ["نقدي", "آجل", "بطاقة"], key="pos_payment")
            
            # أزرار الإجراءات
            col_btn1, col_btn2 = st.columns(2)
            
            with col_btn1:
                if st.button("🗑️ إفراغ السلة", use_container_width=True, key="pos_clear"):
                    st.session_state['cart'] = []
                    st.rerun()
            
            with col_btn2:
                if st.button("✅ إتمام البيع", use_container_width=True, type="primary", key="pos_complete"):
                    # معالجة البيع
                    process_sale(selected_customer, payment_method, total_amount)
        else:
            st.info("السلة فارغة. أضف منتجات للبدء.")
            st.markdown("<div style='text-align: center; font-size: 50px;'>🛒</div>", unsafe_allow_html=True)

def process_sale(customer_name, payment_method, total_amount):
    """معالجة عملية البيع"""
    if len(st.session_state['cart']) == 0:
        st.error("السلة فارغة!")
        return
    
    # إنشاء رقم الفاتورة
    sale_id = generate_id('S')
    
    # حفظ المبيعات
    df_sales = read_excel(SALES_FILE)
    
    # تجميع العناصر كنص
    items_text = "; ".join([f"{item['product_name']} x {item['quantity']}" for item in st.session_state['cart']])
    
    # الحصول على كود العميل
    customer_code = ""
    if customer_name != "عميل نقدي":
        df_customers = read_excel(CUSTOMERS_FILE)
        customer_row = df_customers[df_customers['customer_name'] == customer_name]
        if not customer_row.empty:
            customer_code = customer_row['customer_code'].values[0]
    
    new_sale = {
        'sale_id': sale_id,
        'date': get_current_date(),
        'customer_code': customer_code,
        'customer_name': customer_name,
        'total_amount': total_amount,
        'payment_method': payment_method,
        'user_id': st.session_state['username'],
        'items': items_text
    }
    
    df_sales = pd.concat([df_sales, pd.DataFrame([new_sale])], ignore_index=True)
    save_excel(df_sales, SALES_FILE)
    
    # تحديث المخزون
    df_products = read_excel(PRODUCTS_FILE)
    
    for item in st.session_state['cart']:
        product_idx = df_products[df_products['product_code'] == item['product_code']].index
        if len(product_idx) > 0:
            df_products.loc[product_idx[0], 'quantity'] -= item['quantity']
    
    save_excel(df_products, PRODUCTS_FILE)
    
    # إضافة قيد في سجل الحسابات إذا كان البيع آجل
    if payment_method == "آجل" and customer_code:
        add_ledger_entry(
            party_type='customer',
            party_code=customer_code,
            party_name=customer_name,
            debit=total_amount,
            credit=0,
            description=f'فاتورة بيع آجل - {sale_id}',
            reference_id=sale_id,
            user_id=st.session_state['username']
        )
    
    # إضافة إيراد في سجل الإيرادات
    df_income = read_excel(MANUAL_INCOME_FILE)
    new_income = {
        'income_id': generate_id('I'),
        'date': get_current_date(),
        'description': f'مبيعات - فاتورة {sale_id}',
        'amount': total_amount,
        'customer_code': customer_code,
        'user_id': st.session_state['username']
    }
    df_income = pd.concat([df_income, pd.DataFrame([new_income])], ignore_index=True)
    save_excel(df_income, MANUAL_INCOME_FILE)
    
    # توليد الإيصال
    generate_receipt(sale_id, customer_name, payment_method, total_amount)
    
    # إفراغ السلة
    st.session_state['cart'] = []
    
    st.success(f"تم إتمام البيع بنجاح! رقم الفاتورة: {sale_id}")
    st.rerun()

def generate_receipt(sale_id, customer_name, payment_method, total_amount):
    """توليد إيصال البيع"""
    receipt_text = f"""
    ═══════════════════════════════
           إيصال بيع
    ═══════════════════════════════
    
    رقم الفاتورة: {sale_id}
    التاريخ: {get_current_date()}
    العميل: {customer_name}
    طريقة الدفع: {payment_method}
    
    ───────────────────────────────────
    المنتجات:
    """
    
    for item in st.session_state['cart']:
        receipt_text += f"\n{item['product_name']} x {item['quantity']} = {format_currency(item['total'])}"
    
    receipt_text += f"""
    ───────────────────────────────────
    الإجمالي: {format_currency(total_amount)}
    
    ═══════════════════════════════
        شكراً لزيارتكم!
    ═══════════════════════════════
    """
    
    st.text_area("📄 الإيصال", value=receipt_text, height=300)

# ============================================================================
# صفحة المخزن (معدلة لإصلاح خطأ أنواع البيانات)
# ============================================================================
def inventory_page():
    """صفحة إدارة المخزن"""
    st.markdown("<h1>📦 إدارة المخزن</h1>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["إضافة منتج جديد", "عرض وتعديل المنتجات"])
    
    with tab1:
        st.markdown("### إضافة منتج جديد")
        
        col1, col2 = st.columns(2)
        
        with col1:
            product_code = st.text_input("كود المنتج *", placeholder="مثال: P001", key="inv_code")
            product_name = st.text_input("اسم المنتج *", placeholder="مثال: منتج تجريبي", key="inv_name")
            category = st.text_input("التصنيف", placeholder="مثال: إلكترونيات", key="inv_cat")
            price = st.number_input("سعر البيع *", min_value=0.0, step=0.01, key="inv_price")
            cost = st.number_input("سعر التكلفة", min_value=0.0, step=0.01, key="inv_cost")
        
        with col2:
            quantity = st.number_input("الكمية *", min_value=0, step=1, key="inv_qty")
            min_quantity = st.number_input("الحد الأدنى للتنبيه", min_value=0, step=1, value=5, key="inv_min")
            uploaded_image = st.file_uploader("صورة المنتج", type=['png', 'jpg', 'jpeg'], key="inv_img")
        
        if st.button("حفظ المنتج", use_container_width=True, type="primary", key="inv_save"):
            if product_code and product_name and price >= 0:
                df_products = read_excel(PRODUCTS_FILE)
                
                # التحقق من عدم تكرار الكود
                if not df_products.empty and product_code in df_products['product_code'].values:
                    st.error("كود المنتج موجود مسبقاً!")
                else:
                    # حفظ الصورة
                    image_name = save_product_image(uploaded_image, product_code) if uploaded_image else None
                    
                    new_product = {
                        'product_code': product_code,
                        'product_name': product_name,
                        'price': price,
                        'cost': cost,
                        'quantity': quantity,
                        'min_quantity': min_quantity,
                        'image_name': image_name,
                        'category': category
                    }
                    
                    df_products = pd.concat([df_products, pd.DataFrame([new_product])], ignore_index=True)
                    save_excel(df_products, PRODUCTS_FILE)
                    
                    st.success("تم حفظ المنتج بنجاح!")
                    st.rerun()
            else:
                st.error("يرجى ملء الحقول المطلوبة (*)")
    
    with tab2:
        st.markdown("### المنتجات المسجلة")
        
        df_products = read_excel(PRODUCTS_FILE)
        
        if not df_products.empty:
            # ⚠️ إصلاح خطأ أنواع البيانات: تحويل الأعمدة النصية لـ String
            text_columns = ['product_name', 'category', 'image_name']
            for col in text_columns:
                if col in df_products.columns:
                    df_products[col] = df_products[col].fillna('').astype(str)
            
            # التأكد من أن الأعمدة الرقمية هي أرقام فعلياً
            numeric_columns = ['price', 'cost', 'quantity', 'min_quantity']
            for col in numeric_columns:
                if col in df_products.columns:
                    df_products[col] = pd.to_numeric(df_products[col], errors='coerce').fillna(0)
            
            # عرض الجدول مع إمكانية التعديل
            edited_df = st.data_editor(
                df_products,
                use_container_width=True,
                num_rows="dynamic",
                column_config={
                    "product_code": st.column_config.TextColumn("كود المنتج", disabled=True),
                    "product_name": st.column_config.TextColumn("اسم المنتج"),
                    "price": st.column_config.NumberColumn("سعر البيع"),
                    "cost": st.column_config.NumberColumn("سعر التكلفة"),
                    "quantity": st.column_config.NumberColumn("الكمية"),
                    "min_quantity": st.column_config.NumberColumn("الحد الأدنى"),
                    "category": st.column_config.TextColumn("التصنيف"),
                    "image_name": st.column_config.TextColumn("الصورة", disabled=True)
                },
                hide_index=True,
                key="inv_editor"
            )
            
            # حفظ التعديلات
            if st.button("حفظ التعديلات", key="inv_commit"):
                save_excel(edited_df, PRODUCTS_FILE)
                st.success("تم حفظ التعديلات بنجاح!")
            
            # تنبيهات المخزون المنخفض
            low_stock = df_products[df_products['quantity'] <= df_products['min_quantity']]
            if not low_stock.empty:
                st.markdown("---")
                st.markdown("### ⚠️ تنبيهات المخزون المنخفض")
                st.dataframe(low_stock[['product_code', 'product_name', 'quantity', 'min_quantity']], use_container_width=True)
        else:
            st.info("لا توجد منتجات مسجلة.")

# ============================================================================
# صفحة الحسابات (معدلة لإصلاح خطأ التكرار)
# ============================================================================
def accounts_page():
    """صفحة الحسابات"""
    st.markdown("<h1>💰 الحسابات</h1>", unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["حسابي (إيرادات/مصروفات)", "العملاء", "الموردين", "تقارير مالية"])
    
    with tab1:
        st.markdown("### حسابي - الإيرادات والمصروفات")
        
        sub_tab1, sub_tab2 = st.tabs(["الإيرادات", "المصروفات"])
        
        with sub_tab1:
            st.markdown("#### الإيرادات")
            
            # عرض الإيرادات من المبيعات
            df_sales = read_excel(SALES_FILE)
            df_income = read_excel(MANUAL_INCOME_FILE)
            
            if not df_sales.empty:
                total_sales = df_sales['total_amount'].sum()
                st.metric("إجمالي المبيعات", format_currency(total_sales))
            
            if not df_income.empty:
                total_income = df_income['amount'].sum()
                st.metric("إجمالي الإيرادات اليدوية", format_currency(total_income))
            
            # إضافة إيراد يدوي
            st.markdown("---")
            st.markdown("#### إضافة إيراد يدوي")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                income_desc = st.text_input("وصف الإيراد", key="income_desc_input")
            with col2:
                income_amount = st.number_input("المبلغ", min_value=0.0, step=0.01, key="income_amount_input")
            with col3:
                df_customers = read_excel(CUSTOMERS_FILE)
                customer_options = [""] + list(df_customers['customer_name'].values) if not df_customers.empty else [""]
                income_customer = st.selectbox("العميل (اختياري)", customer_options, key="income_customer_input")
            
            if st.button("إضافة إيراد", key="add_income_btn"):
                if income_desc and income_amount > 0:
                    customer_code = ""
                    if income_customer:
                        cust_row = df_customers[df_customers['customer_name'] == income_customer]
                        if not cust_row.empty:
                            customer_code = cust_row['customer_code'].values[0]
                    
                    new_income = {
                        'income_id': generate_id('I'),
                        'date': get_current_date(),
                        'description': income_desc,
                        'amount': income_amount,
                        'customer_code': customer_code,
                        'user_id': st.session_state['username']
                    }
                    
                    df_income = pd.concat([df_income, pd.DataFrame([new_income])], ignore_index=True)
                    save_excel(df_income, MANUAL_INCOME_FILE)
                    
                    # إضافة قيد في سجل الحسابات إذا كان هناك عميل
                    if customer_code:
                        add_ledger_entry(
                            party_type='customer',
                            party_code=customer_code,
                            party_name=income_customer,
                            debit=0,
                            credit=income_amount,
                            description=f'إيراد يدوي - {income_desc}',
                            reference_id=new_income['income_id'],
                            user_id=st.session_state['username']
                        )
                    
                    st.success("تم إضافة الإيراد بنجاح!")
                    st.rerun()
            
            # عرض سجل الإيرادات
            if not df_income.empty:
                st.markdown("---")
                st.markdown("#### سجل الإيرادات")
                st.dataframe(df_income, use_container_width=True)
        
        with sub_tab2:
            st.markdown("#### المصروفات")
            
            df_expenses = read_excel(EXPENSES_FILE)
            
            if not df_expenses.empty:
                total_expenses = df_expenses['amount'].sum()
                st.metric("إجمالي المصروفات", format_currency(total_expenses))
            
            # إضافة مصروف جديد
            st.markdown("---")
            st.markdown("#### إضافة مصروف جديد")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                expense_desc = st.text_input("وصف المصروف", key="expense_desc_input")
            with col2:
                expense_amount = st.number_input("المبلغ", min_value=0.0, step=0.01, key="expense_amount_input")
            with col3:
                expense_category = st.text_input("تصنيف المصروف", placeholder="مثال: إيجار، كهرباء...", key="expense_category_input")
            
            if st.button("إضافة مصروف", key="add_expense_btn"):
                if expense_desc and expense_amount > 0:
                    new_expense = {
                        'expense_id': generate_id('E'),
                        'date': get_current_date(),
                        'description': expense_desc,
                        'amount': expense_amount,
                        'category': expense_category,
                        'user_id': st.session_state['username']
                    }
                    
                    df_expenses = pd.concat([df_expenses, pd.DataFrame([new_expense])], ignore_index=True)
                    save_excel(df_expenses, EXPENSES_FILE)
                    
                    st.success("تم إضافة المصروف بنجاح!")
                    st.rerun()
            
            # عرض سجل المصروفات
            if not df_expenses.empty:
                st.markdown("---")
                st.markdown("#### سجل المصروفات")
                st.dataframe(df_expenses, use_container_width=True)
    
    with tab2:
        st.markdown("### العملاء")
        
        sub_tab1, sub_tab2 = st.tabs(["قائمة العملاء", "كشف حساب عميل"])
        
        with sub_tab1:
            st.markdown("#### إضافة عميل جديد")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                customer_code = st.text_input("كود العميل *", placeholder="مثال: C001", key="cust_code_input")
                customer_name = st.text_input("اسم العميل *", placeholder="مثال: محمد أحمد", key="cust_name_input")
            with col2:
                customer_phone = st.text_input("الهاتف", placeholder="01xxxxxxxxx", key="cust_phone_input")
                customer_email = st.text_input("البريد الإلكتروني", key="cust_email_input")
            with col3:
                customer_address = st.text_area("العنوان", key="cust_address_input")
            
            if st.button("حفظ العميل", use_container_width=True, key="save_customer_btn"):
                if customer_code and customer_name:
                    df_customers = read_excel(CUSTOMERS_FILE)
                    
                    if not df_customers.empty and customer_code in df_customers['customer_code'].values:
                        st.error("كود العميل موجود مسبقاً!")
                    else:
                        new_customer = {
                            'customer_code': customer_code,
                            'customer_name': customer_name,
                            'phone': customer_phone,
                            'email': customer_email,
                            'address': customer_address
                        }
                        
                        df_customers = pd.concat([df_customers, pd.DataFrame([new_customer])], ignore_index=True)
                        save_excel(df_customers, CUSTOMERS_FILE)
                        
                        st.success("تم حفظ العميل بنجاح!")
                        st.rerun()
                else:
                    st.error("يرجى ملء الحقول المطلوبة (*)")
            
            st.markdown("---")
            st.markdown("#### قائمة العملاء")
            
            df_customers = read_excel(CUSTOMERS_FILE)
            
            if not df_customers.empty:
                # إضافة عمود الرصيد
                df_customers['balance'] = df_customers.apply(
                    lambda row: get_party_balance('customer', row['customer_code']), axis=1
                )
                
                st.dataframe(df_customers, use_container_width=True)
            else:
                st.info("لا يوجد عملاء مسجلين.")
        
        with sub_tab2:
            st.markdown("#### كشف حساب عميل")
            
            df_customers = read_excel(CUSTOMERS_FILE)
            
            if not df_customers.empty:
                selected_customer = st.selectbox("اختر العميل", df_customers['customer_name'].values, key="select_customer_ledger")
                
                if selected_customer:
                    customer_row = df_customers[df_customers['customer_name'] == selected_customer].iloc[0]
                    customer_code = customer_row['customer_code']
                    
                    # عرض معلومات العميل
                    st.markdown(f"**كود العميل:** {customer_code}")
                    st.markdown(f"**الهاتف:** {customer_row.get('phone', 'غير متاح')}")
                    
                    # عرض الحركات من سجل الحسابات
                    df_ledger = read_excel(LEDGER_FILE)
                    
                    if not df_ledger.empty:
                        customer_ledger = df_ledger[df_ledger['party_code'] == customer_code].copy()
                        
                        if not customer_ledger.empty:
                            # حساب الرصيد التراكمي
                            customer_ledger['running_balance'] = (
                                customer_ledger['debit'].cumsum() - customer_ledger['credit'].cumsum()
                            )
                            
                            st.markdown("#### جدول المديونية والدائنية")
                            st.dataframe(
                                customer_ledger[['date', 'description', 'debit', 'credit', 'running_balance']],
                                use_container_width=True
                            )
                            
                            # الرصيد الحالي
                            current_balance = get_party_balance('customer', customer_code)
                            
                            if current_balance > 0:
                                st.markdown(f"### الرصيد الحالي: {format_currency(current_balance)} (مدين - له علينا)")
                            elif current_balance < 0:
                                st.markdown(f"### الرصيد الحالي: {format_currency(abs(current_balance))} (دائن - علينا له)")
                            else:
                                st.markdown("### الرصيد الحالي: 0 (متساوي)")
                        else:
                            st.info("لا توجد حركات مسجلة لهذا العميل.")
                    else:
                        st.info("لا توجد حركات في سجل الحسابات.")
                    
                    # إضافة حركة يدوية
                    st.markdown("---")
                    st.markdown("#### إضافة حركة يدوية")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        manual_amount = st.number_input("المبلغ", min_value=0.0, step=0.01, key="manual_amount_customer")
                        manual_desc = st.text_input("وصف الحركة", key="manual_desc_customer")
                    with col2:
                        manual_type = st.selectbox("نوع الحركة", ["مدين (له علينا)", "دائن (علينا له)"], key="manual_type_customer")
                    
                    if st.button("إضافة الحركة", key="add_manual_customer"):
                        if manual_amount > 0 and manual_desc:
                            debit = manual_amount if "مدين" in manual_type else 0
                            credit = manual_amount if "دائن" in manual_type else 0
                            
                            add_ledger_entry(
                                party_type='customer',
                                party_code=customer_code,
                                party_name=selected_customer,
                                debit=debit,
                                credit=credit,
                                description=manual_desc,
                                reference_id=generate_id('M'),
                                user_id=st.session_state['username']
                            )
                            
                            st.success("تم إضافة الحركة بنجاح!")
                            st.rerun()
                else:
                    st.info("اختر عميل لعرض كشف الحساب.")
            else:
                st.info("لا يوجد عملاء مسجلين.")
    
    with tab3:
        st.markdown("### الموردين")
        
        sub_tab1, sub_tab2 = st.tabs(["قائمة الموردين", "كشف حساب مورد"])
        
        with sub_tab1:
            st.markdown("#### إضافة مورد جديد")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                supplier_code = st.text_input("كود المورد *", placeholder="مثال: S001", key="supp_code_input")
                supplier_name = st.text_input("اسم المورد *", placeholder="مثال: شركة التوريد", key="supp_name_input")
            with col2:
                supplier_phone = st.text_input("الهاتف", placeholder="01xxxxxxxxx", key="supp_phone_input")
                supplier_email = st.text_input("البريد الإلكتروني", key="supp_email_input")
            with col3:
                supplier_address = st.text_area("العنوان", key="supp_address_input")
            
            if st.button("حفظ المورد", use_container_width=True, key="save_supplier_btn"):
                if supplier_code and supplier_name:
                    df_suppliers = read_excel(SUPPLIERS_FILE)
                    
                    if not df_suppliers.empty and supplier_code in df_suppliers['supplier_code'].values:
                        st.error("كود المورد موجود مسبقاً!")
                    else:
                        new_supplier = {
                            'supplier_code': supplier_code,
                            'supplier_name': supplier_name,
                            'phone': supplier_phone,
                            'email': supplier_email,
                            'address': supplier_address
                        }
                        
                        df_suppliers = pd.concat([df_suppliers, pd.DataFrame([new_supplier])], ignore_index=True)
                        save_excel(df_suppliers, SUPPLIERS_FILE)
                        
                        st.success("تم حفظ المورد بنجاح!")
                        st.rerun()
                else:
                    st.error("يرجى ملء الحقول المطلوبة (*)")
            
            st.markdown("---")
            st.markdown("#### قائمة الموردين")
            
            df_suppliers = read_excel(SUPPLIERS_FILE)
            
            if not df_suppliers.empty:
                # إضافة عمود الرصيد
                df_suppliers['balance'] = df_suppliers.apply(
                    lambda row: get_party_balance('supplier', row['supplier_code']), axis=1
                )
                
                st.dataframe(df_suppliers, use_container_width=True)
            else:
                st.info("لا يوجد موردين مسجلين.")
        
        with sub_tab2:
            st.markdown("#### كشف حساب مورد")
            
            df_suppliers = read_excel(SUPPLIERS_FILE)
            
            if not df_suppliers.empty:
                selected_supplier = st.selectbox("اختر المورد", df_suppliers['supplier_name'].values, key="select_supplier_ledger")
                
                if selected_supplier:
                    supplier_row = df_suppliers[df_suppliers['supplier_name'] == selected_supplier].iloc[0]
                    supplier_code = supplier_row['supplier_code']
                    
                    # عرض معلومات المورد
                    st.markdown(f"**كود المورد:** {supplier_code}")
                    st.markdown(f"**الهاتف:** {supplier_row.get('phone', 'غير متاح')}")
                    
                    # عرض الحركات من سجل الحسابات
                    df_ledger = read_excel(LEDGER_FILE)
                    
                    if not df_ledger.empty:
                        supplier_ledger = df_ledger[df_ledger['party_code'] == supplier_code].copy()
                        
                        if not supplier_ledger.empty:
                            # حساب الرصيد التراكمي
                            supplier_ledger['running_balance'] = (
                                supplier_ledger['debit'].cumsum() - supplier_ledger['credit'].cumsum()
                            )
                            
                            st.markdown("#### جدول المديونية والدائنية")
                            st.dataframe(
                                supplier_ledger[['date', 'description', 'debit', 'credit', 'running_balance']],
                                use_container_width=True
                            )
                            
                            # الرصيد الحالي
                            current_balance = get_party_balance('supplier', supplier_code)
                            
                            if current_balance > 0:
                                st.markdown(f"### الرصيد الحالي: {format_currency(current_balance)} (مدين - له علينا)")
                            elif current_balance < 0:
                                st.markdown(f"### الرصيد الحالي: {format_currency(abs(current_balance))} (دائن - علينا له)")
                            else:
                                st.markdown("### الرصيد الحالي: 0 (متساوي)")
                        else:
                            st.info("لا توجد حركات مسجلة لهذا المورد.")
                    else:
                        st.info("لا توجد حركات في سجل الحسابات.")
                else:
                    st.info("اختر مورد لعرض كشف الحساب.")
            else:
                st.info("لا يوجد موردين مسجلين.")
    
    with tab4:
        st.markdown("### التقارير المالية")
        
        # حساب الملخص المالي
        df_sales = read_excel(SALES_FILE)
        df_income = read_excel(MANUAL_INCOME_FILE)
        df_expenses = read_excel(EXPENSES_FILE)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_sales = df_sales['total_amount'].sum() if not df_sales.empty else 0
            st.metric("إجمالي المبيعات", format_currency(total_sales))
        
        with col2:
            total_income = df_income['amount'].sum() if not df_income.empty else 0
            st.metric("إجمالي الإيرادات", format_currency(total_income))
        
        with col3:
            total_expenses = df_expenses['amount'].sum() if not df_expenses.empty else 0
            st.metric("إجمالي المصروفات", format_currency(total_expenses))
        
        with col4:
            net_profit = (total_sales + total_income) - total_expenses
            st.metric("صافي الربح", format_currency(net_profit))
        
        st.markdown("---")
        
        # ✅ عرض جدول بدلاً من الرسم البياني
        st.markdown("#### المبيعات الشهرية")

        if not df_sales.empty:
            df_sales['date'] = pd.to_datetime(df_sales['date'])
            df_sales['month'] = df_sales['date'].dt.to_period('M')
            monthly_sales = df_sales.groupby('month')['total_amount'].sum().reset_index()
            monthly_sales['month'] = monthly_sales['month'].astype(str)
            
            # عرض جدول بدلاً من الرسم البياني
            st.dataframe(monthly_sales, use_container_width=True)

# ============================================================================
# صفحة التقارير
# ============================================================================
def reports_page():
    """صفحة التقارير"""
    st.markdown("<h1>📊 التقارير</h1>", unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["تقارير المبيعات", "تقارير المخزون", "تقارير العملاء والموردين"])
    
    with tab1:
        st.markdown("### تقارير المبيعات")
        
        df_sales = read_excel(SALES_FILE)
        
        if not df_sales.empty:
            # فلترة بالتاريخ
            col1, col2 = st.columns(2)
            
            with col1:
                start_date = st.date_input("من تاريخ", value=datetime.now() - timedelta(days=30), key="rep_start")
            with col2:
                end_date = st.date_input("إلى تاريخ", value=datetime.now(), key="rep_end")
            
            # تحويل التواريخ
            df_sales['date'] = pd.to_datetime(df_sales['date'])
            filtered_sales = df_sales[
                (df_sales['date'] >= pd.Timestamp(start_date)) & 
                (df_sales['date'] <= pd.Timestamp(end_date))
            ]
            
            st.metric("عدد الفواتير", len(filtered_sales))
            st.metric("إجمالي المبيعات", format_currency(filtered_sales['total_amount'].sum()))
            
            st.markdown("---")
            st.markdown("#### تفاصيل المبيعات")
            st.dataframe(filtered_sales, use_container_width=True)
        else:
            st.info("لا توجد مبيعات مسجلة.")
    
    with tab2:
        st.markdown("### تقارير المخزون")
        
        df_products = read_excel(PRODUCTS_FILE)
        
        if not df_products.empty:
            st.metric("عدد الأصناف", len(df_products))
            st.metric("إجمالي القيمة بالمخزن", format_currency((df_products['cost'] * df_products['quantity']).sum()))
            
            st.markdown("---")
            
            # المنتجات منخفضة المخزون
            low_stock = df_products[df_products['quantity'] <= df_products['min_quantity']]
            
            if not low_stock.empty:
                st.markdown("#### ⚠️ منتجات منخفضة المخزون")
                st.dataframe(low_stock, use_container_width=True)
            
            st.markdown("---")
            st.markdown("#### جميع المنتجات")
            st.dataframe(df_products, use_container_width=True)
        else:
            st.info("لا توجد منتجات مسجلة.")
    
    with tab3:
        st.markdown("### تقارير العملاء والموردين")
        
        df_customers = read_excel(CUSTOMERS_FILE)
        df_suppliers = read_excel(SUPPLIERS_FILE)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### العملاء")
            if not df_customers.empty:
                st.metric("عدد العملاء", len(df_customers))
                
                # حساب إجمالي المديونيات
                total_customer_debt = sum(
                    get_party_balance('customer', row['customer_code']) 
                    for _, row in df_customers.iterrows()
                    if get_party_balance('customer', row['customer_code']) > 0
                )
                st.metric("إجمالي مديونيات العملاء", format_currency(total_customer_debt))
            else:
                st.info("لا يوجد عملاء")
        
        with col2:
            st.markdown("#### الموردين")
            if not df_suppliers.empty:
                st.metric("عدد الموردين", len(df_suppliers))
                
                # حساب إجمالي المديونيات
                total_supplier_debt = sum(
                    get_party_balance('supplier', row['supplier_code']) 
                    for _, row in df_suppliers.iterrows()
                    if get_party_balance('supplier', row['supplier_code']) > 0
                )
                st.metric("إجمالي مديونيات الموردين", format_currency(total_supplier_debt))
            else:
                st.info("لا يوجد موردين")

# ============================================================================
# صفحة الإعدادات
# ============================================================================
def settings_page():
    """صفحة الإعدادات"""
    st.markdown("<h1>⚙️ الإعدادات</h1>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["إدارة المستخدمين", "إعدادات النظام"])
    
    with tab1:
        st.markdown("### إدارة المستخدمين")
        
        # عرض المستخدمين الحاليين
        df_users = read_excel(USERS_FILE)
        
        if not df_users.empty:
            st.markdown("#### المستخدمون الحاليون")
            st.dataframe(df_users[['username', 'role', 'name']], use_container_width=True)
        
        st.markdown("---")
        st.markdown("#### إضافة مستخدم جديد")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            new_username = st.text_input("اسم المستخدم *", key="set_user")
            new_name = st.text_input("الاسم الكامل *", key="set_name")
        with col2:
            new_password = st.text_input("كلمة المرور *", type="password", key="set_pass")
            confirm_password = st.text_input("تأكيد كلمة المرور *", type="password", key="set_pass_conf")
        with col3:
            new_role = st.selectbox("الصلاحية", ["admin", "seller"], key="set_role")
        
        if st.button("إضافة مستخدم", use_container_width=True, key="set_add_btn"):
            if new_username and new_password and new_name:
                if new_password != confirm_password:
                    st.error("كلمات المرور غير متطابقة!")
                else:
                    df_users = read_excel(USERS_FILE)
                    
                    if not df_users.empty and new_username in df_users['username'].values:
                        st.error("اسم المستخدم موجود مسبقاً!")
                    else:
                        new_user = {
                            'username': new_username,
                            'password': hash_password(new_password),
                            'role': new_role,
                            'name': new_name
                        }
                        
                        df_users = pd.concat([df_users, pd.DataFrame([new_user])], ignore_index=True)
                        save_excel(df_users, USERS_FILE)
                        
                        st.success("تم إضافة المستخدم بنجاح!")
                        st.rerun()
            else:
                st.error("يرجى ملء الحقول المطلوبة (*)")
    
    with tab2:
        st.markdown("### إعدادات النظام")
        
        st.markdown("#### معلومات النظام")
        st.info(f"إصدار النظام: 1.0.0")
        st.info(f"آخر تحديث: {datetime.now().strftime('%Y-%m-%d')}")
        
        st.markdown("---")
        st.markdown("#### نسخ احتياطي للبيانات")
        
        if st.button("📦 تحميل نسخة احتياطية من جميع البيانات", key="set_backup"):
            st.success("يمكنك نسخ مجلد 'data' كنسخة احتياطية كاملة")
        
        st.markdown("---")
        st.markdown("#### إعادة تعيين النظام")
        
        if st.button("⚠️ حذف جميع البيانات وإعادة التعيين", type="secondary", key="set_reset"):
            st.warning("هذا الإجراء لا يمكن التراجع عنه!")
            if st.checkbox("أوافق على حذف جميع البيانات", key="set_reset_confirm"):
                import shutil
                if os.path.exists(DATA_DIR):
                    shutil.rmtree(DATA_DIR)
                if os.path.exists(IMAGES_DIR):
                    shutil.rmtree(IMAGES_DIR)
                st.success("تم حذف البيانات. يرجى إعادة تشغيل التطبيق.")

# ============================================================================
# الشريط الجانبي والواجهة الرئيسية
# ============================================================================
def sidebar():
    """بناء الشريط الجانبي"""
    with st.sidebar:
        st.markdown("### 👤 معلومات المستخدم")
        st.markdown(f"**الاسم:** {st.session_state.get('name', 'غير معروف')}")
        st.markdown(f"**الصلاحية:** {st.session_state.get('role', 'غير معروف')}")
        
        st.markdown("---")
        
        # القائمة حسب الصلاحية
        if st.session_state.get('role') == 'admin':
            page = st.radio(
                "القائمة الرئيسية",
                ["🛒 نقطة البيع", "📦 المخزن", "💰 الحسابات", "📊 التقارير", "⚙️ الإعدادات"],
                index=0,
                key="sidebar_menu"
            )
        else:
            page = st.radio(
                "القائمة الرئيسية",
                ["🛒 نقطة البيع"],
                index=0,
                key="sidebar_menu_seller"
            )
        
        st.markdown("---")
        
        if st.button("🚪 تسجيل الخروج", use_container_width=True, key="sidebar_logout"):
            st.session_state['logged_in'] = False
            st.session_state['username'] = None
            st.session_state['role'] = None
            st.session_state['name'] = None
            st.session_state['cart'] = []
            st.rerun()
        
        return page

# ============================================================================
# الدالة الرئيسية
# ============================================================================
def main():
    """الدالة الرئيسية للتطبيق"""
    # إنشاء الملفات والمجلدات
    create_excel_files()
    
    # التحقق من تسجيل الدخول
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
    
    if not st.session_state['logged_in']:
        login_page()
    else:
        # عرض الشريط الجانبي والحصول على الصفحة المختارة
        selected_page = sidebar()
        
        # عرض الصفحة المختارة
        if selected_page == "🛒 نقطة البيع":
            pos_page()
        elif selected_page == "📦 المخزن":
            inventory_page()
        elif selected_page == "💰 الحسابات":
            accounts_page()
        elif selected_page == "📊 التقارير":
            reports_page()
        elif selected_page == "⚙️ الإعدادات":
            settings_page()

# ============================================================================
# تشغيل التطبيق
# ============================================================================
if __name__ == "__main__":
    main()
