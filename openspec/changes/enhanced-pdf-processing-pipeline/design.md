# Design: Enhanced PDF Processing Pipeline

## Change ID
`PDF-PIPELINE-002`

## Version
1.0.0

## Status
Draft

## Last Updated
2026-02-08

---

## Design Overview

This document describes the design approach for implementing an enhanced PDF processing pipeline with OCR, advanced extraction, and data normalization.

---

## Part 1: Multi-Layer Text Extraction Design

### Extraction Strategy Decision Tree

```
┌─────────────────────────┐
│   Load PDF Page         │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│ Extract Text Layer      │
└───────────┬─────────────┘
            │
            ▼
      ┌─────────────┐
      │ Has Text?   │
      └──┬──────┬───┘
         │ Yes  │ No
         │      │
         │      ▼
         │  ┌─────────────────┐
         │  │ Detect Images   │
         │  └──┬──────────────┘
         │     │
         │     ▼
         │  ┌─────────────┐
         │  │ Image-Based?│
         │  └──┬──────┬───┘
         │     │ Yes  │ No
         │     │      │
         │     ▼      ▼
         │  ┌────┐ ┌──────────┐
         │  │OCR │ │ Layout   │
         │  │    │ │ Analysis │
         │  └────┘ └──────────┘
         │     │      │
         └─────┴──────┘
               │
               ▼
         ┌─────────────┐
         │ Return Text │
         └─────────────┘
```

### Text Quality Scoring

```javascript
function scoreTextQuality(textContent) {
  const text = textContent.items.map(i => i.str).join(' ');
  
  // Metrics
  const wordCount = text.split(/\s+/).length;
  const avgWordLength = text.length / wordCount;
  const alphaRatio = (text.match(/[a-zA-Z]/g) || []).length / text.length;
  const digitRatio = (text.match(/\d/g) || []).length / text.length;
  
  // Scoring
  let score = 0;
  if (wordCount > 50) score += 0.4;
  if (avgWordLength > 3 && avgWordLength < 10) score += 0.3;
  if (alphaRatio > 0.5) score += 0.2;
  if (digitRatio > 0.05 && digitRatio < 0.5) score += 0.1;
  
  return score; // 0.0 to 1.0
}
```

---

## Part 2: OCR Integration Design

### OCR Workflow

```
┌─────────────────────────────────────────────────┐
│ 1. Render PDF Page to Canvas                   │
│    - High resolution (2x scale)                 │
│    - RGB color space                            │
└─────────────────┬───────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────┐
│ 2. Pre-process Image                            │
│    - Convert to grayscale                       │
│    - Adjust contrast                            │
│    - Denoise                                    │
│    - Binarize (threshold)                       │
└─────────────────┬───────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────┐
│ 3. Perform OCR (Tesseract.js)                   │
│    - Use web worker                             │
│    - Track progress                             │
│    - Extract text + confidence                  │
└─────────────────┬───────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────┐
│ 4. Post-process Results                         │
│    - Correct common OCR errors                  │
│    - Calculate overall confidence               │
│    - Identify low-confidence regions            │
└─────────────────┬───────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────┐
│ 5. Cache Results                                │
│    - Store in localStorage                      │
│    - Key by document hash                       │
└─────────────────────────────────────────────────┘
```

### Image Pre-processing Algorithms

#### Grayscale Conversion
```javascript
function toGrayscale(imageData) {
  const data = imageData.data;
  for (let i = 0; i < data.length; i += 4) {
    const gray = 0.299 * data[i] + 0.587 * data[i+1] + 0.114 * data[i+2];
    data[i] = data[i+1] = data[i+2] = gray;
  }
  return imageData;
}
```

#### Contrast Adjustment
```javascript
function adjustContrast(imageData, factor) {
  const data = imageData.data;
  const intercept = 128 * (1 - factor);
  
  for (let i = 0; i < data.length; i += 4) {
    data[i] = data[i] * factor + intercept;
    data[i+1] = data[i+1] * factor + intercept;
    data[i+2] = data[i+2] * factor + intercept;
  }
  return imageData;
}
```

#### Binarization (Otsu's Method)
```javascript
function binarize(imageData, threshold) {
  const data = imageData.data;
  
  for (let i = 0; i < data.length; i += 4) {
    const value = data[i] > threshold ? 255 : 0;
    data[i] = data[i+1] = data[i+2] = value;
  }
  return imageData;
}
```

---

## Part 3: Data Normalization Design

### Date Parsing Strategy

```javascript
const datePatterns = [
  {
    regex: /(\d{1,2})\/(\d{1,2})\/(\d{4})/,
    parser: (m) => new Date(m[3], m[1]-1, m[2]),
    name: 'MM/DD/YYYY'
  },
  {
    regex: /(\d{4})-(\d{2})-(\d{2})/,
    parser: (m) => new Date(m[1], m[2]-1, m[3]),
    name: 'YYYY-MM-DD'
  },
  {
    regex: /(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\w*\s+(\d{1,2}),?\s+(\d{4})/i,
    parser: (m) => new Date(`${m[1]} ${m[2]}, ${m[3]}`),
    name: 'Month DD, YYYY'
  }
];
```

### Amount Parsing Strategy

