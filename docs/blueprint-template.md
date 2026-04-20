# Day 13 Observability Lab Report

> **Instruction**: Fill in all sections below. This report is designed to be parsed by an automated grading assistant. Ensure all tags (e.g., `[GROUP_NAME]`) are preserved.

## 1. Team Metadata

- [GROUP_NAME]: Chatbot AI trong Chăm sóc Khách hàng Thương mại Điện tử tại Việt Nam
- [MEMBERS]:
  - Member A: Nguyễn Doãn Hiếu | Role: Track 1 - Logging & PII
  - Member B: Mạc Phạm Thiên Long - MSSV 2A202600384 | Role: Track 2 - Tracing & Enrichment
  - Member C: Cao Chí Hải - MSSV 2A202600011 | Role: Track 5 - Alerts & PII Evidence
  - Member D: Bùi Hữu Huấn | Role: Track 3/4 - Dashboard & Incident
  - Member E: Nguyễn Văn Đạt (2A202600411) | Role: Dashboard & Report

---

## 2. Group Performance (Auto-Verified)

- [TOTAL_TRACES_COUNT]: >= 50 trong phiên logs hiện tại; ảnh `docs/evidence/evidence-trace-list.png` cho thấy trace list đã vượt xa mức tối thiểu 10 traces của rubric.
- Regression smoke test: `python -m pytest -q` -> `2 passed`

---

## 3. Technical Evidence (Group)

### 3.1 Logging & Tracing

**Correlation ID**  
![EVIDENCE_CORRELATION_ID_SCREENSHOT](./docs/evidence/evidence-correlation-id.png)

**PII Redaction**  
![EVIDENCE_PII_REDACTION_SCREENSHOT](./docs/evidence/evidence-pii-redaction.png)

**Trace Waterfall**  
![EVIDENCE_TRACE_WATERFALL_SCREENSHOT](./docs/evidence/evidence-trace-waterfall.png)

**Trace explanation**  
The trace completed in only 0.16s with an input/output token ratio of 33→152, indicating a lightweight and fast LLM call. The `quality_score: 0.8` logged automatically within the span demonstrates that the pipeline captures both performance and quality signals in a single trace.

### 3.2 Dashboard & SLOs

**SLO_TABLE**

| SLI | Target | Window | Current Value |
|---|---:|---|---:|
| Latency P95 | < 2500ms | 28d | 187ms |
| Error Rate  | < 1% | 28d | 0.0% |
| Cost Budget | < $2.0/day | 1d | $0.0012 |
| Quality Score | >= 0.75 | 28d | 0.82 |

### 3.3 Alerts & Runbook

![ALERT_RULES_SCREENSHOT](./docs/evidence/alert_rules.png)
![SAMPLE_RUNBOOK_LINK]: docs/alerts.md#1-high-latency-p95

- Ba alert rules đã cấu hình đủ theo rubric: `high_latency_p95` (P2), `high_error_rate` (P1) và `cost_budget_spike` (P2). Các anchor runbook trong `docs/alerts.md` khớp với trường `runbook` trong YAML.

---

## 4. Incident Response (Group)

- **SCENARIO_NAME:** `rag_slow`
- **SYMPTOMS_OBSERVED:** Kịch bản `rag_slow` được dùng để mô phỏng hệ thống quá tải trong giờ Flash Sale. Khi incident được bật, dashboard cho thấy Latency P95 tăng vọt lên khoảng `2650ms`, trong khi chatbot phản hồi chậm rõ rệt với các truy vấn cần tra cứu chính sách hoặc dữ liệu đơn hàng.
- **ROOT_CAUSE_PROVED_BY:** Nhóm phân tích Langfuse Trace Waterfall và xác định span Retrieval là điểm nghẽn chính trong pipeline. Sau đó truy vấn logs theo Correlation ID `req-d3f13bc4` để chứng minh nguyên nhân gốc rễ nằm ở bước truy xuất dữ liệu trong `rag_slow`, không phải ở bước generate của LLM. Chuỗi điều tra được thực hiện theo flow `Dashboard/Grafana -> Langfuse Traces -> Logs`.
- **FIX_ACTION:** Triển khai In-memory Cache trong `app/mock_rag.py` để giảm độ trễ cho các yêu cầu lặp lại, đặc biệt trong các khung giờ tải cao như Flash Sale. Đồng thời giữ kịch bản `rag_slow` làm incident mẫu để kiểm tra hiệu quả khắc phục.
- **PREVENTIVE_MEASURE:** Cập nhật Alert Rules và Runbook để phát hiện sớm khi latency P95 tăng bất thường, tiếp tục giám sát trace waterfall cho span Retrieval, và chuẩn hóa quy trình truy vết bằng Correlation ID để rút ngắn thời gian xử lý sự cố trong tương lai.

---

## 5. Individual Contributions & Evidence

### Nguyễn Doãn Hiếu

- [TASKS_COMPLETED]: Phụ trách track 1: hoàn thiện structured JSON logging, middleware correlation ID, cơ chế hash `user_id`, enrichment fields và pipeline scrub PII cho `message_preview` và `answer_preview`. Đồng thời kiểm tra `validate_logs.py` để bảo đảm log schema, correlation ID propagation, log enrichment và PII scrubbing đều đạt yêu cầu.
- [EVIDENCE_LINK]: Commit liên quan `1abd113`, `71aa801`; file `app/logging_config.py`, `app/middleware.py`, `app/pii.py`, `app/main.py`, `tests/test_pii.py`.

### Mạc Phạm Thiên Long (2A202600384)

