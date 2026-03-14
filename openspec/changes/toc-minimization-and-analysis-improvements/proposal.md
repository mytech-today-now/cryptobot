# Proposal: TOC Minimization and Analysis Improvements

## Change ID
`TOC-ANALYSIS-001`

## Status
Draft

## Created
2026-02-08

## Author
Financial Analysis Team

---

## Problem Statement

The Financial Analysis Report Generator has two significant UX issues:

### 1. Table of Contents Takes Up Too Much Space
The TOC is currently always visible and takes up approximately half the page width, reducing the available space for the actual report content. This creates a poor reading experience, especially on smaller screens.

### 2. Poor Document Analysis Accuracy
The current analysis treats most documents as income statements, when in reality the majority are:
- **Utility bills** (water, electric, internet, phone)
- **Amazon invoices** (178+ invoice PDFs)
- **Bank statements** (Chase statements with pattern `YYYYMMDD-statements-XXXX-.pdf`)
- **Other bills and invoices**

The document type detection and transaction extraction logic is not properly identifying these document types, leading to:
- Incorrect categorization
- Misidentified transactions
- Poor financial insights
- Confusing reports

## Proposed Solution

### Part 1: Collapsible/Minimized TOC
Implement a hover-based TOC that:
- **Minimized state** (default): Shows only a thin vertical bar or icon on the left side
- **Expanded state** (on hover): Expands to show full TOC
- **Smooth transitions**: CSS animations for expand/collapse
- **Accessibility**: Keyboard navigation and screen reader support maintained
- **Mobile-friendly**: Touch-friendly expand/collapse on mobile devices

### Part 2: Enhanced Document Analysis
Improve the document type detection and analysis by:
- **Reviewing actual PDFs**: Analyze sample PDFs from each category to understand their structure
- **Enhanced pattern matching**: Improve filename and content-based detection
- **Better extraction rules**: Create specific extraction rules for each document type
- **Proper categorization**: Ensure bills are categorized as expenses, not income
- **Provider detection**: Accurately identify providers (Xfinity, ComEd, T-Mobile, Amazon, Chase, etc.)

## Benefits

1. **Better UX**: More screen space for report content
2. **Cleaner interface**: Less visual clutter
3. **Accurate analysis**: Correct document type identification
4. **Better insights**: Proper expense categorization and tracking
5. **Improved trust**: Users see accurate analysis of their documents

## Success Criteria

1. TOC takes up <10% of screen width when minimized
2. TOC expands smoothly on hover (within 300ms)
3. All accessibility features maintained
4. Document type detection accuracy >90% for common types
5. Proper categorization of bills as expenses
6. Accurate provider identification for major providers

## Non-Goals

- Complete redesign of the report layout
- Adding new document types beyond what's already in the PDFs
- Server-side processing or AI-based analysis

## Timeline

- **Estimated Duration**: 3-4 days
- **Phase 1**: TOC minimization (1 day)
- **Phase 2**: Document analysis improvements (2-3 days)

## Dependencies

- Existing IDP (Intelligent Document Processing) components
- Current DocumentTypeDetector implementation
- ExtractionEngine and extraction rules

## Risks

- **Low risk**: Changes are primarily CSS and logic improvements
- **Testing needed**: Ensure TOC works on all screen sizes
- **Validation needed**: Test with actual PDFs to verify improvements

