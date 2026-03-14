# Specification: Enhanced Document Detection

## Overview
Improve document type detection to accurately identify Amazon invoices, bank statements, and utility bills.

---

## Requirements

### Functional Requirements

#### FR-1: Amazon Invoice Detection
- Shall detect files matching pattern `amzn-*.pdf` or `Anna_amzn-*.pdf`
- Shall identify Amazon from content keywords: "amazon", "order", "invoice"
- Shall achieve >90% detection accuracy
- Shall assign confidence score of 0.95 for filename match

#### FR-2: Chase Bank Statement Detection
- Shall detect files matching pattern `YYYYMMDD-statements-XXXX-.pdf`
- Shall identify Chase from content keywords: "chase", "account statement"
- Shall achieve >90% detection accuracy
- Shall assign confidence score of 0.95 for filename match

#### FR-3: Water/Sewer Bill Detection
- Shall detect files matching pattern `UB#####-#-YYYYMMDD.pdf`
- Shall identify from content keywords: "water", "sewer", "utility"
- Shall achieve >85% detection accuracy
- Shall assign confidence score of 0.90 for filename match

#### FR-4: Xfinity Bill Detection
- Shall detect files matching pattern `DetailedBill[Month][Year].pdf`
- Shall identify Xfinity from content keywords: "xfinity", "comcast", "internet"
- Shall achieve >85% detection accuracy
- Shall assign confidence score of 0.90 for filename match

#### FR-5: T-Mobile Bill Detection
- Shall detect files matching pattern `[hash]_[account]_MM-DD-YYYY.pdf`
- Shall identify T-Mobile from content keywords: "t-mobile", "wireless"
- Shall achieve >80% detection accuracy
- Shall assign confidence score of 0.85 for filename match

#### FR-6: Generic Invoice Detection
- Shall detect files matching pattern `Invoice #-##-#-#######-[a-z]#?.pdf`
- Shall identify from content keywords: "invoice", "bill to", "total"
- Shall achieve >75% detection accuracy
- Shall assign confidence score of 0.85 for filename match

---

## Technical Specification

### Detection Patterns

```javascript
const documentPatterns = {
  'amazon-invoice': {
    filenamePatterns: [
      {
        regex: /^amzn-\d+\.pdf$/i,
        provider: 'Amazon',
        confidence: 0.95
      },
      {
        regex: /^Anna_amzn-\d+\.pdf$/i,
        provider: 'Amazon',
        confidence: 0.95
      }
    ],
    contentKeywords: ['amazon', 'order', 'invoice', 'items ordered', 'order total'],
    type: 'invoice',
    subtype: 'retail',
    provider: 'Amazon'
  },
  
  'chase-bank-statement': {
    filenamePatterns: [
      {
        regex: /^\d{8}-statements-\d+.*\.pdf$/i,
        provider: 'Chase',
        confidence: 0.95
      }
    ],
    contentKeywords: ['chase', 'account statement', 'beginning balance', 'ending balance', 'deposits', 'withdrawals'],
    type: 'bank-statement',
    subtype: 'checking',
    provider: 'Chase'
  },
  
  'water-sewer-bill': {
    filenamePatterns: [
      {
        regex: /^UB\d+-\d+-\d{8}\.pdf$/i,
        provider: 'Local Utility',
        confidence: 0.90
      }
    ],
    contentKeywords: ['water', 'sewer', 'utility bill', 'account number', 'billing period'],
    type: 'utility-bill',
    subtype: 'water-sewer',
    provider: 'Local Utility'
  },
  
  'xfinity-bill': {
    filenamePatterns: [
      {
        regex: /^DetailedBill[A-Za-z]{3}\d{4}\.pdf$/i,
        provider: 'Xfinity',
        confidence: 0.90
      }
    ],
    contentKeywords: ['xfinity', 'comcast', 'internet', 'cable', 'tv', 'phone'],
    type: 'utility-bill',
    subtype: 'internet-cable',
    provider: 'Xfinity'
  },
  
  'tmobile-bill': {
    filenamePatterns: [
      {
        regex: /^[a-f0-9]{128}_\d+_\d{2}-\d{2}-\d{4}\.pdf$/i,
        provider: 'T-Mobile',
        confidence: 0.85
      }
    ],
    contentKeywords: ['t-mobile', 'wireless', 'mobile', 'phone', 'data'],
    type: 'utility-bill',
    subtype: 'mobile-phone',
    provider: 'T-Mobile'
  },
  
  'generic-invoice': {
    filenamePatterns: [
      {
        regex: /^Invoice\s+\d+-\d+-\d+-\d+-[a-z]\d?\.pdf$/i,
        provider: null,
        confidence: 0.85
      }
    ],
    contentKeywords: ['invoice', 'bill to', 'total amount', 'due date'],
    type: 'invoice',
    subtype: 'generic',
    provider: null
  }
};
```

