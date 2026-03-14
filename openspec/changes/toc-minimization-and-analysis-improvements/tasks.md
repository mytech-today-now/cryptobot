# Tasks: TOC Minimization and Analysis Improvements

## Change ID
`TOC-ANALYSIS-001`

## Version
1.0.0

## Status
Draft

## Last Updated
2026-02-08

---

## Overview

This document breaks down the implementation into discrete tasks organized by phase.

**Total Tasks**: 12
**Estimated Duration**: 3-4 days

---

## Phase 1: TOC Minimization (1 day)

### Task 1.1: Design Minimized TOC UI
**Priority**: High
**Estimated Time**: 2 hours
**Dependencies**: None

**Description**:
Design the visual appearance of the minimized and expanded TOC states.

**Acceptance Criteria**:
- [ ] Minimized state shows vertical bar with icon
- [ ] Expanded state shows full TOC
- [ ] Smooth transition between states
- [ ] Visually appealing and professional

**Deliverables**:
- CSS design for minimized state
- CSS design for expanded state
- Transition animations

---

### Task 1.2: Implement TOC CSS
**Priority**: High
**Estimated Time**: 3 hours
**Dependencies**: Task 1.1

**Description**:
Implement the CSS for collapsible TOC with hover and focus states.

**Acceptance Criteria**:
- [ ] TOC is 40px wide when minimized
- [ ] TOC expands to 280px on hover
- [ ] Smooth 300ms transition
- [ ] Fixed positioning works correctly
- [ ] Content hidden when minimized

**Deliverables**:
- Updated CSS in `financial-analysis.html`
- Responsive styles for mobile

---

### Task 1.3: Add TOC JavaScript Functionality
**Priority**: High
**Estimated Time**: 3 hours
**Dependencies**: Task 1.2

**Description**:
Add JavaScript for pin/unpin, mobile touch, and state management.

**Acceptance Criteria**:
- [ ] Click to pin/unpin TOC
- [ ] Touch support for mobile
- [ ] State persists in localStorage
- [ ] Debounced collapse on mouse leave
- [ ] Keyboard navigation works

**Deliverables**:
- JavaScript for TOC state management
- Event handlers for interactions
- localStorage integration

---

### Task 1.4: Enhance TOC Accessibility
**Priority**: High
**Estimated Time**: 2 hours
**Dependencies**: Task 1.3

**Description**:
Ensure TOC meets accessibility standards with proper ARIA attributes and keyboard support.

**Acceptance Criteria**:
- [ ] `aria-expanded` updates correctly
- [ ] `aria-label` describes state
- [ ] Keyboard navigation (Tab, Enter, Escape)
- [ ] Screen reader announcements
- [ ] Focus indicators visible

**Deliverables**:
- ARIA attributes
- Keyboard event handlers
- Screen reader testing notes

---

## Phase 2: Document Analysis Improvements (2-3 days)

### Task 2.1: Analyze Sample PDFs
**Priority**: High
**Estimated Time**: 4 hours
**Dependencies**: None

**Description**:
Review actual PDFs from each category to understand their structure and content patterns.

**Acceptance Criteria**:
- [ ] Reviewed 5+ Amazon invoices
- [ ] Reviewed 5+ bank statements
- [ ] Reviewed 5+ utility bills (each type)
- [ ] Documented patterns and keywords
- [ ] Identified extraction fields

**Deliverables**:
- PDF analysis notes
- Pattern documentation
- Keyword lists per document type

---

### Task 2.2: Update Document Type Detection Patterns
**Priority**: High
**Estimated Time**: 4 hours
**Dependencies**: Task 2.1

**Description**:
Update `DocumentTypeDetector.js` with improved filename and content patterns.

**Acceptance Criteria**:
- [ ] Amazon invoice pattern added
- [ ] Chase bank statement pattern added
- [ ] Water/sewer bill pattern added
- [ ] Xfinity bill pattern added
- [ ] T-Mobile bill pattern added
- [ ] Generic invoice pattern added
- [ ] All patterns tested

