# Change Proposal: Intelligent Document Processing System

## Change ID
`intelligent-document-processing`

## Status
Proposed

## Summary
Refactor the financial analysis tool to intelligently detect document types, extract structured data using type-specific rules, eliminate duplicate processing, and present comprehensive financial insights from multiple document sources (utility bills, bank statements, invoices, etc.).

## Problem Statement
The current financial analysis tool (`pages/financial-analysis.html`) has several limitations:

1. **No Document Type Detection**: Cannot distinguish between Xfinity bills, bank statements, utility bills, invoices, etc.
2. **Generic Extraction**: Uses one-size-fits-all text extraction without understanding document structure
3. **Duplicate Processing**: Processes the same document multiple times if uploaded again
4. **Missing Context**: Cannot extract provider-specific information (account numbers, usage metrics, service details)
5. **Poor Data Quality**: Extracted data lacks structure and semantic meaning
6. **No Learning**: Cannot improve extraction rules based on document patterns

## Proposed Solution
Build an intelligent document processing system with:

### 1. **Document Type Detection Engine**
- Filename pattern matching (e.g., `UB*` for utility bills, `statements-*` for bank statements)
- Content-based classification using keywords and document structure
- Provider identification (Xfinity, ComEd, Chase, T-Mobile, Amazon, etc.)
- Confidence scoring for classification accuracy

### 2. **Extraction Rule System**
- Type-specific extraction rules for each document category:
  - **Xfinity Bills**: Account, billing period, services, data usage, charges
  - **Water/Sewer/Trash Bills**: Account, usage (gallons/CCF), service charges
  - **Bank Statements**: Account, period, transactions, balances, fees
  - **ComEd Bills**: Account, usage (kWh), rates, delivery/supply charges
  - **Car Warranty Bills**: Coverage type, period, vehicle info, premium
  - **T-Mobile Bills**: Account, plan, lines, usage, equipment charges
  - **Amazon Invoices**: Order number, items, prices, shipping, tax
- Extensible plugin architecture for adding new document types
- Field validation and normalization

### 3. **Duplicate Detection System**
- File hash comparison (exact duplicates)
- Account number + billing period matching (re-uploaded statements)
- Filename similarity analysis with date normalization
- Content fingerprinting of key fields
- Configurable duplicate rules per document type

### 4. **Data Normalization & Storage**
- Standardized data schema across all document types
- Normalized dates, amounts, account identifiers
- Hierarchical categorization (provider → account → statement period)
- Efficient in-memory storage with optional persistence

### 5. **Enhanced Reporting**
- Provider-specific insights (e.g., "ComEd usage increased 15% vs last month")
- Cross-document analysis (e.g., total monthly expenses across all bills)
- Duplicate detection summary
- Extraction confidence indicators

## Goals
- Accurately detect and classify 8+ document types
- Extract structured data with 95%+ accuracy for known document types
- Eliminate 100% of exact duplicates and 90%+ of semantic duplicates
- Process documents 2x faster through intelligent batching
- Provide extensible architecture for adding new document types
- Maintain all existing functionality from current implementation

## Non-Goals
- OCR for handwritten documents
- Real-time document processing (remains batch-based)
- Server-side processing or cloud integration
- Machine learning model training (uses rule-based extraction)
- Support for non-financial documents

## Key Document Types (Initial Support)

| Document Type | Provider | Filename Pattern | Key Fields |
|--------------|----------|------------------|------------|
| Cable/Internet Bill | Xfinity | Hash + date suffix | Account, services, data usage, charges |
| Utility Bill | Barrington Township | `UB*-YYYYMMDD.pdf` | Account, water/sewer/trash, usage |
| Bank Statement | Chase | `YYYYMMDD-statements-*.pdf` | Account, period, transactions, balances |
| Electric Bill | ComEd | UUID pattern | Account, kWh usage, rates, charges |
| Warranty Bill | Car Warranty Service | UUID pattern | Coverage, period, vehicle, premium |
| Cell Phone Bill | T-Mobile | `DetailedBill*.pdf` | Account, plan, lines, usage |
| Invoice | Amazon | `amzn-*.pdf` | Order number, items, total |

## User Experience

### Current Flow
1. User uploads PDFs → Generic text extraction → Basic categorization → Simple report

### Proposed Flow
1. User uploads PDFs
2. System detects document types (with confidence scores)
3. System checks for duplicates (shows what was skipped)
4. System applies type-specific extraction rules
5. System normalizes and validates extracted data
6. System generates enhanced report with:
   - Document type breakdown
   - Provider-specific insights
   - Duplicate detection summary
   - Extraction quality indicators
   - Cross-document analysis

## Technical Approach

### Architecture
```
File Upload → Type Detection → Duplicate Check → Extraction → Normalization → Analysis → Report
                    ↓                ↓               ↓              ↓
              Pattern Match    Hash/Content    Rule Engine    Data Schema
              Content Scan     Fingerprint     Validators     Storage
```

### Components
1. **DocumentTypeDetector**: Classifies documents using filename + content analysis
2. **DuplicateDetector**: Identifies and filters duplicate documents
3. **ExtractionEngine**: Applies type-specific rules to extract structured data
4. **DataNormalizer**: Standardizes extracted data into common schema
5. **AnalysisEngine**: Performs cross-document analysis and generates insights
6. **ReportGenerator**: Creates enhanced HTML report with new sections

### Technologies
- Existing: PDF.js, Chart.js, Tesseract.js (OCR)
- New: Crypto API (for hashing), IndexedDB (optional persistence)

## Success Criteria
- [ ] Correctly identifies 95%+ of documents by type
- [ ] Extracts all key fields for each supported document type
- [ ] Detects and skips 100% of exact duplicates
- [ ] Detects and skips 90%+ of semantic duplicates (same statement, different file)
- [ ] Processes documents without errors or crashes
- [ ] Generates report with provider-specific insights
- [ ] Maintains backward compatibility with existing features
- [ ] Extensible: New document type can be added in <100 lines of code

## Open Questions
1. Should duplicate detection be configurable (strict vs lenient)?
2. Should users be able to manually override document type classification?
3. Should extraction rules be editable by users?
4. Should we persist learned patterns across sessions?
5. How should we handle partially-supported document types?

## References
- Current implementation: `pages/financial-analysis.html`
- Example documents: `pages/fin-analysis/*.pdf`
- PDF.js: https://mozilla.github.io/pdf.js/
- Tesseract.js: https://tesseract.projectnaptha.com/

