# Reflection

## 1. Which issues were the easiest to fix and which were the hardest?
Easiest: Flake8 formatting issues (spacing, continuation-line alignment, the
inline-comment gap) and Pylint docstring and naming warnings. They were
mechanical and did not change behaviour. Hardest: the Bandit findings.
Replacing `os.system` with `subprocess.run` and an argument list meant
understanding command injection, and deciding which low-severity findings
were real risks and which were not.

## 2. Did the tools report any false positives?
Partly. `random.choice` (B311) is flagged as unsafe for security use, but
picking a bonus question is not security-sensitive. I switched to
`secrets.choice` anyway. Switching to `subprocess` produced new low-severity
warnings (B404, B603, B607) that I suppressed with `# nosec` and a comment,
because the call uses a fixed argument list with no shell. The "hardcoded
password" warning was also only a demo value, but moving it to an
environment variable is still better practice.

## 3. How would you integrate static analysis into a real workflow?
Run Flake8, Pylint and Bandit as pre-commit hooks so problems are caught
before each commit, and again in a CI pipeline (for example GitHub Actions)
so a pull request cannot be merged if the checks fail. Pin a minimum Pylint
score and fail the build on medium or high Bandit findings.

## 4. What tangible improvements did I see in the code?
Security: no shell command built from strings, no weak MD5 hash, no secret
in source. Robustness: the mutable default argument bug (`penalties={}`
shared between calls) is fixed. Readability: snake_case names, docstrings,
`enumerate`, early returns and PEP 8 formatting. The program's output is
unchanged and the Pylint score rose from the starting score to above 9.5.
