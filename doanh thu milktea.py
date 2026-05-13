import streamlit as st
import pandas as pd
import joblib
import os

# =========================
# LOAD MODEL
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model_ngay_thuong = joblib.load(os.path.join(BASE_DIR, "model_doanh_thu_ngay_thuong.pkl"))
model_cuoi_tuan = joblib.load(os.path.join(BASE_DIR, "model_doanh_thu_cuoi_tuan.pkl"))
model_tuan = joblib.load(os.path.join(BASE_DIR, "model_doanh_thu_tuan.pkl"))

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="BrewForecast",
    page_icon="☕",
    layout="wide"
)

# =========================
# CUSTOM CSS
# =========================
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0b0b0b 0%, #111111 45%, #1a1a1a 100%);
        color: #f8f5ef;
    }

    .main-title {
        text-align: center;
        font-size: 46px;
        font-weight: 800;
        color: #f4c66d;
        margin-bottom: 8px;
    }

    .sub-title {
        text-align: center;
        font-size: 18px;
        color: #e7c27a;
        margin-bottom: 35px;
    }

    /* Ô tiêu đề section */
    .section-header-box {
        background: rgba(20, 20, 20, 0.96);
        border: 1.5px solid #c6922b;
        border-radius: 22px;
        min-height: 78px;
        padding: 0 32px;
        margin: 10px 0 22px 0;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.35);

        display: flex;
        align-items: center;
        justify-content: center;
    }

    .section-header-text {
        font-size: 22px;
        font-weight: 800;
        color: #f4c66d;
        margin: 0;
        line-height: 1;
        text-align: center;
    }

    .small-note {
        color: #d7b679;
        font-size: 15px;
        margin-bottom: 15px;
    }

    div.stButton {
        display: flex;
        justify-content: center;
        width: 100%;
    }

    div.stButton > button {
        width: 260px;
        height: 58px;
        margin: 0 auto;
        border-radius: 16px;
        background: linear-gradient(90deg, #b7791f, #f4c66d);
        color: black;
        font-size: 17px;
        font-weight: 800;
        border: none;
        box-shadow: 0 8px 22px rgba(244, 198, 109, 0.25);

        display: flex;
        align-items: center;
        justify-content: center;
        text-align: center;
    }

    div.stButton > button:hover {
        background: linear-gradient(90deg, #d89216, #ffda84);
        color: black;
        border: none;
    }

    [data-testid="stMetric"] {
        background: #141414;
        border-radius: 20px;
        padding: 22px;
        box-shadow: 0 8px 22px rgba(0, 0, 0, 0.35);
        border: 1.5px solid #c6922b;
    }

    [data-testid="stMetricLabel"] {
        font-size: 17px;
        color: #f2cf8c;
    }

    [data-testid="stMetricValue"] {
        font-size: 30px;
        color: #ffd27a;
        font-weight: 800;
    }

    .footer-note {
        text-align: center;
        color: #caa56a;
        font-size: 14px;
        margin-top: 30px;
    }

    .stSelectbox label, .stNumberInput label {
        color: #f5d79b !important;
        font-weight: 600;
    }

    .stSelectbox div[data-baseweb="select"] > div,
    .stNumberInput div[data-baseweb="input"] > div {
        background-color: #1a1a1a !important;
        color: #f8f5ef !important;
        border: 1px solid #b8862f !important;
        border-radius: 12px !important;
    }

    input, textarea {
        color: #f8f5ef !important;
    }

    .streamlit-expanderHeader {
        color: #f4c66d !important;
        font-weight: 700;
    }

    div[data-testid="stAlert"] {
        border-radius: 14px;
        border: 1px solid #c6922b;
    }
    .button-center-wrapper {
        width: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 22px 0 18px 0;
    }
            
</style>
""", unsafe_allow_html=True)

def section_header(title, icon):
    st.markdown(
        f"""
        <div class="section-header-box">
            <div class="section-header-text">{icon} {title}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# =========================
# HEADER
# =========================
st.markdown('<div class="main-title">☕ BrewForecast</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">Nhập thông tin quán để hệ thống dự đoán doanh thu ngày thường, cuối tuần và theo tuần.</div>',
    unsafe_allow_html=True
)

# =========================
# FORM INPUT
# =========================
left_col, right_col = st.columns([1, 1], gap="large")

with left_col:
    section_header("Thông tin cơ bản", "🏪")

    loai_quan = st.selectbox(
        "Loại quán",
        ["cafe", "tra_sua", "specialty_coffee", "chain_coffee", "local_cafe"]
    )

    khu_vuc = st.selectbox(
        "Khu vực",
        ["q1", "q3", "q5", "q10", "binh_thanh", "go_vap", "thu_duc", "cau_giay", "my_dinh"]
    )

    col_a, col_b = st.columns(2)

    with col_a:
        dien_tich_num = st.number_input(
            "Diện tích quán (m²)",
            min_value=10,
            max_value=500,
            value=80
        )

        so_nhan_vien_num = st.number_input(
            "Số nhân viên",
            min_value=1,
            max_value=50,
            value=4
        )

    with col_b:
        so_cho_ngoi_num = st.number_input(
            "Số chỗ ngồi",
            min_value=5,
            max_value=300,
            value=40
        )

        doi_thu_num = st.number_input(
            "Số đối thủ trong bán kính 500m",
            min_value=0,
            max_value=50,
            value=6
        )

    st.markdown("<hr>", unsafe_allow_html=True)
    section_header("Vị trí quán", "📍")
    st.markdown('<div class="small-note">Các yếu tố vị trí ảnh hưởng trực tiếp đến lượng khách và doanh thu.</div>', unsafe_allow_html=True)

    col_c, col_d = st.columns(2)

    with col_c:
        gan_truong = st.selectbox("Gần trường học không?", [0, 1], format_func=lambda x: "Có" if x == 1 else "Không")
        mat_tien = st.selectbox("Quán có mặt tiền không?", [0, 1], format_func=lambda x: "Có" if x == 1 else "Không")

    with col_d:
        gan_van_phong = st.selectbox("Gần văn phòng không?", [0, 1], format_func=lambda x: "Có" if x == 1 else "Không")
        trong_hem = st.selectbox("Quán nằm trong hẻm không?", [0, 1], format_func=lambda x: "Có" if x == 1 else "Không")

    vi_tri_score = gan_truong + gan_van_phong + mat_tien - trong_hem

    st.info(f"Điểm vị trí tự động tính: {vi_tri_score}")

    st.markdown("<hr>", unsafe_allow_html=True)
with right_col:
    section_header("Dịch vụ và tiện ích", "🛵")

    col_e, col_f = st.columns(2)

    with col_e:
        delivery = st.selectbox("Có giao hàng online không?", [0, 1], format_func=lambda x: "Có" if x == 1 else "Không")
        may_lanh = st.selectbox("Có máy lạnh không?", [0, 1], format_func=lambda x: "Có" if x == 1 else "Không")

    with col_f:
        wifi = st.selectbox("Có wifi không?", [0, 1], format_func=lambda x: "Có" if x == 1 else "Không")
        cho_ngoi_lau = st.selectbox("Phù hợp ngồi lâu/làm việc không?", [0, 1], format_func=lambda x: "Có" if x == 1 else "Không")

    tep_khach = st.selectbox(
        "Tệp khách chính",
        ["sinh_vien", "hoc_sinh", "van_phong", "gen_z", "freelancer", "cap_doi", "gia_dinh"]
    )

    gio_peak = st.selectbox(
        "Khung giờ cao điểm",
        ["7h-9h", "11h-13h", "14h-21h", "18h-22h", "7pm-10pm"]
    )

    st.markdown("<hr>", unsafe_allow_html=True)
    section_header("Đánh giá và giá bán", "⭐")

    col_g, col_h = st.columns(2)

    with col_g:
        rating_num = st.number_input(
            "Rating Google",
            min_value=1.0,
            max_value=5.0,
            value=4.5,
            step=0.1
        )

        gia_tb_ngay_thuong = st.number_input(
            "Giá trung bình ngày thường",
            min_value=10000,
            max_value=150000,
            value=35000,
            step=1000
        )

    with col_h:
        so_review_num = st.number_input(
            "Số review Google",
            min_value=0,
            max_value=10000,
            value=300
        )

        gia_tb_cuoi_tuan = st.number_input(
            "Giá trung bình cuối tuần",
            min_value=10000,
            max_value=200000,
            value=42000,
            step=1000
        )

    st.markdown("<hr>", unsafe_allow_html=True)
# =========================
# INPUT DATA
# =========================
input_data = pd.DataFrame([{
    "loai_quan": loai_quan,
    "khu_vuc": khu_vuc,
    "gan_truong": gan_truong,
    "gan_van_phong": gan_van_phong,
    "mat_tien": mat_tien,
    "trong_hem": trong_hem,
    "dien_tich_num": dien_tich_num,
    "so_cho_ngoi_num": so_cho_ngoi_num,
    "so_nhan_vien_num": so_nhan_vien_num,
    "rating_num": rating_num,
    "so_review_num": so_review_num,
    "delivery": delivery,
    "wifi": wifi,
    "may_lanh": may_lanh,
    "cho_ngoi_lau": cho_ngoi_lau,
    "tep_khach": tep_khach,
    "gio_peak": gio_peak,
    "doi_thu_num": doi_thu_num,
    "vi_tri_score": vi_tri_score,
    "gia_tb_ngay_thuong": gia_tb_ngay_thuong,
    "gia_tb_cuoi_tuan": gia_tb_cuoi_tuan
}])

# =========================
# PREDICT
# =========================
section_header("Kết quả dự đoán", "🚀")
st.markdown('<div class="button-center-wrapper">', unsafe_allow_html=True)
predict_button = st.button("Dự đoán doanh thu")
st.markdown('</div>', unsafe_allow_html=True)

if predict_button:
    du_doan_ngay_thuong = model_ngay_thuong.predict(input_data)[0]
    du_doan_cuoi_tuan = model_cuoi_tuan.predict(input_data)[0]
    du_doan_tuan = model_tuan.predict(input_data)[0]

    st.success("Dự đoán thành công! Dưới đây là doanh thu ước lượng của quán.")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Ngày thường",
            f"{du_doan_ngay_thuong:,.0f} VNĐ"
        )

    with col2:
        st.metric(
            "Cuối tuần",
            f"{du_doan_cuoi_tuan:,.0f} VNĐ"
        )

    with col3:
        st.metric(
            "Theo tuần",
            f"{du_doan_tuan:,.0f} VNĐ"
        )

    with st.expander("Xem dữ liệu đầu vào đã đưa vào mô hình"):
        st.dataframe(input_data, use_container_width=True)

else:
    st.info("Nhập thông tin quán rồi bấm nút **Dự đoán doanh thu** để xem kết quả.")

st.markdown("<hr>", unsafe_allow_html=True)
st.markdown(
    '<div class="footer-note">Mô hình sử dụng Supervised Learning - Regression để dự đoán doanh thu dựa trên các đặc điểm của quán.</div>',
    unsafe_allow_html=True
)