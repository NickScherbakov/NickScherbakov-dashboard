# NickScherbakov-dashboard
GitHub Profile Dashboard - Repository Market Analytics

This project automatically generates and updates a dashboard with analytics from popular GitHub repositories using GitHub Actions. It supports both GitHub-hosted and self-hosted runners.

## Features

- Automated data collection from GitHub API
- Chart generation with matplotlib and seaborn
- Scheduled updates every 6 hours
- Self-hosted runner support
- Manual workflow triggers

## Self-Hosted Runners

This repository supports self-hosted GitHub Actions runners for more control over the execution environment.

### Quick Setup
```bash
# Run the setup script
./setup-runner.sh
```

### Manual Setup
Visit the [runner settings page](https://github.com/NickScherbakov/NickScherbakov-dashboard/settings/actions/runners/new) to add a new self-hosted runner.

For detailed instructions, see [docs/SELF_HOSTED_RUNNERS.md](docs/SELF_HOSTED_RUNNERS.md).

## Contributors

- [NickScherbakov](https://github.com/NickScherbakov) - Main developer
- GitHub Copilot - AI coding assistant and co-author
