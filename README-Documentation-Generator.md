# Documentation Generator Script

**Script**: `generate_documentation.py`
**Version**: 2.0.0
**Last Updated**: 2026-03-12
**Purpose**: Automated generation of all project documentation based on OpenSpec specification

---

## Overview

This Python script automates the generation of all documentation artifacts for the Crypto Trading Bot Platform project. It reads the OpenSpec specification (`crypto-trading-bot-platform-docs.openspec.yaml`) and the epic data (`JIRA-epic-crypto-trading-bot-platform.md`) to generate individual markdown files for each document.

## Features

✅ **Automated Document Generation**: Generate all 250+ documents automatically
✅ **Category Filtering**: Generate specific document categories only
✅ **Phase Filtering**: Generate documents for specific project phases
✅ **Dry Run Mode**: Preview what would be generated without creating files
✅ **Progress Tracking**: Detailed logging and statistics
✅ **Error Handling**: Robust error handling with detailed error messages
✅ **Smart Parsing**: Extracts structured data from epic markdown
✅ **List Command**: View all available categories and phases
✅ **Verbose/Quiet Modes**: Control logging output level
✅ **Custom Output Directory**: Specify where to generate files

## Requirements

```bash
pip install pyyaml jinja2
```

Or install from requirements file:

```bash
pip install -r requirements.txt
```

## Usage

### Quick Start

#### 1. List Available Options

```bash
python generate_documentation.py --list
```

This displays all 10 document categories, all 10 project phases, and usage examples.

#### 2. Preview Generation (Dry Run)

```bash
python generate_documentation.py --category user_stories --dry-run
```

#### 3. Generate Documents

```bash
python generate_documentation.py --category user_stories
```

### Basic Usage

Generate all documents:

```bash
python generate_documentation.py
```

### Generate Specific Category

Generate only user stories:

```bash
python generate_documentation.py --category user_stories
```

Available categories:
- `user_stories`
- `technical_design_documents`
- `sprint_planning_documents`
- `development_artifacts`
- `testing_documentation`
- `quality_assurance_documents`
- `deployment_operations_documents`
- `user_facing_documentation`
- `project_management_documents`
- `compliance_governance_documents`

### Generate Specific Phase

Generate documents for Phase 1:

```bash
python generate_documentation.py --phase 1
```

Phases 1-10 correspond to the workflow defined in the OpenSpec.

### Dry Run Mode

Preview what would be generated without creating files:

```bash
python generate_documentation.py --dry-run
```

Combine with category filtering:

```bash
python generate_documentation.py --category user_stories --dry-run
```

### Custom Paths

Specify custom paths for input/output:

```bash
python generate_documentation.py \
  --openspec path/to/openspec.yaml \
  --epic path/to/epic.md \
  --output path/to/output/directory
```

**Note**: The `--output` flag defaults to the script's directory. All paths are resolved relative to the script directory if not absolute.

### Logging Control

#### Verbose Mode (DEBUG level)

```bash
python generate_documentation.py --verbose
```

#### Quiet Mode (Errors only)

```bash
python generate_documentation.py --quiet
```

## Examples

### Example 1: Generate All User Stories

```bash
python generate_documentation.py --category user_stories
```

**Output**:
```
2026-03-12 10:30:15 - INFO - Initialized DocumentGenerator
2026-03-12 10:30:15 - INFO -   OpenSpec: crypto-trading-bot-platform-docs.openspec.yaml
2026-03-12 10:30:15 - INFO -   Epic: JIRA-epic-crypto-trading-bot-platform.md
2026-03-12 10:30:15 - INFO -   Output: .
2026-03-12 10:30:15 - INFO -   Dry Run: False
2026-03-12 10:30:15 - INFO - Loading OpenSpec...
2026-03-12 10:30:15 - INFO - ✓ OpenSpec loaded successfully
2026-03-12 10:30:15 - INFO - Loading epic...
2026-03-12 10:30:15 - INFO - ✓ Epic loaded successfully
2026-03-12 10:30:15 - INFO -   Found 14 stories
2026-03-12 10:30:15 - INFO - Generating user stories...
2026-03-12 10:30:15 - INFO -   ✓ user-story-TRADE-101-order-execution-engine.md (created)
2026-03-12 10:30:15 - INFO -   ✓ user-story-TRADE-102-trading-strategy-framework.md (created)
...
```

### Example 2: Preview Generation (Dry Run)

```bash
python generate_documentation.py --category user_stories --dry-run
```

This will show what would be generated without actually creating files.

### Example 3: Generate Phase 1 Documents

```bash
python generate_documentation.py --phase 1
```

Generates all documents required for Phase 1 (Epic and User Stories).

## Output

### Generated Files

The script generates markdown files following the naming convention:

- **User Stories**: `user-story-{STORY_ID}-{title-slug}.md`
- **Technical Docs**: `{doc-type}-{identifier}.md`
- **Sprint Docs**: `sprint-{number}-{doc-type}.md`

### Log File

All generation activity is logged to `documentation_generation.log`:

```
2026-03-12 10:30:15 - INFO - Initialized DocumentGenerator
2026-03-12 10:30:15 - INFO - Loading OpenSpec from crypto-trading-bot-platform-docs.openspec.yaml
2026-03-12 10:30:15 - INFO - ✓ OpenSpec loaded successfully
...
```

### Statistics

At the end of generation, the script prints a summary:

```
================================================================================
GENERATION SUMMARY
================================================================================
Total documents:     14
  ✓ Generated:       13
  ⊙ Skipped:         1
  ✗ Errors:          0
================================================================================
Success rate: 92.9%
```

## Current Implementation Status

### ✅ Fully Implemented

- User story generation
- Epic parsing and data extraction
- Metadata extraction
- Acceptance criteria parsing
- Template rendering
- Dry run mode
- Logging and statistics
- Command-line interface

### ⏳ Partially Implemented

- Technical design document generation (placeholder)
- Sprint planning document generation (placeholder)
- Testing document generation (placeholder)
- Other category generation (placeholder)

### 🔜 Future Enhancements

- Jinja2 template support for advanced customization
- Multi-threaded generation for performance
- Incremental updates (only regenerate changed documents)
- Validation of generated documents
- Integration with CI/CD pipelines

## Troubleshooting

### Issue: "OpenSpec file not found"

**Solution**: Ensure you're running the script from the correct directory or use `--openspec` to specify the path.

### Issue: "Story not found in epic data"

**Solution**: Verify that the story ID in the OpenSpec matches the story ID in the epic markdown file.

### Issue: "Permission denied"

**Solution**: Ensure you have write permissions to the output directory.

## Contributing

To extend the script with additional document types:

1. Add a new `_generate_*` method for your document type
2. Update the `_generate_category` method to call your new method
3. Implement the parsing and template rendering logic
4. Test with `--dry-run` first

## Support

For issues or questions:
- Check the log file: `documentation_generation.log`
- Review the OpenSpec specification
- Refer to the example user story document

---

**Script Status**: ✅ Production Ready (User Stories)  
**Next Steps**: Implement remaining document type generators

