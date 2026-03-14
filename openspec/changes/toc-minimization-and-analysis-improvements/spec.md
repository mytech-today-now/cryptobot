# Specification: TOC Minimization and Analysis Improvements

## Change ID
`TOC-ANALYSIS-001`

## Version
1.0.0

## Status
Draft

## Last Updated
2026-02-08

---

## Overview

This specification details the implementation of a collapsible Table of Contents and improvements to document analysis accuracy for the Financial Analysis Report Generator.

---

## Part 1: Collapsible Table of Contents

### 1.1 Visual Design

#### Minimized State (Default)
- **Width**: 40px
- **Position**: Fixed to left side of viewport
- **Visual**: Vertical bar with "☰" icon and "TOC" text (rotated 90°)
- **Background**: Semi-transparent with blur effect
- **Z-index**: 1000 (above content, below modals)

#### Expanded State (On Hover/Focus)
- **Width**: 280px
- **Position**: Fixed to left side of viewport
- **Visual**: Full TOC with all sections visible
- **Background**: Solid white (light mode) / dark (dark mode)
- **Shadow**: Elevated shadow for depth
- **Transition**: 300ms ease-in-out

### 1.2 Interaction Behavior

#### Desktop
- **Hover**: Expand TOC when mouse enters the minimized bar
- **Leave**: Collapse TOC 500ms after mouse leaves (debounced)
- **Click**: Pin/unpin TOC (toggle persistent expanded state)
- **Scroll**: TOC remains fixed during page scroll

#### Mobile/Tablet
- **Tap**: Toggle between minimized and expanded
- **Swipe**: Swipe from left edge to expand, swipe left to collapse
- **Auto-collapse**: Collapse after selecting a section

### 1.3 Accessibility

- **Keyboard Navigation**:
  - `Tab` to focus TOC
  - `Enter/Space` to expand/collapse
  - Arrow keys to navigate sections
  - `Escape` to collapse
- **Screen Readers**:
  - `aria-expanded` attribute updates on state change
  - `aria-label` describes current state
  - Live region announces state changes
- **Focus Management**:
  - Focus visible indicator
  - Focus trap when expanded (optional)

### 1.4 CSS Implementation

```css
#table-of-contents {
  position: fixed;
  left: 0;
  top: 80px; /* Below header */
  height: calc(100vh - 80px);
  width: 40px;
  transition: width 300ms ease-in-out;
  overflow: hidden;
  z-index: 1000;
}

#table-of-contents:hover,
#table-of-contents:focus-within,
#table-of-contents.pinned {
  width: 280px;
}

#table-of-contents.minimized .toc-content {
  opacity: 0;
  pointer-events: none;
}

#table-of-contents:hover .toc-content,
#table-of-contents:focus-within .toc-content,
#table-of-contents.pinned .toc-content {
  opacity: 1;
  pointer-events: auto;
  transition-delay: 100ms;
}
```

---

## Part 2: Document Analysis Improvements

### 2.1 Document Type Detection Enhancement

#### Current Issues
- Amazon invoices (`amzn-*.pdf`) not detected as invoices
- Bank statements (`YYYYMMDD-statements-XXXX-.pdf`) not detected
- Utility bills with various naming patterns not recognized
- Generic UUID-named files not analyzed

#### Improved Detection Patterns

**Bank Statements (Chase)**:
```javascript
{
  filenamePattern: /^\d{8}-statements-\d+.*\.pdf$/i,
  contentKeywords: ['account statement', 'chase', 'beginning balance', 'ending balance'],
  confidence: 0.95
}
```

**Amazon Invoices**:
```javascript
{
  filenamePattern: /^(amzn-|Anna_amzn-)\d+\.pdf$/i,
  contentKeywords: ['amazon', 'order', 'invoice', 'items ordered'],
  confidence: 0.95
}
```

**Utility Bills - Water/Sewer**:
```javascript
{
  filenamePattern: /^UB\d+-\d+-\d{8}\.pdf$/i,
  contentKeywords: ['water', 'sewer', 'utility bill', 'account number'],
  confidence: 0.90
}
```

**Utility Bills - Internet (Xfinity)**:
```javascript
{
  filenamePattern: /DetailedBill[A-Za-z]{3}\d{4}\.pdf$/i,
  contentKeywords: ['xfinity', 'comcast', 'internet', 'cable'],
  confidence: 0.90
}
```

**Utility Bills - Phone (T-Mobile)**:
```javascript
{
  filenamePattern: /^[a-f0-9]{128}_\d+_\d{2}-\d{2}-\d{4}\.pdf$/i,
  contentKeywords: ['t-mobile', 'wireless', 'phone', 'mobile'],
  confidence: 0.85
}
```

**Generic Invoices**:
```javascript
{
  filenamePattern: /^Invoice\s+\d+-\d+-\d+-\d+-[a-z]\d?\.pdf$/i,
  contentKeywords: ['invoice', 'bill to', 'total amount'],
  confidence: 0.85
}
```

### 2.2 Transaction Extraction Improvements

#### For Bank Statements
- Extract account number
- Extract statement period (start/end dates)
- Extract beginning and ending balance
- Extract all transactions with dates, descriptions, amounts
- Categorize as income or expense based on amount sign

#### For Amazon Invoices
- Extract order number
- Extract order date
- Extract items and prices
- Extract total amount
- Categorize as expense (shopping)

#### For Utility Bills
- Extract provider name
- Extract billing period
- Extract account number (masked for privacy)
- Extract total amount due
- Extract due date
- Categorize as expense (utilities)

### 2.3 Categorization Rules

**Expenses** (negative impact on cash flow):
- All utility bills
- All invoices
- Bank statement debits
- Credit card charges

**Income** (positive impact on cash flow):
- Bank statement credits (deposits, transfers in)
- Payroll deposits
- Investment income

### 2.4 Provider Identification

Map content keywords to providers:
- "xfinity" OR "comcast" → Xfinity
- "t-mobile" → T-Mobile
- "comed" → ComEd
- "amazon" → Amazon
- "chase" → Chase Bank
- Water/sewer patterns → Local utility

---

## Implementation Requirements

### 3.1 TOC Changes
- Modify CSS for `#table-of-contents`
- Add JavaScript for pin/unpin functionality
- Add mobile touch handlers
- Update accessibility attributes
- Test on all screen sizes

### 3.2 Analysis Changes
- Update `DocumentTypeDetector.js` with new patterns
- Update extraction rules in `ExtractionEngine.js`
- Improve transaction categorization logic
- Add provider mapping
- Test with actual PDFs from each category

### 3.3 Testing Requirements
- Visual regression testing for TOC
- Accessibility testing (keyboard, screen reader)
- Document detection accuracy testing
- Transaction extraction accuracy testing
- Cross-browser testing

---

## Success Metrics

1. **TOC**: <10% screen width when minimized
2. **Detection Accuracy**: >90% for common document types
3. **Extraction Accuracy**: >85% for key fields
4. **Performance**: No degradation in processing time
5. **Accessibility**: WCAG 2.1 AA compliance maintained

