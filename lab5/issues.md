# Static Code Analysis Issues

> Preliminary issue inventory based on manual inspection of the starter script. Replace or update line numbers and findings after running Pylint, Bandit, and Flake8 and saving their actual reports.

|Issue|Type|Line(s) in starter|Description|Fix approach|
|-|-|-:|-|-|
|Mutable default argument|Bug / maintainability|10|`equipment\_list=\[]` reuses the same list object across calls if it is modified.|Use `None` as the default and create a list inside the function.|
|Broad exception handler|Reliability|25–30|Bare `except` hides unrelated bugs and silently ignores failed cancellation.|Look up the reservation explicitly and return `False` when it does not exist.|
|Shell command injection risk|Security|40|`os.system("cat " + file)` builds a shell command from a parameter that may contain shell metacharacters.|Avoid shell execution; use Python file APIs and a logger.|
|Unclosed file handles|Reliability / resource management|34–38|Files are opened and closed manually, and the log file is not closed at all.|Use `with open(...)` context managers and specify UTF-8 encoding.|
|Missing input/type validation|Bug|14–21, 45–47|Unknown equipment can raise `KeyError`, equipment counts may become negative, and an integer slot fails later when split.|Validate equipment availability and slot format at function boundaries.|
|Invalid time slot in demonstration|Bug|46|The starter calls `slot\_hours` on `"14-12"`, an end time earlier than the start.|Use a valid slot and explicitly reject invalid intervals.|
|Program runs on import|Maintainability / testability|58|Calling `main()` unconditionally causes prompting and file writes when another module imports the script.|Guard execution using `if \_\_name\_\_ == "\_\_main\_\_":`.|
|Inconsistent naming and formatting|Style|Multiple|`logConflicts`, single-letter variables, and long/poorly spaced code reduce readability.|Use snake\_case, descriptive names, and apply Flake8 formatting expectations.|



