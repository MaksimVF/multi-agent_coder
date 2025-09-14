
---
name: github
type: knowledge
version: 1.0.0
agent: DeveloperAgent
triggers:
- github
- git
- pull request
- pr
- repository
- repo
- branch
- commit
- push
- clone
---

You have access to an environment variable, `GITHUB_TOKEN`, which allows you to interact with
the GitHub API.

<IMPORTANT>
You can use `curl` with the `GITHUB_TOKEN` to interact with GitHub's API.
ALWAYS use the GitHub API for operations instead of a web browser.
</IMPORTANT>

Here are some instructions for pushing, but ONLY do this if the user asks you to:
* NEVER push directly to the `main` or `master` branch
* Git config (username and email) is pre-set. Do not modify.
* Use the `create_pr` tool to create a pull request, if you haven't already
* Use the main branch as the base branch, unless the user requests otherwise
* After opening or updating a pull request, send the user a short message with a link to the pull request.

Example GitHub API usage:
```bash
# Get repository info
curl -H "Authorization: token ${GITHUB_TOKEN}" https://api.github.com/repos/owner/repo

# Create a pull request
curl -X POST -H "Authorization: token ${GITHUB_TOKEN}" \
    -d '{"title":"My PR","head":"my-branch","base":"main","body":"Description"}' \
    https://api.github.com/repos/owner/repo/pulls
```

