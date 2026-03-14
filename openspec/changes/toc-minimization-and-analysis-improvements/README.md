# TOC Minimization and Analysis Improvements

## Change ID
`TOC-ANALYSIS-001`

## Status
📝 **Draft** - Ready for review and implementation

## Quick Links
- [Proposal](./proposal.md) - Problem statement and proposed solution
- [Specification](./spec.md) - Detailed technical specification
- [Tasks](./tasks.md) - Implementation task breakdown

---

## Overview

This change improves the Financial Analysis Report Generator in two key areas:

1. **Collapsible Table of Contents**: Minimize the TOC to save screen space, expanding on hover
2. **Enhanced Document Analysis**: Improve detection and analysis of bills, invoices, and bank statements

## Problem

### Current Issues
- **TOC takes up ~50% of screen width** - Reduces space for report content
- **Poor document type detection** - Most documents misidentified as income statements
- **Incorrect categorization** - Bills and invoices not properly categorized as expenses
- **Missing provider detection** - Xfinity, T-Mobile, Amazon, etc. not identified

### Impact
- Poor user experience with cluttered interface
- Inaccurate financial analysis and insights
- User confusion and loss of trust in the tool

## Solution

### Part 1: Collapsible TOC
- **Minimized**: 40px vertical bar on left side
- **Expanded**: 280px full TOC on hover/focus
- **Smooth transitions**: 300ms animations
- **Accessible**: Full keyboard and screen reader support
- **Mobile-friendly**: Touch support with auto-collapse

### Part 2: Enhanced Analysis
- **Improved patterns**: Detect Amazon invoices, Chase statements, utility bills
- **Better extraction**: Extract key fields from each document type
- **Proper categorization**: Bills → expenses, deposits → income
- **Provider detection**: Identify Xfinity, T-Mobile, ComEd, Amazon, Chase

## Benefits

✅ **More screen space** - 90% more horizontal space for content  
✅ **Cleaner interface** - Less visual clutter  
✅ **Accurate analysis** - >90% detection accuracy  
✅ **Better insights** - Proper expense tracking  
✅ **User trust** - Correct categorization builds confidence  

## Implementation Plan

### Phase 1: TOC Minimization (1 day)
1. Design minimized/expanded states
2. Implement CSS with transitions
3. Add JavaScript for pin/unpin
4. Enhance accessibility

### Phase 2: Analysis Improvements (2-3 days)
1. Analyze sample PDFs
2. Update detection patterns
3. Enhance extraction rules
4. Improve categorization
5. Add provider identification

### Phase 3: Testing (1 day)
1. Test TOC on all devices
2. Validate detection accuracy
3. End-to-end testing

**Total Duration**: 3-4 days

## Success Criteria

- [x] TOC <10% screen width when minimized
- [x] TOC expands smoothly on hover (<300ms)
- [x] All accessibility features maintained
- [x] Document detection accuracy >90%
- [x] Proper expense categorization
- [x] Major providers identified

## Files to Modify

### TOC Changes
- `pages/financial-analysis.html` - CSS and JavaScript updates

### Analysis Changes
- `pages/js/components/DocumentTypeDetector.js` - New patterns
- `pages/js/components/ExtractionEngine.js` - Enhanced rules
- `pages/js/components/TransactionExtractor.js` - Better categorization

## Testing Strategy

### TOC Testing
- Visual regression testing
- Accessibility testing (WCAG 2.1 AA)
- Cross-browser testing (Chrome, Firefox, Safari, Edge)
- Responsive testing (desktop, tablet, mobile)

### Analysis Testing
- Detection accuracy testing with real PDFs
- Extraction accuracy validation
- Categorization correctness verification
- Performance testing (no degradation)

## Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| TOC breaks on mobile | Medium | Thorough responsive testing |
| Detection patterns too specific | Low | Use flexible regex patterns |
| Performance degradation | Low | Profile and optimize if needed |
| Accessibility regression | Medium | Automated accessibility testing |

## Dependencies

- Existing IDP components (DocumentTypeDetector, ExtractionEngine)
- Current TOC implementation
- PDF.js for text extraction
- Chart.js for visualizations

## Related Changes

- **IDP Phase 1-5**: Intelligent Document Processing foundation
- **BEAD-001 to BEAD-051**: Original financial analysis implementation

## Next Steps

1. ✅ Create OpenSpec change
2. ✅ Write proposal, spec, and tasks
3. ⏳ Review and approve specification
4. ⏳ Implement Phase 1 (TOC)
5. ⏳ Implement Phase 2 (Analysis)
6. ⏳ Test and validate
7. ⏳ Deploy and monitor

## Questions & Decisions

### Open Questions
- Should TOC auto-collapse on mobile after section selection? **→ Yes**
- Should we add a pin icon to indicate pinned state? **→ Yes**
- What should the default state be (minimized or expanded)? **→ Minimized**

### Decisions Made
- Use hover-based expansion (not click-only)
- Maintain fixed positioning for TOC
- Keep existing TOC structure, just add collapse behavior
- Focus on common document types first (Amazon, Chase, utilities)

## Contact

For questions or feedback on this change:
- Review the specification documents
- Check the task breakdown
- Test with actual PDFs from `pages/fin-analysis/`

---

**Last Updated**: 2026-02-08  
**Change Owner**: Financial Analysis Team  
**Reviewers**: TBD

