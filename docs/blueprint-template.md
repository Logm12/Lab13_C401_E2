# Day 13 Observability Lab Report

> **Instruction**: Fill in all sections below. This report is designed to be parsed by an automated grading assistant. Ensure all tags (e.g., `[GROUP_NAME]`) are preserved.

## 1. Team Metadata
- [GROUP_NAME]: 
- [REPO_URL]: 
- [MEMBERS]:
  - Member A: [Name] | Role: Logging & PII
  - Member B: [Name] | Role: Tracing & Enrichment
  - Member C: [Name] | Role: SLO & Alerts
  - Member A: Bùi Hữu Huấn | Role: Full-stack Observability Engineer
  - Member E: [Name] | Role: Demo & Report

---

## 2. Group Performance (Auto-Verified)
- [VALIDATE_LOGS_FINAL_SCORE]: /100
- [TOTAL_TRACES_COUNT]: 
- [PII_LEAKS_FOUND]: 

---

## 3. Technical Evidence (Group)

### 3.1 Logging & Tracing
- [EVIDENCE_CORRELATION_ID_SCREENSHOT]: [Path to image]
- [EVIDENCE_PII_REDACTION_SCREENSHOT]: [Path to image]
- [EVIDENCE_TRACE_WATERFALL_SCREENSHOT]: [Path to image]
- [TRACE_WATERFALL_EXPLANATION]: (Briefly explain one interesting span in your trace)

### 3.2 Dashboard & SLOs
- [DASHBOARD_6_PANELS_SCREENSHOT]: [Path to image]
- [SLO_TABLE]:
| SLI | Target | Window | Current Value |
|---|---:|---|---:|
| Latency P95 | < 3000ms | 28d | |
| Error Rate | < 2% | 28d | |
| Cost Budget | < $2.5/day | 1d | |

### 3.3 Alerts & Runbook
- [ALERT_RULES_SCREENSHOT]: [Path to image]
- [SAMPLE_RUNBOOK_LINK]: [docs/alerts.md#L...]

---


## 4. Incident Response (Group)
- [SCENARIO_NAME]: rag_slow — "High Latency during Flash Sale Catalog Retrieval"
- [SYMPTOMS_OBSERVED]: Hệ thống giám sát ghi nhận Latency P95 tăng vọt từ mức bình thường (~200ms) lên mức ổn định ~2650ms. Chatbot vẫn trả lời đúng nội dung nhưng tốc độ phản hồi rất chậm, gây ảnh hưởng đến trải nghiệm khách hàng trong khung giờ cao điểm.
- [ROOT_CAUSE_PROVED_BY]: Phân tích Trace ID (Langfuse) cho thấy span `retrieve` chiếm 95% thời gian request. Chứng minh bằng log thực tế: Correlation ID `req-d3f13bc4` có `latency_ms: 2651`. Điểm nghẽn xác định tại layer Retrieval do dữ liệu catalog quá tải.
- [FIX_ACTION]: Tạm thời ngắt giả lập sự cố. Triển khai cơ chế Simple In-memory Cache trong `app/mock_rag.py` cho các từ khóa phổ biến để bỏ qua bước truy vấn chậm khi đã có kết quả trước đó.
- [PREVENTIVE_MEASURE]: Cấu hình Alert P2 cho Latency P95 > 2s. Thiết lập Circuit Breaker để tự động chuyển sang câu trả lời FAQ mặc định nếu Vector Database không phản hồi trong 1.5s.

---

## 5. Individual Contributions & Evidence

### [MEMBER_A_NAME]
- [TASKS_COMPLETED]: 
- [EVIDENCE_LINK]: (Link to specific commit or PR)

### [MEMBER_B_NAME]
- [TASKS_COMPLETED]: 
- [EVIDENCE_LINK]: 

### [MEMBER_C_NAME]
- [TASKS_COMPLETED]: 
- [EVIDENCE_LINK]: 

### Bùi Hữu Huấn
- [TASKS_COMPLETED]: 
  - Thiết lập kịch bản sự cố `rag_slow` để mô phỏng tình trạng quá tải hệ thống trong giờ Flash Sale.
  - Sử dụng Grafana Dashboard để phát hiện triệu chứng Latency P95 tăng vọt lên mức 2650ms.
  - Phân tích Langfuse Trace Waterfall để xác định điểm nghẽn tại bước Retrieval.
  - Truy vấn Logs qua Correlation ID `req-d3f13bc4` để chứng minh nguyên nhân gốc rễ.
  - Triển khai giải pháp khắc phục bằng In-memory Cache trong `app/mock_rag.py` giúp giảm độ trễ cho các yêu cầu lặp lại.
  - Cập nhật Alert Rules và Runbook để cải thiện khả năng ứng phó sự cố trong tương lai.
- [EVIDENCE_LINK]: [Link](https://github.com/Logm12/Lab13_C401_E2/commits/main/)

### [MEMBER_E_NAME]
- [TASKS_COMPLETED]: 
- [EVIDENCE_LINK]: 

---

## 6. Bonus Items (Optional)
- [BONUS_COST_OPTIMIZATION]: (Description + Evidence)
- [BONUS_AUDIT_LOGS]: (Description + Evidence)
- [BONUS_CUSTOM_METRIC]: (Description + Evidence)
