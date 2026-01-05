# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2026-01-05

### Added
- 🎉 Complete MCP Server implementation with two core tools
- `get_focused_projects()` tool - Returns favorite projects with git metadata
- `scan_project(path, options)` tool - Performs on-demand recursive scanning
- Clear separation between declared and derived metadata
- Comprehensive git information extraction (has_git, dirty, last_commit_days)
- Flexible directory scanning with depth and extension filters
- Support for both absolute and relative project paths
- Automatic ignoring of common directories (node_modules, __pycache__, venv)
- YAML-based configuration for declared metadata
- JSON-serializable outputs for all tools
- Complete error handling with timeouts for git operations
- Permission error handling for filesystem access
- Test script for validating functionality
- Comprehensive documentation:
  - README.md with feature overview
  - QUICKSTART.md for quick setup
  - CLAUDE_CODE_SETUP.md for Linux CLI users 🐧
  - CONFIG_REFERENCE.md for quick configuration reference
  - DEVELOPMENT.md with architecture details
  - ARCHITECTURE_DIAGRAMS.md with 8 Mermaid diagrams
  - PROJECT_STRUCTURE.md with complete project structure
  - Example Claude Desktop configuration

### Technical Details
- Built on `mcp` Python package (>=1.1.0)
- Uses stdio for MCP communication
- Implements MCP tools with proper decorators
- Modular helper functions for maintainability
- Type hints for better code clarity

### Design Principles
- **Declared Metadata**: User-defined, persistent in YAML
- **Derived Metadata**: Calculated on-demand, not stored
- **Responsibility Boundary**: MCP provides facts, LLM makes decisions
- **Minimal and Lightweight**: Fast operations with timeouts
- **Extensible**: Easy to add new tools and metadata fields

### Documentation
- 📚 Full README with installation and usage guide
- 🛠️ Development documentation with architecture diagrams
- ⚡ Quick start guide for 5-minute setup
- 📝 Example configurations and use cases
- 🧪 Test scripts with multiple scenarios

## [Future Releases]

### Planned for v2.1.0
- [ ] Caching mechanism for large project collections
- [ ] Additional derived metadata (LOC, complexity metrics)
- [ ] Project health scoring
- [ ] Better performance for large repositories

### Planned for v3.0.0
- [ ] WebSocket support for real-time updates
- [ ] Multiple dashboard state profiles
- [ ] Project dependency graph visualization
- [ ] Custom metadata plugin system

---

## Release Notes

### v2.0.0 - Initial MCP Server Release

This is the first complete release of the Project Dashboard MCP Server, designed from the ground up as a Model Context Protocol server for LLM integration.

**Key Features:**
- Two powerful tools for project management
- Clear metadata classification (declared vs derived)
- Comprehensive git integration
- Flexible project scanning
- Production-ready error handling

**Perfect For:**
- Developers managing multiple projects
- Teams needing project status visibility
- Anyone wanting AI-assisted project management

**Getting Started:**
See [QUICKSTART.md](QUICKSTART.md) for a 5-minute setup guide.

**Upgrading from v1:**
This is a complete rewrite. v1 was a Flask web dashboard, v2 is an MCP server.
They serve different purposes and can coexist.
