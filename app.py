
import streamlit as st

st.set_page_config(
    page_title="ZaloBot Affiliate",
    page_icon="🤖",
    layout="wide"
)

st.markdown("""
<style>
.main {
    background-color: #f5f7fb;
}
[data-testid="stSidebar"] {
    background-color: #172554;
}
[data-testid="stSidebar"] * {
    color: white !important;
}
h1 {
    color: #172554;
}
.card {
    background: white;
    padding: 22px;
    border-radius: 12px;
    border: 1px solid #e5e7eb;
    margin-bottom: 12px;
}
</style>
""", unsafe_allow_html=True)

st.sidebar.title("🤖 ZaloBot Affiliate")
st.sidebar.caption("Hệ thống quản lý Affiliate")

menu = st.sidebar.radio(
    "DANH MỤC",
    [
        "Tổng quan",
        "Quản lý tài khoản Zalo",
        "Quản lý nhóm",
        "Chuyển link Affiliate",
        "Quản lý thành viên",
        "Đơn hàng",
        "Hoa hồng",
        "Lịch sử hoạt động",
        "Cài đặt"
    ]
)

st.title("🤖 ZaloBot Affiliate")
st.caption("Phần mềm quản lý tiếp thị liên kết")

if menu == "Tổng quan":

    st.subheader("Tổng quan hệ thống")

    a, b, c, d = st.columns(4)

    a.metric("Tài khoản Zalo", "0")
    b.metric("Nhóm quản lý", "0")
    c.metric("Link đã chuyển", "0")
    d.metric("Hoa hồng", "0 đ")

    st.divider()

    st.subheader("Trạng thái hệ thống")

    st.info("Chưa kết nối tài khoản Zalo")

    st.success("Giao diện quản trị đã sẵn sàng")

elif menu == "Quản lý tài khoản Zalo":
    st.header("Quản lý tài khoản Zalo")
    st.info("Chức năng kết nối Zalo sẽ được phát triển ở bước tiếp theo.")

elif menu == "Quản lý nhóm":
    st.header("Quản lý nhóm Zalo")
    st.info("Chức năng quản lý nhóm đang chờ kết nối.")

elif menu == "Chuyển link Affiliate":
    st.header("Chuyển link Affiliate")

    link = st.text_input(
        "Dán đường link sản phẩm Shopee"
    )

    if st.button("Chuyển link"):
        if link:
            st.warning("Chưa cấu hình API Affiliate Shopee.")
        else:
            st.error("Vui lòng nhập đường link.")

elif menu == "Quản lý thành viên":
    st.header("Quản lý thành viên")

elif menu == "Đơn hàng":
    st.header("Quản lý đơn hàng")

elif menu == "Hoa hồng":
    st.header("Quản lý hoa hồng")

elif menu == "Lịch sử hoạt động":
    st.header("Lịch sử hoạt động")

elif menu == "Cài đặt":
    st.header("Cài đặt hệ thống")
    st.write("ZaloBot Affiliate phiên bản 1.0")
