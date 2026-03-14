# Design Document: Intelligent Document Processing System

## Overview
This document details the technical design for the intelligent document processing system that will enhance the financial analysis tool with type detection, structured extraction, and duplicate elimination.

## System Architecture

### High-Level Architecture
```
┌─────────────────────────────────────────────────────────────────┐
│                        User Interface                            │
│  (File Upload, Progress Display, Report Visualization)          │
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

## Core Components

### 1. Document Type Detector

**Purpose**: Identify document type and provider from filename and content.

**Interface**:
```javascript
class DocumentTypeDetector {
  detect(file, extractedText) {
    // Returns: { type, provider, confidence, metadata }
  }
}
```

**Detection Strategy**:
1. **Filename Pattern Matching** (Fast, 60% confidence)
   - Regex patterns for each document type
   - Examples:
     - `/^UB\d+-\d+-\d{8}\.pdf$/` → Water/Sewer bill
     - `/^\d{8}-statements-\d+.*\.pdf$/` → Bank statement
     - `/^amzn-/` → Amazon invoice

2. **Content-Based Detection** (Slower, 90% confidence)
   - Extract first 2 pages of text
   - Search for provider keywords:
     - "Xfinity" → Xfinity bill
     - "ComEd" → Electric bill
     - "T-Mobile" → Cell phone bill
   - Search for document type indicators:
     - "Account Statement" → Bank statement
     - "Invoice" → Invoice
     - "Billing Statement" → Utility bill

3. **Hybrid Approach** (Best accuracy)
   - Combine filename + content scores
   - Weighted average: 40% filename, 60% content
   - Confidence threshold: 70% to classify, else "unknown"

**Data Structure**:
```javascript
{
  type: 'utility-bill',           // Document category
  subtype: 'water-sewer-trash',   // Specific type
  provider: 'Barrington Township', // Provider name
  confidence: 0.95,                // 0-1 confidence score
  detectionMethod: 'hybrid',       // 'filename' | 'content' | 'hybrid'
  metadata: {
    accountPattern: /UB\d+/,      // Detected patterns
    keywords: ['water', 'sewer']  // Found keywords
  }
}
```

### 2. Duplicate Detector

**Purpose**: Identify and filter duplicate documents to avoid reprocessing.

**Interface**:
```javascript
class DuplicateDetector {
  isDuplicate(file, extractedData, existingDocuments) {
    // Returns: { isDuplicate, reason, matchedDocument }
  }
}
```

**Detection Rules**:

1. **Exact File Hash** (100% confidence)
   ```javascript
   const fileHash = await crypto.subtle.digest('SHA-256', fileBuffer);
   ```

2. **Account + Period Match** (95% confidence)
   ```javascript
   {
     accountNumber: '1234567890',
     statementPeriod: '2024-01',
     provider: 'Chase'
   }
   // If all three match → duplicate
   ```

3. **Filename Similarity** (80% confidence)
   ```javascript
   // Normalize dates and compare
   '20250530-statements-7969-.pdf'
   '20250530-statements-7969- (1).pdf'
   // → Same base, different suffix → likely duplicate
   ```

4. **Content Fingerprint** (85% confidence)
   ```javascript
   // Hash of key fields
   const fingerprint = hash({
     accountNumber,
     totalAmount,
     statementDate,
     provider
   });
   ```

**Duplicate Handling**:
- Keep first occurrence
- Track all duplicates with reasons
- Report duplicates in summary section
- Allow user override (manual processing)

### 3. Extraction Engine

**Purpose**: Extract structured data using type-specific rules.

**Interface**:
```javascript
class ExtractionEngine {
  extract(file, documentType, extractedText) {
    // Returns: { fields, confidence, errors }
  }
}
```

**Rule-Based Extraction**:
Each document type has an extraction rule set:

```javascript
const extractionRules = {
  'bank-statement-chase': {
    accountNumber: {
      pattern: /Account\s+Number[:\s]+(\d{4,})/i,
      required: true,
      validator: (val) => val.length >= 4
    },
    statementPeriod: {
      pattern: /Statement\s+Period[:\s]+(\d{2}\/\d{2}\/\d{4})\s*-\s*(\d{2}\/\d{2}\/\d{4})/i,
      required: true,
      parser: (match) => ({ start: match[1], end: match[2] })
    },
    beginningBalance: {
      pattern: /Beginning\s+Balance[:\s]+\$?([\d,]+\.\d{2})/i,
      required: true,
      parser: parseFloat
    }
    // ... more fields
  }
};
```

**Extraction Process**:
1. Select rule set based on document type
2. Apply each field's pattern to extracted text
3. Validate extracted values
4. Parse/normalize values
5. Calculate confidence score
6. Return structured data

### 4. Data Normalizer

**Purpose**: Convert extracted data into standardized schema.

**Common Schema**:
```javascript
{
  document: {
    id: 'uuid',
    type: 'bank-statement',
    provider: 'Chase',
    filename: 'original.pdf',
    uploadDate: '2025-01-15T10:30:00Z',
    processingDate: '2025-01-15T10:30:05Z',
    hash: 'sha256-hash',
    confidence: 0.95
  },
  account: {
    number: '****7969',        // Masked for privacy
    type: 'checking',
    holder: null               // Not extracted for privacy
  },
  period: {
    start: '2025-05-01',       // ISO 8601 date
    end: '2025-05-30',
    dueDate: '2025-06-15'
  },
  financial: {
    currency: 'USD',
    beginningBalance: 1234.56,
    endingBalance: 2345.67,
    totalDeposits: 5000.00,
    totalWithdrawals: 3888.89,
    fees: 12.00,
    interest: 1.23
  },
  transactions: [
    {
      date: '2025-05-15',
      description: 'Purchase at Store',
      amount: -45.67,
      balance: 1500.00,
      category: 'shopping'      // Auto-categorized
    }
  ],
  metadata: {
    pageCount: 5,
    extractionMethod: 'rule-based',
    extractionDuration: 234,   // milliseconds
    warnings: []
  }
}
```

**Normalization Rules**:
- Dates → ISO 8601 format
- Amounts → Float with 2 decimal places
- Account numbers → Masked (show last 4 digits)
- Categories → Standardized taxonomy
- Providers → Canonical names

### 5. Processing Pipeline

**Workflow**:
```javascript
async function processDocuments(files) {
  const results = {
    processed: [],
    duplicates: [],
    errors: []
  };

  for (const file of files) {
    try {
      // Step 1: Extract text
      const text = await extractText(file);

      // Step 2: Detect type
      const typeInfo = await typeDetector.detect(file, text);

      // Step 3: Check duplicates
      const dupCheck = await duplicateDetector.check(file, results.processed);
      if (dupCheck.isDuplicate) {
        results.duplicates.push({ file, reason: dupCheck.reason });
        continue;
      }

      // Step 4: Extract data
      const extracted = await extractionEngine.extract(file, typeInfo, text);

      // Step 5: Normalize
      const normalized = await dataNormalizer.normalize(extracted, typeInfo);

      // Step 6: Store
      results.processed.push(normalized);

    } catch (error) {
      results.errors.push({ file, error });
    }
  }

  return results;
}
```

## Data Structures

### Document Registry
Tracks all processed documents:
```javascript
{
  documents: Map<fileHash, DocumentInfo>,
  byProvider: Map<provider, Set<fileHash>>,
  byType: Map<type, Set<fileHash>>,
  byPeriod: Map<period, Set<fileHash>>
}
```

### Extraction Rules Registry
Stores all extraction rules:
```javascript
{
  rules: Map<documentType, ExtractionRuleSet>,
  validators: Map<fieldType, ValidatorFunction>,
  parsers: Map<fieldType, ParserFunction>
}
```

## Performance Considerations

1. **Batch Processing**: Process files in batches of 20 to maintain UI responsiveness
2. **Caching**: Cache extracted text and type detection results
3. **Lazy Loading**: Only extract full data when needed
4. **Web Workers**: Offload heavy processing to background threads
5. **IndexedDB**: Persist processed data for faster subsequent loads

## Error Handling

1. **Graceful Degradation**: If type detection fails, fall back to generic extraction
2. **Partial Extraction**: Return partial data if some fields fail
3. **User Feedback**: Show extraction confidence and warnings
4. **Retry Logic**: Allow manual retry for failed documents
5. **Logging**: Detailed error logs for debugging

## Security & Privacy

1. **Client-Side Only**: All processing happens in browser
2. **No External Calls**: No data sent to servers
3. **Data Masking**: Mask sensitive fields (account numbers, SSN)
4. **Secure Storage**: Use encrypted IndexedDB if persisting
5. **Clear Data**: Provide option to clear all processed data

## Extensibility

### Adding New Document Type
1. Create extraction rule set
2. Add filename patterns
3. Add content keywords
4. Define data schema mapping
5. Add tests

Example:
```javascript
// Add to extraction rules
extractionRules['utility-bill-electric-comed'] = {
  accountNumber: { pattern: /Account\s*#[:\s]*(\d+)/i },
  usageKwh: { pattern: /Total\s+kWh[:\s]*([\d,]+)/i },
  // ... more fields
};

// Add to type detector
typeDetector.addPattern({
  type: 'utility-bill',
  subtype: 'electric',
  provider: 'ComEd',
  filenamePattern: /^[0-9a-f]{8}-[0-9a-f]{4}-/i,
  contentKeywords: ['ComEd', 'kWh', 'electric']
});
```

## Testing Strategy

1. **Unit Tests**: Each component tested independently
2. **Integration Tests**: Full pipeline with sample documents
3. **Regression Tests**: Ensure existing functionality works
4. **Performance Tests**: Measure processing time for 100+ documents
5. **Accuracy Tests**: Validate extraction accuracy against known data

## Migration Plan

1. **Phase 1**: Add new components alongside existing code
2. **Phase 2**: Integrate type detection into upload flow
3. **Phase 3**: Add duplicate detection
4. **Phase 4**: Implement extraction rules for each document type
5. **Phase 5**: Update report generation with new data
6. **Phase 6**: Remove old generic extraction code

## Next Steps
See `tasks.md` for detailed implementation tasks.

