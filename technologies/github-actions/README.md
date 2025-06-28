# ⚡ GitHub Actions CI/CD - Industrial IoT Stack

**GitHub Actions automates** our development workflow with continuous integration, deployment, and Claude Code integration for the industrial IoT stack.

## 🚀 Quick Start for Claude Instances

**New to GitHub Actions integration?** Start here:
1. `setup-guides/GITHUB_AUTH_SETUP.md` - Authentication configuration
2. `setup-guides/GITHUB_ACTIONS_CLAUDE_INTEGRATION.md` - Claude integration
3. `claude-code-action-fork/` - Custom Claude Code action
4. `setup-guides/CT-030_GITHUB_ACTIONS_COMPLETION_GUIDE.md` - Complete setup

## 🎯 What GitHub Actions Does in Our Stack

### Core Capabilities
- **Automated Testing**: Run test suites on every commit
- **Deployment Automation**: Deploy to production environments
- **Claude Code Integration**: AI-powered code assistance in CI/CD
- **Repository Management**: Automated maintenance tasks

### Key Workflows
- **Claude Code Action**: AI assistance for pull requests
- **Industrial IoT Testing**: Automated stack component testing
- **Documentation Updates**: Auto-generate documentation
- **Security Scanning**: Vulnerability detection and alerts

## 🏭 Production Features

- **Matrix Builds**: Test across multiple environments
- **Secure Secrets**: Encrypted environment variables
- **Status Checks**: Required checks for branch protection
- **Notifications**: Discord integration for build status
- **Artifact Management**: Build output storage and distribution

## 📂 Directory Structure

```
technologies/github-actions/
├── README.md                    # You are here
├── setup-guides/                # Installation and configuration
└── claude-code-action-fork/     # Custom Claude Code action
```

## 🔧 Essential Workflows

```yaml
# Basic CI workflow
name: Industrial IoT Stack CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run Tests
        run: ./scripts/run_tests.sh
```

## 🔗 Related Technologies

- **GitHub**: Repository hosting and version control
- **Claude Code**: AI-powered development assistance
- **Docker**: Containerized build environments
- **Discord**: Build status notifications

---
*Files Organized: 8+ | Technology Status: ✅ CI/CD Ready*