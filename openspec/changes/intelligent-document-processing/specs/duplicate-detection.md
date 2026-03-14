# Specification: Duplicate Detection

## Overview
The Duplicate Detection system identifies and filters duplicate documents to prevent redundant processing and data duplication in reports.

## Requirements

### Functional Requirements

**FR-1**: System SHALL detect exact file duplicates (same binary content)
**FR-2**: System SHALL detect semantic duplicates (same statement, different file)
**FR-3**: System SHALL track duplicate detection method and confidence
**FR-4**: System SHALL preserve first occurrence and skip subsequent duplicates
**FR-5**: System SHALL report all duplicates with reasons in summary
**FR-6**: System SHALL allow manual override to process duplicates

### Non-Functional Requirements

**NFR-1**: Duplicate detection SHALL complete within 100ms per document
**NFR-2**: System SHALL handle 500+ documents without performance degradation
**NFR-3**: False positive rate SHALL be < 1%

## Duplicate Detection Rules

### Rule 1: Exact File Hash (100% Confidence)

**Description**: Compare SHA-256 hash of file contents

**Algorithm**:
```javascript
async function computeFileHash(file) {
  const buffer = await file.arrayBuffer();
  const hashBuffer = await crypto.subtle.digest('SHA-256', buffer);
  const hashArray = Array.from(new Uint8Array(hashBuffer));
  return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
}

function checkExactDuplicate(fileHash, processedHashes) {
  if (processedHashes.has(fileHash)) {
    return {
      isDuplicate: true,
      confidence: 1.0,
      reason: 'exact-file-match',
      method: 'file-hash'
    };
  }
  return { isDuplicate: false };
}
```

**Use Case**: User uploads same file twice (e.g., `statement.pdf` and `statement (1).pdf`)

### Rule 2: Account + Period Match (95% Confidence)

**Description**: Compare account number, statement period, and provider

**Algorithm**:
```javascript
function checkAccountPeriodDuplicate(extractedData, processedDocuments) {
  const key = {
    accountNumber: extractedData.account.number,
    periodStart: extractedData.period.start,
    periodEnd: extractedData.period.end,
    provider: extractedData.document.provider
  };

  for (const doc of processedDocuments) {
    if (doc.account.number === key.accountNumber &&
        doc.period.start === key.periodStart &&
        doc.period.end === key.periodEnd &&
        doc.document.provider === key.provider) {
      return {
        isDuplicate: true,
        confidence: 0.95,
        reason: 'account-period-match',
        method: 'semantic',
        matchedDocument: doc.document.id
      };
    }
  }

  return { isDuplicate: false };
}
```

**Use Case**: Same Chase statement downloaded twice with different filenames

**Example**:
- File 1: `20250530-statements-7969-.pdf`
- File 2: `20250530-statements-7969- (1).pdf`
- Both have: Account `****7969`, Period `2025-05-01` to `2025-05-30`, Provider `Chase`
- Result: Duplicate detected

### Rule 3: Filename Similarity (80% Confidence)

**Description**: Normalize and compare filename patterns

**Algorithm**:
```javascript
function normalizeFilename(filename) {
  // Remove common suffixes
  let normalized = filename.replace(/\s*\(\d+\)\.pdf$/i, '.pdf');
  
  // Normalize dates
  normalized = normalized.replace(/\d{8}/g, 'YYYYMMDD');
  
  // Remove extensions
  normalized = normalized.replace(/\.pdf$/i, '');
  
  return normalized.toLowerCase();
}

function checkFilenameSimilarity(filename, processedFilenames) {
  const normalized = normalizeFilename(filename);
  
  for (const [processedFile, processedNormalized] of processedFilenames) {
    if (normalized === processedNormalized) {
      return {
        isDuplicate: true,
        confidence: 0.80,
        reason: 'filename-similarity',
        method: 'filename-pattern',
        matchedFilename: processedFile
      };
    }
  }
  
  return { isDuplicate: false };
}
```

**Use Case**: Browser auto-renamed files

**Examples**:
- `statement.pdf` vs `statement (1).pdf` → Duplicate
- `20250530-statements-7969-.pdf` vs `20250530-statements-7969- (2).pdf` → Duplicate

### Rule 4: Content Fingerprint (85% Confidence)

**Description**: Hash key financial fields to detect semantic duplicates

