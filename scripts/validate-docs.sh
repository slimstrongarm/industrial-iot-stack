#!/bin/bash

# Validate Documentation Script
# Checks documentation completeness and consistency

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
COMPONENTS_DIR="$PROJECT_ROOT/stack-components"
TEMPLATES_DIR="$PROJECT_ROOT/templates"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "🔍 Validating Documentation..."
echo "================================"

# Track validation results
ERRORS=0
WARNINGS=0

# Function to check if required sections exist in a markdown file
check_required_sections() {
    local file=$1
    local component_name=$2
    local missing_sections=()
    
    # Required sections for component documentation
    local required_sections=(
        "## Overview"
        "## Capabilities"
        "## Current Implementation Status"
        "## Integration Points"
        "## Configuration"
        "## Best Practices"
    )
    
    echo -e "\n📄 Checking $component_name..."
    
    for section in "${required_sections[@]}"; do
        if ! grep -q "^$section" "$file" 2>/dev/null; then
            missing_sections+=("$section")
        fi
    done
    
    if [ ${#missing_sections[@]} -eq 0 ]; then
        echo -e "${GREEN}✓ All required sections present${NC}"
    else
        echo -e "${RED}✗ Missing sections:${NC}"
        for section in "${missing_sections[@]}"; do
            echo -e "  ${YELLOW}- $section${NC}"
            ((ERRORS++))
        done
    fi
}

# Function to check for template placeholders
check_placeholders() {
    local file=$1
    local component_name=$2
    
    # Common placeholders that shouldn't be in final docs
    local placeholders=(
        "\[Component Name\]"
        "\[Description\]"
        "\[Link\]"
        "\[Date\]"
        "\[Version\]"
        "\[TODO\]"
        "\[YYYY-MM-DD\]"
        "link-to-"
    )
    
    local found_placeholders=()
    
    for placeholder in "${placeholders[@]}"; do
        if grep -q "$placeholder" "$file" 2>/dev/null; then
            found_placeholders+=("$placeholder")
        fi
    done
    
    if [ ${#found_placeholders[@]} -gt 0 ]; then
        echo -e "${YELLOW}⚠ Found template placeholders:${NC}"
        for placeholder in "${found_placeholders[@]}"; do
            echo -e "  ${YELLOW}- $placeholder${NC}"
            ((WARNINGS++))
        done
    fi
}

# Function to check file consistency
check_file_consistency() {
    local component_dir=$1
    local component_name=$2
    
    # Check if README.md exists
    if [ ! -f "$component_dir/README.md" ]; then
        echo -e "${RED}✗ Missing README.md${NC}"
        ((ERRORS++))
        return
    fi
    
    # Check README.md content
    check_required_sections "$component_dir/README.md" "$component_name"
    check_placeholders "$component_dir/README.md" "$component_name"
    
    # Check for additional documentation files
    local doc_count=$(find "$component_dir" -name "*.md" -type f | wc -l)
    if [ "$doc_count" -gt 1 ]; then
        echo -e "${GREEN}✓ Additional documentation found ($doc_count files total)${NC}"
    fi
}

# Check each component directory
echo -e "\n📁 Checking Component Documentation..."
echo "------------------------------------"

for component_dir in "$COMPONENTS_DIR"/*; do
    if [ -d "$component_dir" ]; then
        component_name=$(basename "$component_dir")
        check_file_consistency "$component_dir" "$component_name"
    fi
done

# Check main documentation files
echo -e "\n📁 Checking Main Documentation..."
echo "--------------------------------"

# Check STACK-OVERVIEW.md
if [ -f "$PROJECT_ROOT/STACK-OVERVIEW.md" ]; then
    echo -e "${GREEN}✓ STACK-OVERVIEW.md exists${NC}"
    check_placeholders "$PROJECT_ROOT/STACK-OVERVIEW.md" "STACK-OVERVIEW"
else
    echo -e "${RED}✗ STACK-OVERVIEW.md missing${NC}"
    ((ERRORS++))
fi

# Check README.md
if [ -f "$PROJECT_ROOT/README.md" ]; then
    echo -e "${GREEN}✓ README.md exists${NC}"
else
    echo -e "${RED}✗ README.md missing${NC}"
    ((ERRORS++))
fi

# Check templates
echo -e "\n📁 Checking Templates..."
echo "----------------------"

for template in "$TEMPLATES_DIR"/*.md; do
    if [ -f "$template" ]; then
        template_name=$(basename "$template")
        echo -e "${GREEN}✓ $template_name exists${NC}"
    fi
done

# Summary
echo -e "\n================================"
echo "📊 Validation Summary"
echo "================================"
echo -e "Errors:   ${RED}$ERRORS${NC}"
echo -e "Warnings: ${YELLOW}$WARNINGS${NC}"

if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
    echo -e "\n${GREEN}✅ All documentation validation checks passed!${NC}"
    exit 0
elif [ $ERRORS -eq 0 ]; then
    echo -e "\n${YELLOW}⚠️  Documentation has warnings but no errors.${NC}"
    exit 0
else
    echo -e "\n${RED}❌ Documentation validation failed with errors.${NC}"
    exit 1
fi