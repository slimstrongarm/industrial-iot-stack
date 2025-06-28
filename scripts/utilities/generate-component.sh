#!/bin/bash

# Generate Component Documentation Script
# Creates new component documentation from template

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
COMPONENTS_DIR="$PROJECT_ROOT/stack-components"
TEMPLATE_FILE="$PROJECT_ROOT/templates/component-template.md"

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to display usage
usage() {
    echo "Usage: $0 <component-name>"
    echo "Example: $0 kepware-server"
    echo ""
    echo "This will create a new component directory with documentation template"
    exit 1
}

# Check if component name is provided
if [ $# -eq 0 ]; then
    echo -e "${RED}Error: Component name is required${NC}"
    usage
fi

COMPONENT_NAME="$1"
COMPONENT_DIR="$COMPONENTS_DIR/$COMPONENT_NAME"
DISPLAY_NAME=$(echo "$COMPONENT_NAME" | sed 's/-/ /g' | awk '{for(i=1;i<=NF;i++)sub(/./,toupper(substr($i,1,1)),$i)}1')

# Check if component already exists
if [ -d "$COMPONENT_DIR" ]; then
    echo -e "${YELLOW}Warning: Component '$COMPONENT_NAME' already exists${NC}"
    read -p "Do you want to overwrite it? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Aborted."
        exit 1
    fi
fi

# Create component directory
echo -e "📁 Creating component directory: ${GREEN}$COMPONENT_DIR${NC}"
mkdir -p "$COMPONENT_DIR"

# Copy template and replace placeholders
echo -e "📄 Creating documentation from template..."
cp "$TEMPLATE_FILE" "$COMPONENT_DIR/README.md"

# Replace [Component Name] with actual component name
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    sed -i '' "s/\[Component Name\]/$DISPLAY_NAME/g" "$COMPONENT_DIR/README.md"
else
    # Linux
    sed -i "s/\[Component Name\]/$DISPLAY_NAME/g" "$COMPONENT_DIR/README.md"
fi

# Add current date to the document
CURRENT_DATE=$(date '+%Y-%m-%d')
if [[ "$OSTYPE" == "darwin"* ]]; then
    sed -i '' "s/\[Date\]/$CURRENT_DATE/g" "$COMPONENT_DIR/README.md"
    sed -i '' "s/YYYY-MM-DD/$CURRENT_DATE/g" "$COMPONENT_DIR/README.md"
else
    sed -i "s/\[Date\]/$CURRENT_DATE/g" "$COMPONENT_DIR/README.md"
    sed -i "s/YYYY-MM-DD/$CURRENT_DATE/g" "$COMPONENT_DIR/README.md"
fi

# Create additional subdirectories
echo -e "📁 Creating subdirectories..."
mkdir -p "$COMPONENT_DIR"/{configs,examples,docs,scripts}

# Create a basic .gitkeep in each subdirectory
touch "$COMPONENT_DIR/configs/.gitkeep"
touch "$COMPONENT_DIR/examples/.gitkeep"
touch "$COMPONENT_DIR/docs/.gitkeep"
touch "$COMPONENT_DIR/scripts/.gitkeep"

# Create a basic example configuration file
cat > "$COMPONENT_DIR/configs/example-config.yaml" << EOF
# Example configuration for $DISPLAY_NAME
# This is a placeholder - replace with actual configuration

$COMPONENT_NAME:
  enabled: true
  version: "1.0.0"
  settings:
    # Add your configuration settings here
    setting1: value1
    setting2: value2
EOF

# Create a basic integration example
cat > "$COMPONENT_DIR/examples/integration-example.md" << EOF
# $DISPLAY_NAME Integration Example

## Overview
This example demonstrates how to integrate $DISPLAY_NAME with other stack components.

## Prerequisites
- Component installed and configured
- Network connectivity established
- Required credentials available

## Integration Steps
1. Configure $DISPLAY_NAME settings
2. Set up connection parameters
3. Test the integration
4. Monitor data flow

## Example Code
\`\`\`yaml
# Add your integration example here
\`\`\`

## Troubleshooting
- Check network connectivity
- Verify credentials
- Review log files
EOF

echo -e "\n${GREEN}✅ Component documentation created successfully!${NC}"
echo -e "\n📍 Component location: ${GREEN}$COMPONENT_DIR${NC}"
echo -e "\n📝 Next steps:"
echo -e "  1. Edit ${YELLOW}$COMPONENT_DIR/README.md${NC} to add component details"
echo -e "  2. Add configuration examples to ${YELLOW}$COMPONENT_DIR/configs/${NC}"
echo -e "  3. Add integration examples to ${YELLOW}$COMPONENT_DIR/examples/${NC}"
echo -e "  4. Run ${YELLOW}./scripts/update-stack-overview.sh${NC} to update the main overview"
echo -e "\n💡 Tip: Use ${YELLOW}./scripts/validate-docs.sh${NC} to check your documentation"