**Algorithm**:
```javascript
function computeContentFingerprint(extractedData) {
  const keyFields = {
    account: extractedData.account.number,
    provider: extractedData.document.provider,
    total: extractedData.financial.totalAmount,
    date: extractedData.period.end,
    type: extractedData.document.type
  };
  
  const fingerprintString = JSON.stringify(keyFields);
  return simpleHash(fingerprintString);
}

function checkContentFingerprint(fingerprint, processedFingerprints) {
  if (processedFingerprints.has(fingerprint)) {
    return {
      isDuplicate: true,
      confidence: 0.85,
      reason: 'content-fingerprint-match',
      method: 'content-hash'
    };
  }
  return { isDuplicate: false };
}
```

**Use Case**: Same bill from different sources (email vs download)

## Detection Pipeline

### Processing Order
1. **File Hash Check** (fastest, highest confidence)
2. **Filename Similarity** (fast, medium confidence)
3. **Content Fingerprint** (medium speed, high confidence)
4. **Account + Period Match** (slowest, highest semantic confidence)

### Decision Logic
```javascript
async function detectDuplicate(file, extractedData, registry) {
  // Check 1: Exact file hash
  const fileHash = await computeFileHash(file);
  const exactMatch = checkExactDuplicate(fileHash, registry.fileHashes);
  if (exactMatch.isDuplicate) return exactMatch;

  // Check 2: Filename similarity
  const filenameMatch = checkFilenameSimilarity(file.name, registry.filenames);
  if (filenameMatch.isDuplicate && filenameMatch.confidence >= 0.80) {
    return filenameMatch;
  }

  // Check 3: Content fingerprint (requires extraction)
  if (extractedData) {
    const fingerprint = computeContentFingerprint(extractedData);
    const fingerprintMatch = checkContentFingerprint(fingerprint, registry.fingerprints);
    if (fingerprintMatch.isDuplicate) return fingerprintMatch;

    // Check 4: Account + period match
    const accountMatch = checkAccountPeriodDuplicate(extractedData, registry.documents);
    if (accountMatch.isDuplicate) return accountMatch;
  }

  return { isDuplicate: false };
}
```

## Registry Data Structure

```javascript
const duplicateRegistry = {
  fileHashes: new Set(),           // SHA-256 hashes
  filenames: new Map(),            // filename → normalized filename
  fingerprints: new Set(),         // Content fingerprints
  documents: [],                   // Processed document data
  duplicates: []                   // Detected duplicates
};
```

## Output Format

### Duplicate Detected
```javascript
{
  isDuplicate: true,
  confidence: 0.95,
  reason: 'account-period-match',
  method: 'semantic',
  matchedDocument: {
    id: 'doc-uuid-123',
    filename: '20250530-statements-7969-.pdf',
    uploadDate: '2025-01-15T10:30:00Z'
  },
  currentFile: {
    filename: '20250530-statements-7969- (1).pdf',
    uploadDate: '2025-01-15T10:35:00Z'
  }
}
```

### Not Duplicate
```javascript
{
  isDuplicate: false
}
```

## User Interface

### Duplicate Summary Section
```
Duplicate Detection Summary
---------------------------
Total Files Uploaded: 25
Unique Documents: 18
Duplicates Detected: 7

Duplicates:
1. statement (1).pdf → Duplicate of statement.pdf (Exact match)
2. 20250530-statements-7969- (2).pdf → Duplicate of 20250530-statements-7969-.pdf (Account + Period match)
3. invoice-copy.pdf → Duplicate of invoice.pdf (Content fingerprint match)
...

[Show All Duplicates] [Process Duplicates Anyway]
```

## Configuration

### Duplicate Detection Settings
```javascript
const duplicateConfig = {
  enabled: true,
  strictMode: false,              // If true, only exact matches count
  confidenceThreshold: 0.70,      // Minimum confidence to mark as duplicate
  allowManualOverride: true,      // Allow user to force process duplicates
  reportDuplicates: true          // Include duplicates in report summary
};
```

## Edge Cases

1. **Partial Extraction Failure**: If extraction fails, only use file hash and filename
2. **Multiple Accounts**: Same period but different accounts → Not duplicate
3. **Amended Statements**: Same period but different amounts → Not duplicate (low confidence)
4. **Corrected Statements**: Provider reissues statement → User decides

## Testing

### Test Cases
1. Upload same file twice → Detected as exact duplicate
2. Upload same statement with different filename → Detected as semantic duplicate
3. Upload statements from different months → Not duplicate
4. Upload statements from different accounts → Not duplicate
5. Upload 100 files with 20 duplicates → All 20 detected correctly

### Performance Tests
- 500 files with 100 duplicates → Detection completes in < 10 seconds
- Memory usage stays < 100MB for 500 files

### Acceptance Criteria
- 100% detection of exact duplicates
- 95% detection of semantic duplicates
- < 1% false positive rate
- < 100ms per document detection time

