
import streamlit as st
import csv
import io
from openpyxl import load_workbook
from supabase import create_client

st.set_page_config(
    page_title="ZaloBot Affiliate",
    page_icon="🤖",
    layout="wide"
)

@st.cache_resource
def ket_noi_supabase():
    return create_client(
        st.secrets["SUPABASE_URL"],
        st.secrets["SUPABASE_KEY"]
    )

try:
    supabase = ket_noi_supabase()
    ket_noi_thanh_cong = True
except Exception as e:
    supabase = None
    ket_noi_thanh_cong = False
    loi_ket_noi = str(e)

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

if not ket_noi_thanh_cong:
    st.error("Chưa kết nối được Supabase. Hãy kiểm tra Secrets.")
    st.code(loi_ket_noi)

else:
    try:
        danh_sach = (
            supabase.table("affiliate_links")
            .select("*")
            .order("created_at", desc=True)
            .execute()
            .data or []
        )

        if menu == "Tổng quan":
            st.subheader("Tổng quan hệ thống")
            a, b, c, d = st.columns(4)
            a.metric("Tài khoản Zalo", "0")
            b.metric("Nhóm quản lý", "0")
            c.metric("Link đã lưu", len(danh_sach))
            d.metric("Hoa hồng", "0 đ")
            st.success("Đã kết nối cơ sở dữ liệu Supabase!")

        elif menu == "Chuyển link Affiliate":
            st.header("🔗 Chuyển link Affiliate")
            st.write("Quản lý link sản phẩm Shopee và link tiếp thị liên kết.")

            tab1, tab2 = st.tabs([
                "➕ Thêm link thủ công",
                "📥 Nhập Excel hàng loạt"
            ])

            with tab1:
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
                        st.error("Vui lòng nhập đủ 2 đường link.")

                    elif not link_goc.startswith(("http://", "https://")):
                        st.error("Link sản phẩm không đúng định dạng.")

                    elif not link_aff.startswith(("http://", "https://")):
                        st.error("Link Affiliate không đúng định dạng.")

                    else:
                        trung = (
                            supabase.table("affiliate_links")
                            .select("id")
                            .eq("product_link", link_goc)
                            .limit(1)
                            .execute()
                        )

                        if trung.data:
                            st.warning("Link sản phẩm này đã tồn tại!")
                        else:
                            supabase.table("affiliate_links").insert({
                                "product_link": link_goc,
                                "affiliate_link": link_aff,
                                "note": ghi_chu
                            }).execute()

                            st.success("Đã lưu link thành công!")
                            st.rerun()

            with tab2:
                st.subheader("📥 Nhập danh sách link từ Excel")

                st.write(
                    "File Excel cần có 3 cột: "
                    "Link sản phẩm Shopee, Link Affiliate Shopee, Ghi chú."
                )

                st.caption(
                    "Dữ liệu bắt đầu từ dòng 2. "
                    "Dòng 1 là tiêu đề cột."
                )

                file_excel = st.file_uploader(
                    "Chọn file Excel (.xlsx)",
                    type=["xlsx"],
                    key="file_excel"
                )

                if file_excel is not None:
                    if st.button("🔍 Kiểm tra file Excel"):
                        try:
                            workbook = load_workbook(
                                file_excel,
                                read_only=True,
                                data_only=True
                            )

                            sheet = workbook.active
                            du_lieu = list(
                                sheet.iter_rows(
                                    min_row=2,
                                    values_only=True
                                )
                            )

                            workbook.close()

                            hop_le = []
                            loi = 0
                            bo_qua = 0

                            for row in du_lieu:
                                if not row or len(row) < 2:
                                    bo_qua += 1
                                    continue

                                link_sp = str(row[0] or "").strip()
                                link_aff = str(row[1] or "").strip()
                                note = str(row[2] or "").strip() if len(row) > 2 else ""

                                if not link_sp or not link_aff:
                                    loi += 1
                                    continue

                                if not link_sp.startswith(("http://", "https://")):
                                    loi += 1
                                    continue

                                if not link_aff.startswith(("http://", "https://")):
                                    loi += 1
                                    continue

                                hop_le.append({
                                    "product_link": link_sp,
                                    "affiliate_link": link_aff,
                                    "note": note
                                })

                            st.session_state["excel_hop_le"] = hop_le
                            st.session_state["excel_loi"] = loi
                            st.session_state["excel_bo_qua"] = bo_qua

                            st.success(
                                f"Đọc được {len(hop_le)} dòng hợp lệ."
                            )
                            st.info(
                                f"Dòng lỗi: {loi} | Dòng trống bỏ qua: {bo_qua}"
                            )

                        except Exception as e:
                            st.error("Không đọc được file Excel.")
                            st.code(str(e))

                if "excel_hop_le" in st.session_state:
                    so_dong = len(st.session_state["excel_hop_le"])

                    if so_dong > 0:
                        st.write(f"**Số link hợp lệ: {so_dong}**")

                        if st.button("💾 Bắt đầu nhập vào hệ thống"):
                            thanh_cong = 0
                            trung = 0
                            loi_nhap = 0

                            tien_do = st.progress(0)
                            trang_thai = st.empty()

                            for i, item in enumerate(
                                st.session_state["excel_hop_le"]
                            ):
                                try:
                                    kiem_tra = (
                                        supabase.table("affiliate_links")
                                        .select("id")
                                        .eq(
                                            "product_link",
                                            item["product_link"]
                                        )
                                        .limit(1)
                                        .execute()
                                    )

                                    if kiem_tra.data:
                                        trung += 1
                                    else:
                                        supabase.table("affiliate_links").insert(
                                            item
                                        ).execute()
                                        thanh_cong += 1

                                except Exception:
                                    loi_nhap += 1

                                tien_do.progress((i + 1) / so_dong)
                                trang_thai.write(
                                    f"Đang xử lý {i + 1}/{so_dong}"
                                )

                            st.session_state.pop("excel_hop_le", None)

                            st.success(
                                f"Hoàn tất! Đã thêm: {thanh_cong} link."
                            )
                            st.info(
                                f"Trùng: {trung} | Lỗi khi lưu: {loi_nhap}"
                            )
                            st.rerun()

            st.divider()
            st.subheader("📋 Danh sách link đã lưu")

            st.metric("Tổng số link", len(danh_sach))

            tu_khoa = st.text_input(
                "Tìm kiếm link hoặc ghi chú",
                placeholder="Nhập tên sản phẩm hoặc link cần tìm"
            )

            ket_qua = [
                x for x in danh_sach
                if tu_khoa.lower() in (
                    str(x.get("product_link", "")) + " " +
                    str(x.get("affiliate_link", "")) + " " +
                    str(x.get("note", ""))
                ).lower()
            ]

            st.caption(f"Tìm thấy {len(ket_qua)} kết quả")

            for i, item in enumerate(ket_qua):
                ma_id = item["id"]

                with st.expander(
                    f"{i + 1}. {item.get('note') or 'Sản phẩm chưa ghi chú'}"
                ):
                    st.caption("Mã link: " + str(ma_id))
                    st.caption("Ngày lưu: " + str(item.get("created_at", "")))

                    st.write("Link sản phẩm Shopee")
                    st.code(item.get("product_link", ""))

                    st.write("Link Affiliate Shopee")
                    st.code(item.get("affiliate_link", ""))

                    st.divider()
                    st.write("✏️ Chỉnh sửa thông tin")

                    with st.form(f"form_sua_{ma_id}"):
                        link_goc_moi = st.text_input(
                            "Link sản phẩm Shopee",
                            value=item.get("product_link", "")
                        )

                        link_aff_moi = st.text_input(
                            "Link Affiliate Shopee",
                            value=item.get("affiliate_link", "")
                        )

                        ghi_chu_moi = st.text_input(
                            "Ghi chú",
                            value=item.get("note") or ""
                        )

                        nut_cap_nhat = st.form_submit_button(
                            "💾 Cập nhật link"
                        )

                    if nut_cap_nhat:
                        link_goc_moi = link_goc_moi.strip()
                        link_aff_moi = link_aff_moi.strip()
                        ghi_chu_moi = ghi_chu_moi.strip()

                        if not link_goc_moi or not link_aff_moi:
                            st.error("Vui lòng nhập đủ 2 đường link.")

                        elif not link_goc_moi.startswith(("http://", "https://")):
                            st.error("Link sản phẩm không hợp lệ.")

                        elif not link_aff_moi.startswith(("http://", "https://")):
                            st.error("Link Affiliate không hợp lệ.")

                        else:
                            try:
                                trung = (
                                    supabase.table("affiliate_links")
                                    .select("id")
                                    .eq("product_link", link_goc_moi)
                                    .neq("id", ma_id)
                                    .limit(1)
                                    .execute()
                                )

                                if trung.data:
                                    st.warning("Link sản phẩm này đã tồn tại ở dòng khác!")
                                else:
                                    supabase.table("affiliate_links").update({
                                        "product_link": link_goc_moi,
                                        "affiliate_link": link_aff_moi,
                                        "note": ghi_chu_moi
                                    }).eq("id", ma_id).execute()

                                    st.success("Đã cập nhật thành công!")
                                    st.rerun()

                            except Exception as e:
                                st.error("Lỗi khi cập nhật:")
                                st.code(str(e))

                    st.divider()
                    st.write("🗑️ Xóa link")

                    xac_nhan = st.checkbox(
                        "Tôi xác nhận muốn xóa link này",
                        key=f"xac_nhan_xoa_{ma_id}"
                    )

                    if st.button(
                        "🗑️ Xóa link",
                        key=f"xoa_{ma_id}",
                        disabled=not xac_nhan
                    ):
                        try:
                            supabase.table("affiliate_links").delete().eq(
                                "id", ma_id
                            ).execute()

                            st.success("Đã xóa link thành công!")
                            st.rerun()

                        except Exception as e:
                            st.error("Lỗi khi xóa:")
                            st.code(str(e))

            if danh_sach:
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

                for item in danh_sach:
                    writer.writerow({
                        "Thời gian": item.get("created_at", ""),
                        "Link sản phẩm": item.get("product_link", ""),
                        "Link Affiliate": item.get("affiliate_link", ""),
                        "Ghi chú": item.get("note", "")
                    })

                st.download_button(
                    "📥 Tải danh sách về máy",
                    data="\ufeff" + output.getvalue(),
                    file_name="danh_sach_link_affiliate.csv",
                    mime="text/csv"
                )

        else:
            st.header(menu)
            st.info("Mục này sẽ được phát triển ở các bước tiếp theo.")

    except Exception as e:
        st.error("Có lỗi khi đọc dữ liệu từ Supabase:")
        st.code(str(e))