### Detection Algorithm

```javascript
class EnhancedDocumentTypeDetector {
  detect(filename, content) {
    // Step 1: Try filename matching
    const filenameResult = this.detectByFilename(filename);
    
    // Step 2: Try content matching
    const contentResult = this.detectByContent(content);
    
    // Step 3: Hybrid scoring
    if (filenameResult.confidence > 0 && contentResult.confidence > 0) {
      return this.hybridDetection(filenameResult, contentResult);
    }
    
    // Step 4: Return best result
    if (filenameResult.confidence >= contentResult.confidence) {
      return filenameResult;
    }
    return contentResult;
  }
  
  detectByFilename(filename) {
    for (const [typeId, config] of Object.entries(documentPatterns)) {
      for (const pattern of config.filenamePatterns) {
        if (pattern.regex.test(filename)) {
          return {
            type: config.type,
            subtype: config.subtype,
            provider: pattern.provider || config.provider,
            confidence: pattern.confidence,
            method: 'filename',
            typeId: typeId
          };
        }
      }
    }
    
    return { type: 'unknown', confidence: 0, method: 'filename' };
  }
  
  detectByContent(content) {
    const contentLower = content.toLowerCase();
    const matches = [];
    
    for (const [typeId, config] of Object.entries(documentPatterns)) {
      let keywordMatches = 0;
      const foundKeywords = [];
      
      for (const keyword of config.contentKeywords) {
        if (contentLower.includes(keyword.toLowerCase())) {
          keywordMatches++;
          foundKeywords.push(keyword);
        }
      }
      
      if (keywordMatches > 0) {
        const confidence = Math.min(0.95, 0.5 + (keywordMatches / config.contentKeywords.length) * 0.45);
        matches.push({
          type: config.type,
          subtype: config.subtype,
          provider: config.provider,
          confidence: confidence,
          method: 'content',
          typeId: typeId,
          keywordMatches: keywordMatches,
          foundKeywords: foundKeywords
        });
      }
    }
    
    if (matches.length === 0) {
      return { type: 'unknown', confidence: 0, method: 'content' };
    }
    
    // Return highest confidence match
    matches.sort((a, b) => b.confidence - a.confidence);
    return matches[0];
  }
  
  hybridDetection(filenameResult, contentResult) {
    // If both agree, high confidence
    if (filenameResult.typeId === contentResult.typeId) {
      return {
        ...filenameResult,
        confidence: Math.min(0.98, filenameResult.confidence * 0.4 + contentResult.confidence * 0.6),
        method: 'hybrid',
        filenameConfidence: filenameResult.confidence,
        contentConfidence: contentResult.confidence
      };
    }
    
    // If they disagree, use weighted average
    const finalConfidence = filenameResult.confidence * 0.4 + contentResult.confidence * 0.6;
    
    if (contentResult.confidence > filenameResult.confidence) {
      return {
        ...contentResult,
        confidence: finalConfidence,
        method: 'hybrid-content-preferred'
      };
    }
    
    return {
      ...filenameResult,
      confidence: finalConfidence,
      method: 'hybrid-filename-preferred'
    };
  }
}
```

---

## Acceptance Criteria

- [ ] Amazon invoices detected with >90% accuracy
- [ ] Chase bank statements detected with >90% accuracy
- [ ] Water/sewer bills detected with >85% accuracy
- [ ] Xfinity bills detected with >85% accuracy
- [ ] T-Mobile bills detected with >80% accuracy
- [ ] Generic invoices detected with >75% accuracy
- [ ] Hybrid detection improves accuracy by >5%
- [ ] No false positives for known document types
- [ ] Unknown documents gracefully handled
- [ ] Provider correctly identified for all major providers

