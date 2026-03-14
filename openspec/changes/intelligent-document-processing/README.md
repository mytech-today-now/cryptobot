# OpenSpec Change: Intelligent Document Processing

## Quick Links
- [Proposal](./proposal.md) - High-level overview and goals
- [Design](./design.md) - Technical architecture and components
- [Tasks](./tasks.md) - Implementation breakdown
- [Specifications](./specs/) - Detailed component specs

## Overview
This OpenSpec Change refactors the financial analysis tool to intelligently detect document types, extract structured data using type-specific rules, eliminate duplicate processing, and present comprehensive financial insights.

## Problem
The current system treats all documents the same, using generic text extraction without understanding document structure or provider-specific information. This results in:
- Poor data quality
- Duplicate processing
- Missing context
- Generic insights

## Solution
Build an intelligent processing system with:
1. **Document Type Detection** - Identify document type and provider
2. **Duplicate Detection** - Skip redundant processing
3. **Type-Specific Extraction** - Extract structured data using rules
4. **Data Normalization** - Standardize data across all types
5. **Enhanced Reporting** - Provider-specific insights

## Supported Document Types

| Type | Provider | Example Filename | Status |
|------|----------|------------------|--------|
| Bank Statement | Chase | `20250530-statements-7969-.pdf` | Planned |
| Cable/Internet Bill | Xfinity | `0aa04849..._8771101010267769_07-18-2025.pdf` | Planned |
| Water/Sewer/Trash | Barrington Township | `UB17133-0-20240131.pdf` | Planned |
| Electric Bill | ComEd | `64935768-6652-439f-8ede-a356e00e2315.pdf` | Planned |
| Cell Phone Bill | T-Mobile | `DetailedBillApr2025.pdf` | Planned |
| Car Warranty | Various | `bc587460-0c38-4419-93b7-84e6f02370b3.pdf` | Planned |
| Invoice | Amazon | `amzn-01.pdf` | Planned |
| Generic Invoice | Various | `invoice-*.pdf` | Planned |

## Key Features

### 1. Intelligent Type Detection
- Filename pattern matching (fast, 60% confidence)
- Content-based detection (slower, 90% confidence)
- Hybrid approach (best accuracy, 95% confidence)
- Extensible for new document types

### 2. Duplicate Detection
- Exact file hash matching (100% confidence)
- Account + period matching (95% confidence)
- Filename similarity (80% confidence)
- Content fingerprinting (85% confidence)

### 3. Structured Extraction
- Type-specific extraction rules
- Required and optional fields
- Field validation and parsing
- Confidence scoring per field
- Graceful error handling

### 4. Data Normalization
- Standardized schema across all types
- ISO 8601 dates
- Consistent currency formatting
- Account number masking for privacy
- Canonical provider names

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        User Interface                            │
└────────────────────────┬────────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────────┐
│                   Processing Pipeline                            │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐       │
│  │  Type    │→ │ Duplicate│→ │Extraction│→ │  Data    │       │
│  │ Detection│  │ Detection│  │  Engine  │  │Normalize │       │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘       │
└────────────────────────┬────────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────────┐
│                    Data Layer                                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │  Document    │  │  Extraction  │  │   Analysis   │         │
│  │   Registry   │  │    Rules     │  │    Results   │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
└─────────────────────────────────────────────────────────────────┘
```

## Implementation Phases

### Phase 1: Foundation (3-4 days)
- Core module structure
- File hashing utility
- Document registry

### Phase 2: Type Detection (2-3 days)
- Filename pattern matching
- Content-based detection
- Hybrid detection
- Extensibility framework

### Phase 3: Duplicate Detection (2 days)
- File hash detection
- Filename similarity
- Content fingerprinting
- Account + period matching

### Phase 4: Extraction Rules (4-5 days)
- Extraction engine core
- Bank statement rules
- Utility bill rules (4 types)
- Invoice rules (2 types)
- Warranty rules

### Phase 5: Data Normalization (2 days)
- Data schema definition
- Normalization functions
- Validation logic

### Phase 6: Integration (3 days)
- Pipeline integration
- Report updates
- Configuration UI

### Phase 7: Testing (2 days)
- End-to-end testing
- Documentation

**Total**: 18-22 days

## Success Criteria
- ✅ 95% document type detection accuracy
- ✅ 90% extraction accuracy for required fields
- ✅ 100% exact duplicate detection
- ✅ 90% semantic duplicate detection
- ✅ < 2 seconds per document processing time
- ✅ Extensible architecture (new type in < 100 lines)
- ✅ No breaking changes to existing functionality

## Getting Started

### For Developers
1. Read [proposal.md](./proposal.md) for context
2. Review [design.md](./design.md) for architecture
3. Check [tasks.md](./tasks.md) for implementation plan
4. Read specs in [specs/](./specs/) for detailed requirements

### For Reviewers
1. Review proposal for alignment with goals
2. Validate design decisions
3. Check task breakdown for completeness
4. Provide feedback on specifications

## Files in This Change

```
intelligent-document-processing/
├── README.md                           # This file
├── proposal.md                         # High-level proposal
├── design.md                           # Technical design
├── tasks.md                            # Implementation tasks
├── specs/
│   ├── document-type-detection.md     # Type detection spec
│   ├── duplicate-detection.md         # Duplicate detection spec
│   ├── extraction-rules.md            # Extraction rules spec
│   ├── data-schema.md                 # Data schema spec (TODO)
│   └── processing-pipeline.md         # Pipeline spec (TODO)
└── examples/
    └── sample-extractions.json        # Example outputs (TODO)
```

## Questions or Feedback?
Please review the proposal and design documents and provide feedback on:
1. Are the goals aligned with project needs?
2. Is the architecture sound?
3. Are there missing requirements?
4. Is the timeline realistic?
5. Are there any risks not addressed?

## Status
**Current Status**: Proposed
**Last Updated**: 2025-01-15
**Owner**: TBD
**Reviewers**: TBD

## Next Steps
1. Review and approve proposal
2. Validate design decisions
3. Begin Phase 1 implementation
4. Set up testing framework
5. Create sample test documents