**Deliverables**:
- Updated `DocumentTypeDetector.js`
- Unit tests for new patterns

---

### Task 2.3: Enhance Extraction Rules
**Priority**: High
**Estimated Time**: 6 hours
**Dependencies**: Task 2.1, Task 2.2

**Description**:
Create or update extraction rules for each document type in `ExtractionEngine.js`.

**Acceptance Criteria**:
- [ ] Bank statement extraction rules
- [ ] Amazon invoice extraction rules
- [ ] Utility bill extraction rules
- [ ] All required fields extracted
- [ ] >85% extraction accuracy

**Deliverables**:
- Updated extraction rules
- Field validators and parsers
- Unit tests for extraction

---

### Task 2.4: Improve Transaction Categorization
**Priority**: High
**Estimated Time**: 3 hours
**Dependencies**: Task 2.3

**Description**:
Update transaction categorization logic to properly classify bills as expenses.

**Acceptance Criteria**:
- [ ] Utility bills categorized as expenses
- [ ] Invoices categorized as expenses
- [ ] Bank deposits categorized as income
- [ ] Proper subcategories assigned
- [ ] Category confidence scores

**Deliverables**:
- Updated categorization logic
- Category mapping rules
- Unit tests

---

### Task 2.5: Add Provider Identification
**Priority**: Medium
**Estimated Time**: 2 hours
**Dependencies**: Task 2.2

**Description**:
Implement provider detection and mapping for major providers.

**Acceptance Criteria**:
- [ ] Xfinity/Comcast detected
- [ ] T-Mobile detected
- [ ] ComEd detected
- [ ] Amazon detected
- [ ] Chase detected
- [ ] Provider shown in reports

**Deliverables**:
- Provider mapping logic
- Provider display in UI

---

## Phase 3: Testing & Validation (1 day)

### Task 3.1: Test TOC on All Devices
**Priority**: High
**Estimated Time**: 2 hours
**Dependencies**: Task 1.4

**Description**:
Test TOC functionality on desktop, tablet, and mobile devices.

**Acceptance Criteria**:
- [ ] Works on Chrome, Firefox, Safari, Edge
- [ ] Works on desktop (1920x1080, 1366x768)
- [ ] Works on tablet (768x1024)
- [ ] Works on mobile (375x667)
- [ ] No layout issues

**Deliverables**:
- Testing report
- Bug fixes if needed

---

### Task 3.2: Validate Document Detection Accuracy
**Priority**: High
**Estimated Time**: 3 hours
**Dependencies**: Task 2.2

**Description**:
Test document type detection with actual PDFs from the fin-analysis directory.

**Acceptance Criteria**:
- [ ] >90% accuracy on Amazon invoices
- [ ] >90% accuracy on bank statements
- [ ] >85% accuracy on utility bills
- [ ] All major providers detected
- [ ] No false positives

**Deliverables**:
- Accuracy test results
- Confusion matrix
- Bug fixes if needed

---

### Task 3.3: End-to-End Testing
**Priority**: High
**Estimated Time**: 3 hours
**Dependencies**: All previous tasks

**Description**:
Perform complete end-to-end testing with full document set.

**Acceptance Criteria**:
- [ ] Upload and analyze 50+ PDFs
- [ ] Verify correct categorization
- [ ] Verify extraction accuracy
- [ ] Verify report generation
- [ ] No errors or crashes

**Deliverables**:
- E2E test report
- Performance metrics
- Final bug fixes

---

## Task Summary

### By Phase
- **Phase 1**: 4 tasks (1 day)
- **Phase 2**: 5 tasks (2-3 days)
- **Phase 3**: 3 tasks (1 day)

**Total**: 12 tasks, 3-4 days

### By Priority
- **High**: 11 tasks
- **Medium**: 1 task

