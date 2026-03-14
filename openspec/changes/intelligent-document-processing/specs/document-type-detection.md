# Specification: Document Type Detection

## Overview
The Document Type Detection system identifies the type and provider of financial documents using filename patterns and content analysis.

## Requirements

### Functional Requirements

**FR-1**: System SHALL detect document type with minimum 70% confidence
**FR-2**: System SHALL identify provider name when available
**FR-3**: System SHALL support both filename-based and content-based detection
**FR-4**: System SHALL return confidence score for each detection
**FR-5**: System SHALL classify documents as "unknown" when confidence < 70%
**FR-6**: System SHALL support at least 8 document types initially

### Non-Functional Requirements

**NFR-1**: Detection SHALL complete within 500ms per document
**NFR-2**: System SHALL be extensible for new document types
**NFR-3**: Detection accuracy SHALL be >= 95% for known document types

## Supported Document Types

### 1. Bank Statements (Chase)
- **Type**: `bank-statement`
- **Subtype**: `checking` | `savings`
- **Provider**: `Chase`
- **Filename Patterns**:
  - `YYYYMMDD-statements-NNNN-.pdf`
  - `YYYYMMDD-statements-NNNN- (N).pdf`
- **Content Keywords**: `Chase`, `Account Statement`, `Checking`, `Savings`
- **Confidence Weights**: Filename 40%, Content 60%

### 2. Cable/Internet Bills (Xfinity)
- **Type**: `utility-bill`
- **Subtype**: `cable-internet`
- **Provider**: `Xfinity`
- **Filename Patterns**:
  - Long hash followed by account number and date: `[0-9a-f]{64,}_\d+_\d{2}-\d{2}-\d{4}\.pdf`
- **Content Keywords**: `Xfinity`, `Comcast`, `Internet`, `Cable`, `Data Usage`
- **Confidence Weights**: Filename 30%, Content 70%

### 3. Water/Sewer/Trash Bills (Barrington Township)
- **Type**: `utility-bill`
- **Subtype**: `water-sewer-trash`
- **Provider**: `Barrington Township`
- **Filename Patterns**:
  - `UB\d+-\d+-\d{8}\.pdf`
- **Content Keywords**: `Barrington`, `Water`, `Sewer`, `Trash`, `Utility Bill`
- **Confidence Weights**: Filename 70%, Content 30%

### 4. Electric Bills (ComEd)
- **Type**: `utility-bill`
- **Subtype**: `electric`
- **Provider**: `ComEd`
- **Filename Patterns**:
  - UUID format: `[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\.pdf`
- **Content Keywords**: `ComEd`, `Commonwealth Edison`, `kWh`, `Electric`, `Delivery Charges`
- **Confidence Weights**: Filename 20%, Content 80%

### 5. Cell Phone Bills (T-Mobile)
- **Type**: `utility-bill`
- **Subtype**: `cell-phone`
- **Provider**: `T-Mobile`
- **Filename Patterns**:
  - `DetailedBill[A-Za-z]{3}\d{4}\.pdf`
  - `T-Mobile.*Bill.*\.pdf`
- **Content Keywords**: `T-Mobile`, `Wireless`, `Data Usage`, `Voice`, `Text Messages`
- **Confidence Weights**: Filename 50%, Content 50%

### 6. Car Warranty Bills
- **Type**: `insurance-warranty`
- **Subtype**: `car-warranty`
- **Provider**: Extracted from content
- **Filename Patterns**:
  - UUID format: `[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\.pdf`
- **Content Keywords**: `Warranty`, `Vehicle`, `Coverage`, `Premium`, `Auto`
- **Confidence Weights**: Filename 10%, Content 90%

### 7. Amazon Invoices
- **Type**: `invoice`
- **Subtype**: `retail`
- **Provider**: `Amazon`
- **Filename Patterns**:
  - `amzn-.*\.pdf`
  - `amazon.*invoice.*\.pdf`
- **Content Keywords**: `Amazon`, `Invoice`, `Order Number`, `Ship to`
- **Confidence Weights**: Filename 60%, Content 40%

### 8. Generic Invoices
- **Type**: `invoice`
- **Subtype**: `generic`
- **Provider**: Extracted from content
- **Filename Patterns**:
  - `invoice.*\.pdf`
  - `.*invoice.*\.pdf`
