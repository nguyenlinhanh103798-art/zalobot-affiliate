
import streamlit as st
import csv
import io
from datetime import datetime

st.set_page_config(
    page_title="ZaloBot Affiliate",
    page_icon="🤖",
    layout="wide"
)

# Giao diện
st.markdown("""
<style>
.main {background-color: #f5f7fb;}
[data-testid="stSidebar"] {
    background-color: #172554;
}
[data-testid="stSidebar"] * {
    color: white !important;
}
h1 {color: #172554;}
</style>
""", unsafe_allow_html=True)

# Bộ nhớ tạm của ứng dụng
if "links" not in st.session_state:
    st.session_state.links = []

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

# TỔNG QUAN
if menu == "Tổng quan":
    st.subheader("Tổng quan hệ thống")

    a, b, c, d = st.columns(4)
    a.metric("Tài khoản Zalo", "0")
    b.metric("Nhóm quản lý", "0")
    c.metric("Link đã lưu", len(st.session_state.links))
    d.metric("Hoa hồng", "0 đ")

    st.divider()
    st.subheader("Trạng thái hệ thống")
    st.info("Chưa kết nối tài khoản Zalo.")
    st.success("Giao diện quản trị đang hoạt động.")

# CHUYỂN LINK AFFILIATE
elif menu == "Chuyển link Affiliate":
    st.header("🔗 Chuyển link Affiliate")
    st.write("Quản lý link sản phẩm Shopee và link tiếp thị liên kết.")

    with st.form("form_link"):
        link_goc = st.text_input(
            "1. Link sản phẩm Shopee",
            placeholder="Dán link sản phẩm Shopee vào đây"
        )

        link_aff = st.text_input(
            "2. Link Shopee Affiliate",
            placeholder="Dán link Affiliate đã tạo vào đây"
        )

        ghi_chu = st.text_input(
            "3. Ghi chú (không bắt buộc)",
            placeholder="Ví dụ: Áo khoác mùa đông"
        )

        nut_luu = st.form_submit_button(
            "Lưu link vào danh sách",
            use_container_width=True
        )

    if nut_luu:
        if not link_goc.strip() or not link_aff.strip():
            st.error("Bạn cần nhập cả link Shopee và link Affiliate.")
        elif "shopee." not in link_goc.lower():
            st.error("Link sản phẩm chưa đúng định dạng Shopee.")
        elif not link_goc.startswith("http") or not link_aff.startswith("http"):
            st.error("Link phải bắt đầu bằng http hoặc https.")
        else:
            st.session_state.links.append({
                "Thời gian": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                "Link sản phẩm": link_goc.strip(),
                "Link Affiliate": link_aff.strip(),
                "Ghi chú": ghi_chu.strip()
            })
            st.success("Đã lưu link thành công!")
            st.rerun()

    st.divider()
    st.subheader("📋 Danh sách link đã lưu")

    links = st.session_state.links

    if links:
        tu_khoa = st.text_input(
            "Tìm kiếm link hoặc ghi chú",
            placeholder="Nhập từ khóa cần tìm..."
        )

        ket_qua = [
            item for item in links
            if tu_khoa.lower() in (
                item["Link sản phẩm"] + " " +
                item["Link Affiliate"] + " " +
                item["Ghi chú"]
            ).lower()
        ]

        st.write(f"Đang có **{len(links)}** link. Tìm thấy **{len(ket_qua)}** kết quả.")

        for i, item in enumerate(ket_qua):
            with st.expander(f"Link {i + 1} — {item['Ghi chú'] or 'Chưa có ghi chú'}"):
                st.caption("Thời gian lưu: " + item["Thời gian"])
                st.write("Link sản phẩm Shopee:")
                st.code(item["Link sản phẩm"], language=None)
                st.write("Link Affiliate:")
                st.code(item["Link Affiliate"], language=None)

        # Xuất danh sách CSV
        noi_dung = io.StringIO()
        writer = csv.DictWriter(
            noi_dung,
            fieldnames=[
                "Thời gian",
                "Link sản phẩm",
                "Link Affiliate",
                "Ghi chú"
            ]
        )
        writer.writeheader()
        writer.writerows(links)

        st.download_button(
            "⬇️ Tải danh sách link về máy (CSV)",
            data="\ufeff" + noi_dung.getvalue(),
            file_name="danh_sach_link_affiliate.csv",
            mime="text/csv",
            use_container_width=True
        )

        st.divider()
        st.subheader("Xóa link")

        lua_chon = st.selectbox(
            "Chọn link cần xóa",
            options=list(range(len(links))),
            format_func=lambda i: (
                f"Link {i + 1} - "
                f"{links[i]['Ghi chú'] or links[i]['Link sản phẩm'][:45]}"
            )
        )

        if st.button("🗑️ Xóa link đã chọn", type="secondary"):
            st.session_state.links.pop(lua_chon)
            st.success("Đã xóa link.")
            st.rerun()

        if st.button("Xóa toàn bộ danh sách", type="secondary"):
            st.session_state.links = []
            st.rerun()

    else:
        st.info("Chưa có link nào. Hãy nhập link ở phía trên.")

    st.warning(
        "Lưu ý: Hiện tại bạn cần tự tạo link Affiliate rồi dán vào ô thứ hai. "
        "Chức năng tự động chuyển link sẽ được kết nối API ở bước sau. "
        "Danh sách hiện lưu tạm trong phiên sử dụng; có thể mất khi ứng dụng "
        "khởi động lại hoặc phiên bị làm mới. Hãy tải CSV để sao lưu."
    )

# CÁC MỤC ĐANG PHÁT TRIỂN
elif menu == "Quản lý tài khoản Zalo":
    st.header("Quản lý tài khoản Zalo")
    st.info("Chức năng kết nối tài khoản Zalo sẽ được phát triển ở bước tiếp theo.")

elif menu == "Quản lý nhóm":
    st.header("Quản lý nhóm Zalo")
    st.info("Chức năng quản lý nhóm đang chờ phát triển.")

elif menu == "Quản lý thành viên":
    st.header("Quản lý thành viên")
    st.info("Chức năng quản lý thành viên đang chờ phát triển.")

elif menu == "Đơn hàng":
    st.header("Quản lý đơn hàng")
    st.info("Chức năng đơn hàng đang chờ kết nối dữ liệu.")

elif menu == "Hoa hồng":
    st.header("Quản lý hoa hồng")
    st.info("Chức năng thống kê hoa hồng đang chờ phát triển.")

elif menu == "Lịch sử hoạt động":
    st.header("Lịch sử hoạt động")
    st.info("Lịch sử hệ thống sẽ được phát triển ở bước tiếp theo.")

elif menu == "Cài đặt":
    st.header("Cài đặt hệ thống")
    st.write("ZaloBot Affiliate phiên bản 1.1")
