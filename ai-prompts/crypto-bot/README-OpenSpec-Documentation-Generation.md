# Crypto Trading Bot Platform - Documentation Generation Guide

**Document Type**: OpenSpec Usage Guide  
**Version**: 1.0.0  
**Last Updated**: 2026-03-12  
**Owner**: Development Team Lead  

---

## Overview

This guide explains how to use the **OpenSpec specification** (`crypto-trading-bot-platform-docs.openspec.yaml`) to generate comprehensive documentation for the Crypto Trading Bot Platform (Epic TRADE-001).

The OpenSpec defines the structure, templates, and generation rules for **all project documentation** including:

- ✅ User Stories (14 stories)
- ✅ Technical Design Documents (ADRs, API specs, database schemas, architecture diagrams)
- ✅ Sprint Planning Documents (9 sprints)
- ✅ Development Artifacts (code docs, READMEs, runbooks)
- ✅ Testing Documentation (test plans, test cases, test data)
- ✅ Quality Assurance Documents (DoD, acceptance tests, code review checklists)
- ✅ Deployment & Operations Documents (deployment plans, release notes, rollback procedures)
- ✅ User-Facing Documentation (user guides, API docs, training materials)
- ✅ Project Management Documents (retrospectives, velocity reports, risk registers)
- ✅ Compliance & Governance Documents (security audits, compliance checklists, DPIAs)

---

## What is OpenSpec?

**OpenSpec** is a specification format (similar to OpenAPI for APIs) that defines:

1. **Document Structure**: What sections each document should contain
2. **Templates**: Reusable templates for consistent documentation
3. **Generation Rules**: How to automatically generate documents from source data
4. **Standards**: Formatting, naming conventions, and quality requirements
5. **Workflow**: The sequence and dependencies for document creation

---

## Quick Start

### Step 1: Review the OpenSpec

Open and review the specification file:

```bash
code crypto-trading-bot-platform-docs.openspec.yaml
```

### Step 2: Understand the Structure

The OpenSpec is organized into 14 sections:

1. **User Stories Generation** - Templates for 14 user stories
2. **Technical Design Documents** - ADRs, API specs, database schemas, architecture diagrams
3. **Sprint Planning Documents** - Sprint backlogs, goals, capacity planning
4. **Development Artifacts** - Code docs, READMEs, configuration docs, runbooks
5. **Testing Documentation** - Test plans, test cases, test data
6. **Quality Assurance Documents** - DoD, acceptance tests, code review checklists
7. **Deployment & Operations Documents** - Deployment plans, release notes, monitoring setup
8. **User-Facing Documentation** - User guides, API docs, training materials
9. **Project Management Documents** - Retrospectives, velocity reports, risk registers
10. **Compliance & Governance Documents** - Security audits, compliance checklists
11. **Document Generation Workflow** - 10-phase generation sequence
12. **Document Templates and Standards** - Markdown standards, metadata headers
13. **Automation and Tooling** - Document generators, validation tools
14. **Maintenance and Review** - Review schedules, update triggers, archival policies

### Step 3: Generate Documents

You can generate documents in three ways:

#### Option A: Manual Generation (Recommended for Learning)

Use the OpenSpec as a reference and manually create documents following the templates:

```bash
# Example: Create a user story document
# Reference: Section 1 (user_stories) in the OpenSpec
# Template: user-story-{story_id}-{title_slug}.md

# Create user story for TRADE-101
touch user-story-TRADE-101-order-execution-engine.md
```

Then populate the document using the template structure defined in the OpenSpec.

#### Option B: AI-Assisted Generation

Use an AI assistant (like this one) to generate documents based on the OpenSpec:

```
Prompt: "Using the OpenSpec specification in crypto-trading-bot-platform-docs.openspec.yaml, 
generate the user story document for TRADE-101 (Order Execution Engine)"
```

#### Option C: Automated Generation (Advanced)

Create Python scripts using the OpenSpec as a schema:

```python
# Example: user_story_generator.py
import yaml
from jinja2 import Template

# Load OpenSpec
with open('crypto-trading-bot-platform-docs.openspec.yaml') as f:
    spec = yaml.safe_load(f)

# Load epic data
with open('JIRA-epic-crypto-trading-bot-platform.md') as f:
    epic_data = parse_epic(f.read())

# Generate user stories
for story in spec['user_stories']['story_list']:
    generate_user_story(story, epic_data)
```

---

## Document Generation Workflow

Follow this **10-phase workflow** (defined in Section 11 of the OpenSpec):

