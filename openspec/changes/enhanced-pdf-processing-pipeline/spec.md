# Specification: Enhanced PDF Processing Pipeline

## Change ID
`PDF-PIPELINE-002`

## Version
1.0.0

## Status
Draft

## Last Updated
2026-02-08

---

## Overview

This specification details the implementation of an enhanced PDF processing pipeline with multi-layer text extraction, OCR capabilities, and intelligent data normalization.

---

## Part 1: Advanced Text Extraction

### 1.1 Multi-Layer Extraction Strategy

#### Layer 1: PDF Text Layer (Primary)
- **Method**: PDF.js `getTextContent()`
- **Speed**: Fast (~100ms per page)
- **Accuracy**: 100% for text-based PDFs
- **Use case**: Standard PDFs with embedded text

#### Layer 2: Layout Analysis (Secondary)
- **Method**: Canvas rendering + position analysis
- **Speed**: Medium (~500ms per page)
- **Accuracy**: 90% for structured documents
- **Use case**: Tables, multi-column layouts

#### Layer 3: OCR (Tertiary)
- **Method**: Tesseract.js
- **Speed**: Slow (~3-5s per page)
- **Accuracy**: 85-95% depending on quality
- **Use case**: Scanned PDFs, images

### 1.2 Extraction Decision Tree

```javascript
async function extractText(page) {
  // Try text layer first
  const textContent = await page.getTextContent();
  
  if (hasSignificantText(textContent)) {
    return { text: extractFromTextLayer(textContent), method: 'text-layer', confidence: 1.0 };
  }
  
  // Check if page is image-based
  const isImageBased = await detectImageBasedPage(page);
  
  if (isImageBased) {
    // Use OCR
    return await performOCR(page);
  }
  
  // Try layout analysis for complex structures
  return await analyzeLayout(page);
}
```

### 1.3 Table Detection and Extraction

```javascript
class TableExtractor {
  detectTables(textContent) {
    // Analyze text positions to find grid patterns
    const grid = this.buildPositionGrid(textContent);
    const tables = this.findTableRegions(grid);
    return tables;
  }
  
  extractTable(tableRegion) {
    // Convert table region to structured data
    const rows = this.groupIntoRows(tableRegion);
    const columns = this.detectColumns(rows);
    return this.buildTableData(rows, columns);
  }
}
```

---

## Part 2: OCR Integration

### 2.1 Tesseract.js Configuration

```javascript
const ocrConfig = {
  lang: 'eng',
  oem: 1, // LSTM neural net mode
  psm: 3, // Fully automatic page segmentation
  tessedit_char_whitelist: '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz$.,-()/: ',
};
```

### 2.2 Image Pre-processing

```javascript
class ImagePreprocessor {
  async enhance(imageData) {
    // 1. Convert to grayscale
    const grayscale = this.toGrayscale(imageData);
    
    // 2. Increase contrast
    const contrasted = this.adjustContrast(grayscale, 1.5);
    
    // 3. Denoise
    const denoised = this.denoise(contrasted);
    
    // 4. Binarize (black and white)
    const binary = this.binarize(denoised, 128);
    
    return binary;
  }
}
```

### 2.3 OCR Processor

```javascript
class OCRProcessor {
  async processPage(page, progressCallback) {
    // Render page to canvas
    const canvas = await this.renderToCanvas(page);
    
    // Pre-process image
    const preprocessor = new ImagePreprocessor();
    const enhanced = await preprocessor.enhance(canvas);
    
    // Perform OCR
    const result = await Tesseract.recognize(enhanced, 'eng', {
      logger: (m) => progressCallback(m.progress)
    });
    
    return {
      text: result.data.text,
      confidence: result.data.confidence / 100,
      method: 'ocr',
      words: result.data.words
    };
  }
}
```

### 2.4 Confidence Scoring

```javascript
function calculateConfidence(ocrResult) {
  const wordConfidences = ocrResult.words.map(w => w.confidence);
  const avgConfidence = wordConfidences.reduce((a, b) => a + b, 0) / wordConfidences.length;
  
  // Penalize if too many low-confidence words
  const lowConfWords = wordConfidences.filter(c => c < 60).length;
  const penalty = lowConfWords / wordConfidences.length;
  
  return Math.max(0, avgConfidence - (penalty * 20));
}
```

---

## Part 3: Data Normalization

