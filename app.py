import json
from pathlib import Path

import streamlit as st


# =========================================================
# 1. PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="우수인재 특별귀화 Checklist",
    page_icon="🇰🇷",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# 2. PATHS
# =========================================================

BASE_DIR = Path(__file__).parent
DATA_FILE = BASE_DIR / "data" / "checklists.json"


# =========================================================
# 3. LOAD DATA
# =========================================================

@st.cache_data
def load_data():
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


data = load_data()

visa_key = "excellent_talent_naturalization"
visa_data = data[visa_key]


# =========================================================
# 4. CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    .block-container {
        max-width: 1150px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    html, body, [class*="css"] {
        font-size: 24px;
    }

    .hero {
        padding: 2.3rem;
        border-radius: 22px;
        background:
            linear-gradient(
                135deg,
                #0f172a,
                #1d4ed8
            );
        color: white;
        margin-bottom: 1.5rem;
        box-shadow: 0 15px 35px rgba(0,0,0,0.15);
    }

    .hero h1 {
        margin: 0;
        font-size: 2.5rem;
    }

    .hero h3 {
        margin-top: 0.5rem;
        font-weight: 400;
        opacity: 0.92;
    }

    .hero p {
        margin-top: 1rem;
        margin-bottom: 0;
        opacity: 0.85;
    }

    .warning-box {
        background: rgba(245, 158, 11, 0.12);
        border: 1px solid rgba(245, 158, 11, 0.35);
        border-radius: 14px;
        padding: 1rem 1.2rem;
        margin-bottom: 1.5rem;
    }

    .section-title {
        font-size: 1.2rem;
        font-weight: 700;
        margin-bottom: 0.8rem;
    }

    .required {
        color: #ef4444;
        font-weight: 700;
    }

    .optional {
        color: #64748b;
        font-size: 0.85rem;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# 5. SIDEBAR
# =========================================================

with st.sidebar:

    st.title("🇰🇷 Quốc tịch Hàn Quốc")

    st.write(
        """
        **Diện:** Nhân tài ưu tú  
        **Korean:** 우수인재 특별귀화
        """
    )

    st.divider()

    st.subheader("📌 Mục tiêu")

    st.write(
        """
        Theo dõi toàn bộ quá trình chuẩn bị hồ sơ:
        - hồ sơ cá nhân
        - hồ sơ nghiên cứu
        - điểm cộng
        - dịch thuật
        - lịch nộp
        - giai đoạn sau khi nộp
        """
    )

    st.divider()

    show_optional = st.toggle(
        "Hiển thị hồ sơ không bắt buộc",
        value=True
    )

    st.divider()

    st.caption(
        "Checklist này được xây dựng dựa trên tài liệu hướng dẫn "
        "우수인재 특별귀화. Trước khi nộp cần xác nhận lại với cơ quan "
        "xuất nhập cảnh hoặc 1345."
    )


# =========================================================
# 6. HEADER
# =========================================================

st.markdown(
    f"""
    <div class="hero">
        <h1>🇰🇷 {visa_data["title"]}</h1>
        <h3>{visa_data["subtitle"]}</h3>
        <p>{visa_data["description"]}</p>
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# 7. WARNING
# =========================================================

st.markdown(
    """
    <div class="warning-box">
        <strong>⚠️ Lưu ý pháp lý:</strong><br>
        Đây là checklist cá nhân dùng để quản lý hồ sơ.
        Danh sách thực tế có thể được cơ quan xuất nhập cảnh yêu cầu bổ sung
        tùy theo hồ sơ từng người.
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# 8. PREPARE ITEMS
# =========================================================

all_items = []

for category in visa_data["categories"]:
    for item in category["items"]:
        item_copy = item.copy()
        item_copy["category"] = category["name"]
        all_items.append(item_copy)


visible_items = [
    item
    for item in all_items
    if item["required"] or show_optional
]


# =========================================================
# 9. PROGRESS
# =========================================================

completed = sum(
    st.session_state.get(
        f"check_{item['id']}",
        False
    )
    for item in visible_items
)

total = len(visible_items)

progress = completed / total if total else 0


col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Hoàn thành",
        completed
    )

with col2:
    st.metric(
        "Tổng mục",
        total
    )

with col3:
    required_total = sum(
        item["required"]
        for item in visible_items
    )

    st.metric(
        "Mục bắt buộc",
        required_total
    )

with col4:
    st.metric(
        "Tiến độ",
        f"{progress:.0%}"
    )

st.progress(progress)


# =========================================================
# 10. CHECKLIST
# =========================================================

st.divider()

st.header("📋 Checklist hồ sơ")


for category in visa_data["categories"]:

    category_items = [
        item
        for item in category["items"]
        if item["required"] or show_optional
    ]

    if not category_items:
        continue

    category_completed = sum(
        st.session_state.get(
            f"check_{item['id']}",
            False
        )
        for item in category_items
    )

    category_total = len(category_items)

    expander_title = (
        f"{category['name']} "
        f"({category_completed}/{category_total})"
    )

    with st.expander(
        expander_title,
        expanded=True
    ):

        for item in category_items:

            col_check, col_type = st.columns(
                [8, 2]
            )

            with col_check:

                st.checkbox(
                    item["label"],
                    key=f"check_{item['id']}",
                    help=item.get("note", "")
                )

                if item.get("note"):
                    st.caption(
                        f"↳ {item['note']}"
                    )

            with col_type:

                if item["required"]:
                    st.markdown(
                        '<span class="required">BẮT BUỘC</span>',
                        unsafe_allow_html=True
                    )

                else:
                    st.markdown(
                        '<span class="optional">TÙY TRƯỜNG HỢP</span>',
                        unsafe_allow_html=True
                    )


# =========================================================
# 11. PERSONAL NOTES
# =========================================================

st.divider()

st.header("📝 Ghi chú hồ sơ")

notes = st.text_area(
    "Ghi chú cá nhân",
    placeholder=(
        "Ví dụ:\n"
        "- Xin 재직증명서 từ PNU\n"
        "- Chuẩn bị danh sách SCIE\n"
        "- Xin giấy xác nhận patent\n"
        "- Kiểm tra người có thẩm quyền 추천서\n"
        "- Gọi 1345 xác nhận hồ sơ..."
    ),
    height=200,
    key="personal_notes"
)


# =========================================================
# 12. PERSONAL PROFILE
# =========================================================

st.divider()

st.header("👤 Hồ sơ cá nhân")

col1, col2 = st.columns(2)

with col1:

    applicant_name = st.text_input(
        "Họ tên",
        placeholder="Tên người nộp hồ sơ"
    )

    current_status = st.text_input(
        "Tình trạng hiện tại",
        placeholder="Ví dụ: Researcher / Postdoc"
    )

    current_visa = st.text_input(
        "Visa hiện tại",
        placeholder="Ví dụ: E-3, E-7..."
    )


with col2:

    degree = st.text_input(
        "Học vị cao nhất",
        placeholder="Ví dụ: Ph.D."
    )

    field = st.text_input(
        "Lĩnh vực",
        placeholder="Ví dụ: Naval Architecture / Hydrogen / Fuel Cell"
    )

    years_in_korea = st.number_input(
        "Số năm cư trú hợp pháp tại Hàn Quốc",
        min_value=0.0,
        max_value=50.0,
        value=0.0,
        step=0.5
    )


# =========================================================
# 13. RESEARCH PROFILE
# =========================================================

st.divider()

st.header("🔬 Hồ sơ nghiên cứu")

col1, col2, col3 = st.columns(3)

with col1:

    papers = st.number_input(
        "Số bài báo quốc tế",
        min_value=0,
        step=1
    )

with col2:

    first_author = st.number_input(
        "Số bài first author",
        min_value=0,
        step=1
    )

with col3:

    patents = st.number_input(
        "Số patent",
        min_value=0,
        step=1
    )


st.text_area(
    "Các thành tích chính",
    placeholder=(
        "Ví dụ:\n"
        "- SCIE publications\n"
        "- Patent\n"
        "- Research award\n"
        "- Government / university commendation\n"
        "- Research contribution"
    ),
    height=150
)


# =========================================================
# 14. RESET
# =========================================================

st.divider()

if st.button(
    "🔄 Đặt lại checklist",
    use_container_width=True
):

    checkbox_keys = [
        key
        for key in st.session_state.keys()
        if key.startswith("check_")
    ]

    for key in checkbox_keys:
        del st.session_state[key]

    st.rerun()


# =========================================================
# 15. OFFICIAL LINKS
# =========================================================

st.divider()

st.header("🔗 Liên kết hữu ích")

col1, col2, col3 = st.columns(3)

with col1:

    st.link_button(
        "Hi Korea",
        "https://www.hikorea.go.kr/",
        use_container_width=True
    )

with col2:

    st.link_button(
        "Korea Immigration Service",
        "https://www.immigration.go.kr/",
        use_container_width=True
    )

with col3:

    st.link_button(
        "Korea Visa Portal",
        "https://www.visa.go.kr/",
        use_container_width=True
    )


# =========================================================
# 16. FOOTER
# =========================================================

st.divider()

st.caption(
    "Personal Korea Naturalization Checklist · "
    "우수인재 특별귀화"
)