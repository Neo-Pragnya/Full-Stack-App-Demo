#!/bin/bash

# Documentation Build Script for Numerology Chat App
# This script builds the Sphinx documentation with proper error handling and optimization

set -e  # Exit on any error

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
DOCS_DIR="docs/sphinx"
BUILD_DIR="_build"
OUTPUT_DIR="${BUILD_DIR}/html"
PORT=8080

# Function to print colored output
print_message() {
    local color=$1
    local message=$2
    echo -e "${color}${message}${NC}"
}

# Function to check dependencies
check_dependencies() {
    print_message $BLUE "🔍 Checking dependencies..."
    
    # Check Python
    if ! command -v python3 &> /dev/null; then
        print_message $RED "❌ Python 3 is not installed"
        exit 1
    fi
    
    # Check required packages
    local packages=("sphinx" "sphinx-rtd-theme" "myst-parser")
    for package in "${packages[@]}"; do
        if ! python3 -c "import ${package//-/_}" &> /dev/null; then
            print_message $YELLOW "⚠️  Installing missing package: $package"
            pip3 install "$package"
        fi
    done
    
    print_message $GREEN "✅ All dependencies satisfied"
}

# Function to clean previous builds
clean_build() {
    print_message $BLUE "🧹 Cleaning previous builds..."
    
    if [ -d "$DOCS_DIR/$BUILD_DIR" ]; then
        rm -rf "$DOCS_DIR/$BUILD_DIR"
        print_message $GREEN "✅ Cleaned $BUILD_DIR directory"
    else
        print_message $YELLOW "ℹ️  No previous build found"
    fi
}

# Function to build documentation
build_docs() {
    local build_type=${1:-html}
    
    print_message $BLUE "📚 Building $build_type documentation..."
    
    cd "$DOCS_DIR"
    
    # Build with warnings as errors and keep going on errors
    if sphinx-build -b "$build_type" -W --keep-going . "$BUILD_DIR/$build_type"; then
        print_message $GREEN "✅ Documentation built successfully"
        
        # Show build statistics
        local html_files=$(find "$BUILD_DIR/$build_type" -name "*.html" | wc -l)
        local total_size=$(du -sh "$BUILD_DIR/$build_type" | cut -f1)
        
        print_message $BLUE "📊 Build Statistics:"
        echo "   📄 HTML files: $html_files"
        echo "   💾 Total size: $total_size"
        echo "   📁 Output location: $DOCS_DIR/$BUILD_DIR/$build_type"
    else
        print_message $RED "❌ Documentation build failed"
        cd - > /dev/null
        exit 1
    fi
    
    cd - > /dev/null
}

# Function to serve documentation locally
serve_docs() {
    local serve_port=${1:-$PORT}
    
    print_message $BLUE "🌐 Starting local documentation server..."
    
    if [ ! -d "$DOCS_DIR/$OUTPUT_DIR" ]; then
        print_message $RED "❌ No built documentation found. Run build first."
        exit 1
    fi
    
    cd "$DOCS_DIR/$OUTPUT_DIR"
    
    print_message $GREEN "🚀 Documentation server started!"
    print_message $BLUE "📍 URL: http://localhost:$serve_port"
    print_message $YELLOW "Press Ctrl+C to stop the server"
    
    python3 -m http.server "$serve_port"
}

# Function to watch and auto-rebuild
watch_docs() {
    print_message $BLUE "👀 Starting auto-rebuild watcher..."
    
    # Check if sphinx-autobuild is installed
    if ! command -v sphinx-autobuild &> /dev/null; then
        print_message $YELLOW "⚠️  Installing sphinx-autobuild..."
        pip3 install sphinx-autobuild
    fi
    
    cd "$DOCS_DIR"
    
    print_message $GREEN "🚀 Auto-rebuild server started!"
    print_message $BLUE "📍 URL: http://localhost:$PORT"
    print_message $YELLOW "📝 Watching for file changes..."
    print_message $YELLOW "Press Ctrl+C to stop watching"
    
    sphinx-autobuild . "$BUILD_DIR/html" --port "$PORT" --host 0.0.0.0
}

# Function to check for broken links
check_links() {
    print_message $BLUE "🔗 Checking for broken links..."
    
    cd "$DOCS_DIR"
    
    if sphinx-build -b linkcheck . "$BUILD_DIR/linkcheck"; then
        print_message $GREEN "✅ Link check completed"
        
        # Show link check results
        if [ -f "$BUILD_DIR/linkcheck/output.txt" ]; then
            local broken_links=$(grep -c "broken" "$BUILD_DIR/linkcheck/output.txt" || echo "0")
            local redirects=$(grep -c "redirect" "$BUILD_DIR/linkcheck/output.txt" || echo "0")
            
            print_message $BLUE "🔗 Link Check Results:"
            echo "   ❌ Broken links: $broken_links"
            echo "   ➡️  Redirects: $redirects"
            
            if [ "$broken_links" -gt 0 ]; then
                print_message $YELLOW "⚠️  Check $BUILD_DIR/linkcheck/output.txt for details"
            fi
        fi
    else
        print_message $RED "❌ Link check failed"
        exit 1
    fi
    
    cd - > /dev/null
}

