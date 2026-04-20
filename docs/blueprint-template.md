# Day 13 Observability Lab Report

> **Instruction**: Fill in all sections below. This report is designed to be parsed by an automated grading assistant. Ensure all tags (e.g., `[GROUP_NAME]`) are preserved.

---

## 1. Team Metadata

- **[GROUP_NAME]**: Chatbot AI trong Chăm sóc Khách hàng Thương mại Điện tử tại Việt Nam
- **[REPO_URL]**: https://github.com/Logm12/Lab13_C401_E2
- **[MEMBERS]**:

| Phase | Role | Thành viên |
|---|---|---|
| Phase 1 | Logging + PII | Nguyễn Doãn Hiếu |
| Phase 2 | Tracing + Tags | Mạc Phạm Thiên Long |
| Phase 3 | SLO + Alerts | Cao Chí Hải |
| Phase 4 | Load test + Incident | Bùi Hữu Huấn |
| Phase 5 | Dashboard + Evidence | Nguyễn Văn Đạt |
| Phase 6 | Blueprint + Demo lead | Cao Chí Hải |

---

## 2. Group Performance (Auto-Verified)

- **[VALIDATE_LOGS_FINAL_SCORE]**: 100/100 (`python scripts/validate_logs.py`)
- **[TOTAL_TRACES_COUNT]**: >= 50 trong phiên logs hiện tại; ảnh `docs/evidence/evidence-trace-list.png` cho thấy trace list đã vượt xa mức tối thiểu 10 traces của rubric.
- **[PII_LEAKS_FOUND]**: 0
- **Regression smoke test**: `python -m pytest -q` → `2 passed`

---

## 3. Technical Evidence (Group)

### 3.1 Logging & Tracing

- **[EVIDENCE_CORRELATION_ID_SCREENSHOT]**: `docs/evidence/evidence-correlation-id.png`
- **[EVIDENCE_PII_REDACTION_SCREENSHOT]**: `docs/evidence/evidence-pii-redaction.png`
- **[EVIDENCE_TRACE_WATERFALL_SCREENSHOT]**: `docs/evidence/evidence-trace-waterfall.png`
- **[TRACE_WATERFALL_EXPLANATION]**: Trace được tạo từ `@observe()` trong `app/agent.py`. Mỗi request chatbot đi qua bước retrieval ở `app/mock_rag.py`, bước generate ở `app/mock_llm.py`, sau đó `update_current_trace()` gắn `user_id` đã hash, `session_id`, tags `lab/feature/model`, còn `update_current_span()` gắn `doc_count`, `query_preview`, `tokens_in` và `tokens_out`. Ở lớp API, `CorrelationIdMiddleware` trong `app/middleware.py` tạo hoặc propagate `correlation_id`, trả về `x-request-id` và `x-response-time-ms`, nên nhóm có thể nối trace với JSON logs và dashboard khi debug latency, chi phí hoặc lỗi.

### 3.2 Dashboard & SLOs

- **[DASHBOARD_6_PANELS_SCREENSHOT]**: `docs/evidence/evidence-dashboard-6-panels.png`
- **[SLO_TABLE]**:

| SLI | Target | Window | Current Value |
|---|---:|---|---|
| Latency P95 | < 3000ms | 28d | `164ms` theo `data/logs.jsonl` hiện tại; ảnh dashboard demo hiển thị `2667ms` trong một phiên stress/incident khác |
| Error Rate | < 2% | 28d | `0.00%` theo `data/logs.jsonl` hiện tại; ảnh dashboard demo hiển thị `33.33%` trong một phiên incident khác |
| Cost Budget | < $2.5/day | 1d | `$0.1092` tổng chi phí theo logs hiện tại; ảnh dashboard demo hiển thị `$0.2143` |
| Quality Score Avg | >= 0.75 | 28d | `0.856` theo logs hiện tại; ảnh dashboard demo hiển thị `0.86` |

- Dashboard triển khai đúng checklist trong `docs/dashboard-spec.md`: 6 panel bắt buộc gồm latency, traffic, error rate, cost, tokens in/out và quality proxy; ngoài ra còn có raw JSONL inspection và incident toggles để hỗ trợ điều tra.

### 3.3 Alerts & Runbook

