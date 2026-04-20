from __future__ import annotations

import time
import unicodedata

from .incidents import STATE

CORPUS = {
    "doi_tra": [
        "Chính sách đổi trả: khách có thể yêu cầu đổi size hoặc trả hàng trong vòng 7 ngày kể từ khi nhận đơn nếu sản phẩm còn nguyên tem, chưa qua sử dụng và có mã đơn hàng hợp lệ."
    ],
    "van_chuyen": [
        "Chính sách vận chuyển: đơn nội thành Hà Nội và Hồ Chí Minh thường giao trong 1 đến 2 ngày, đơn liên tỉnh trong 3 đến 5 ngày tùy đối tác vận chuyển và thời điểm cao điểm."
    ],
    "hoan_tien": [
        "Hoàn tiền: sau khi yêu cầu trả hàng được duyệt và kho xác nhận hàng hợp lệ, tiền hoàn sẽ về tài khoản hoặc ví điện tử trong 3 đến 7 ngày làm việc."
    ],
    "giao_hang": [
        "Theo dõi giao hàng: chatbot nên giải thích trạng thái đơn, thời gian dự kiến, hướng dẫn khách kiểm tra địa chỉ và liên hệ CSKH nếu đơn chậm hơn SLA đã công bố."
    ],
    "ma_giam_gia": [
        "Mã giảm giá chỉ áp dụng khi đáp ứng điều kiện giá trị đơn tối thiểu, ngành hàng phù hợp, thời gian hiệu lực và giới hạn số lần sử dụng."
    ],
    "hoa_don": [
        "Xuất hóa đơn VAT: khách cần cung cấp mã đơn hàng, tên công ty, mã số thuế, địa chỉ xuất hóa đơn và email nhận hóa đơn điện tử."
    ],
    "pii": [
        "PII trong log phải được che hoàn toàn, bao gồm email, số điện thoại, số CCCD, số thẻ thanh toán và địa chỉ giao hàng chi tiết."
    ],
    "observability": [
        "Metrics giúp phát hiện triệu chứng, traces chỉ ra span chậm hoặc lỗi, còn logs với correlation_id giúp chứng minh root cause trong các tình huống chatbot CSKH bị chậm hoặc lỗi."
    ],
}


def _normalize(text: str) -> str:
    text = unicodedata.normalize("NFD", text)
    text = "".join(ch for ch in text if unicodedata.category(ch) != "Mn")
    return text.lower()


def retrieve(message: str) -> list[str]:
    if STATE["tool_fail"]:
        raise RuntimeError("Công cụ tra cứu đơn hàng/tồn kho bị timeout")
    if STATE["rag_slow"]:
        time.sleep(2.5)
    lowered = _normalize(message)

    keyword_map = {
        "doi_tra": ["doi size", "doi tra", "tra hang", "hoan hang"],
        "van_chuyen": ["van chuyen", "phi ship", "ship", "noi thanh", "lien tinh"],
        "hoan_tien": ["hoan tien", "vi dien tu", "momo"],
        "giao_hang": ["giao hang", "don hang", "trang thai", "da nang", "ha noi", "ho chi minh"],
        "ma_giam_gia": ["ma giam gia", "khuyen mai", "voucher"],
        "hoa_don": ["hoa don", "vat", "ma so thue"],
        "pii": ["pii", "email", "so dien thoai", "cccd", "4111", "dia chi"],
        "observability": ["metrics", "traces", "logs", "dashboard", "alert", "latency", "error rate"],
    }

    for corpus_key, keywords in keyword_map.items():
        if any(keyword in lowered for keyword in keywords):
            return CORPUS[corpus_key]
    return ["Không tìm thấy tài liệu miền phù hợp. Chatbot nên dùng câu trả lời FAQ tổng quát và hướng dẫn khách cung cấp thêm thông tin."]