### Phase 1: Epic and User Stories (Week 0)
**Status**: ✅ Epic complete, ⏳ User stories pending

- [x] Epic specification (already exists)
- [ ] 14 user story documents
- [ ] Story dependency matrix

**Action**: Generate user stories using Section 1 templates

### Phase 2: Technical Design Documents (Week 0-1)
**Status**: ⏳ Pending

- [ ] 8 Architecture Decision Records
- [ ] 5 API specifications (OpenAPI)
- [ ] 4 Database schema documents
- [ ] 3 System architecture diagrams
- [ ] 6 Exchange integration specifications

**Action**: Generate technical design docs using Section 2 templates

### Phase 3: Sprint Planning Documents (Start of each sprint)
**Status**: ⏳ Pending

- [ ] 9 sprint backlog documents
- [ ] 9 sprint goal documents
- [ ] Capacity planning spreadsheets
- [ ] Task breakdown for each story

**Action**: Generate sprint planning docs using Section 3 templates

### Phase 4-10: Continue through remaining phases...

(See Section 11 of the OpenSpec for complete workflow)

---

## Key Features of the OpenSpec

### 1. Comprehensive Coverage

The OpenSpec covers **every document type** mentioned in your requirements:

- ✅ User Stories with acceptance criteria
- ✅ Technical Design Documents (ADRs, API specs, DB schemas)
- ✅ Sprint Planning Documents
- ✅ Development Artifacts (code docs, READMEs, runbooks)
- ✅ Testing Documentation (test plans, test cases)
- ✅ QA Documents (DoD, acceptance tests, code review checklists)
- ✅ Deployment & Operations Documents
- ✅ User-Facing Documentation
- ✅ Project Management Documents
- ✅ Compliance & Governance Documents

### 2. Detailed Templates

Each document type includes:

- **Template Structure**: Required sections and subsections
- **Field Definitions**: What information to include
- **Format Specifications**: How to format the content
- **Examples**: Sample entries for reference

### 3. Standards and Conventions

The OpenSpec defines:

- **File Naming Convention**: `{document_type}-{story_id}-{title_slug}.md`
- **Markdown Standards**: Heading levels, formatting, tables, links
- **Metadata Headers**: Required and optional fields
- **Version Control**: Semantic versioning for documents
- **Diagram Standards**: Mermaid diagram types and style guide

### 4. Automation Support

The OpenSpec includes:

- **Document Generators**: Python scripts with Jinja2 templates
- **Validation Tools**: markdownlint, vale, openapi-validator
- **CI/CD Integration**: Automated builds, link checking, spell checking

---

## Example: Generating a User Story

Let's walk through generating a user story document for **TRADE-101: Order Execution Engine**.

### Step 1: Reference the OpenSpec Template

From Section 1 (`user_stories`), the template structure is:

```yaml
template_structure:
  metadata:
    fields:
      - story_id
      - story_name
      - story_type
      - story_points
      - priority
      - sprint
      # ... (see OpenSpec for full list)
      
  sections:
    - name: "User Story"
      format: "As a [role], I need [capability], So that [benefit]"
    - name: "Business Context"
    - name: "Acceptance Criteria"
    - name: "Technical Requirements"
    - name: "Dependencies"
    - name: "Testing Requirements"
    - name: "Definition of Done"
```

### Step 2: Extract Story Data

From the epic file (`JIRA-epic-crypto-trading-bot-platform.md`), extract data for TRADE-101:

- Story ID: TRADE-101
- Story Name: Implement Multi-Type Order Execution System
- Story Points: 13
- Priority: Critical (P0)
- Sprint: Sprint 3
- (See lines 495-822 of the epic file for complete details)

### Step 3: Generate the Document

Create `user-story-TRADE-101-order-execution-engine.md` using the template and extracted data.

(The epic file already contains detailed acceptance criteria, technical requirements, etc. for TRADE-101)

---

## Next Steps

1. **Review the OpenSpec**: Familiarize yourself with all 14 sections
2. **Start with User Stories**: Generate the 14 user story documents (Phase 1)
3. **Create Technical Design Docs**: Generate ADRs, API specs, DB schemas (Phase 2)
4. **Follow the Workflow**: Progress through Phases 3-10 as development proceeds

---

## Support and Resources

- **OpenSpec File**: `crypto-trading-bot-platform-docs.openspec.yaml`
- **Epic File**: `JIRA-epic-crypto-trading-bot-platform.md`
- **Output Directory**: `G:\_kyle\temp_documents\GitHub\financial\ai-prompts\crypto-bot`

For questions or assistance, contact the Development Team Lead.

