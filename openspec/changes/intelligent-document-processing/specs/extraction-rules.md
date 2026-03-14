# Specification: Extraction Rules

## Overview
The Extraction Rules system defines type-specific patterns and logic for extracting structured data from different financial document types.

## Requirements

### Functional Requirements

**FR-1**: System SHALL support extraction rules for 8+ document types
**FR-2**: Each rule SHALL define required and optional fields
**FR-3**: Rules SHALL include regex patterns, validators, and parsers
**FR-4**: System SHALL calculate extraction confidence per field
**FR-5**: System SHALL handle partial extraction failures gracefully
**FR-6**: Rules SHALL be extensible without code changes

### Non-Functional Requirements

**NFR-1**: Extraction SHALL complete within 2 seconds per document
**NFR-2**: Extraction accuracy SHALL be >= 90% for required fields
**NFR-3**: System SHALL handle malformed data gracefully

## Extraction Rule Structure

```javascript
{
  documentType: 'bank-statement-chase',
  version: '1.0',
  fields: {
    accountNumber: {
      required: true,
      pattern: /Account\s+Number[:\s]+(\d{4,})/i,
      validator: (val) => val && val.length >= 4,
      parser: (match) => match[1],
      fallbackPatterns: [
        /Account[:\s]+(\d{4,})/i,
        /Acct[:\s]+(\d{4,})/i
      ]
    },
    statementPeriod: {
      required: true,
      pattern: /Statement\s+Period[:\s]+(\d{2}\/\d{2}\/\d{4})\s*-\s*(\d{2}\/\d{2}\/\d{4})/i,
      validator: (val) => val && val.start && val.end,
      parser: (match) => ({
        start: new Date(match[1]),
        end: new Date(match[2])
      })
    },
    // ... more fields
  },
  postProcessing: (extractedData) => {
    // Custom logic after extraction
    return extractedData;
  }
}
```

## Document Type Rules

### 1. Bank Statement (Chase)

**Document Type**: `bank-statement-chase`

**Required Fields**:
- Account Number
- Statement Period (start, end)
- Beginning Balance
- Ending Balance

**Optional Fields**:
- Total Deposits
- Total Withdrawals
- Interest Earned
- Fees Charged
- Transactions

**Extraction Rules**:
```javascript
{
  accountNumber: {
    pattern: /Account\s+Number[:\s]+(\d{4,})/i,
    validator: (val) => /^\d{4,}$/.test(val),
    parser: (match) => match[1].slice(-4) // Last 4 digits only
  },
  statementPeriod: {
    pattern: /(\d{2}\/\d{2}\/\d{4})\s*-\s*(\d{2}\/\d{2}\/\d{4})/i,
    parser: (match) => ({
      start: match[1],
      end: match[2]
    })
  },
  beginningBalance: {
    pattern: /Beginning\s+Balance[:\s]+\$?([\d,]+\.\d{2})/i,
    parser: (match) => parseFloat(match[1].replace(/,/g, ''))
  },
  endingBalance: {
    pattern: /Ending\s+Balance[:\s]+\$?([\d,]+\.\d{2})/i,
    parser: (match) => parseFloat(match[1].replace(/,/g, ''))
  },
  totalDeposits: {
    pattern: /Total\s+Deposits[:\s]+\$?([\d,]+\.\d{2})/i,
    parser: (match) => parseFloat(match[1].replace(/,/g, ''))
  },
  transactions: {
    pattern: /(\d{2}\/\d{2})\s+(.+?)\s+(-?\$?[\d,]+\.\d{2})\s+(\$?[\d,]+\.\d{2})/gm,
    parser: (matches) => matches.map(m => ({
      date: m[1],
      description: m[2].trim(),
      amount: parseFloat(m[3].replace(/[$,]/g, '')),
      balance: parseFloat(m[4].replace(/[$,]/g, ''))
    }))
  }
}
```

### 2. Xfinity Bill

**Document Type**: `utility-bill-xfinity`

**Required Fields**:
- Account Number
- Billing Period
- Amount Due
- Due Date

**Optional Fields**:
- Services (Internet, TV, Phone)
- Data Usage
- Equipment Charges
- Previous Balance
- Payments Received