### 3.1 Date Parser

```javascript
class DateParser {
  parse(dateString) {
    const formats = [
      /(\d{1,2})\/(\d{1,2})\/(\d{4})/,           // MM/DD/YYYY
      /(\d{4})-(\d{2})-(\d{2})/,                 // YYYY-MM-DD
      /(\w+)\s+(\d{1,2}),?\s+(\d{4})/,           // Month DD, YYYY
      /(\d{1,2})-(\w+)-(\d{4})/,                 // DD-Mon-YYYY
    ];
    
    for (const format of formats) {
      const match = dateString.match(format);
      if (match) {
        return this.parseMatch(match, format);
      }
    }
    
    throw new Error(`Unable to parse date: ${dateString}`);
  }
}
```

### 3.2 Amount Parser

```javascript
class AmountParser {
  parse(amountString) {
    // Remove currency symbols and whitespace
    let cleaned = amountString.replace(/[$€£¥\s]/g, '');

    // Handle parentheses (negative)
    const isNegative = cleaned.startsWith('(') && cleaned.endsWith(')');
    if (isNegative) {
      cleaned = cleaned.slice(1, -1);
    }

    // Remove commas
    cleaned = cleaned.replace(/,/g, '');

    // Parse float
    const amount = parseFloat(cleaned);

    if (isNaN(amount)) {
      throw new Error(`Unable to parse amount: ${amountString}`);
    }

    return isNegative ? -amount : amount;
  }
}
```

### 3.3 Field Validators

```javascript
class FieldValidator {
  validateDate(date) {
    if (!(date instanceof Date) || isNaN(date)) {
      return { valid: false, error: 'Invalid date' };
    }

    // Check reasonable range (1900-2100)
    const year = date.getFullYear();
    if (year < 1900 || year > 2100) {
      return { valid: false, error: 'Date out of range' };
    }

    return { valid: true };
  }

  validateAmount(amount) {
    if (typeof amount !== 'number' || isNaN(amount)) {
      return { valid: false, error: 'Invalid amount' };
    }

    // Check reasonable range
    if (Math.abs(amount) > 1000000000) {
      return { valid: false, error: 'Amount too large' };
    }

    return { valid: true };
  }
}
```

### 3.4 OCR Error Correction

```javascript
class OCRErrorCorrector {
  correctCommonErrors(text) {
    const corrections = {
      // Common OCR mistakes
      'O': '0',  // Letter O → Zero (in numeric contexts)
      'l': '1',  // Lowercase L → One (in numeric contexts)
      'I': '1',  // Capital I → One (in numeric contexts)
      'S': '5',  // S → 5 (in numeric contexts)
      'B': '8',  // B → 8 (in numeric contexts)
    };

    // Apply corrections in numeric contexts
    return this.smartCorrect(text, corrections);
  }

  smartCorrect(text, corrections) {
    // Only correct in contexts that should be numeric
    // (e.g., after $, in date patterns, etc.)
    return text; // Implementation details
  }
}
```

---

## Part 4: Integration Architecture

### 4.1 Processing Pipeline

```
┌─────────────────────────────────────────────────┐
│           PDF Document Upload                   │
└─────────────────┬───────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────┐
│     AdvancedTextExtractor                       │
│  - Detect extraction method needed              │
│  - Try text layer → layout → OCR                │
│  - Extract tables if present                    │
└─────────────────┬───────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────┐
│     DataNormalizer                              │
│  - Parse dates to ISO 8601                      │
│  - Parse amounts to float                       │
│  - Validate all fields                          │
│  - Correct OCR errors                           │
└─────────────────┬───────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────┐
│     DocumentTypeDetector                        │
│  - Use normalized data for detection            │
└─────────────────┬───────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────┐
│     ExtractionEngine                            │
│  - Apply type-specific rules                    │
│  - Use validated, normalized data               │
└─────────────────┬───────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────┐
│     Report Generation                           │
└─────────────────────────────────────────────────┘
```

---

## Success Metrics

1. **Coverage**: Process 100% of PDFs (including scanned)
2. **OCR Accuracy**: >85% for clear scans, >70% for poor quality
3. **Date Parsing**: >95% accuracy across all formats
4. **Amount Parsing**: >95% accuracy across all formats
5. **Performance**: <5s per page including OCR
6. **Error Rate**: <5% failed extractions requiring manual review


