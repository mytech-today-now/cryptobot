# Specification: Enhanced Transaction Categorization

## Overview
Improve transaction categorization to properly classify bills as expenses and bank deposits as income.

---

## Requirements

### Functional Requirements

#### FR-1: Bill Categorization
- All utility bills shall be categorized as expenses
- All invoices shall be categorized as expenses
- Subcategories shall be assigned based on provider/type
- Confidence score shall be >0.90 for bills

#### FR-2: Bank Statement Categorization
- Positive amounts (deposits) shall be categorized as income
- Negative amounts (withdrawals) shall be categorized as expenses
- Transaction descriptions shall be analyzed for better categorization
- Confidence score shall be >0.85 for bank transactions

#### FR-3: Provider-Based Categorization
- Amazon → Shopping/Retail
- Xfinity → Utilities/Internet
- T-Mobile → Utilities/Phone
- Water/Sewer → Utilities/Water
- ComEd → Utilities/Electric
- Chase deposits → Income/Deposit

---

## Technical Specification

### Categorization Rules

```javascript
const categorizationRules = {
  // Document type based rules
  'utility-bill': {
    type: 'expense',
    category: 'utilities',
    confidence: 0.95,
    subcategoryMap: {
      'water-sewer': 'water-sewer',
      'internet-cable': 'internet',
      'mobile-phone': 'phone',
      'electric': 'electric',
      'gas': 'gas'
    }
  },
  
  'invoice': {
    type: 'expense',
    category: 'shopping',
    confidence: 0.90,
    providerMap: {
      'Amazon': 'retail',
      'default': 'general'
    }
  },
  
  'bank-statement': {
    // Amount-based categorization
    rules: [
      {
        condition: (amount) => amount > 0,
        type: 'income',
        category: 'deposit',
        confidence: 0.85
      },
      {
        condition: (amount) => amount < 0,
        type: 'expense',
        category: 'withdrawal',
        confidence: 0.85
      }
    ]
  }
};

const providerCategories = {
  'Amazon': { category: 'shopping', subcategory: 'retail' },
  'Xfinity': { category: 'utilities', subcategory: 'internet' },
  'T-Mobile': { category: 'utilities', subcategory: 'phone' },
  'Local Utility': { category: 'utilities', subcategory: 'water-sewer' },
  'ComEd': { category: 'utilities', subcategory: 'electric' },
  'Chase': { category: 'banking', subcategory: 'account' }
};
```

### Categorization Algorithm

```javascript
class TransactionCategorizer {
  categorize(transaction, documentType, provider) {
    // Step 1: Check document type rules
    const typeRule = categorizationRules[documentType];
    
    if (typeRule) {
      // For bills and invoices
      if (typeRule.type === 'expense') {
        return {
          type: 'expense',
          category: typeRule.category,
          subcategory: this.getSubcategory(typeRule, documentType, provider),
          confidence: typeRule.confidence,
          reason: `Document type: ${documentType}`
        };
      }
      
      // For bank statements (amount-based)
      if (typeRule.rules) {
        for (const rule of typeRule.rules) {
          if (rule.condition(transaction.amount)) {
            return {
              type: rule.type,
              category: rule.category,
              subcategory: this.analyzeDescription(transaction.description),
              confidence: rule.confidence,
              reason: `Amount-based: ${transaction.amount > 0 ? 'deposit' : 'withdrawal'}`
            };
          }
        }
      }
    }
    
    // Step 2: Provider-based categorization
    if (provider && providerCategories[provider]) {
      const providerCat = providerCategories[provider];
      return {
        type: 'expense', // Most providers are expenses
        category: providerCat.category,
        subcategory: providerCat.subcategory,
        confidence: 0.85,
        reason: `Provider: ${provider}`
      };
    }
    
    // Step 3: Description analysis (fallback)
    return this.analyzeDescription(transaction.description);
  }
  
  getSubcategory(typeRule, documentType, provider) {
    // Check subtype map
    if (typeRule.subcategoryMap) {
      const docSubtype = documentType.split('-')[1]; // e.g., 'water-sewer' from 'utility-bill-water-sewer'
      if (typeRule.subcategoryMap[docSubtype]) {
        return typeRule.subcategoryMap[docSubtype];
      }
    }
    
    // Check provider map
    if (typeRule.providerMap && provider) {
      return typeRule.providerMap[provider] || typeRule.providerMap['default'];
    }
    
    return 'general';
  }
  
  analyzeDescription(description) {
    const descLower = description.toLowerCase();
    
    // Income keywords
    const incomeKeywords = ['deposit', 'payroll', 'salary', 'dividend', 'interest', 'refund'];
    for (const keyword of incomeKeywords) {
      if (descLower.includes(keyword)) {
        return {
          type: 'income',
          category: 'deposit',
          subcategory: keyword,
          confidence: 0.75,
          reason: `Description keyword: ${keyword}`
        };
      }
    }
    
    // Expense keywords
    const expenseKeywords = {
      'grocery': ['grocery', 'supermarket', 'food'],
      'gas': ['gas', 'fuel', 'shell', 'chevron'],
      'restaurant': ['restaurant', 'cafe', 'dining'],
      'shopping': ['amazon', 'walmart', 'target'],
      'utilities': ['electric', 'water', 'internet', 'phone']
    };
    
    for (const [category, keywords] of Object.entries(expenseKeywords)) {
      for (const keyword of keywords) {
        if (descLower.includes(keyword)) {
          return {
            type: 'expense',
            category: category,
            subcategory: keyword,
            confidence: 0.70,
            reason: `Description keyword: ${keyword}`
          };
        }
      }
    }
    
    // Default: unknown
    return {
      type: 'unknown',
      category: 'uncategorized',
      subcategory: null,
      confidence: 0.0,
      reason: 'No matching patterns'
    };
  }
}
```

### Integration with Existing Code

```javascript
// In TransactionExtractor or similar
function extractAndCategorizeTransaction(text, documentType, provider) {
  // Extract transaction data
  const transaction = extractTransaction(text);
  
  // Categorize using new logic
  const categorizer = new TransactionCategorizer();
  const categorization = categorizer.categorize(transaction, documentType, provider);
  
  // Merge categorization into transaction
  return {
    ...transaction,
    type: categorization.type,
    category: categorization.category,
    subcategory: categorization.subcategory,
    confidence: categorization.confidence,
    categorizationReason: categorization.reason
  };
}
```

---

## Category Hierarchy

```
Income
├── Deposit
│   ├── Payroll
│   ├── Transfer
│   └── Refund
├── Investment
│   ├── Dividend
│   └── Interest
└── Other

Expense
├── Utilities
│   ├── Electric
│   ├── Gas
│   ├── Water/Sewer
│   ├── Internet
│   └── Phone
├── Shopping
│   ├── Retail
│   ├── Grocery
│   └── General
├── Dining
│   ├── Restaurant
│   └── Fast Food
├── Transportation
│   ├── Gas
│   └── Parking
└── Other
```

---

## Acceptance Criteria

- [ ] All utility bills categorized as expenses
- [ ] All invoices categorized as expenses
- [ ] Bank deposits categorized as income
- [ ] Bank withdrawals categorized as expenses
- [ ] Provider-specific subcategories assigned
- [ ] Confidence scores >0.85 for document-based categorization
- [ ] Confidence scores >0.70 for description-based categorization
- [ ] Category hierarchy properly implemented
- [ ] Categorization reason provided for debugging
- [ ] No misclassification of major document types

