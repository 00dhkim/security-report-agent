# Monthly SOC Report Intelligence Agent (ADK)

[한국어 README](README_ko.md)

This project is an AI agent system that automatically analyzes monthly Security Operations Center (SOC) reports and performs **threat detection → risk assessment → Korean summary generation** in a single pipeline. It uses ADK (Agent Development Kit) to build modular agents and fully automates the workflow from document ingestion to threat intelligence lookup, risk evaluation, and summarization.

---

## 📌 System Overview

Monthly SOC reports (.doc), provided by security monitoring vendors, contain key connection logs (e.g., `src_ip`, `dst_ip`, `dst_port`, `count`), but analysts must manually review them to determine anomalies — a time-consuming process.

This project aims to achieve:

* **Automatic DOC report parsing**
* **Automated threat intelligence lookup for IPs and ports**
* **Security-expert-level risk assessment**
* **A concise, one-paragraph Korean summary**

---

## 🧩 Agent Architecture

The full analysis pipeline consists of four agents:

1. **ReportExtractionAgent** – Extracts data from the report
2. **ThreatSearchAgent** – Searches for threat information based on extracted data
3. **RiskAssessmentAgent** – Assesses overall risk based on identified threats
4. **SummaryAgent** – Produces the final summary of all analysis results

Each agent follows the single-responsibility principle and communicates with the next using a standardized input/output schema.

![graph](graph.png)

---

## 🧠 Agent Details

### 1) ReportExtractionAgent

* **Role:** Parses the DOC report into CSV format and converts it into a normalized list of `ReportRecord` objects stored in the `state`.
* **Description:** Takes a monthly SOC `doc` report, uses the `doc_report_to_csv` and `csv_to_records` tools to extract `src_ip`, `dst_ip`, `dst_port`, and `count`, and saves them in the `records` field so later agents do not need to parse the document again.

### 2) ThreatSearchAgent

* **Role:** Automatically queries threat intelligence for every IP/port and stores the results in `ThreatInfo` objects within the `state`.
* **Description:** Uses `ip_lookup` and `port_lookup` tools to identify malicious indicators, threat levels, and related tags for each record, storing the results in a structured `threats` field.

### 3) RiskAssessmentAgent

* **Role:** Determines the month’s risk level from a security expert’s perspective and generates `overall_level`, `key_findings`, and `recommended_actions`.
* **Description:** Combines traffic records and threat intelligence to classify risk as “Normal,” “Caution,” or “High.” Evaluates factors such as frequency of malicious IPs and high-risk port patterns to generate structured findings and recommendations.

### 4) SummaryAgent

* **Role:** Produces a one-paragraph Korean summary based on the final risk assessment.
* **Description:** Generates a concise, easy-to-understand summary for security staff, covering overall risk level, major anomalies, noteworthy IP/port patterns, and recommended actions.

---

## 🚀 Processing Flow Summary

1. **User:** Uploads DOC report
2. **ReportExtractionAgent:** Creates CSV and parsed records
3. **ThreatSearchAgent:** Automatically looks up IP/port threats
4. **RiskAssessmentAgent:** Produces integrated risk evaluation
5. **SummaryAgent:** Generates one-paragraph summary
6. **Final Result Returned**

---

## ⚙️ Installation & Setup

Follow these steps to configure and run the agent.

1. **Prerequisites:**

   * Python 3.12+
   * `uv` installed (`pip install uv` if not installed)
   * **LibreOffice** (Required for `.doc` file processing)
     ```bash
     sudo apt install libreoffice  # For Ubuntu/Debian
     ```

2. **Clone the repository:**

   ```bash
   git clone https://github.com/00dhkim/security-report-agent.git
   cd security-report-agent
   ```

3. **Install dependencies:**
   Create a virtual environment and synchronize dependencies from `pyproject.toml`.

   ```bash
   uv sync
   source .venv/bin/activate
   ```

   This command creates a `.venv` directory if it doesn’t exist and installs required packages.

4. **Environment variables:**
   Create a `.env` file inside `security_report_agent/` and populate it with required configuration values (e.g., API keys).

   ```bash
   cp security_report_agent/.env.example security_report_agent/.env
   ```

---

## ▶️ Usage

To run the agent through the web interface, use:

```bash
adk web
```

This starts a local web server where you can run the `SecurityReportPipelineAgent` and view results in your browser. The `root_agent` defined in `security_report_agent/agent.py` orchestrates the full workflow, and the final summary is shown as the output.