- **[ALERT_RULES_SCREENSHOT]**: Repo hiện chưa có file PNG riêng cho alert rules; bằng chứng trực tiếp nằm ở `config/alert_rules.yaml` và runbook `docs/alerts.md`.
- **[SAMPLE_RUNBOOK_LINK]**: `docs/alerts.md#1-high-latency-p95`
- Ba alert rules đã cấu hình đủ theo rubric: `high_latency_p95` (P2), `high_error_rate` (P1) và `cost_budget_spike` (P2). Các anchor runbook trong `docs/alerts.md` khớp với trường `runbook` trong YAML.

---

## 4. Incident Response (Group)

- **[SCENARIO_NAME]**: `rag_slow`
- **[SYMPTOMS_OBSERVED]**: Kịch bản `rag_slow` được dùng để mô phỏng hệ thống quá tải trong giờ Flash Sale. Khi incident được bật, dashboard cho thấy Latency P95 tăng vọt lên khoảng `2650ms`, trong khi chatbot phản hồi chậm rõ rệt với các truy vấn cần tra cứu chính sách hoặc dữ liệu đơn hàng.
- **[ROOT_CAUSE_PROVED_BY]**: Nhóm phân tích Langfuse Trace Waterfall và xác định span Retrieval là điểm nghẽn chính trong pipeline. Sau đó truy vấn logs theo Correlation ID `req-d3f13bc4` để chứng minh nguyên nhân gốc rễ nằm ở bước truy xuất dữ liệu trong `rag_slow`, không phải ở bước generate của LLM. Chuỗi điều tra được thực hiện theo flow `Dashboard/Grafana → Langfuse Traces → Logs`.
- **[FIX_ACTION]**: Triển khai In-memory Cache trong `app/mock_rag.py` để giảm độ trễ cho các yêu cầu lặp lại, đặc biệt trong các khung giờ tải cao như Flash Sale. Đồng thời giữ kịch bản `rag_slow` làm incident mẫu để kiểm tra hiệu quả khắc phục.
- **[PREVENTIVE_MEASURE]**: Cập nhật Alert Rules và Runbook để phát hiện sớm khi latency P95 tăng bất thường, tiếp tục giám sát trace waterfall cho span Retrieval, và chuẩn hóa quy trình truy vết bằng Correlation ID để rút ngắn thời gian xử lý sự cố trong tương lai.

---

## 5. Individual Contributions & Evidence

### [MEMBER_A_NAME]: Nguyễn Doãn Hiếu — Phase 1: Logging + PII

- **[TASKS_COMPLETED]**: Phụ trách Phase 1 — hoàn thiện structured JSON logging, middleware correlation ID, cơ chế hash `user_id`, enrichment fields và pipeline scrub PII cho `message_preview` và `answer_preview`. Đồng thời kiểm tra `validate_logs.py` để bảo đảm log schema, correlation ID propagation, log enrichment và PII scrubbing đều đạt yêu cầu.
- **[EVIDENCE_LINK]**: Commit liên quan `1abd113`, `71aa801`; file `app/logging_config.py`, `app/middleware.py`, `app/pii.py`, `app/main.py`, `tests/test_pii.py`.

---

### [MEMBER_B_NAME]: Mạc Phạm Thiên Long — Phase 2: Tracing + Tags

- **[TASKS_COMPLETED]**: Phụ trách Phase 2 — triển khai tích hợp Langfuse tracing cho hệ thống. Sử dụng decorator `@observe` để tracking luồng xử lý từ request đến RAG và LLM. Cấu hình enrichment metadata gồm `user_id`, `session_id`, `tags` để truy vết chính xác theo ngữ cảnh E-commerce. Đảm bảo thu thập đầy đủ evidence trace waterfall phục vụ phân tích latency và root cause incident.
- **[EVIDENCE_LINK]**: https://github.com/Logm12/Lab13_C401_E2/commit/895bb9874d1bc37851dfa8ce675b06d51a275f66

---

### [MEMBER_C_NAME]: Cao Chí Hải — Phase 3: SLO + Alerts

