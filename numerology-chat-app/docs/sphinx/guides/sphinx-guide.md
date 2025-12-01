# Sphinx Documentation Generation

This guide explains how to build and maintain the Sphinx documentation for the Numerology Chat Application.

## 📚 What is Sphinx?

Sphinx is a powerful documentation generation tool that creates beautiful, searchable documentation from reStructuredText and Markdown files. Our project uses:

- **ReadTheDocs Theme**: Professional, mobile-responsive design
- **Auto-documentation**: Automatically generates API docs from code
- **Cross-references**: Links between different documentation sections
- **Search functionality**: Built-in full-text search
- **Multiple output formats**: HTML, PDF, EPUB

## 🛠️ Installation & Setup

### Prerequisites

Make sure you have Python and the required packages installed:

```bash
pip install sphinx sphinx-rtd-theme sphinx-autodoc-typehints
```

### Project Structure

Our documentation is organized in `docs/sphinx/`:

```
docs/sphinx/
├── conf.py              # Sphinx configuration
├── index.rst            # Main documentation page
├── _static/
│   └── custom.css       # Custom styling
├── _templates/          # Custom templates (optional)
├── api/
│   ├── index.md         # API documentation index
│   ├── endpoints.md     # API endpoints reference
│   ├── models.md        # Data models documentation
│   └── examples.md      # Usage examples
├── guides/
│   ├── quickstart.md    # Quick start guide
│   ├── overview.md      # Project overview
│   └── deployment.md    # Deployment guide
└── _build/              # Generated documentation (auto-created)
```

## ⚙️ Configuration Details

### conf.py Explained

Our `conf.py` file configures Sphinx with these key settings:

```python
# Project information
project = 'Numerology Chat App'
copyright = '2025, Numerology Team'
author = 'Numerology Team'
version = '1.0.0'
release = '1.0.0'

# Extensions for enhanced functionality
extensions = [
    'sphinx.ext.autodoc',        # Auto-generate docs from docstrings
    'sphinx.ext.viewcode',       # Include source code links
    'sphinx.ext.napoleon',       # Support Google/NumPy docstring styles
    'sphinx_rtd_theme',          # ReadTheDocs theme
    'myst_parser',               # Markdown support
]

# Theme configuration
html_theme = 'sphinx_rtd_theme'
html_theme_options = {
    'canonical_url': '',
    'analytics_id': '',
    'logo_only': False,
    'display_version': True,
    'prev_next_buttons_location': 'bottom',
    'style_external_links': False,
    'collapse_navigation': True,
    'sticky_navigation': True,
    'navigation_depth': 4,
    'includehidden': True,
    'titles_only': False
}
```

### Custom CSS Styling

Our custom CSS (`_static/custom.css`) provides:

- **Color scheme**: Consistent with the app's branding
- **Typography**: Enhanced readability
- **API styling**: Special formatting for endpoints and models
- **Responsive design**: Mobile-friendly layout
- **Code highlighting**: Improved syntax highlighting

## 🚀 Building Documentation

### Local Development

1. **Navigate to the docs directory:**
   ```bash
   cd docs/sphinx
   ```

2. **Build HTML documentation:**
   ```bash
   sphinx-build -b html . _build/html
   ```

3. **Serve locally for testing:**
   ```bash
   # Python 3
   python -m http.server 8080 -d _build/html
   
   # Then open: http://localhost:8080
   ```

4. **Auto-rebuild during development:**
   ```bash
   # Install sphinx-autobuild
   pip install sphinx-autobuild
   
   # Auto-rebuild and serve
   sphinx-autobuild . _build/html --port 8080
   ```

### Production Builds

For production deployment:

```bash
# Clean previous builds
rm -rf _build/

# Build with enhanced settings
sphinx-build -b html -W --keep-going . _build/html

# Build PDF (requires LaTeX)
sphinx-build -b latex . _build/latex
cd _build/latex && make
```

## 📖 Writing Documentation

### File Formats

We support both reStructuredText (`.rst`) and Markdown (`.md`) files:

**reStructuredText example (`index.rst`):**
```rst
Numerology Chat Application
===========================

Welcome to the comprehensive documentation for the Numerology Chat Application.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   guides/quickstart
   guides/overview
   api/index

Quick Links
-----------

* :doc:`guides/quickstart` - Get started in 5 minutes
* :doc:`api/endpoints` - Complete API reference
* :doc:`guides/deployment` - Deploy to production
```

**Markdown example:**
```markdown
# Quick Start Guide

This guide will help you get the Numerology Chat Application up and running.

## Prerequisites

- Python 3.9+
- Node.js 16+
- Docker (optional)

## Installation Steps

1. Clone the repository
2. Install dependencies
3. Start the services
```

### Documentation Standards

Follow these conventions for consistent documentation:

#### Section Headers

Use consistent heading levels:
```markdown
# Main Title (H1) - One per page
## Major Sections (H2)
### Subsections (H3)
#### Details (H4)
```

#### Code Examples

Always include language specification:
````markdown
```python
# Python code example
def calculate_life_path(birth_date):
    return sum(digits)
```

```bash
# Shell commands
pip install requirements.txt
```

```json
{
  "example": "JSON data"
}
```
````

#### API Documentation

Use consistent formatting for endpoints:
```markdown
### Calculate Numerology Profile
<div class="api-endpoint">
<span class="method post">POST</span> <code>/api/v1/calculate</code>
</div>

**Request Body:**
\```json
{
  "full_name": "John Smith",
  "birth_date": "1990-01-15"
}
\```

**Response:**
\```json
{
  "status": "success",
  "data": {...}
}
\```
```