- **Content Keywords**: `Invoice`, `Bill To`, `Total Due`, `Payment`
- **Confidence Weights**: Filename 30%, Content 70%

## Detection Algorithm

### Step 1: Filename Analysis
```javascript
function analyzeFilename(filename) {
  const patterns = [
    { regex: /^UB\d+-\d+-\d{8}\.pdf$/i, type: 'water-sewer-trash', score: 0.7 },
    { regex: /^\d{8}-statements-\d+.*\.pdf$/i, type: 'bank-statement', score: 0.6 },
    { regex: /^amzn-/i, type: 'amazon-invoice', score: 0.8 },
    { regex: /^DetailedBill[A-Za-z]{3}\d{4}\.pdf$/i, type: 'tmobile-bill', score: 0.7 },
    // ... more patterns
  ];

  for (const pattern of patterns) {
    if (pattern.regex.test(filename)) {
      return { type: pattern.type, confidence: pattern.score, method: 'filename' };
    }
  }

  return { type: 'unknown', confidence: 0, method: 'filename' };
}
```

### Step 2: Content Analysis
```javascript
async function analyzeContent(text) {
  const keywords = {
    'xfinity': { type: 'xfinity-bill', weight: 0.9 },
    'comcast': { type: 'xfinity-bill', weight: 0.8 },
    'comed': { type: 'comed-bill', weight: 0.9 },
    'commonwealth edison': { type: 'comed-bill', weight: 0.95 },
    't-mobile': { type: 'tmobile-bill', weight: 0.9 },
    'chase': { type: 'chase-statement', weight: 0.8 },
    'amazon': { type: 'amazon-invoice', weight: 0.85 },
    // ... more keywords
  };

  const textLower = text.toLowerCase();
  const matches = [];

  for (const [keyword, info] of Object.entries(keywords)) {
    if (textLower.includes(keyword)) {
      matches.push(info);
    }
  }

  if (matches.length === 0) {
    return { type: 'unknown', confidence: 0, method: 'content' };
  }

  // Return highest weighted match
  const best = matches.reduce((a, b) => a.weight > b.weight ? a : b);
  return { type: best.type, confidence: best.weight, method: 'content' };
}
```

### Step 3: Hybrid Decision
```javascript
function combineResults(filenameResult, contentResult) {
  const filenameWeight = 0.4;
  const contentWeight = 0.6;

  // If both agree, high confidence
  if (filenameResult.type === contentResult.type) {
    return {
      type: filenameResult.type,
      confidence: Math.max(filenameResult.confidence, contentResult.confidence),
      method: 'hybrid-agreement'
    };
  }

  // Calculate weighted score
  const filenameScore = filenameResult.confidence * filenameWeight;
  const contentScore = contentResult.confidence * contentWeight;

  if (contentScore > filenameScore) {
    return {
      type: contentResult.type,
      confidence: contentScore,
      method: 'hybrid-content'
    };
  } else {
    return {
      type: filenameResult.type,
      confidence: filenameScore,
      method: 'hybrid-filename'
    };
  }
}
```

## Output Format

```javascript
{
  type: 'utility-bill',              // Primary category
  subtype: 'electric',               // Specific type
  provider: 'ComEd',                 // Provider name
  confidence: 0.92,                  // 0-1 confidence score
  detectionMethod: 'hybrid-content', // Detection method used
  metadata: {
    filenameMatch: true,             // Filename pattern matched
    contentKeywords: ['ComEd', 'kWh'], // Keywords found
    alternativeTypes: [              // Other possible types
      { type: 'invoice', confidence: 0.3 }
    ]
  }
}
```

## Error Handling

1. **Low Confidence**: If confidence < 0.7, classify as "unknown"
2. **Ambiguous Detection**: Return top 3 alternatives in metadata
3. **No Text Extracted**: Fall back to filename-only detection
4. **Multiple Providers**: Choose highest confidence provider

## Testing

### Test Cases
1. Each document type with valid filename → Correct type, high confidence
2. Each document type with generic filename → Correct type via content
3. Unknown document type → "unknown" classification
4. Ambiguous document → Multiple alternatives returned
5. Corrupted PDF → Graceful error handling

### Acceptance Criteria
- 95% accuracy on known document types
- < 5% false positives
- < 500ms detection time per document
- Extensible for new types without code changes

