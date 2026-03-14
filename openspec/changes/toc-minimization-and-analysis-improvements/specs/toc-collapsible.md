# Specification: Collapsible Table of Contents

## Overview
Implement a hover-based collapsible Table of Contents that minimizes to save screen space.

---

## Requirements

### Functional Requirements

#### FR-1: Minimized State
- TOC shall be minimized by default on page load
- Minimized width shall be 40px
- Shall display a vertical bar with hamburger icon (☰)
- Shall display "TOC" text rotated 90° clockwise

#### FR-2: Expanded State
- TOC shall expand to 280px width on hover
- Shall display full table of contents with all sections
- Shall include a pin icon in the top-right corner
- Shall show all navigation links

#### FR-3: Hover Behavior
- TOC shall expand 100ms after mouse enters the minimized bar
- TOC shall collapse 500ms after mouse leaves (debounced)
- Hover state shall not apply when TOC is pinned

#### FR-4: Pin/Unpin Functionality
- User shall be able to click pin icon to keep TOC expanded
- Pinned state shall persist across page reloads (localStorage)
- Pin icon shall change appearance when pinned (filled vs outline)
- Clicking pin icon again shall unpin and allow auto-collapse

#### FR-5: Mobile Behavior
- On mobile/tablet, tap shall toggle TOC expanded/collapsed
- TOC shall auto-collapse after selecting a section
- Swipe gestures shall be supported (optional)

### Non-Functional Requirements

#### NFR-1: Performance
- Transition animation shall complete within 300ms
- No layout shift or jank during animation
- Smooth 60fps animation

#### NFR-2: Accessibility
- Keyboard navigation shall work (Tab, Enter, Escape)
- `aria-expanded` attribute shall update on state change
- Screen readers shall announce state changes
- Focus indicators shall be visible
- WCAG 2.1 AA compliance maintained

#### NFR-3: Responsive Design
- Shall work on desktop (1920x1080, 1366x768)
- Shall work on tablet (768x1024)
- Shall work on mobile (375x667, 414x896)
- No horizontal scrolling on any screen size

---

## Technical Specification

### HTML Structure

```html
<nav id="table-of-contents" 
     class="toc-minimized" 
     aria-label="Report table of contents"
     aria-expanded="false">
  
  <!-- Minimized view -->
  <div class="toc-minimized-bar">
    <span class="toc-icon">☰</span>
    <span class="toc-label">TOC</span>
  </div>
  
  <!-- Expanded view -->
  <div class="toc-content">
    <div class="toc-header">
      <h2>Table of Contents</h2>
      <button class="toc-pin-btn" 
              aria-label="Pin table of contents"
              aria-pressed="false">
        📌
      </button>
    </div>
    <ul class="toc-list">
      <!-- TOC items -->
    </ul>
  </div>
</nav>
```

### CSS Specification

```css
#table-of-contents {
  position: fixed;
  left: 0;
  top: 80px;
  height: calc(100vh - 80px);
  width: 40px;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-right: 1px solid #e0e0e0;
  box-shadow: 2px 0 8px rgba(0, 0, 0, 0.05);
  transition: width 300ms cubic-bezier(0.4, 0.0, 0.2, 1);
  overflow: hidden;
  z-index: 1000;
}

#table-of-contents:hover,
#table-of-contents:focus-within,
#table-of-contents.pinned {
  width: 280px;
  box-shadow: 4px 0 12px rgba(0, 0, 0, 0.15);
}

.toc-minimized-bar {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 1rem 0;
  gap: 0.5rem;
}

.toc-icon {
  font-size: 1.5rem;
  color: var(--primary-color);
}

.toc-label {
  writing-mode: vertical-rl;
  text-orientation: mixed;
  font-weight: 600;
  color: var(--primary-color);
  letter-spacing: 0.1em;
}

.toc-content {
  opacity: 0;
  pointer-events: none;
  transition: opacity 200ms ease-in-out 100ms;
  padding: 1.5rem;
}

#table-of-contents:hover .toc-content,
#table-of-contents:focus-within .toc-content,
#table-of-contents.pinned .toc-content {
  opacity: 1;
  pointer-events: auto;
}

.toc-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.toc-pin-btn {
  background: none;
  border: none;
  font-size: 1.2rem;
  cursor: pointer;
  padding: 0.25rem;
  opacity: 0.6;
  transition: opacity 200ms;
}

.toc-pin-btn:hover {
  opacity: 1;
}

.toc-pin-btn[aria-pressed="true"] {
  opacity: 1;
  filter: grayscale(0);
}

/* Mobile styles */
@media (max-width: 768px) {
  #table-of-contents {
    width: 0;
    border-right: none;
  }
  
  #table-of-contents.expanded {
    width: 280px;
  }
  
  .toc-minimized-bar {
    display: none;
  }
}
```

### JavaScript Specification

```javascript
class TOCController {
  constructor() {
    this.toc = document.getElementById('table-of-contents');
    this.pinBtn = this.toc.querySelector('.toc-pin-btn');
    this.isPinned = localStorage.getItem('toc-pinned') === 'true';
    this.collapseTimeout = null;
    
    this.init();
  }
  
  init() {
    // Restore pinned state
    if (this.isPinned) {
      this.pin();
    }
    
    // Event listeners
    this.pinBtn.addEventListener('click', () => this.togglePin());
    this.toc.addEventListener('mouseenter', () => this.handleMouseEnter());
    this.toc.addEventListener('mouseleave', () => this.handleMouseLeave());
    
    // Mobile touch support
    if ('ontouchstart' in window) {
      this.setupMobileTouch();
    }
  }
  
  togglePin() {
    this.isPinned = !this.isPinned;
    localStorage.setItem('toc-pinned', this.isPinned);
    
    if (this.isPinned) {
      this.pin();
    } else {
      this.unpin();
    }
  }
  
  pin() {
    this.toc.classList.add('pinned');
    this.pinBtn.setAttribute('aria-pressed', 'true');
    this.pinBtn.setAttribute('aria-label', 'Unpin table of contents');
    this.announceToScreenReader('Table of contents pinned');
  }
  
  unpin() {
    this.toc.classList.remove('pinned');
    this.pinBtn.setAttribute('aria-pressed', 'false');
    this.pinBtn.setAttribute('aria-label', 'Pin table of contents');
    this.announceToScreenReader('Table of contents unpinned');
  }
  
  handleMouseEnter() {
    if (!this.isPinned) {
      clearTimeout(this.collapseTimeout);
      this.toc.setAttribute('aria-expanded', 'true');
    }
  }
  
  handleMouseLeave() {
    if (!this.isPinned) {
      this.collapseTimeout = setTimeout(() => {
        this.toc.setAttribute('aria-expanded', 'false');
      }, 500);
    }
  }
  
  setupMobileTouch() {
    // Mobile-specific touch handlers
  }
  
  announceToScreenReader(message) {
    // Create live region announcement
  }
}
```

---

## Acceptance Criteria

- [ ] TOC is 40px wide when minimized
- [ ] TOC expands to 280px on hover within 300ms
- [ ] Pin/unpin functionality works correctly
- [ ] Pinned state persists across page reloads
- [ ] Mobile tap-to-toggle works
- [ ] Keyboard navigation works (Tab, Enter, Escape)
- [ ] Screen reader announces state changes
- [ ] No layout shift during animation
- [ ] Works on all supported browsers and devices
- [ ] WCAG 2.1 AA compliant

