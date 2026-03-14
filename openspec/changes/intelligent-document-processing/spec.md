# Specification Summary: Intelligent Document Processing

## Change Information
- **Change ID**: `intelligent-document-processing`
- **Status**: Proposed
- **Created**: 2025-01-15
- **Estimated Effort**: 18-22 days
- **Priority**: High

## Executive Summary
Refactor the financial analysis tool to intelligently detect document types (bank statements, utility bills, invoices), extract structured data using type-specific rules, eliminate duplicate processing, and provide enhanced insights based on provider-specific information.

## Motivation
The current system uses generic text extraction for all documents, resulting in:
- Poor data quality and missing context
- Duplicate processing of the same documents
- Generic insights that don't leverage provider-specific information
- Inability to distinguish between different document types

## Goals
1. **Accurate Type Detection**: 95% accuracy in identifying document type and provider
2. **Structured Extraction**: 90% accuracy in extracting required fields
3. **Duplicate Elimination**: 100% exact duplicate detection, 90% semantic duplicate detection
4. **Enhanced Insights**: Provider-specific analysis and recommendations
5. **Extensibility**: New document types can be added in < 100 lines of code

## Supported Document Types (Initial)

### 1. Bank Statements (Chase)
- **Filename Pattern**: `YYYYMMDD-statements-NNNN-.pdf`
- **Key Fields**: Account, period, balances, transactions
- **Example**: `20250530-statements-7969-.pdf`

### 2. Cable/Internet Bills (Xfinity)
- **Filename Pattern**: Hash + account + date
- **Key Fields**: Account, services, data usage, charges
- **Example**: `0aa04849...._8771101010267769_07-18-2025.pdf`

### 3. Water/Sewer/Trash Bills (Barrington Township)
- **Filename Pattern**: `UB*-*-YYYYMMDD.pdf`
- **Key Fields**: Account, usage, service charges
- **Example**: `UB17133-0-20240131.pdf`

### 4. Electric Bills (ComEd)
- **Filename Pattern**: UUID format
- **Key Fields**: Account, kWh usage, delivery/supply charges
- **Example**: `64935768-6652-439f-8ede-a356e00e2315.pdf`

### 5. Cell Phone Bills (T-Mobile)
- **Filename Pattern**: `DetailedBill*.pdf`
- **Key Fields**: Account, plan, usage, charges
- **Example**: `DetailedBillApr2025.pdf`

### 6. Car Warranty Bills
- **Filename Pattern**: UUID format
- **Key Fields**: Policy, coverage, vehicle, premium
- **Example**: `bc587460-0c38-4419-93b7-84e6f02370b3.pdf`

### 7. Amazon Invoices
- **Filename Pattern**: `amzn-*.pdf`
- **Key Fields**: Order number, items, total
- **Example**: `amzn-01.pdf`

### 8. Generic Invoices
- **Filename Pattern**: `*invoice*.pdf`
- **Key Fields**: Invoice number, date, total
- **Example**: `invoice-123.pdf`

## Core Components

### 1. Document Type Detector
**Purpose**: Identify document type and provider

**Methods**:
- Filename pattern matching (40% weight)
- Content keyword analysis (60% weight)
- Hybrid decision with confidence scoring

**Output**: Type, subtype, provider, confidence (0-1)

### 2. Duplicate Detector
**Purpose**: Identify and skip duplicate documents

**Methods**:
- Exact file hash (SHA-256) - 100% confidence
- Account + period matching - 95% confidence
- Filename similarity - 80% confidence
- Content fingerprinting - 85% confidence

**Output**: isDuplicate, reason, matched document

### 3. Extraction Engine
**Purpose**: Extract structured data using type-specific rules

**Features**:
- Regex pattern matching
- Field validation
- Value parsing and normalization
- Confidence scoring
- Graceful error handling

**Output**: Extracted fields, confidence, errors

### 4. Data Normalizer
**Purpose**: Standardize extracted data

**Normalizations**:
- Dates → ISO 8601
- Amounts → Float with 2 decimals
- Account numbers → Masked (last 4 digits)
- Categories → Standardized taxonomy
- Providers → Canonical names

