# Security Report Agent Context

## Project Overview
The **Security Report Agent** is an AI-powered system designed to automate the analysis of monthly Security Operations Center (SOC) reports. It processes `.doc` report files, extracts traffic data (IPs, ports), performs automated threat intelligence lookups, assesses security risks, and generates a concise summary in Korean.

The project is built using the **Google Agent Development Kit (ADK)** and follows a sequential multi-agent architecture.

## Architecture
The system utilizes a `SequentialAgent` pipeline consisting of four specialized sub-agents:

1.  **ReportExtractionAgent:** 
    *   Parses `.doc` files using `libreoffice` (conversion to `.docx`) and `python-docx`.
    *   Supports both file paths and **direct file uploads** via the ADK web interface.
    *   Extracts connection logs (Source IP, Dest IP, Port, Count) into a normalized format.
2.  **ThreatSearchAgent:** 
    *   Queries external threat intelligence sources for extracted IPs and ports.
    *   Enriches data with reputation scores and threat levels.
3.  **RiskAssessmentAgent:** 
    *   Evaluates the overall security risk based on traffic patterns and threat intelligence.
    *   Classifies risk as Normal, Caution, or High.
4.  **SummaryAgent:** 
    *   Synthesizes all findings into a one-paragraph Korean summary for security analysts.

## Key Files & Directories
*   `security_report_agent/agent.py`: Defines the `root_agent` (`SecurityReportPipelineAgent`) which orchestrates the sub-agents.
*   `security_report_agent/agents/`: Contains the logic for the four individual agents.
*   `security_report_agent/state/state.py`: Defines the Pydantic models (`ReportRecord`, `ThreatInfo`, `RiskAssessment`) used for state management and data exchange between agents.
*   `security_report_agent/tools/`: Contains utility functions, including `extraction_tools.py` (document parsing) and `threat_tools.py` (intelligence lookup).
*   `pyproject.toml`: Project dependencies and configuration (managed by `uv`).

## Setup & Prerequisites

### System Requirements
*   **Python:** 3.12 or higher.
*   **Package Manager:** `uv` is used for dependency management.
*   **External Tools:** `libreoffice` is **required** for converting `.doc` files to `.docx` during the extraction phase.
    *   *Linux:* `sudo apt install libreoffice` (or equivalent).

### Environment Variables
Create a `.env` file in `security_report_agent/.env` (based on `.env.example`):
*   `FRIENDLI_TOKEN`: For model inference (if used).
*   `VT_API_KEY`: VirusTotal API key for threat lookups.
*   `GEMINI_API_KEY`: Gemini API key for LLM operations.

## Development & Usage

### Installation
```bash
git clone https://github.com/00dhkim/security-report-agent.git
cd security-report-agent
uv sync
source .venv/bin/activate
```

### Running the Agent
The project is designed to be run via the ADK web interface:
```bash
adk web
```
This launches a local web server where you can interact with the `SecurityReportPipelineAgent` and trigger the analysis workflow.

### Code Style & Conventions
*   **Type Hinting:** Extensive use of Pydantic models for strict type checking and schema validation between agents.
*   **Modularity:** Each agent has a single responsibility and is isolated in its own module.
*   **Tools:** Capabilities are encapsulated as tools (functions) within the `tools/` directory.
