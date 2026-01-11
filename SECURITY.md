# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability in Calcora, please report it by opening a GitHub issue with the label "security". For sensitive security issues, you can contact the maintainers directly through GitHub.

### What to include in your report:

- Description of the vulnerability
- Steps to reproduce the issue
- Potential impact
- Suggested fix (if you have one)

### What to expect:

- **Response time**: We aim to acknowledge security reports within 48 hours
- **Updates**: You'll receive updates on the status of your report
- **Resolution**: Critical security issues will be prioritized and addressed in patch releases

## Security Considerations

### Local Execution

Calcora is designed to run locally on your machine. It does not send data to external servers or collect telemetry.

### Expression Parsing

Calcora uses SymPy for mathematical expression parsing. While SymPy is generally safe, be cautious when parsing expressions from untrusted sources, as complex expressions could potentially consume significant computational resources.

### Plugin System

Third-party plugins should be reviewed before installation, as they execute with the same privileges as the Calcora application.

## Best Practices

- Only download Calcora from official sources (GitHub releases, PyPI)
- Keep your Python environment and dependencies up to date
- Review third-party plugins before installation
- Run Calcora in isolated environments when processing untrusted input