**Extraction Rules**:
```javascript
{
  accountNumber: {
    pattern: /Account\s+Number[:\s]+(\d{10,})/i,
    validator: (val) => /^\d{10,}$/.test(val)
  },
  billingPeriod: {
    pattern: /Billing\s+Period[:\s]+([A-Z][a-z]+\s+\d{1,2})\s*-\s*([A-Z][a-z]+\s+\d{1,2},\s+\d{4})/i,
    parser: (match) => ({
      start: match[1],
      end: match[2]
    })
  },
  amountDue: {
    pattern: /Amount\s+Due[:\s]+\$?([\d,]+\.\d{2})/i,
    parser: (match) => parseFloat(match[1].replace(/,/g, ''))
  },
  dueDate: {
    pattern: /Due\s+Date[:\s]+([A-Z][a-z]+\s+\d{1,2},\s+\d{4})/i,
    parser: (match) => new Date(match[1])
  },
  dataUsage: {
    pattern: /Data\s+Usage[:\s]+([\d,]+)\s*(GB|MB)/i,
    parser: (match) => ({
      amount: parseFloat(match[1].replace(/,/g, '')),
      unit: match[2]
    })
  },
  services: {
    pattern: /(Internet|TV|Phone|Voice)[:\s]+\$?([\d,]+\.\d{2})/gi,
    parser: (matches) => matches.map(m => ({
      service: m[1],
      charge: parseFloat(m[2].replace(/,/g, ''))
    }))
  }
}
```

### 3. Water/Sewer/Trash Bill (Barrington Township)

**Document Type**: `utility-bill-water-sewer-trash`

**Required Fields**:
- Account Number
- Billing Period
- Total Amount Due
- Due Date

**Optional Fields**:
- Water Usage (gallons/CCF)
- Water Charges
- Sewer Charges
- Trash/Recycling Fees
- Previous Balance

**Extraction Rules**:
```javascript
{
  accountNumber: {
    pattern: /Account[:\s]+(UB\d+-\d+)/i,
    validator: (val) => /^UB\d+-\d+$/.test(val)
  },
  billingPeriod: {
    pattern: /Billing\s+Period[:\s]+(\d{2}\/\d{2}\/\d{4})\s*-\s*(\d{2}\/\d{2}\/\d{4})/i,
    parser: (match) => ({
      start: match[1],
      end: match[2]
    })
  },
  waterUsage: {
    pattern: /Water\s+Usage[:\s]+([\d,]+)\s*(Gallons|CCF)/i,
    parser: (match) => ({
      amount: parseFloat(match[1].replace(/,/g, '')),
      unit: match[2]
    })
  },
  waterCharges: {
    pattern: /Water\s+Charges?[:\s]+\$?([\d,]+\.\d{2})/i,
    parser: (match) => parseFloat(match[1].replace(/,/g, ''))
  },
  sewerCharges: {
    pattern: /Sewer\s+Charges?[:\s]+\$?([\d,]+\.\d{2})/i,
    parser: (match) => parseFloat(match[1].replace(/,/g, ''))
  },
  trashFees: {
    pattern: /(?:Trash|Refuse|Recycling)\s+(?:Fee|Charges?)[:\s]+\$?([\d,]+\.\d{2})/i,
    parser: (match) => parseFloat(match[1].replace(/,/g, ''))
  }
}
```

### 4. ComEd Electric Bill

**Document Type**: `utility-bill-electric-comed`

**Required Fields**:
- Account Number
- Billing Period
- Total Amount Due
- Usage (kWh)

**Optional Fields**:
- Delivery Charges
- Supply Charges
- Rate per kWh
- Taxes
- Previous Balance

**Extraction Rules**:
```javascript
{
  accountNumber: {
    pattern: /Account\s+(?:Number|#)[:\s]+(\d{10,})/i,
    validator: (val) => /^\d{10,}$/.test(val)
  },
  usageKwh: {
    pattern: /(?:Total\s+)?kWh\s+(?:Used|Usage)[:\s]+([\d,]+)/i,
    parser: (match) => parseFloat(match[1].replace(/,/g, ''))
  },
  deliveryCharges: {
    pattern: /Delivery\s+Charges?[:\s]+\$?([\d,]+\.\d{2})/i,
    parser: (match) => parseFloat(match[1].replace(/,/g, ''))
  },
  supplyCharges: {
    pattern: /(?:Supply|Energy)\s+Charges?[:\s]+\$?([\d,]+\.\d{2})/i,
    parser: (match) => parseFloat(match[1].replace(/,/g, ''))
  },
  ratePerKwh: {
    pattern: /Rate[:\s]+\$?([\d.]+)\s*\/\s*kWh/i,
    parser: (match) => parseFloat(match[1])
  }
}
```

