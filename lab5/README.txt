Lab 5 working files

- scheduler_system.py: improved starter script
- issues.md: initial issue table (verify line numbers and tool findings)
- reflection.md: reflection responses

Run from this directory:
  python -m venv venv
  # Windows PowerShell: .\venv\Scripts\Activate.ps1
  # macOS/Linux: source venv/bin/activate
  python -m pip install pylint bandit flake8
  python scheduler_system.py

Before changes, save baseline reports from an untouched copy of the starter script. After changes, save reports again:
  pylint scheduler_system.py > pylint_report_after.txt
  bandit -r scheduler_system.py > bandit_report_after.txt
  flake8 scheduler_system.py > flake8_report_after.txt

The tool has not been run in this environment. Do not claim a verified Pylint score until the command is executed locally.
