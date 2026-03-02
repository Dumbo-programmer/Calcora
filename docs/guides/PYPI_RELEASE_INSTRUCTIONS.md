# PyPI Release Instructions for Calcora v0.3.0

## Prerequisites

1. **PyPI Account**: You need a PyPI account with access to the `calcora` project
2. **GitHub Repository Access**: Admin access to https://github.com/Dumbo-programmer/Calcora

## Step 1: Set Up PyPI Trusted Publishing

This only needs to be done once per repository:

1. Go to https://pypi.org/manage/account/publishing/
2. Click "Add a new pending publisher"  
3. Fill in the form:
   - **PyPI Project Name**: `calcora`
   - **Owner**: `Dumbo-programmer`
   - **Repository name**: `Calcora`
   - **Workflow name**: `publish-pypi.yml`
   - **Environment name**: (leave blank)
4. Click "Add"

**Note**: PyPI will show this as a "pending publisher" until the first successful publish. After the first release, it becomes an active publisher.

## Step 2: Create GitHub Release

### Option A: Via GitHub Web UI (Recommended)

1. Go to https://github.com/Dumbo-programmer/Calcora/releases/new
2. Fill in the form:
   - **Tag**: `v0.3.0` (create new tag from: main)
   - **Release title**: `v0.3.0 - Production Release`
   - **Description**: (Copy from below)
   
```markdown
# v0.3.0 - Production Release

**Date**: March 2, 2026

## 🎉 Highlights

- ✅ **73/73 tests passing** (100% pass rate)
- ✅ **Python 3.10+ support** (previously 3.11+)
- ✅ **LaTeX export** for homework and teaching
- ✅ **Complete documentation** with examples gallery
- ✅ **Mobile-responsive** website

## 🚀 New Features

### LaTeX Export
Students can now export step-by-step solutions as LaTeX:
```bash
curl 'localhost:5000/differentiate?expr=x**2&format=latex'
```
Returns properly formatted LaTeX markup ready for homework assignments!

### Enhanced Documentation
- **Common Examples Library**: Physics, economics, calculus problems
- **Error Troubleshooting Guide**: Clear fixes for common issues
- **Mobile-optimized** docs and demo pages

### Infrastructure Improvements
- **CI/CD**: Tests on 9 platform combinations (3 OS × 3 Python versions)
- **Coverage**: 54% overall (differentiation: 89%, integration: 73%)
- **Changelog** link added to footer for transparency

## 📦 Installation

```bash
pip install calcora
```

Or download the [Windows Desktop App](https://github.com/Dumbo-programmer/Calcora/releases/latest/download/Calcora.exe)

## 📚 Documentation

- **[User Guide](https://calcoralive.netlify.app/docs-user-guide)** - Getting started with examples
- **[API Reference](https://calcoralive.netlify.app/docs-api)** - Complete endpoint documentation
- **[Live Demo](https://calcoralive.netlify.app/demo)** - Try it in your browser

## 🔧 What's Changed

### Features
- Add LaTeX renderer for mathematical expressions (@d0782ee)
- Common examples library with physics/economics problems (@050f62c)
- Error messages and troubleshooting section (@050f62c)

### Infrastructure  
- Lower Python requirement to >=3.10 for broader compatibility (@46cddf2)
- Add missing 'test' optional dependency for CI (@c4cf62d)
- Update README for v0.3.0 with current stats (@13e1779)
- Add mathematical symbols (∫, ∂) to feature icons (@59735cc)

### Testing
- 73/73 tests passing (100% pass rate)
- Added LaTeX renderer test suite (4 tests)
- CI tests on Python 3.10, 3.11, 3.12

## 🙏 Contributors

Thank you to everyone who contributed to this release!

**Full Changelog**: https://github.com/Dumbo-programmer/Calcora/blob/main/CHANGELOG.md
```

3. Click "Publish release"

### Option B: Via Command Line

```bash
# Create and push tag
git tag v0.3.0
git push origin v0.3.0

# Then create release via GitHub API or web UI
```

## Step 3: Monitor Workflow

1. Go to https://github.com/Dumbo-programmer/Calcora/actions
2. Watch the "Publish to PyPI" workflow run
3. Expected duration: 2-3 minutes
4. Check for green checkmark ✅

## Step 4: Verify PyPI Publication

After the workflow succeeds:

1. Visit https://pypi.org/project/calcora/
2. Verify version shows **0.3.0**
3. Test installation:
   ```bash
   pip install --upgrade calcora
   python -c "import calcora; print(calcora.__version__)"
   # Should output: 0.3.0
   ```

## Troubleshooting

### "Pending publisher not found"
- Make sure you completed Step 1 (PyPI trusted publishing setup)
- Verify the workflow name matches exactly: `publish-pypi.yml`

### "Permission denied"
- Workflow needs `id-token: write` permission (already configured)
- Check that PyPI project name matches: `calcora`

### "Build failed"
- Check pyproject.toml syntax
- Ensure all dependencies are specified correctly
- Review GitHub Actions logs for details

## Post-Release Checklist

- [ ] PyPI page shows v0.3.0
- [ ] `pip install calcora` works globally
- [ ] Update website with PyPI installation instructions
- [ ] Announce on GitHub Discussions / social media
- [ ] Update ROADMAP.md to mark v0.3.0 as completed

## Next Steps

After successful v0.3.0 release:
1. Monitor for any installation issues
2. Respond to PyPI project page questions
3. Begin work on v0.4.0 features (LaTeX improvements, PyWebView)

## Reference Links

- **PyPI Trusted Publishing Docs**: https://docs.pypi.org/trusted-publishers/
- **GitHub Actions PyPI Publish**: https://github.com/marketplace/actions/pypi-publish
- **Calcora Workflows**: https://github.com/Dumbo-programmer/Calcora/tree/main/.github/workflows
