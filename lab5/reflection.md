# \# Lab 5 Reflection

# 

# \## 1. What is static code analysis, and why is it useful?

# 

# Static code analysis checks source code without running the program. It helps identify potential bugs, security risks, and coding-style problems early, making the code easier to maintain and review.

# 

# \## 2. What is the difference between Pylint, Bandit, and Flake8?

# 

# Pylint checks code quality, naming conventions, and maintainability. Bandit identifies common security risks in Python code. Flake8 checks code formatting and style, including many PEP 8 violations.

# 

# \## 3. Which issues did you find and fix?

# 

# The starter script had several problems, including a mutable default argument, a broad exception handler, unsafe shell-command construction, and files that were not consistently managed safely. It also lacked sufficient validation for equipment and time slots and executed the demonstration code when imported.

# 

# I improved the program by using a safe default argument, handling missing reservations explicitly, replacing shell-command execution with Python file operations, using context managers, validating time slots and equipment, and adding a main guard. I also corrected naming and formatting issues. After making these changes, the final code achieved a Pylint score of 10.00/10, Bandit reported no security issues, and Flake8 reported no errors.

# 

# \## 4. How does static analysis improve software quality?

# 

# Static analysis provides repeatable checks that help identify potential problems before execution or code review. Using multiple tools provides broader coverage of code quality, security, and formatting. However, the findings still require human judgment, and static analysis does not replace running and testing the program.

