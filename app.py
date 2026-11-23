
import streamlit as st
import csv
import io
from datetime import datetime

st.set_page_config(
    page_title="ZaloBot Affiliate",
    page_icon="🤖",
    layout="wide"
)

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

if menu == "Tổng quan":
    st.subheader("Tổng quan hệ thống")
    a, b, c, d = st.columns(4)
    a.metric("Tài khoản Zalo", "0")
    b.metric("Nhóm quản lý", "0")
    c.metric("Link đã lưu", len(st.session_state.links))
    d.metric("Hoa hồng", "0 đ")
    st.info("Chưa kết nối tài khoản Zalo.")

elif menu == "Chuyển link Affiliate":
    st.header("🔗 Chuyển link Affiliate")
    st.write("Quản lý link sản phẩm Shopee và link tiếp thị liên kết.")

    with st.form("form_link"):
        link_goc = st.text_input(
            "1. Link sản phẩm Shopee",
            placeholder="Dán link sản phẩm Shopee"
        )
        link_aff = st.text_input(
            "2. Link Affiliate Shopee",
            placeholder="Dán link Affiliate Shopee"
        )
        ghi_chu = st.text_input(
            "3. Ghi chú",
            placeholder="Tên sản phẩm hoặc thông tin ghi nhớ"
        )
        nut_luu = st.form_submit_button(
            "Lưu link vào danh sách",
            use_container_width=True
        )

    if nut_luu:
        link_goc = link_goc.strip()
        link_aff = link_aff.strip()
        ghi_chu = ghi_chu.strip()

        if not link_goc or not link_aff:
            st.error("Vui lòng nhập đủ link sản phẩm và link Affiliate.")
        elif not link_goc.startswith(("http://", "https://")):
            st.error("Link sản phẩm không đúng định dạng.")
        elif not link_aff.startswith(("http://", "https://")):
            st.error("Link Affiliate không đúng định dạng.")
        elif any(x["Link sản phẩm"] == link_goc for x in st.session_state.links):
            st.warning("Link sản phẩm này đã có trong danh sách.")
        else:
            st.session_state.links.append({
                "Thời gian": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                "Link sản phẩm": link_goc,
                "Link Affiliate": link_aff,
                "Ghi chú": ghi_chu
            })
            st.success("Đã lưu link thành công!")
            st.rerun()

    st.divider()
    st.subheader("📋 Danh sách link đã lưu")

    links = st.session_state.links
    st.metric("Tổng số link", len(links))

    tu_khoa = st.text_input(
        "Tìm kiếm link hoặc ghi chú",
        placeholder="Nhập tên sản phẩm hoặc link cần tìm"
    )

    ket_qua = [
        x for x in links
        if tu_khoa.lower() in (
            x["Link sản phẩm"] + " " +
            x["Link Affiliate"] + " " +
            x["Ghi chú"]
        ).lower()
    ]

    st.caption(f"Tìm thấy {len(ket_qua)} kết quả")

    for i, item in enumerate(ket_qua):
        with st.expander(
            f"{i + 1}. {item['Ghi chú'] or 'Sản phẩm chưa ghi chú'}"
        ):
            st.caption("Ngày lưu: " + item["Thời gian"])
            st.write("Link sản phẩm Shopee")
            st.code(item["Link sản phẩm"])
            st.write("Link Affiliate Shopee")
            st.code(item["Link Affiliate"])

    if links:
        output = io.StringIO()
        writer = csv.DictWriter(
            output,
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
            "Tải danh sách về máy",
            data="\ufeff" + output.getvalue(),
            file_name="danh_sach_link_affiliate.csv",
            mime="text/csv"
        )

    st.warning(
        "Dữ liệu hiện đang lưu tạm trong phiên sử dụng. "
        "Hãy tải danh sách về máy để sao lưu. "
        "Chưa có chức năng tự động tạo link Affiliate."
    )

else:
    st.header(menu)
    st.info("Mục này sẽ được phát triển ở các bước tiếp theo.")