# Function to create documentation archive
create_archive() {
    local archive_name="numerology-docs-$(date +%Y%m%d-%H%M%S).tar.gz"
    
    print_message $BLUE "📦 Creating documentation archive..."
    
    if [ ! -d "$DOCS_DIR/$OUTPUT_DIR" ]; then
        print_message $RED "❌ No built documentation found. Run build first."
        exit 1
    fi
    
    cd "$DOCS_DIR"
    tar -czf "$archive_name" -C "$BUILD_DIR" html
    
    print_message $GREEN "✅ Archive created: $DOCS_DIR/$archive_name"
    
    cd - > /dev/null
}

# Function to deploy documentation
deploy_docs() {
    local deployment_target=${1:-"local"}
    
    print_message $BLUE "🚀 Deploying documentation to $deployment_target..."
    
    case $deployment_target in
        "netlify")
            print_message $BLUE "📤 Deploying to Netlify..."
            # Add Netlify deployment logic here
            print_message $YELLOW "ℹ️  Netlify deployment requires additional setup"
            ;;
        "github-pages")
            print_message $BLUE "📤 Deploying to GitHub Pages..."
            # Add GitHub Pages deployment logic here
            print_message $YELLOW "ℹ️  GitHub Pages deployment requires additional setup"
            ;;
        "docker")
            print_message $BLUE "🐳 Building Docker image..."
            build_docker_image
            ;;
        *)
            print_message $YELLOW "ℹ️  Local deployment - documentation ready for manual copying"
            print_message $BLUE "📁 Source: $DOCS_DIR/$OUTPUT_DIR"
            ;;
    esac
}

# Function to build Docker image for documentation
build_docker_image() {
    local image_name="numerology-docs"
    local tag="latest"
    
    print_message $BLUE "🐳 Building Docker image for documentation..."
    
    # Create temporary Dockerfile
    cat > "$DOCS_DIR/Dockerfile.docs" << EOF
FROM nginx:alpine

# Copy built documentation
COPY $BUILD_DIR/html /usr/share/nginx/html

# Add custom nginx configuration
RUN echo 'server { \
    listen 80; \
    location / { \
        root /usr/share/nginx/html; \
        index index.html; \
        try_files \$uri \$uri/ /index.html; \
    } \
}' > /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
EOF

    cd "$DOCS_DIR"
    
    if docker build -f Dockerfile.docs -t "$image_name:$tag" .; then
        print_message $GREEN "✅ Docker image built successfully"
        print_message $BLUE "🐳 Image: $image_name:$tag"
        print_message $BLUE "🚀 Run with: docker run -p 8080:80 $image_name:$tag"
        
        # Clean up
        rm -f Dockerfile.docs
    else
        print_message $RED "❌ Docker build failed"
        rm -f Dockerfile.docs
        exit 1
    fi
    
    cd - > /dev/null
}

# Function to show help
show_help() {
    cat << EOF
📚 Numerology Chat App - Documentation Build Script

Usage: $0 [COMMAND] [OPTIONS]

Commands:
  build [TYPE]     Build documentation (default: html)
                   Types: html, latex, epub, man
  serve [PORT]     Serve documentation locally (default port: 8080)
  watch           Auto-rebuild and serve with file watching
  check-links     Check for broken links in documentation
  clean           Clean previous builds
  archive         Create documentation archive
  deploy [TARGET] Deploy documentation
                   Targets: local (default), netlify, github-pages, docker
  deps            Check and install dependencies
  help            Show this help message

Examples:
  $0 build              # Build HTML documentation
  $0 build latex        # Build LaTeX/PDF documentation
  $0 serve              # Serve on default port (8080)
  $0 serve 3000         # Serve on port 3000
  $0 watch              # Auto-rebuild and serve
  $0 check-links        # Check for broken links
  $0 deploy docker      # Build Docker image
  $0 clean && $0 build  # Clean and rebuild

Environment Variables:
  DOCS_PORT           Port for serving (default: 8080)
  DOCS_BUILD_TYPE     Default build type (default: html)

Dependencies:
  - Python 3.x
  - sphinx
  - sphinx-rtd-theme
  - myst-parser
  - sphinx-autobuild (for watch mode)

For more information, see: docs/sphinx/guides/sphinx-guide.md
EOF
}

# Main script logic
main() {
    # Check if we're in the right directory
    if [ ! -d "$DOCS_DIR" ]; then
        print_message $RED "❌ Please run this script from the project root directory (docs/sphinx not found)"
        exit 1
    fi
    
    local command=${1:-"help"}
    shift || true  # Remove first argument, ignore error if no args
    
    case $command in
        "build")
            check_dependencies
            build_docs "${1:-html}"
            ;;
        "serve")
            serve_docs "${1:-$PORT}"
            ;;
        "watch")
            check_dependencies
            watch_docs
            ;;
        "check-links"|"links")
            check_dependencies
            check_links
            ;;
        "clean")
            clean_build
            ;;
        "archive")
            create_archive
            ;;
        "deploy")
            deploy_docs "${1:-local}"
            ;;
        "deps"|"dependencies")
            check_dependencies
            ;;
        "docker")
            check_dependencies
            build_docs html
            build_docker_image
            ;;
        "full"|"all")
            print_message $BLUE "🔄 Running full documentation pipeline..."
            check_dependencies
            clean_build
            build_docs html
            check_links
            create_archive
            print_message $GREEN "✅ Full pipeline completed successfully"
            ;;
        "help"|"--help"|"-h")
            show_help
            ;;
        *)
            print_message $RED "❌ Unknown command: $command"
            print_message $YELLOW "Run '$0 help' for usage information"
            exit 1
            ;;
    esac
}

# Run main function with all arguments
main "$@"