- [TASKS_COMPLETED]: Triển khai tích hợp Langfuse tracing cho hệ thống. Sử dụng decorator `@observe` để tracking luồng xử lý từ request đến RAG và LLM. Cấu hình enrichment metadata gồm `user_id`, `session_id`, `tags` để truy vết chính xác theo ngữ cảnh E-commerce. Đảm bảo thu thập đầy đủ evidence trace waterfall phục vụ phân tích latency và root cause incident.
- [EVIDENCE_LINK]: https://github.com/Logm12/Lab13_C401_E2/commit/895bb9874d1bc37851dfa8ce675b06d51a275f66

### Cao Chí Hải (2A202600011)

- [TASKS_COMPLETED]: Phụ trách track 5: rà soát và hoàn thiện phần Alerts & PII Evidence cho hệ thống observability. Cụ thể gồm kiểm tra 3 alert rules `high_latency_p95`, `high_error_rate`, `cost_budget_spike` trong `config/alert_rules.yaml`; đối chiếu runbook anchors trong `docs/alerts.md`; xác minh log đã redact PII qua evidence `docs/evidence/evidence-pii-redaction.png`; và bổ sung mô tả chứng cứ kỹ thuật cho mục Alerts & Runbook trong blueprint.
- [EVIDENCE_LINK]: Commit liên quan `00f5b59`, `71aa801`, `1abd113`; file `config/alert_rules.yaml`, `docs/alerts.md`, `docs/evidence/evidence-pii-redaction.png`, `docs/blueprint-template.md`.

### Bùi Hữu Huấn

- [TASKS_COMPLETED]: Thiết lập kịch bản sự cố `rag_slow` để mô phỏng tình trạng quá tải hệ thống trong giờ Flash Sale. Sử dụng Grafana Dashboard để phát hiện triệu chứng Latency P95 tăng lên mức `2650ms`. Phân tích Langfuse Trace Waterfall để xác định điểm nghẽn tại bước Retrieval. Truy vấn logs qua Correlation ID `req-d3f13bc4` để chứng minh nguyên nhân gốc rễ. Triển khai giải pháp khắc phục bằng In-memory Cache trong `app/mock_rag.py` giúp giảm độ trễ cho các yêu cầu lặp lại. Đồng thời cập nhật Alert Rules và Runbook để cải thiện khả năng ứng phó sự cố trong tương lai.

### Nguyễn Văn Đạt (2A202600411)

- [TASKS_COMPLETED]:
  - Implement dashboard 6 panels tại `/dashboard` endpoint (HTML + SVG sparklines, auto-refresh 15s, SLO threshold lines)
  - Thêm `/dashboard-data` API endpoint trả `snapshot`, `history`, `slo_targets`, `raw_logs`, `incidents` từ `data/logs.jsonl`
  - Nâng cấp `app/metrics.py`: thêm `METRIC_HISTORY`, `_append_history_point()`, `history()`, `error_rate_pct()` để dashboard có time-series data
  - Cập nhật `config/slo.yaml` với group target: P95 < 2500ms, error < 1%, cost < $2/day
  - Tạo `docs/evidence/` với screenshot dashboard 6 panels
- [EVIDENCE_LINK](https://github.com/Logm12/Lab13_C401_E2/commit/54a6593e3a55d404b5f9a6abfdd7e3b6a917484a)

#### Giải thích kỹ thuật (B1 — Individual Report Quality)

**Cách tính P95:**
P95 (percentile thứ 95) là giá trị latency mà 95% requests hoàn thành trong thời gian đó hoặc nhanh hơn. Công thức trong `metrics.py`:

```python
items = sorted(values)
idx = max(0, min(len(items) - 1, round((p / 100) * len(items) + 0.5) - 1))
return float(items[idx])
```

Ví dụ: 100 requests, sort latency, lấy phần tử thứ 95 → đó là P95. Nếu P95 = 2700ms > SLO 2500ms thì dashboard hiện badge "Attention Required" màu cam.

**Dashboard architecture:**

- `/dashboard-data` đọc `data/logs.jsonl`, filter theo `window_seconds`, tính metrics từ log events `response_sent` và `request_failed`, build `history_points` theo thứ tự thời gian.
- `/dashboard` phục vụ HTML tĩnh với JavaScript `fetch("/dashboard-data")` mỗi 15 giây, render 6 SVG sparklines. SLO line được vẽ bằng `<line stroke-dasharray="5 3">` màu amber trên mỗi chart.
- **6 panels**: (1) Latency P50/P95/P99 + SLO line, (2) Traffic req/min, (3) Error rate % + breakdown JSON, (4) Cost USD cumulative + budget line, (5) Tokens in/out total, (6) Quality score avg + target threshold.

**`METRIC_HISTORY` design:**
Giới hạn 120 điểm (xóa điểm cũ nhất khi vượt) để tránh memory leak trong long-running server. `history()` trả 60 điểm gần nhất cho sparklines đủ mượt mà không quá nặng.

---

## 6. Bonus Items (Optional)

- [BONUS_COST_OPTIMIZATION]: Repo hiện mới dừng ở mức đề xuất tối ưu trong runbook và phần fix action, chưa có benchmark before/after riêng để chứng minh tiết kiệm chi phí nên chưa chốt bonus này.
- [BONUS_AUDIT_LOGS]: Chưa triển khai sink `data/audit.jsonl` hoặc module audit riêng; bonus này hiện chưa hoàn thành trong repo.
- [BONUS_CUSTOM_METRIC]: Đã có lớp custom investigation metric trong `app/main.py` gồm `quality_avg`, `records_in_window`, `raw_logs`, `live_metrics` và giao diện raw JSONL inspection trên dashboard để phục vụ điều tra incident theo ngữ cảnh chatbot CSKH TMĐT.
