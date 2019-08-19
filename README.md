You need to have python 3.2 above


`brew install pre-commit`

`pre-commit install -t pre-commit`

`pre-commit install -t commit-msg`

Make sure you repository has a file named `.pre-commit-config.yaml` containing:

`
repos:
- repo: https://github.com/pre-commit/pre-commit-hooks
  rev: v2.3.0
  hooks:
  - id: check-yaml
- repo: /Users/hossein/workspaces/hooks
  rev: c950754ec6c772641957616f1126642ec67c4a9f
  hooks:
  - id: commit-message-check
    stages: ['commit-msg']
`