### 5. T-Mobile Cell Phone Bill

**Document Type**: `utility-bill-cell-phone-tmobile`

**Required Fields**:
- Account Number
- Billing Period
- Total Amount Due

**Optional Fields**:
- Plan Name
- Number of Lines
- Data Usage
- Voice Minutes
- Text Messages
- Equipment Installments

### 6. Car Warranty Bill

**Document Type**: `insurance-warranty-car`

**Required Fields**:
- Policy/Contract Number
- Coverage Period
- Premium Amount

**Optional Fields**:
- Vehicle Information (Year, Make, Model, VIN)
- Coverage Type
- Deductible

### 7. Amazon Invoice

**Document Type**: `invoice-amazon`

**Required Fields**:
- Order Number
- Order Date
- Total Amount

**Optional Fields**:
- Items (name, quantity, price)
- Subtotal
- Tax
- Shipping
- Ship To Address

**Extraction Rules**:
```javascript
{
  orderNumber: {
    pattern: /Order\s+(?:Number|#)[:\s]+(\d{3}-\d{7}-\d{7})/i,
    validator: (val) => /^\d{3}-\d{7}-\d{7}$/.test(val)
  },
  orderDate: {
    pattern: /Order\s+Date[:\s]+([A-Z][a-z]+\s+\d{1,2},\s+\d{4})/i,
    parser: (match) => new Date(match[1])
  },
  items: {
    pattern: /(.+?)\s+Qty:\s*(\d+)\s+\$?([\d,]+\.\d{2})/gm,
    parser: (matches) => matches.map(m => ({
      name: m[1].trim(),
      quantity: parseInt(m[2]),
      price: parseFloat(m[3].replace(/,/g, ''))
    }))
  },
  subtotal: {
    pattern: /Subtotal[:\s]+\$?([\d,]+\.\d{2})/i,
    parser: (match) => parseFloat(match[1].replace(/,/g, ''))
  },
  tax: {
    pattern: /Tax[:\s]+\$?([\d,]+\.\d{2})/i,
    parser: (match) => parseFloat(match[1].replace(/,/g, ''))
  },
  shipping: {
    pattern: /Shipping[:\s]+\$?([\d,]+\.\d{2})/i,
    parser: (match) => parseFloat(match[1].replace(/,/g, ''))
  }
}
```

## Extraction Process

### Step 1: Select Rule Set
```javascript
function selectRuleSet(documentType) {
  return extractionRules[documentType] || extractionRules['generic'];
}
```

### Step 2: Apply Patterns
```javascript
function extractField(text, fieldRule) {
  const match = text.match(fieldRule.pattern);
  if (!match) return null;
  
  const value = fieldRule.parser ? fieldRule.parser(match) : match[1];
  
  if (fieldRule.validator && !fieldRule.validator(value)) {
    return null;
  }
  
  return value;
}
```

### Step 3: Calculate Confidence
```javascript
function calculateConfidence(extractedFields, ruleSet) {
  const requiredFields = Object.entries(ruleSet.fields)
    .filter(([_, rule]) => rule.required);
  
  const extractedRequired = requiredFields
    .filter(([name, _]) => extractedFields[name] !== null);
  
  return extractedRequired.length / requiredFields.length;
}
```

## Output Format

```javascript
{
  fields: {
    accountNumber: '7969',
    statementPeriod: {
      start: '2025-05-01',
      end: '2025-05-30'
    },
    beginningBalance: 1234.56,
    endingBalance: 2345.67
    // ... more fields
  },
  confidence: 0.95,
  extractedFieldCount: 12,
  requiredFieldCount: 4,
  missingFields: [],
  errors: []
}
```

## Error Handling

1. **Missing Required Field**: Log warning, continue with partial data
2. **Invalid Format**: Try fallback patterns
3. **Validation Failure**: Mark field as null, log error
4. **Parser Exception**: Catch and log, return null for field

## Testing

### Test Cases
- Each document type with valid data → All required fields extracted
- Malformed document → Graceful degradation
- Missing optional fields → No errors
- Invalid field values → Validation catches errors

### Acceptance Criteria
- 90% extraction accuracy for required fields
- 80% extraction accuracy for optional fields
- No crashes on malformed data

