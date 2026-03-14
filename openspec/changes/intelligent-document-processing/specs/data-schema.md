# Specification: Data Schema

## Overview
This specification defines the standardized data schema for all processed financial documents, ensuring consistency across different document types and providers.

## Common Document Schema

All processed documents follow this base schema:

```javascript
{
  document: {
    id: String,              // Unique identifier (UUID)
    type: String,            // Primary category (e.g., 'bank-statement', 'utility-bill')
    subtype: String,         // Specific type (e.g., 'checking', 'electric')
    provider: String,        // Provider name (e.g., 'Chase', 'ComEd')
    filename: String,        // Original filename
    uploadDate: String,      // ISO 8601 timestamp
    processingDate: String,  // ISO 8601 timestamp
    hash: String,            // SHA-256 file hash
    confidence: Number,      // 0-1 type detection confidence
    detectionMethod: String  // 'filename' | 'content' | 'hybrid-*'
  },
  account: {
    number: String,          // Masked account number (e.g., '****7969')
    type: String,            // Account type (e.g., 'checking', 'residential')
    holder: String | null    // Account holder (null for privacy)
  },
  period: {
    start: String,           // ISO 8601 date (YYYY-MM-DD)
    end: String,             // ISO 8601 date (YYYY-MM-DD)
    dueDate: String | null   // ISO 8601 date or null
  },
  financial: {
    currency: String,        // ISO 4217 currency code (e.g., 'USD')
    // Type-specific financial fields
  },
  metadata: {
    pageCount: Number,
    extractionMethod: String,
    extractionDuration: Number,  // milliseconds
    warnings: Array<String>
  }
}
```

## Type-Specific Schemas

### Bank Statement Schema

```javascript
{
  // ... common fields
  financial: {
    currency: 'USD',
    beginningBalance: Number,
    endingBalance: Number,
    totalDeposits: Number,
    totalWithdrawals: Number,
    fees: Number,
    interest: Number
  },
  transactions: [
    {
      date: String,          // ISO 8601 date
      description: String,
      amount: Number,        // Negative for withdrawals
      balance: Number,
      category: String       // Auto-categorized
    }
  ]
}
```

### Utility Bill Schema (Base)

```javascript
{
  // ... common fields
  financial: {
    currency: 'USD',
    amountDue: Number,
    previousBalance: Number,
    paymentsReceived: Number,
    newCharges: Number
  }
}
```

### Cable/Internet Bill (Xfinity)

```javascript
{
  // ... common fields + utility bill base
  services: [
    {
      name: String,          // 'Internet', 'TV', 'Phone'
      charge: Number,
      details: String
    }
  ],
  usage: {
    dataUsage: {
      amount: Number,
      unit: String,          // 'GB', 'MB'
      limit: Number | null
    }
  }
}
```

### Water/Sewer/Trash Bill

```javascript
{
  // ... common fields + utility bill base
  financial: {
    // ... base financial fields
    waterCharges: Number,
    sewerCharges: Number,
    trashFees: Number
  },
  usage: {
    waterUsage: {
      amount: Number,
      unit: String           // 'Gallons', 'CCF'
    }
  }
}
```

### Electric Bill (ComEd)

```javascript
{
  // ... common fields + utility bill base
  financial: {
    // ... base financial fields
    deliveryCharges: Number,
    supplyCharges: Number,
    taxes: Number
  },
  usage: {
    electricUsage: {
      amount: Number,
      unit: 'kWh',
      ratePerKwh: Number
    }
  }
}
```

### Cell Phone Bill (T-Mobile)

```javascript
{
  // ... common fields + utility bill base
  plan: {
    name: String,
    lines: Number
  },
  usage: {
    dataUsage: {
      amount: Number,
      unit: 'GB'
    },
    voiceMinutes: Number,
    textMessages: Number
  },
  equipment: [
    {
      device: String,
      installment: Number,
      remainingBalance: Number
    }
  ]
}
```

### Car Warranty Bill

```javascript
{
  // ... common fields
  policy: {
    number: String,
    type: String,            // 'Extended Warranty', 'Service Contract'
    coveragePeriod: {
      start: String,         // ISO 8601 date
      end: String
    }
  },
  vehicle: {
    year: Number | null,
    make: String | null,
    model: String | null,
    vin: String | null       // Masked
  },
  financial: {
    currency: 'USD',
    premium: Number,
    deductible: Number | null
  }
}
```