## 🔧 Advanced Features

### Auto-documentation

Generate API documentation from Python docstrings:

```python
# In your Python module
def calculate_life_path(birth_date: str) -> int:
    """Calculate the life path number from birth date.
    
    Args:
        birth_date: Birth date in YYYY-MM-DD format
        
    Returns:
        Life path number (1-9, 11, 22, 33)
        
    Example:
        >>> calculate_life_path("1990-01-15")
        5
    """
    # Implementation here
```

Then in your `.rst` file:
```rst
.. automodule:: your_module
   :members:
```

### Cross-references

Link between documents:
```rst
See :doc:`api/endpoints` for details.
See :ref:`installation-section` for setup.
```

### Custom Directives

Add warning boxes and notes:
```rst
.. warning::
   This feature is experimental.

.. note::
   Remember to restart the service.

.. tip::
   Use environment variables for configuration.
```

## 🎨 Customization

### Theme Customization

Modify `_static/custom.css` for visual changes:

```css
/* Custom colors */
.wy-side-nav-search {
    background-color: #6366f1;
}

/* API endpoint styling */
.api-endpoint {
    background: #f8fafc;
    border-left: 4px solid #6366f1;
    padding: 1rem;
    margin: 1rem 0;
}

.method.post {
    background: #dc2626;
    color: white;
    padding: 0.25rem 0.5rem;
    border-radius: 4px;
    font-weight: bold;
}
```

### Custom Templates

Create templates in `_templates/` directory:

```html
<!-- _templates/page.html -->
{% extends "!page.html" %}

{% block extrahead %}
    <meta name="description" content="{{ meta.description or 'Numerology Chat App Documentation' }}">
{% endblock %}
```

## 📊 Analytics & Monitoring

### Google Analytics

Add analytics to `conf.py`:
```python
html_theme_options = {
    'analytics_id': 'UA-XXXXXXX-1',
    # other options...
}
```

### Search Analytics

Monitor search usage:
```javascript
// Custom search tracking
document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.querySelector('[name="q"]');
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            // Track search queries
            console.log('Search:', this.value);
        });
    }
});
```

## 🚀 Deployment Options

### Static Hosting

Deploy to static hosting services:

1. **Netlify:**
   ```bash
   # Build command
   sphinx-build -b html docs/sphinx docs/sphinx/_build/html
   
   # Publish directory
   docs/sphinx/_build/html
   ```

2. **GitHub Pages:**
   ```yaml
   # .github/workflows/docs.yml
   name: Documentation
   on:
     push:
       branches: [main]
   jobs:
     docs:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v2
         - name: Setup Python
           uses: actions/setup-python@v2
         - name: Install dependencies
           run: pip install sphinx sphinx-rtd-theme myst-parser
         - name: Build docs
           run: sphinx-build -b html docs/sphinx docs/sphinx/_build/html
         - name: Deploy
           uses: peaceiris/actions-gh-pages@v3
           with:
             github_token: ${{ secrets.GITHUB_TOKEN }}
             publish_dir: docs/sphinx/_build/html
   ```

3. **ReadTheDocs:**
   - Connect your GitHub repository
   - Add `.readthedocs.yaml` configuration
   - Automatic builds on commits

### Docker Deployment

Create a documentation container:

```dockerfile
# Dockerfile.docs
FROM python:3.9-slim

WORKDIR /docs
COPY docs/sphinx/ .
COPY requirements-docs.txt .

RUN pip install -r requirements-docs.txt
RUN sphinx-build -b html . _build/html

FROM nginx:alpine
COPY --from=0 /docs/_build/html /usr/share/nginx/html
EXPOSE 80
```

## 🔍 Troubleshooting

### Common Issues

**Build errors:**
```bash
# Check for syntax errors
sphinx-build -W -b html . _build/html

# Verbose output
sphinx-build -v -b html . _build/html
```

**Missing modules:**
```python
# In conf.py, mock missing imports
autodoc_mock_imports = ['fastapi', 'uvicorn', 'pydantic']
```

**Theme issues:**
```python
# Ensure theme is installed
pip install sphinx-rtd-theme

# Check theme path
html_theme_path = ['_themes']
```

### Performance Optimization

For large documentation sets:
```python
# In conf.py
html_copy_source = False
html_show_sourcelink = False
html_use_smartypants = False
```

## 📈 Maintenance

### Regular Tasks

1. **Update dependencies:**
   ```bash
   pip install --upgrade sphinx sphinx-rtd-theme
   ```

2. **Check for broken links:**
   ```bash
   sphinx-build -b linkcheck . _build/linkcheck
   ```

3. **Update version numbers:**
   Update `conf.py` when releasing new versions

4. **Review and update content:**
   - Keep API docs synchronized with code changes
   - Update examples and screenshots
   - Review and improve unclear sections

### Automation

Set up automated documentation updates:

```bash
#!/bin/bash
# scripts/update-docs.sh

# Pull latest changes
git pull origin main

# Install/update dependencies
pip install -r requirements-docs.txt

# Build documentation
cd docs/sphinx
sphinx-build -b html . _build/html

# Deploy (customize based on your deployment method)
rsync -av _build/html/ user@server:/var/www/docs/
```

This comprehensive Sphinx documentation setup provides a professional, maintainable documentation system for your Numerology Chat Application.