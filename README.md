# nuclei-tool
custom nuclei wrapper tool

# Nuclei Custom Tool

A Python-based Command Line Interface (CLI) wrapper for [ProjectDiscovery's Nuclei](https://github.com/projectdiscovery/nuclei) scanner. This tool provides a streamlined way to run scans, format the output beautifully in the terminal, and save your scan history and findings to a local SQLite database.

## Features

- **Simple CLI:** Easy-to-use commands powered by `Typer`.
- **Beautiful Output:** Formatted tables and progress spinners using `Rich`.
- **Local History:** Automatically saves scan results and findings to a local `scans.db` SQLite database.
- **Smart Path Detection:** Automatically finds the Nuclei binary and templates whether they are in your system PATH, a local `bin` folder, or defined in a `.env` file.

---

## Prerequisites

Before you begin, ensure you have:
1. **Python 3.9+** installed.
2. **Nuclei** installed on your system. 
   - *Option A:* Install via package manager (e.g., `choco install nuclei -y` on Windows).
   - *Option B:* Download the binary from the [Nuclei Releases](https://github.com/projectdiscovery/nuclei/releases/latest) and place `nuclei.exe` inside the `nuclei_tool/bin/` directory of this project.

---

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/artechnism/nuclei-tool.git
   cd nuclei-tool
Create and activate a virtual environment:


python -m venv .venv
.venv\Scripts\activate
Install the required Python dependencies:

bash
pip install -r requirements.txt
Configure Environment Variables:

Duplicate the .env.example file and rename it to .env.

Open the .env file and set the paths to your Nuclei binary and templates if they are not in the default locations:

env
NUCLEI_PATH=C:\Tools\nuclei\nuclei.exe
NUCLEI_TEMPLATES=C:\Users\YourUser\nuclei-templates
Update Nuclei Templates (Important):
Make sure your Nuclei templates are up to date:


nuclei -update-templates
Usage
The tool uses a sub-command structure. You can always see the available commands by running:


python main.py --help
1. Running a Scan
To run a scan against a target, use the scan command:


python main.py scan <TARGET> [OPTIONS]
Options & Arguments for scan:

Argument / Option	Shortcut	Description	Default
TARGET	-	The URL or IP address to scan (Required).	-
--severity	-s	Filter by severity level (e.g., critical, high, medium). Can be used multiple times.	All levels
--tags	-t	Filter by template tags (e.g., xss, sqli, cve). Can be used multiple times.	All tags
--rate-limit	-	Maximum number of requests per second.	100
--save / --no-save	-	Save the results to the SQLite database or not.	--save
Examples:

Run a basic scan on a target:


python main.py scan "https://example.com"
Scan only for High and Critical severity XSS vulnerabilities:


python main.py scan "https://example.com" --severity high --severity critical --tags xss
Run a scan but do not save it to the database:


python main.py scan "http://testphp.vulnweb.com/" --no-save
2. Viewing Scan History
To view a list of your previous scans stored in the database, use the history command:


python main.py history
This will display a table showing the Scan ID, Target, and Date of previous scans.
