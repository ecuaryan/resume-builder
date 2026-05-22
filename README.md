# resume-builder

Generate a PDF resume from Python using [ReportLab](https://www.reportlab.com/).

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Build

```bash
python resume.py
```

The PDF is written to `output/Ryan_Willmore_Resume.pdf`. That directory is gitignored so generated files stay local.

## Workflow

Edit content and styling in `resume.py`, run the script to regenerate the PDF, then commit and push source changes only.