**Output**: Normalized document object

## Data Flow

```
File Upload
    ↓
Extract Text (PDF.js / Tesseract.js)
    ↓
Detect Type (DocumentTypeDetector)
    ↓
Check Duplicates (DuplicateDetector)
    ↓ (if not duplicate)
Extract Data (ExtractionEngine)
    ↓
Normalize Data (DataNormalizer)
    ↓
Store in Registry
    ↓
Generate Report
```

## Key Features

### Intelligent Type Detection
- Combines filename and content analysis
- Returns confidence score
- Provides alternative classifications
- Extensible for new types

### Robust Duplicate Detection
- Multiple detection strategies
- Configurable confidence thresholds
- Detailed duplicate reporting
- Manual override option

### Structured Data Extraction
- Type-specific extraction rules
- Required and optional fields
- Field-level validation
- Partial extraction support

### Enhanced Reporting
- Document type breakdown
- Provider-specific insights
- Duplicate detection summary
- Extraction quality indicators
- Cross-document analysis

## Performance Targets
- Type detection: < 500ms per document
- Duplicate detection: < 100ms per document
- Data extraction: < 2 seconds per document
- Total processing: < 3 seconds per document
- Memory usage: < 100MB for 500 documents

## Privacy & Security
- All processing client-side (no server uploads)
- Account numbers masked in output
- Secure file hashing (SHA-256)
- Optional encrypted storage (IndexedDB)
- Clear data option

## Extensibility

### Adding New Document Type
1. Define filename patterns
2. Define content keywords
3. Create extraction rule set
4. Add to type detector registry
5. Test with sample documents

**Example**: Adding a new utility provider takes < 100 lines of code

## Testing Strategy
- Unit tests for each component
- Integration tests for full pipeline
- Regression tests for existing features
- Performance tests with 100+ documents
- Accuracy tests with real documents

## Success Metrics
- ✅ 95% type detection accuracy
- ✅ 90% extraction accuracy (required fields)
- ✅ 100% exact duplicate detection
- ✅ 90% semantic duplicate detection
- ✅ < 3 seconds per document processing
- ✅ Zero breaking changes
- ✅ Extensible architecture

## Implementation Phases
1. **Foundation** (3-4 days): Core modules, registry, hashing
2. **Type Detection** (2-3 days): Pattern matching, content analysis
3. **Duplicate Detection** (2 days): All detection methods
4. **Extraction Rules** (4-5 days): Rules for all 8 types
5. **Normalization** (2 days): Schema, validation, normalization
6. **Integration** (3 days): Pipeline, UI, configuration
7. **Testing** (2 days): E2E tests, documentation

**Total**: 18-22 days

## Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| PDF parsing accuracy | High | Use robust PDF.js, add OCR fallback |
| Performance with many files | Medium | Batch processing, web workers |
| Extraction rule maintenance | Medium | Plugin architecture, clear documentation |
| Provider format changes | Medium | Version extraction rules, fallback patterns |
| Browser compatibility | Low | Use standard APIs, polyfills |

## Dependencies
- PDF.js (already integrated)
- Tesseract.js (already integrated)
- Web Crypto API (standard)
- IndexedDB (optional, standard)

## Breaking Changes
None. All new functionality is additive.

## Migration Path
1. Add new components alongside existing code
2. Integrate into upload pipeline
3. Update report generation
4. Remove old generic extraction (optional)

## Documentation
- [Proposal](./proposal.md) - Detailed proposal
- [Design](./design.md) - Technical architecture
- [Tasks](./tasks.md) - Implementation breakdown
- [Specs](./specs/) - Component specifications
- [Examples](./examples/) - Sample outputs

## Approval Checklist
- [ ] Proposal reviewed and approved
- [ ] Design validated by technical lead
- [ ] Tasks reviewed for completeness
- [ ] Timeline approved
- [ ] Resources allocated
- [ ] Test plan approved

## Next Steps
1. Review and approve this specification
2. Set up development environment
3. Create test document set
4. Begin Phase 1 implementation
5. Weekly progress reviews

