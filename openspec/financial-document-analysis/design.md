# Design Document: Financial Document Analysis System

## Change ID
`FIN-ANALYSIS-001`

## Version
1.0.0

## Status
Draft

## Last Updated
2026-02-06

---

## Table of Contents
1. [Architecture Overview](#architecture-overview)
2. [System Architecture](#system-architecture)
3. [Component Design](#component-design)
4. [Data Flow](#data-flow)
5. [UI/UX Design](#uiux-design)
6. [File Structure](#file-structure)
7. [Technology Stack](#technology-stack)

---

## Architecture Overview

### Design Principles
1. **Client-Side First**: All processing occurs in the browser for privacy
2. **Modular Architecture**: Separation of concerns with clear module boundaries
3. **Progressive Enhancement**: Core functionality works without JavaScript
4. **Accessibility First**: WCAG 2.1 AA compliance from the start
5. **Performance Optimized**: Lazy loading, code splitting, efficient algorithms
6. **Responsive Design**: Mobile-first approach

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        User Interface                        │
│  (Upload Zone, Report Display, Charts, Export Controls)     │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Application Layer                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Upload     │  │   Analysis   │  │    Export    │      │
│  │  Controller  │  │  Controller  │  │  Controller  │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                     Business Logic Layer                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Document   │  │ Transaction  │  │    Chart     │      │
│  │    Parser    │  │  Extractor   │  │  Generator   │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Categorizer  │  │   Analysis   │  │   Report     │      │
│  │    Engine    │  │    Engine    │  │  Exporter    │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      Data Access Layer                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   IndexedDB  │  │  LocalStorage│  │   Session    │      │
│  │   Manager    │  │   Manager    │  │   Storage    │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    External Libraries                        │
│  PDF.js  │  Tesseract.js  │  Chart.js  │  jsPDF            │
└─────────────────────────────────────────────────────────────┘
```

---

## System Architecture

### Component Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    financial-analysis.html                   │
│                                                               │
│  ┌─────────────────────────────────────────────────────┐    │
│  │                  Upload Section                      │    │
│  │  - Drag & Drop Zone                                  │    │
│  │  - File Browser Button                               │    │
│  │  - File List with Progress                           │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                               │
│  ┌─────────────────────────────────────────────────────┐    │
│  │                  Report Section                      │    │
│  │  ┌─────────────────────────────────────────────┐    │    │
│  │  │  Table of Contents (Sticky Sidebar)         │    │    │
│  │  └─────────────────────────────────────────────┘    │    │
│  │  ┌─────────────────────────────────────────────┐    │    │
│  │  │  Executive Summary                           │    │    │
│  │  │  - Key Metrics Cards                         │    │    │
│  │  │  - Quick Stats                               │    │    │
│  │  └─────────────────────────────────────────────┘    │    │
│  │  ┌─────────────────────────────────────────────┐    │    │
│  │  │  Income Analysis                             │    │    │
│  │  │  - Summary Cards                             │    │    │
│  │  │  - Charts (Category, Monthly)                │    │    │
│  │  └─────────────────────────────────────────────┘    │    │
│  │  ┌─────────────────────────────────────────────┐    │    │
│  │  │  Expense Analysis                            │    │    │
│  │  │  - Summary Cards                             │    │    │
│  │  │  - Charts (Category, Monthly)                │    │    │
│  │  └─────────────────────────────────────────────┘    │    │
│  │  ┌─────────────────────────────────────────────┐    │    │
│  │  │  Additional Sections (Assets, Liabilities,   │    │    │
│  │  │  Cash Flow, Investments, Debts, etc.)        │    │    │
│  │  └─────────────────────────────────────────────┘    │    │
│  │  ┌─────────────────────────────────────────────┐    │    │
│  │  │  Detailed Transactions Table                 │    │    │
│  │  │  - Sortable, Filterable, Searchable          │    │    │
│  │  └─────────────────────────────────────────────┘    │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                               │
│  ┌─────────────────────────────────────────────────────┐    │
│  │                  Action Bar (Sticky)                 │    │
│  │  [Download PDF] [Print] [Email] [Save] [New Window] │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

---

## Component Design

### 1. DocumentUploader Component

**Responsibility**: Handle file uploads and validation

**Public Interface**:
```javascript
class DocumentUploader {
  constructor(options)
  async uploadFiles(files)
  validateFile(file)
  on(event, callback)
}
```

**Events**:
- `upload-start`: Fired when upload begins
- `upload-progress`: Fired during upload (with progress %)
- `upload-complete`: Fired when upload completes
- `upload-error`: Fired on error

**Internal Methods**:
- `_createUploadZone()`: Create drag-drop UI
- `_handleDrop(event)`: Handle file drop
- `_handleFileSelect(event)`: Handle file browser selection
- `_validateFileType(file)`: Check file type
- `_validateFileSize(file)`: Check file size
- `_showProgress(fileId, progress)`: Update progress UI

### 2. DocumentParser Component

**Responsibility**: Extract text from documents (PDF, images)

**Public Interface**:
```javascript
class DocumentParser {
  constructor(options)
  async parseDocument(document)
  async performOCR(document)
  detectDocumentType(text)
}
```

**Dependencies**:
- PDF.js for PDF text extraction
- Tesseract.js for OCR

**Internal Methods**:
- `_extractPDFText(pdfDocument)`: Extract text from PDF
- `_preprocessImage(image)`: Prepare image for OCR
- `_runOCR(image)`: Execute OCR
- `_cleanExtractedText(text)`: Remove noise from text

### 3. TransactionExtractor Component

**Responsibility**: Extract and categorize transactions from text

**Public Interface**:
```javascript
class TransactionExtractor {
  constructor(categoryRules)
  extractTransactions(text, documentType)
  categorizeTransaction(transaction)
  addCategoryRule(pattern, category)
}
```

**Pattern Matching**:
- Date patterns: `MM/DD/YYYY`, `DD-MM-YYYY`, `YYYY-MM-DD`
- Amount patterns: `$X,XXX.XX`, `(XXX.XX)`, `-XXX.XX`
- Description extraction: Context-aware text between date and amount

**Category Rules**:
```javascript
const categoryRules = {
  income: {
    salary: ['PAYROLL', 'SALARY', 'WAGES', 'DIRECT DEPOSIT'],
    freelance: ['FREELANCE', 'CONTRACT', 'CONSULTING'],
    investment: ['DIVIDEND', 'INTEREST', 'CAPITAL GAIN']
  },
  expenses: {
    housing: ['RENT', 'MORTGAGE', 'HOA'],
    utilities: ['ELECTRIC', 'GAS', 'WATER', 'INTERNET', 'PHONE'],
    food: ['GROCERY', 'RESTAURANT', 'FOOD', 'DINING'],
    transportation: ['GAS STATION', 'UBER', 'LYFT', 'PARKING'],
    // ... more categories
  }
}
```

### 4. AnalysisEngine Component

**Responsibility**: Calculate financial summaries and metrics

**Public Interface**:
```javascript
class AnalysisEngine {
  constructor()
  generateSummary(transactions, options)
  calculateMetric(metric, transactions)
  groupByPeriod(transactions, period)
  groupByCategory(transactions)
}
```

**Calculations**:
- **Net Worth**: `sum(assets) - sum(liabilities)`
- **Cash Flow**: `sum(income) - sum(expenses)`
- **Savings Rate**: `(income - expenses) / income * 100`
- **Average Monthly**: `sum(transactions) / months`

**Internal Methods**:
- `_filterByDateRange(transactions, start, end)`
- `_filterByCategory(transactions, category)`
- `_aggregateByMonth(transactions)`
- `_calculateTrend(values)`

### 5. ChartGenerator Component

**Responsibility**: Generate interactive charts

**Public Interface**:
```javascript
class ChartGenerator {
  constructor(chartLibrary)
  generateChart(type, data, options)
  renderChart(canvasId, config)
  updateChart(chartInstance, newData)
  destroyChart(chartInstance)
}
```

**Chart Configurations**:

**Pie Chart (Category Breakdown)**:
```javascript
{
  type: 'doughnut',
  data: {
    labels: ['Housing', 'Food', 'Transportation', ...],
    datasets: [{
      data: [1200, 500, 300, ...],
      backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', ...]
    }]
  },
  options: {
    responsive: true,
    plugins: {
      legend: { position: 'right' },
      tooltip: { enabled: true }
    }
  }
}
```

**Line Chart (Time Series)**:
```javascript
{
  type: 'line',
  data: {
    labels: ['Jan', 'Feb', 'Mar', ...],
    datasets: [{
      label: 'Income',
      data: [5000, 5200, 4800, ...],
      borderColor: '#36A2EB',
      fill: false
    }]
  },
  options: {
    responsive: true,
    scales: {
      y: { beginAtZero: true }
    }
  }
}
```

### 6. ReportExporter Component

**Responsibility**: Export reports in various formats

**Public Interface**:
```javascript
class ReportExporter {
  constructor()
  async exportToPDF(element, filename)
  async saveAsJSON(data, filename)
  generateEmailLink(pdfBlob, subject)
  openInNewWindow(htmlContent)
}
```

**PDF Generation**:
- Use jsPDF or html2pdf.js
- Preserve layout and styling
- Include charts as images
- Add page numbers and headers

**Internal Methods**:
- `_captureCharts()`: Convert charts to images
- `_generatePDFContent(element)`: Create PDF structure
- `_addPageBreaks()`: Smart page break insertion
- `_createBlob(pdfDoc)`: Generate downloadable blob

---

## Data Flow

### Upload to Report Flow

```
1. User Uploads Files
   │
   ├─> DocumentUploader.uploadFiles()
   │   ├─> Validate files
   │   ├─> Show progress
   │   └─> Emit 'upload-complete'
   │
2. Parse Documents
   │
   ├─> DocumentParser.parseDocument()
   │   ├─> Extract text (PDF.js or OCR)
   │   ├─> Detect document type
   │   └─> Return parsed text
   │
3. Extract Transactions
   │
   ├─> TransactionExtractor.extractTransactions()
   │   ├─> Find date patterns
   │   ├─> Find amount patterns
   │   ├─> Extract descriptions
   │   ├─> Categorize transactions
   │   └─> Return Transaction[]
   │
4. Generate Analysis
   │
   ├─> AnalysisEngine.generateSummary()
   │   ├─> Calculate all 20 summaries
   │   ├─> Group by period
   │   ├─> Group by category
   │   └─> Return Summary object
   │
5. Generate Charts
   │
   ├─> ChartGenerator.generateChart() (x19)
   │   ├─> Transform data for chart
   │   ├─> Create chart config
   │   ├─> Render to canvas
   │   └─> Add interactivity
   │
6. Render Report
   │
   ├─> ReportRenderer.render()
   │   ├─> Generate HTML structure
   │   ├─> Insert summaries
   │   ├─> Insert charts
   │   ├─> Add table of contents
   │   ├─> Add search/filter UI
   │   └─> Display to user
   │
7. Export (Optional)
   │
   └─> ReportExporter.exportToPDF()
       ├─> Capture current state
       ├─> Generate PDF
       └─> Download file
```

### State Management

```javascript
const AppState = {
  documents: [],           // Uploaded documents
  transactions: [],        // All extracted transactions
  summary: null,          // Generated summary
  charts: {},             // Chart instances
  filters: {              // Active filters
    dateRange: null,
    categories: [],
    amountRange: null
  },
  ui: {
    currentView: 'upload', // 'upload' | 'report'
    loading: false,
    error: null
  }
}
```

---

## UI/UX Design

### Color Palette

```css
:root {
  /* Primary Colors */
  --primary-blue: #2563eb;
  --primary-blue-dark: #1e40af;
  --primary-blue-light: #60a5fa;

  /* Semantic Colors */
  --success-green: #10b981;
  --warning-yellow: #f59e0b;
  --error-red: #ef4444;
  --info-blue: #3b82f6;

  /* Neutral Colors */
  --gray-50: #f9fafb;
  --gray-100: #f3f4f6;
  --gray-200: #e5e7eb;
  --gray-300: #d1d5db;
  --gray-700: #374151;
  --gray-900: #111827;

  /* Chart Colors */
  --chart-1: #3b82f6;
  --chart-2: #10b981;
  --chart-3: #f59e0b;
  --chart-4: #ef4444;
  --chart-5: #8b5cf6;
  --chart-6: #ec4899;
}
```

### Typography

```css
:root {
  /* Font Families */
  --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  --font-mono: 'Fira Code', 'Courier New', monospace;

  /* Font Sizes */
  --text-xs: 0.75rem;    /* 12px */
  --text-sm: 0.875rem;   /* 14px */
  --text-base: 1rem;     /* 16px */
  --text-lg: 1.125rem;   /* 18px */
  --text-xl: 1.25rem;    /* 20px */
  --text-2xl: 1.5rem;    /* 24px */
  --text-3xl: 1.875rem;  /* 30px */
  --text-4xl: 2.25rem;   /* 36px */

  /* Font Weights */
  --font-normal: 400;
  --font-medium: 500;
  --font-semibold: 600;
  --font-bold: 700;
}
```

### Layout Grid

```css
.container {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 1rem;
}

.grid-2-col {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
}

.grid-3-col {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
}

@media (max-width: 768px) {
  .grid-2-col,
  .grid-3-col {
    grid-template-columns: 1fr;
  }
}
```

### Wireframes

#### Upload Screen
```
┌─────────────────────────────────────────────────────────────┐
│  Financial Analysis Tool                    [Help] [Settings]│
├─────────────────────────────────────────────────────────────┤
│                                                               │
│   ┌───────────────────────────────────────────────────┐     │
│   │                                                     │     │
│   │         📁  Drag & Drop Files Here                 │     │
│   │                                                     │     │
│   │         or click to browse                         │     │
│   │                                                     │     │
│   │   Supported: PDF, PNG, JPG, CSV (max 10MB each)   │     │
│   │                                                     │     │
│   └───────────────────────────────────────────────────┘     │
│                                                               │
│   Uploaded Files:                                            │
│   ┌───────────────────────────────────────────────────┐     │
│   │ 📄 bank_statement.pdf        [████████░░] 80%     │     │
│   │ 📄 utility_bill.pdf          [██████████] ✓       │     │
│   │ 📄 invoice_jan.pdf           [██░░░░░░░░] 20%     │     │
│   └───────────────────────────────────────────────────┘     │
│                                                               │
│                          [Generate Report]                    │
└─────────────────────────────────────────────────────────────┘
```

#### Report Screen
```
┌─────────────────────────────────────────────────────────────┐
│  Financial Report                [PDF] [Print] [Email] [Save]│
├──────────┬──────────────────────────────────────────────────┤
│          │  Executive Summary                                │
│ TOC      │  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐            │
│ ├ Summary│  │Income│ │Expense│ │Cash  │ │Net   │            │
│ ├ Income │  │$5,200│ │$3,800│ │Flow  │ │Worth │            │
│ ├ Expense│  │      │ │      │ │$1,400│ │$45K  │            │
│ ├ Assets │  └──────┘ └──────┘ └──────┘ └──────┘            │
│ ├ Debts  │                                                   │
│ └ Details│  Income Analysis                                  │
│          │  ┌─────────────────────────────────────────┐     │
│ [Search] │  │  Income by Category                     │     │
│          │  │  ┌─────────────────────────────────┐   │     │
│          │  │  │     [Pie Chart]                 │   │     │
│          │  │  │   Salary: 80%                   │   │     │
│          │  │  │   Freelance: 15%                │   │     │
│          │  │  │   Other: 5%                     │   │     │
│          │  │  └─────────────────────────────────┘   │     │
│          │  └─────────────────────────────────────────┘     │
│          │                                                   │
│          │  ┌─────────────────────────────────────────┐     │
│          │  │  Income by Month                        │     │
│          │  │  ┌─────────────────────────────────┐   │     │
│          │  │  │     [Line Chart]                │   │     │
│          │  │  │                                 │   │     │
│          │  │  └─────────────────────────────────┘   │     │
│          │  └─────────────────────────────────────────┘     │
└──────────┴──────────────────────────────────────────────────┘
```

---

## File Structure

```
financial/
├── pages/
│   └── financial-analysis.html          # Main HTML file
├── js/
│   ├── app.js                           # Application entry point
│   ├── components/
│   │   ├── DocumentUploader.js          # Upload component
│   │   ├── DocumentParser.js            # Parser component
│   │   ├── TransactionExtractor.js      # Extractor component
│   │   ├── AnalysisEngine.js            # Analysis component
│   │   ├── ChartGenerator.js            # Chart component
│   │   └── ReportExporter.js            # Export component
│   ├── utils/
│   │   ├── dateUtils.js                 # Date utilities
│   │   ├── currencyUtils.js             # Currency utilities
│   │   ├── validationUtils.js           # Validation utilities
│   │   └── storageUtils.js              # Storage utilities
│   ├── config/
│   │   ├── categoryRules.js             # Category rules
│   │   └── chartConfigs.js              # Chart configurations
│   └── lib/
│       ├── pdf.min.js                   # PDF.js library
│       ├── tesseract.min.js             # Tesseract.js library
│       ├── chart.min.js                 # Chart.js library
│       └── jspdf.min.js                 # jsPDF library
├── css/
│   ├── main.css                         # Main styles
│   ├── components/
│   │   ├── upload.css                   # Upload styles
│   │   ├── report.css                   # Report styles
│   │   ├── charts.css                   # Chart styles
│   │   └── export.css                   # Export styles
│   └── print.css                        # Print stylesheet
└── tests/
    ├── unit/
    │   ├── DocumentParser.test.js
    │   ├── TransactionExtractor.test.js
    │   ├── AnalysisEngine.test.js
    │   └── ChartGenerator.test.js
    └── integration/
        ├── upload-flow.test.js
        ├── analysis-flow.test.js
        └── export-flow.test.js
```

---

## Technology Stack

### Core Technologies
- **HTML5**: Semantic markup, drag-and-drop API
- **CSS3**: Grid, Flexbox, Custom Properties, Media Queries
- **JavaScript (ES6+)**: Classes, Modules, Async/Await, Promises

### Libraries & Frameworks

#### Document Processing
- **PDF.js** (v3.x): PDF text extraction
  - Pros: Mozilla-backed, robust, widely used
  - Cons: Large bundle size (~500KB)
- **Tesseract.js** (v4.x): OCR for scanned documents
  - Pros: Client-side, no server needed
  - Cons: Slower processing, accuracy varies

#### Data Visualization
- **Chart.js** (v4.x): Interactive charts
  - Pros: Simple API, responsive, accessible
  - Cons: Limited customization vs D3.js
- **Alternative**: D3.js (v7.x) for advanced visualizations

#### PDF Export
- **jsPDF** (v2.x): PDF generation
  - Pros: Lightweight, good documentation
  - Cons: Limited layout control
- **Alternative**: html2pdf.js for HTML-to-PDF conversion

#### Utilities
- **DOMPurify**: HTML sanitization
- **date-fns** or **Day.js**: Date manipulation
- **Lodash** (optional): Utility functions

### Development Tools
- **ESLint**: Code linting
- **Prettier**: Code formatting
- **Jest**: Unit testing
- **Cypress/Playwright**: Integration testing
- **Lighthouse**: Performance auditing
- **axe DevTools**: Accessibility testing

---

## Performance Optimization

### Code Splitting
```javascript
// Lazy load heavy libraries
const loadPDFParser = () => import('./lib/pdf.min.js');
const loadOCR = () => import('./lib/tesseract.min.js');
const loadChartLib = () => import('./lib/chart.min.js');
```

### Caching Strategy
```javascript
// Cache parsed documents
const documentCache = new Map();

async function parseDocument(document) {
  if (documentCache.has(document.id)) {
    return documentCache.get(document.id);
  }

  const result = await parser.parse(document);
  documentCache.set(document.id, result);
  return result;
}
```

### Web Workers
```javascript
// Offload heavy processing to Web Worker
const parserWorker = new Worker('js/workers/parser-worker.js');

parserWorker.postMessage({ document, action: 'parse' });
parserWorker.onmessage = (e) => {
  const { transactions } = e.data;
  // Update UI
};
```

---

## Accessibility Features

### Keyboard Navigation
- Tab order follows logical flow
- All interactive elements focusable
- Escape key closes modals/dialogs
- Arrow keys navigate charts

### Screen Reader Support
```html
<!-- ARIA labels for charts -->
<canvas id="income-chart"
        role="img"
        aria-label="Income by category pie chart showing Salary 80%, Freelance 15%, Other 5%">
</canvas>

<!-- Live regions for dynamic updates -->
<div role="status" aria-live="polite" aria-atomic="true">
  Processing document 3 of 5...
</div>
```

### Color Contrast
- All text meets 4.5:1 contrast ratio
- Charts use patterns in addition to colors
- Focus indicators clearly visible

---

## Security Considerations

### Input Validation
```javascript
function validateFile(file) {
  // Check file type
  const allowedTypes = ['application/pdf', 'image/png', 'image/jpeg', 'text/csv'];
  if (!allowedTypes.includes(file.type)) {
    throw new Error('Invalid file type');
  }

  // Check file size
  const maxSize = 10 * 1024 * 1024; // 10MB
  if (file.size > maxSize) {
    throw new Error('File too large');
  }

  // Check file extension
  const allowedExtensions = ['.pdf', '.png', '.jpg', '.jpeg', '.csv'];
  const extension = file.name.toLowerCase().match(/\.[^.]+$/)?.[0];
  if (!allowedExtensions.includes(extension)) {
    throw new Error('Invalid file extension');
  }

  return true;
}
```

### Content Security Policy
```html
<meta http-equiv="Content-Security-Policy"
      content="default-src 'self';
               script-src 'self' 'unsafe-inline' 'unsafe-eval';
               style-src 'self' 'unsafe-inline';
               img-src 'self' data: blob:;">
```

### Data Sanitization
```javascript
import DOMPurify from 'dompurify';

function displayTransactionDescription(description) {
  const clean = DOMPurify.sanitize(description);
  element.innerHTML = clean;
}
```

---

## Change Log

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-02-06 | Financial Team | Initial design document |


**Events**:
- `upload-start`: Fired when upload begins
- `upload-progress`: Fired during upload (with progress %)
- `upload-complete`: Fired when upload completes
- `upload-error`: Fired on error

**Internal Methods**:
- `_createUploadZone()`: Create drag-drop UI
- `_handleDrop(event)`: Handle file drop
- `_handleFileSelect(event)`: Handle file browser selection
- `_validateFileType(file)`: Check file type
- `_validateFileSize(file)`: Check file size
- `_showProgress(fileId, progress)`: Update progress UI


