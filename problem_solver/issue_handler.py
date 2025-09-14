


"""
Issue Handler for Problem Solver

This module handles integration with issue tracking systems like GitHub, GitLab, and Bitbucket.
"""

import os
import httpx
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from abc import ABC, abstractmethod

@dataclass
class Issue:
    """Represents an issue from an issue tracker"""
    platform: str
    owner: str
    repo: str
    number: int
    title: str
    body: str
    comments: Optional[List[str]] = None
    labels: Optional[List[str]] = None
    assignees: Optional[List[str]] = None

class IssueHandlerInterface(ABC):
    """Interface for issue handlers"""

    @abstractmethod
    def get_issue(self, issue_number: int) -> Issue:
        pass

    @abstractmethod
    def get_issues(self, labels: Optional[List[str]] = None) -> List[Issue]:
        pass

    @abstractmethod
    def create_comment(self, issue_number: int, comment: str) -> bool:
        pass

    @abstractmethod
    def update_issue(self, issue_number: int, **update_data) -> bool:
        pass

class GitHubIssueHandler(IssueHandlerInterface):
    """Handles GitHub issues"""

    def __init__(self, owner: str, repo: str, token: str, base_url: str = 'https://api.github.com'):
        self.owner = owner
        self.repo = repo
        self.token = token
        self.base_url = base_url
        self.headers = {
            'Authorization': f'token {token}',
            'Accept': 'application/vnd.github.v3+json',
        }

    def get_issue(self, issue_number: int) -> Issue:
        """Get a single GitHub issue"""
        url = f'{self.base_url}/repos/{self.owner}/{self.repo}/issues/{issue_number}'
        response = httpx.get(url, headers=self.headers)
        response.raise_for_status()

        issue_data = response.json()
        comments = self._get_issue_comments(issue_number)

        return Issue(
            platform='github',
            owner=self.owner,
            repo=self.repo,
            number=issue_data['number'],
            title=issue_data['title'],
            body=issue_data['body'],
            comments=comments,
            labels=issue_data.get('labels', []),
            assignees=issue_data.get('assignees', [])
        )

    def get_issues(self, labels: Optional[List[str]] = None) -> List[Issue]:
        """Get issues from GitHub repository"""
        params = {'state': 'open', 'per_page': 100}

        if labels:
            params['labels'] = ','.join(labels)

        url = f'{self.base_url}/repos/{self.owner}/{self.repo}/issues'
        response = httpx.get(url, headers=self.headers, params=params)
        response.raise_for_status()

        issues = []
        for issue_data in response.json():
            comments = self._get_issue_comments(issue_data['number'])
            issues.append(Issue(
                platform='github',
                owner=self.owner,
                repo=self.repo,
                number=issue_data['number'],
                title=issue_data['title'],
                body=issue_data['body'],
                comments=comments,
                labels=issue_data.get('labels', []),
                assignees=issue_data.get('assignees', [])
            ))

        return issues

    def create_comment(self, issue_number: int, comment: str) -> bool:
        """Create a comment on a GitHub issue"""
        url = f'{self.base_url}/repos/{self.owner}/{self.repo}/issues/{issue_number}/comments'
        data = {'body': comment}

        response = httpx.post(url, headers=self.headers, json=data)
        return response.status_code == 201

    def update_issue(self, issue_number: int, **update_data) -> bool:
        """Update a GitHub issue"""
        url = f'{self.base_url}/repos/{self.owner}/{self.repo}/issues/{issue_number}'
        response = httpx.patch(url, headers=self.headers, json=update_data)
        return response.status_code == 200

    def _get_issue_comments(self, issue_number: int) -> List[str]:
        """Get comments for a GitHub issue"""
        url = f'{self.base_url}/repos/{self.owner}/{self.repo}/issues/{issue_number}/comments'
        response = httpx.get(url, headers=self.headers)
        response.raise_for_status()

        return [comment['body'] for comment in response.json()]

class GitLabIssueHandler(IssueHandlerInterface):
    """Handles GitLab issues"""

    def __init__(self, owner: str, repo: str, token: str, base_url: str = 'https://gitlab.com'):
        self.owner = owner
        self.repo = repo
        self.token = token
        self.base_url = base_url
        self.headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
        }

    def get_issue(self, issue_number: int) -> Issue:
        """Get a single GitLab issue"""
        url = f'{self.base_url}/api/v4/projects/{self.owner}%2F{self.repo}/issues/{issue_number}'
        response = httpx.get(url, headers=self.headers)
        response.raise_for_status()

        issue_data = response.json()
        comments = self._get_issue_comments(issue_number)

        return Issue(
            platform='gitlab',
            owner=self.owner,
            repo=self.repo,
            number=issue_data['iid'],
            title=issue_data['title'],
            body=issue_data['description'],
            comments=comments,
            labels=issue_data.get('labels', []),
            assignees=issue_data.get('assignees', [])
        )

    def get_issues(self, labels: Optional[List[str]] = None) -> List[Issue]:
        """Get issues from GitLab repository"""
        params = {'state': 'opened', 'per_page': 100}

        if labels:
            params['labels'] = ','.join(labels)

        url = f'{self.base_url}/api/v4/projects/{self.owner}%2F{self.repo}/issues'
        response = httpx.get(url, headers=self.headers, params=params)
        response.raise_for_status()

        issues = []
        for issue_data in response.json():
            comments = self._get_issue_comments(issue_data['iid'])
            issues.append(Issue(
                platform='gitlab',
                owner=self.owner,
                repo=self.repo,
                number=issue_data['iid'],
                title=issue_data['title'],
                body=issue_data['description'],
                comments=comments,
                labels=issue_data.get('labels', []),
                assignees=issue_data.get('assignees', [])
            ))

        return issues

    def create_comment(self, issue_number: int, comment: str) -> bool:
        """Create a comment on a GitLab issue"""
        url = f'{self.base_url}/api/v4/projects/{self.owner}%2F{self.repo}/issues/{issue_number}/notes'
        data = {'body': comment}

        response = httpx.post(url, headers=self.headers, json=data)
        return response.status_code == 201

    def update_issue(self, issue_number: int, **update_data) -> bool:
        """Update a GitLab issue"""
        url = f'{self.base_url}/api/v4/projects/{self.owner}%2F{self.repo}/issues/{issue_number}'
        response = httpx.put(url, headers=self.headers, json=update_data)
        return response.status_code == 200

    def _get_issue_comments(self, issue_number: int) -> List[str]:
        """Get comments for a GitLab issue"""
        url = f'{self.base_url}/api/v4/projects/{self.owner}%2F{self.repo}/issues/{issue_number}/notes'
        response = httpx.get(url, headers=self.headers)
        response.raise_for_status()

        return [note['body'] for note in response.json()]

class IssueHandlerFactory:
    """Factory for creating issue handlers"""

    @staticmethod
    def create_handler(platform: str, owner: str, repo: str, token: str, **kwargs) -> IssueHandlerInterface:
        """Create an issue handler based on the platform"""
        if platform.lower() == 'github':
            return GitHubIssueHandler(owner, repo, token, **kwargs)
        elif platform.lower() == 'gitlab':
            return GitLabIssueHandler(owner, repo, token, **kwargs)
        else:
            raise ValueError(f"Unsupported platform: {platform}")