- **[TASKS_COMPLETED]**: Phụ trách Phase 3 — rà soát và hoàn thiện phần Alerts & PII Evidence cho hệ thống observability. Cụ thể gồm kiểm tra 3 alert rules `high_latency_p95`, `high_error_rate`, `cost_budget_spike` trong `config/alert_rules.yaml`; đối chiếu runbook anchors trong `docs/alerts.md`; xác minh log đã redact PII qua evidence `docs/evidence/evidence-pii-redaction.png`; và bổ sung mô tả chứng cứ kỹ thuật cho mục Alerts & Runbook trong blueprint.
- **[EVIDENCE_LINK]**: Commit liên quan `00f5b59`, `71aa801`, `1abd113`; file `config/alert_rules.yaml`, `docs/alerts.md`, `docs/evidence/evidence-pii-redaction.png`, `docs/blueprint-template.md`.

---

### [MEMBER_D_NAME]: Bùi Hữu Huấn — Phase 4: Load test + Incident

- **[TASKS_COMPLETED]**: Phụ trách Phase 4 — thiết lập kịch bản sự cố `rag_slow` để mô phỏng tình trạng quá tải hệ thống trong giờ Flash Sale. Sử dụng Grafana Dashboard để phát hiện triệu chứng Latency P95 tăng lên mức `2650ms`. Phân tích Langfuse Trace Waterfall để xác định điểm nghẽn tại bước Retrieval. Truy vấn logs qua Correlation ID `req-d3f13bc4` để chứng minh nguyên nhân gốc rễ. Triển khai giải pháp khắc phục bằng In-memory Cache trong `app/mock_rag.py` giúp giảm độ trễ cho các yêu cầu lặp lại. Đồng thời cập nhật Alert Rules và Runbook để cải thiện khả năng ứng phó sự cố trong tương lai.
- **[EVIDENCE_LINK]**: https://github.com/Logm12/Lab13_C401_E2/commits/main/

---

### [MEMBER_E_NAME]: Nguyễn Văn Đạt — Phase 5: Dashboard + Evidence

- **[TASKS_COMPLETED]**: Phụ trách Phase 5 — xây dựng và hoàn thiện Grafana Dashboard với đầy đủ 6 panel bắt buộc (latency, traffic, error rate, cost, tokens in/out, quality proxy). Thu thập và tổng hợp toàn bộ evidence screenshots trong `docs/evidence/`, bao gồm correlation ID, PII redaction, trace waterfall và trace list. Đối chiếu dashboard với `docs/dashboard-spec.md` để đảm bảo đủ tiêu chí rubric.
- **[EVIDENCE_LINK]**: file `docs/evidence/evidence-correlation-id.png`, `docs/evidence/evidence-dashboard-6-panels.png`, `docs/evidence/evidence-trace-list.png`, `docs/evidence/evidence-trace-waterfall.png`.

---

### [MEMBER_F_NAME]: Cao Chí Hải — Phase 6: Blueprint + Demo lead

- **[TASKS_COMPLETED]**: Phụ trách Phase 6 — hoàn thiện `docs/blueprint-template.md`, tổng hợp evidence screenshots, đối chiếu rubric 60/40, cập nhật phần Group Performance, Technical Evidence, Incident Response và Git Evidence để báo cáo nhóm bám sát nội dung repo. Đồng thời chuẩn hóa mô tả theo flow điều tra `metrics → traces → logs` và liên kết các minh chứng từ `docs/evidence/`. Dẫn dắt buổi demo cuối khoá.
- **[EVIDENCE_LINK]**: Commit liên quan `00f5b59`, `71aa801`; file `docs/blueprint-template.md`, `docs/grading-evidence.md`, `docs/evidence/evidence-correlation-id.png`, `docs/evidence/evidence-dashboard-6-panels.png`, `docs/evidence/evidence-trace-list.png`, `docs/evidence/evidence-trace-waterfall.png`.

---

## 6. Bonus Items (Optional)

- **[BONUS_COST_OPTIMIZATION]**: Repo hiện mới dừng ở mức đề xuất tối ưu trong runbook và phần fix action, chưa có benchmark before/after riêng để chứng minh tiết kiệm chi phí nên chưa chốt bonus này.
- **[BONUS_AUDIT_LOGS]**: Chưa triển khai sink `data/audit.jsonl` hoặc module audit riêng; bonus này hiện chưa hoàn thành trong repo.
- **[BONUS_CUSTOM_METRIC]**: Đã có lớp custom investigation metric trong `app/main.py` gồm `quality_avg`, `records_in_window`, `raw_logs`, `live_metrics` và giao diện raw JSONL inspection trên dashboard để phục vụ điều tra incident theo ngữ cảnh chatbot CSKH TMĐT.
