# Alert Rules and Runbooks

## 1. High latency P95
- Severity: P2
- Trigger: `latency_p95_ms > 5000 for 30m`
- Impact: chatbot CSKH phản hồi chậm, khách phải chờ lâu trong giờ cao điểm sale
- First checks:
  1. Mở các trace chậm nhất trong 1 giờ gần nhất
  2. So sánh span retrieval chính sách đơn hàng với span sinh phản hồi
  3. Kiểm tra incident toggle `rag_slow` có đang bật hay không
- Mitigation:
  - rút gọn prompt cho các câu hỏi FAQ lặp lại
  - chuyển sang nguồn FAQ fallback nếu retrieval chính quá chậm
  - ưu tiên câu trả lời mẫu ngắn gọn cho khung giờ flash sale

## 2. High error rate
- Severity: P1
- Trigger: `error_rate_pct > 5 for 5m`
- Impact: khách không tra cứu được đơn hàng, hoàn tiền hoặc đổi trả
- First checks:
  1. Nhóm log theo `error_type`
  2. Kiểm tra trace của request lỗi gần nhất
  3. Xác định lỗi đến từ tra cứu đơn hàng, tồn kho, hay bước sinh phản hồi
- Mitigation:
  - tạm tắt công cụ tra cứu lỗi và trả về thông báo fallback
  - kiểm tra dịch vụ tra cứu đơn hàng/tồn kho
  - retry bằng phản hồi mẫu hoặc model fallback nếu phù hợp

## 3. Cost budget spike
- Severity: P2
- Trigger: `hourly_cost_usd > 2x_baseline for 15m`
- Impact: chi phí chatbot tăng nhanh trong khung giờ sale lớn
- First checks:
  1. Chia trace theo feature và model
  2. So sánh `tokens_in` và `tokens_out` giữa các request
  3. Kiểm tra incident `cost_spike` có đang bật hay không
- Mitigation:
  - rút gọn prompt và response template cho FAQ
  - chuyển các câu hỏi đơn giản sang luồng trả lời rẻ hơn
  - cache các truy vấn lặp lại như giao hàng, đổi trả, hoàn tiền
