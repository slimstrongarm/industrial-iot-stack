# Industrial IoT Stack Documentation System

## Overview
This project creates a unified documentation system for an Industrial IoT stack centered around Ignition Edge and Node-RED. Each technology component maintains its own documentation that feeds into a central overview.

## Purpose
- Provide clear visibility into each technology's role, capabilities, and current implementation
- Create a single source of truth for the entire IIoT stack
- Enable each technology expert (or AI agent) to maintain their own documentation
- Automatically aggregate into a unified view

## Structure

```
industrial-iot-stack/
├── stack-components/          # Individual technology documentation
│   ├── ignition-edge/
│   │   ├── README.md         # Ignition Edge overview
│   │   ├── capabilities.md   # What it can do
│   │   ├── current-state.md  # Current implementation
│   │   └── integration.md    # How it connects to other components
│   ├── node-red/
│   │   ├── README.md
│   │   ├── capabilities.md
│   │   ├── current-state.md
│   │   └── integration.md
│   ├── mqtt/
│   ├── databases/
│   ├── edge-computing/
│   └── protocols/
├── templates/                 # Documentation templates
├── scripts/                   # Automation scripts
├── STACK-OVERVIEW.md         # Aggregated view of all components
└── README.md                 # Project documentation

## Integration with Steel Bonnet
- Steel Bonnet Repository: Contains actual implementation scripts
- This Repository: Contains documentation and architecture overview
- Cross-references between repos for complete picture

## How to Use
1. Each technology maintainer updates their component folder
2. Run aggregation script to update STACK-OVERVIEW.md
3. Use STACK-OVERVIEW.md for unified view of entire stack