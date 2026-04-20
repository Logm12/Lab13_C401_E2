from __future__ import annotations

import random
import time
from dataclasses import dataclass

from .incidents import STATE


@dataclass
class FakeUsage:
    input_tokens: int
    output_tokens: int


@dataclass
class FakeResponse:
    text: str
    usage: FakeUsage
    model: str


class FakeLLM:
    def __init__(self, model: str = "claude-sonnet-4-5") -> None:
        self.model = model

    def generate(self, prompt: str) -> FakeResponse:
        time.sleep(0.15)
        input_tokens = max(20, len(prompt) // 4)
        output_tokens = random.randint(80, 180)
        if STATE["cost_spike"]:
            output_tokens *= 4
        question = prompt.split("Question=", 1)[-1].strip().lower()
        answer = self._answer_for_question(question)
        return FakeResponse(text=answer, usage=FakeUsage(input_tokens, output_tokens), model=self.model)

    def _answer_for_question(self, question: str) -> str:
        if "đổi size" in question or "doi size" in question or "đổi trả" in question or "doi tra" in question:
            return (
                "Dạ shop hỗ trợ đổi size trong vòng 7 ngày kể từ khi khách nhận đơn hàng, với điều kiện sản phẩm còn nguyên tem "
                "và chưa qua sử dụng. Anh/chị vui lòng cung cấp mã đơn hàng, hình ảnh sản phẩm và chọn size muốn đổi để chatbot "
                "tạo yêu cầu hỗ trợ nhanh hơn."
            )
        if "giao hàng thứ 7" in question or "giao hàng thứ 7 chủ nhật" in question or "giao hàng" in question and "hà nội" in question:
            return (
                "Dạ hiện shop có hỗ trợ giao hàng cuối tuần tại Hà Nội tùy khu vực và đối tác vận chuyển. Với đơn gấp trong 2 ngày, "
                "chatbot nên kiểm tra tồn kho, xác nhận địa chỉ, sau đó ưu tiên gợi ý giao nhanh hoặc hỏa tốc nếu hệ thống hỗ trợ."
            )
        if "vận chuyển" in question or "phí ship" in question:
            return (
                "Tóm tắt chính sách vận chuyển: đơn nội thành Hồ Chí Minh thường giao trong 1 đến 2 ngày, phí ship phụ thuộc giá trị đơn "
                "và chương trình miễn phí vận chuyển. Chatbot nên nêu rõ thời gian giao hàng dự kiến, phí ship và điều kiện áp dụng ưu đãi."
            )
        if "chờ xác nhận" in question:
            return (
                "Dạ với đơn đã thanh toán nhưng còn ở trạng thái chờ xác nhận, chatbot nên xin khách đợi thêm ít phút, kiểm tra mã đơn hàng, "
                "xác nhận phương thức thanh toán và hướng dẫn liên hệ nhân viên nếu trạng thái không thay đổi sau thời gian cam kết."
            )
        if "số điện thoại" in question or "so dien thoai" in question or "ẩn gì" in question or "an gi" in question:
            return (
                "Hệ thống chỉ nên log mã đơn hàng, loại lỗi và correlation_id để phục vụ điều tra. Các trường nhạy cảm như số điện thoại, "
                "email, địa chỉ giao hàng hoặc thông tin thanh toán phải được redact trước khi ghi vào app log và audit log."
            )
        if "hoàn tiền" in question or "hoan tien" in question:
            return (
                "Dạ sau khi shop xác nhận hàng trả về hợp lệ, tiền hoàn thường được xử lý trong 3 đến 7 ngày làm việc tùy phương thức thanh toán. "
                "Chatbot nên thông báo rõ mốc thời gian, trạng thái xử lý và kênh hỗ trợ nếu quá hạn."
            )
        if "không được xuất hiện trong log" in question or "khong duoc xuat hien trong log" in question:
            return (
                "Những thông tin không được xuất hiện trong log gồm PII như số điện thoại, email, địa chỉ giao hàng, số CCCD, mã thẻ thanh toán "
                "và nội dung nhạy cảm do khách cung cấp. Log chỉ nên giữ dữ liệu đã redact, mã đơn hàng và ngữ cảnh vận hành cần thiết."
            )
        if "flash sale" in question or "trả lời chậm" in question or "tra loi cham" in question:
            return (
                "Để debug chatbot chậm trong giờ flash sale, nhóm nên đi theo thứ tự metrics → traces → logs. Trước hết xem traffic và latency P95, "
                "sau đó mở trace chậm nhất để xác định span retrieval hay generate, cuối cùng dùng correlation_id trong logs để chứng minh nguyên nhân."
            )
        if "4111" in question or "địa chỉ giao hàng" in question or "dia chi giao hang" in question or "cccd" in question:
            return (
                "Các trường như số thẻ, số CCCD, email, số điện thoại và địa chỉ giao hàng phải được redact hoàn toàn trước khi lưu log. "
                "Hệ thống nên thay bằng các token như [REDACTED_CREDIT_CARD], [REDACTED_CCCD], [REDACTED_EMAIL] hoặc [REDACTED_ADDRESS]."
            )
        if "alert" in question or "cảnh báo" in question or "canh bao" in question:
            return (
                "Ba alert quan trọng cho chatbot CSKH TMĐT là latency P95 tăng cao, error rate vượt ngưỡng và cost spike theo giờ. "
                "Các alert này giúp đội vận hành phát hiện sớm tình trạng quá tải, lỗi tra cứu đơn hàng và chi phí token tăng bất thường trong dịp sale."
            )
        if "hủy đơn" in question or "huy don" in question:
            return (
                "Nếu đơn chưa đóng gói, chatbot nên xác nhận mã đơn hàng, kiểm tra trạng thái xử lý và hỗ trợ hủy đơn ngay trên hệ thống. "
                "Sau đó cần thông báo rõ thời gian hoàn tiền, kênh theo dõi trạng thái và trường hợp nào không thể hủy tự động."
            )
        if "thiếu sản phẩm" in question or "thieu san pham" in question:
            return (
                "Khi khách báo thiếu sản phẩm, chatbot nên xin lỗi trước, xác nhận mã đơn hàng, yêu cầu ảnh kiện hàng và phiếu giao, "
                "sau đó tạo ticket để kho hoặc CSKH kiểm tra trong SLA đã công bố."
            )
        if "đổi địa chỉ" in question or "doi dia chi" in question:
            return (
                "Chatbot nên kiểm tra trạng thái đơn trước, vì chỉ các đơn chưa bàn giao cho đơn vị vận chuyển mới có thể đổi địa chỉ dễ dàng. "
                "Nếu đơn đã xuất kho, chatbot cần hướng dẫn khách liên hệ tổng đài hoặc chờ đơn vị vận chuyển hỗ trợ cập nhật."
            )
        if "mã giảm giá" in question or "ma giam gia" in question:
            return (
                "Trước khi phản hồi, chatbot nên kiểm tra hạn sử dụng mã, điều kiện giá trị đơn tối thiểu, danh mục áp dụng, số lần sử dụng "
                "và việc mã có áp dụng đồng thời với chương trình khuyến mãi khác hay không."
            )
        if "hóa đơn vat" in question or "hoa don vat" in question:
            return (
                "Để xuất hóa đơn VAT, chatbot nên hướng dẫn khách chuẩn bị mã đơn hàng, tên công ty, mã số thuế, địa chỉ xuất hóa đơn "
                "và email nhận hóa đơn điện tử. Sau đó cần nêu rõ thời gian xử lý dự kiến."
            )
        if "dashboard" in question or "latency, error rate, cost" in question:
            return (
                "Dashboard cho chatbot CSKH nên có 6 panel cốt lõi: latency P50/P95/P99, traffic, error rate với breakdown, cost over time, "
                "tokens in/out và quality proxy. Mỗi panel cần có đơn vị rõ ràng, auto refresh và threshold SLO để đội vận hành quan sát nhanh."
            )
        if "metrics" in question and "traces" in question and "logs" in question:
            return (
                "Metrics giúp phát hiện triệu chứng như latency hoặc error rate tăng, traces cho biết span nào chậm, còn logs cung cấp correlation_id "
                "và chi tiết lỗi cụ thể. Kết hợp cả ba lớp sẽ giúp nhóm xác định nguyên nhân nhanh và chứng minh được root cause."
            )
        if "tóm tắt" in question or "tom tat" in question or "viết" in question or "viet" in question:
            return (
                "Dạ chatbot CSKH nên trả lời ngắn gọn, lịch sự và theo đúng ngữ cảnh thương mại điện tử: nêu mã đơn hàng khi cần, "
                "thời gian xử lý dự kiến, chính sách áp dụng và bước tiếp theo để khách dễ theo dõi."
            )
        return (
            "Dạ em có thể hỗ trợ khách về trạng thái đơn hàng, đổi trả, hoàn tiền, giao hàng, mã giảm giá và thông tin hóa đơn. "
            "Để xử lý nhanh hơn, chatbot nên xác nhận mã đơn hàng, tóm tắt vấn đề của khách và cung cấp hướng dẫn rõ ràng theo chính sách hiện hành."
        )
