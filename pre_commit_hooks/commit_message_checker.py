import re
import sys
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
    if git_branch_name == 'master':
        print('You are not allowed to commit/push to the master branch!')
        sys.exit(1)
    jira_issue_key = extract_jira_issue_key(git_branch_name)
    if not jira_issue_key:
        exit_with_error(
            f'Commit aborted! To continue, please rename your branch to a Jira '
            f'issue key with:\n$ git branch -m {git_branch_name} <KEY-123>')

    # Read the commit message.
    commit_msg_filepath = sys.argv[1]
    with open(commit_msg_filepath, 'r') as f:
        commit_msg = f.read()


    # Split the commit into a subject and body and apply some light formatting.
    commit_elements = commit_msg.split('\n', maxsplit=1)
    commit_subject = commit_elements[0].strip()
    commit_subject.capitalize()
    commit_subject = re.sub(r'\.+$', '', commit_subject)
    commit_body = None if len(commit_elements) == 1 else commit_elements[1]
    commit_body = commit_body.strip()
    # Build the new commit message:
    # 1. If there is a body, turn it into a comment on the issue.
    if '#comment' not in commit_msg and commit_body:
        commit_body = f'{jira_issue_key} #comment {commit_body}'
    # 2. Add the time worked to the Work Log in the commit body.
    if '#time' not in commit_msg:
        exit_with_error(f'You forgot to register the hours you worked on this commit.'
                        f'Use the #time command from JIRA smart commits to do so.')
    # 3. Make sure the subject starts with a Jira issue key.
    if not extract_jira_issue_key(commit_subject):
        commit_subject = f'{jira_issue_key} {commit_subject}'
    # Assemble the commit message as the subject plus body.
    commit_msg = f'{commit_subject}\n\n{commit_body}'
    # Override commit message.
    with open(commit_msg_filepath, 'w') as f:
        f.write(commit_msg)


if __name__ == '__main__':
    main()