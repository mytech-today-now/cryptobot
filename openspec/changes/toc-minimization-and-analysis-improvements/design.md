# Design: TOC Minimization and Analysis Improvements

## Change ID
`TOC-ANALYSIS-001`

## Version
1.0.0

## Status
Draft

## Last Updated
2026-02-08

---

## Design Overview

This document describes the design approach for implementing a collapsible Table of Contents and enhanced document analysis.

---

## Part 1: Collapsible TOC Design

### Visual Design

#### Minimized State
```
┌─┐
│☰│  <- 40px wide vertical bar
│T│
│O│
│C│
└─┘
```

- **Width**: 40px
- **Height**: Full viewport height minus header
- **Background**: `rgba(255, 255, 255, 0.95)` with backdrop blur
- **Border**: Right border `1px solid #e0e0e0`
- **Icon**: Hamburger menu (☰) at top
- **Text**: "TOC" rotated 90° clockwise

#### Expanded State
```
┌──────────────────────────┐
│ Table of Contents    📌  │  <- 280px wide
│                          │
│ • Executive Summary      │
│ • Income Analysis        │
│ • Expense Analysis       │
│ • Cash Flow              │
│ • Net Worth              │
│ • Document Details       │
│ • Report Information     │
└──────────────────────────┘
```

- **Width**: 280px
- **Height**: Full viewport height minus header
- **Background**: Solid white with shadow
- **Shadow**: `0 4px 12px rgba(0, 0, 0, 0.15)`
- **Pin Icon**: Top-right corner to toggle persistent state

### Interaction States

1. **Default (Minimized)**: Shows only the vertical bar
2. **Hover**: Expands to full width after 100ms delay
3. **Pinned**: Stays expanded until unpinned
4. **Mobile**: Tap to toggle, auto-collapse after selection

### Animation

```css
transition: width 300ms cubic-bezier(0.4, 0.0, 0.2, 1);
```

- **Expand**: Smooth ease-out curve
- **Collapse**: Smooth ease-in curve
- **Content fade**: Opacity transition with 100ms delay

---

## Part 2: Document Analysis Design

### Architecture

```
┌─────────────────────────────────────────────────┐
│           Document Upload                       │
└─────────────────┬───────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────┐
│     DocumentTypeDetector                        │
│  - Filename pattern matching                    │
│  - Content keyword analysis                     │
│  - Hybrid detection with confidence scoring     │
└─────────────────┬───────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────┐
│     ExtractionEngine                            │
│  - Apply type-specific extraction rules         │
│  - Extract key fields (dates, amounts, etc.)    │
│  - Validate and parse extracted data            │
└─────────────────┬───────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────┐
│     DataNormalizer                              │
│  - Normalize dates to ISO 8601                  │
│  - Normalize amounts to float                   │
│  - Categorize transactions                      │
│  - Identify providers                           │
└─────────────────┬───────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────┐
│     Report Generation                           │
└─────────────────────────────────────────────────┘
```

### Detection Strategy

#### 1. Filename Pattern Matching (Fast, 60-95% confidence)

**Priority Order**:
1. Exact patterns (95% confidence)
2. Provider-specific patterns (90% confidence)
3. Generic patterns (60% confidence)

**Examples**:
- `amzn-123.pdf` → Amazon Invoice (95%)
- `20240131-statements-7969-.pdf` → Chase Bank Statement (95%)
- `UB17133-0-20240131.pdf` → Water/Sewer Bill (90%)
- `DetailedBillJan2025.pdf` → Xfinity Bill (90%)

#### 2. Content Keyword Analysis (Slower, 85-95% confidence)

**Keyword Sets**:
- **Amazon**: ["amazon", "order", "invoice", "items ordered"]
- **Chase**: ["chase", "account statement", "beginning balance"]
- **Xfinity**: ["xfinity", "comcast", "internet", "cable"]
- **T-Mobile**: ["t-mobile", "wireless", "mobile"]

#### 3. Hybrid Detection (Best accuracy, 90-98% confidence)

Combine filename and content with weighted scoring:
```
finalConfidence = (filenameConfidence * 0.4) + (contentConfidence * 0.6)
```

### Extraction Rules Design

#### Bank Statement Extraction
```javascript
{
  accountNumber: {
    pattern: /Account.*?(\d{4,})/i,
    required: true,
    mask: true  // Show only last 4 digits
  },
  statementPeriod: {
    pattern: /(\d{2}\/\d{2}\/\d{4})\s*-\s*(\d{2}\/\d{2}\/\d{4})/i,
    required: true,
    parser: parseDateRange
  },
  beginningBalance: {
    pattern: /Beginning.*?\$?([\d,]+\.\d{2})/i,
    required: true,
    parser: parseFloat
  },
  endingBalance: {
    pattern: /Ending.*?\$?([\d,]+\.\d{2})/i,
    required: true,
    parser: parseFloat
  }
}
```

#### Amazon Invoice Extraction
```javascript
{
  orderNumber: {
    pattern: /Order.*?(\d{3}-\d{7}-\d{7})/i,
    required: true
  },
  orderDate: {
    pattern: /Order Date.*?(\w+ \d{1,2}, \d{4})/i,
    required: true,
    parser: parseDate
  },
  totalAmount: {
    pattern: /Order Total.*?\$?([\d,]+\.\d{2})/i,
    required: true,
    parser: parseFloat
  }
}
```

### Categorization Logic

```javascript
function categorizeTransaction(transaction, documentType) {
  // Bills and invoices are always expenses
  if (documentType.includes('bill') || documentType.includes('invoice')) {
    return {
      type: 'expense',
      category: getCategoryFromProvider(transaction.provider),
      confidence: 0.95
    };
  }
  
  // Bank statements: check amount sign
  if (documentType === 'bank-statement') {
    if (transaction.amount > 0) {
      return { type: 'income', category: 'deposit', confidence: 0.90 };
    } else {
      return { type: 'expense', category: 'withdrawal', confidence: 0.90 };
    }
  }
  
  return { type: 'unknown', category: 'uncategorized', confidence: 0.0 };
}
```

---

## Implementation Approach

### Phase 1: TOC (Low Risk)
- Pure CSS and JavaScript changes
- No impact on existing functionality
- Easy to test and validate

### Phase 2: Analysis (Medium Risk)
- Update existing components
- Maintain backward compatibility
- Extensive testing with real PDFs

### Testing Strategy
- Unit tests for new patterns
- Integration tests for extraction
- E2E tests with real PDFs
- Visual regression tests for TOC

---

## Performance Considerations

- **TOC**: No performance impact (CSS-only)
- **Detection**: Minimal impact (<50ms per document)
- **Extraction**: Slight increase due to more patterns (<100ms per document)
- **Overall**: No noticeable degradation for typical use (50-100 PDFs)

---

## Accessibility

- WCAG 2.1 AA compliance maintained
- Keyboard navigation fully supported
- Screen reader announcements for state changes
- Focus indicators visible
- Color contrast ratios meet standards