### Invoice Schema (Amazon)

```javascript
{
  // ... common fields
  order: {
    orderNumber: String,
    orderDate: String        // ISO 8601 date
  },
  financial: {
    currency: 'USD',
    subtotal: Number,
    tax: Number,
    shipping: Number,
    total: Number
  },
  items: [
    {
      name: String,
      quantity: Number,
      price: Number,
      total: Number
    }
  ],
  shipping: {
    address: String | null   // Null for privacy
  }
}
```

### Generic Invoice Schema

```javascript
{
  // ... common fields
  invoice: {
    number: String,
    date: String             // ISO 8601 date
  },
  financial: {
    currency: 'USD',
    subtotal: Number | null,
    tax: Number | null,
    total: Number
  },
  items: [
    {
      description: String,
      quantity: Number | null,
      price: Number | null,
      total: Number
    }
  ]
}
```

## Field Normalization Rules

### Dates
- **Input**: Various formats (MM/DD/YYYY, Month DD, YYYY, etc.)
- **Output**: ISO 8601 (YYYY-MM-DD)
- **Example**: "January 15, 2025" → "2025-01-15"

### Amounts
- **Input**: Various formats ($1,234.56, (1234.56), 1234.56)
- **Output**: Float with 2 decimal places
- **Example**: "$1,234.56" → 1234.56
- **Negative**: "(1234.56)" → -1234.56

### Account Numbers
- **Input**: Full account number
- **Output**: Masked with last 4 digits
- **Example**: "1234567890" → "****7890"

### Categories
- **Input**: Transaction descriptions
- **Output**: Standardized category
- **Categories**: income, shopping, groceries, utilities, transportation, healthcare, entertainment, other

### Providers
- **Input**: Various spellings/formats
- **Output**: Canonical name
- **Examples**:
  - "CHASE BANK" → "Chase"
  - "Commonwealth Edison" → "ComEd"
  - "T-MOBILE USA" → "T-Mobile"

## Validation Rules

### Required Fields (All Documents)
- document.id
- document.type
- document.provider
- document.filename
- document.uploadDate
- account.number
- period.start
- period.end
- financial.currency

### Type-Specific Required Fields

**Bank Statement**:
- financial.beginningBalance
- financial.endingBalance

**Utility Bills**:
- financial.amountDue
- period.dueDate

**Invoices**:
- financial.total

### Field Constraints

**Dates**:
- Must be valid ISO 8601 format
- period.end >= period.start
- period.dueDate >= period.end (if present)

**Amounts**:
- Must be numeric
- Must have exactly 2 decimal places
- Can be negative (for withdrawals/credits)

**Confidence**:
- Must be between 0 and 1
- Recommended minimum: 0.7

## Error Handling

### Missing Required Field
```javascript
{
  error: 'missing_required_field',
  field: 'financial.amountDue',
  document: 'doc-123'
}
```

### Invalid Field Value
```javascript
{
  error: 'invalid_field_value',
  field: 'period.start',
  value: 'invalid-date',
  expected: 'ISO 8601 date',
  document: 'doc-123'
}
```

### Validation Failure
```javascript
{
  error: 'validation_failed',
  field: 'period.end',
  reason: 'End date before start date',
  document: 'doc-123'
}
```

## Storage Format

### In-Memory (During Processing)
- JavaScript objects following schema
- Indexed by document.id
- Grouped by type and provider

### Persistence (Optional)
- IndexedDB for browser storage
- JSON format
- Encrypted if sensitive data present

### Export Formats
- **JSON**: Full schema with all fields
- **CSV**: Flattened schema for spreadsheet import
- **HTML**: Formatted report

## Schema Versioning

Current version: **1.0**

Future versions will maintain backward compatibility:
- New optional fields can be added
- Required fields cannot be removed
- Field types cannot change
- Migration functions provided for breaking changes

## Testing

### Schema Validation Tests
- All required fields present
- Field types correct
- Constraints satisfied
- Normalization applied correctly

### Serialization Tests
- JSON round-trip (serialize → deserialize)
- No data loss
- Consistent formatting