```javascript
const amountPatterns = [
  {
    regex: /\$\s*([\d,]+\.\d{2})/,
    parser: (m) => parseFloat(m[1].replace(/,/g, '')),
    name: 'USD with symbol'
  },
  {
    regex: /\(([\d,]+\.\d{2})\)/,
    parser: (m) => -parseFloat(m[1].replace(/,/g, '')),
    name: 'Negative in parentheses'
  },
  {
    regex: /([\d,]+\.\d{2})\s*CR/i,
    parser: (m) => parseFloat(m[1].replace(/,/g, '')),
    name: 'Credit notation'
  },
  {
    regex: /([\d,]+\.\d{2})\s*DR/i,
    parser: (m) => -parseFloat(m[1].replace(/,/g, '')),
    name: 'Debit notation'
  }
];
```

### Validation Rules

```javascript
const validationRules = {
  date: {
    required: true,
    minYear: 1900,
    maxYear: 2100,
    validator: (date) => {
      if (!(date instanceof Date) || isNaN(date)) return false;
      const year = date.getFullYear();
      return year >= 1900 && year <= 2100;
    }
  },

  amount: {
    required: true,
    minValue: -1000000000,
    maxValue: 1000000000,
    validator: (amount) => {
      if (typeof amount !== 'number' || isNaN(amount)) return false;
      return Math.abs(amount) <= 1000000000;
    }
  },

  accountNumber: {
    required: false,
    pattern: /^\d{4,}$/,
    validator: (acct) => {
      return /^\d{4,}$/.test(acct);
    }
  }
};
```

---

## Part 4: Performance Optimization Design

### Web Worker Architecture

```javascript
// Main thread
class OCRProcessor {
  constructor() {
    this.worker = new Worker('ocr-worker.js');
    this.worker.onmessage = (e) => this.handleWorkerMessage(e);
  }

  async processPage(imageData) {
    return new Promise((resolve, reject) => {
      this.worker.postMessage({ type: 'process', imageData });
      this.pendingResolve = resolve;
      this.pendingReject = reject;
    });
  }
}

// Worker thread (ocr-worker.js)
importScripts('tesseract.min.js');

self.onmessage = async (e) => {
  if (e.data.type === 'process') {
    const result = await Tesseract.recognize(e.data.imageData);
    self.postMessage({ type: 'result', data: result });
  }
};
```

### Caching Strategy

```javascript
class OCRCache {
  constructor() {
    this.maxSize = 10 * 1024 * 1024; // 10MB
    this.expirationDays = 30;
  }

  async get(documentHash, pageNumber) {
    const key = `ocr_${documentHash}_${pageNumber}`;
    const cached = localStorage.getItem(key);

    if (!cached) return null;

    const data = JSON.parse(cached);

    // Check expiration
    if (Date.now() - data.timestamp > this.expirationDays * 86400000) {
      localStorage.removeItem(key);
      return null;
    }

    return data.result;
  }

  async set(documentHash, pageNumber, result) {
    const key = `ocr_${documentHash}_${pageNumber}`;
    const data = {
      result,
      timestamp: Date.now()
    };

    // Check size before storing
    const size = JSON.stringify(data).length;
    if (this.getCurrentSize() + size > this.maxSize) {
      this.cleanup();
    }

    localStorage.setItem(key, JSON.stringify(data));
  }

  cleanup() {
    // Remove oldest entries
    const keys = Object.keys(localStorage).filter(k => k.startsWith('ocr_'));
    const entries = keys.map(k => ({
      key: k,
      timestamp: JSON.parse(localStorage.getItem(k)).timestamp
    }));

    entries.sort((a, b) => a.timestamp - b.timestamp);

    // Remove oldest 25%
    const toRemove = Math.ceil(entries.length * 0.25);
    for (let i = 0; i < toRemove; i++) {
      localStorage.removeItem(entries[i].key);
    }
  }
}
```

---

## Part 5: Error Handling Design

### Error Types and Recovery

```javascript
class ExtractionError extends Error {
  constructor(type, message, recoverable = false) {
    super(message);
    this.type = type;
    this.recoverable = recoverable;
  }
}

const errorTypes = {
  NO_TEXT: { recoverable: true, fallback: 'ocr' },
  OCR_FAILED: { recoverable: true, fallback: 'manual' },
  PARSE_FAILED: { recoverable: true, fallback: 'skip' },
  VALIDATION_FAILED: { recoverable: true, fallback: 'flag' },
  CRITICAL: { recoverable: false, fallback: null }
};

async function extractWithRecovery(page) {
  try {
    return await extractText(page);
  } catch (error) {
    if (error.type === 'NO_TEXT') {
      // Fallback to OCR
      return await performOCR(page);
    } else if (error.type === 'OCR_FAILED') {
      // Allow manual correction
      return await requestManualInput(page);
    } else {
      throw error;
    }
  }
}
```

---

## Implementation Approach

### Phase 1: Text Extraction (Low Risk)
- Build on existing PDF.js integration
- Add table detection incrementally
- No breaking changes to existing code

### Phase 2: OCR (Medium Risk)
- Add as optional enhancement
- Graceful degradation if OCR fails
- Extensive testing with various scan qualities

### Phase 3: Normalization (Low Risk)
- Pure data transformation
- Easy to test and validate
- No impact on extraction logic

### Phase 4: Testing (Critical)
- Test with 100+ diverse PDFs
- Performance profiling
- User acceptance testing

---

## Accessibility Considerations

- Progress indicators for long OCR operations
- Keyboard shortcuts for manual correction
- Screen reader announcements for processing status
- High contrast UI for low-confidence regions
- Alternative text for visual indicators

---

## Security Considerations

- All processing client-side (no data sent to servers)
- OCR library loaded from trusted CDN
- Cache stored in localStorage (user-controlled)
- No sensitive data in error logs
- Document hashes use SHA-256


