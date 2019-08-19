import datetime
import re
import sys
from math import floor
from subprocess import check_output
from typing import Optional


def exit_with_error(message: str) -> None:
    print(message)
    sys.exit(1)


def run_command(command: str) -> str:
    return check_output(command.split()).decode('utf-8').strip()


def current_git_branch_name() -> str:
    return run_command('git symbolic-ref --short HEAD')


def extract_jira_issue_key(message: str) -> Optional[str]:
    project_key, issue_number = r'[A-Z]{2,}', r'[0-9]+'
    match = re.search(f'{project_key}-{issue_number}', message)
    return match and match.group(0)


def main():
    # Verify that the branch name is a Jira issue key.
    git_branch_name = current_git_branch_name()
    jira_issue_key = extract_jira_issue_key(git_branch_name)
    if not jira_issue_key:
        exit_with_error(
            f'Commit aborted! To continue, please rename your branch to a Jira '
            f'issue key with:\n$ git branch -m {git_branch_name} <KEY-123>')

if __name__ == '__main__':
    main()