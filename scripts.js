const divider = document.getElementById('divider');
const left = document.getElementById('left');
const right = document.getElementById('right');
const container = document.getElementById('container');


divider.addEventListener('mousedown', () => {
  document.addEventListener('mousemove', resize);
  document.addEventListener('mouseup', () => {
    document.removeEventListener('mousemove', resize);
  });
});

function resize(e) {
  const containerWidth = container.offsetWidth;
  const leftWidth = e.clientX / containerWidth * 100;
  left.style.flex = leftWidth;
  right.style.flex = 100 - leftWidth;
}

function toggleContent(id) {
  document.getElementById('start').style.display = 'none';
  document.getElementById('element').style.display = 'none';
  document.getElementById('channel').style.display = 'none';
  document.getElementById('code').style.display = 'none';
  document.getElementById(id).style.display = 'block';
}

// Tooltip boundary detection - wrapped in DOMContentLoaded to ensure elements exist
document.addEventListener('DOMContentLoaded', function() {
  initializeTooltips();
});

// Also initialize when page is already loaded (for dynamic content)
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initializeTooltips);
} else {
  initializeTooltips();
}

function initializeTooltips() {
  document.querySelectorAll('.fs-tooltip').forEach(tooltip => {
    tooltip.addEventListener('mouseenter', function(e) {
      const tooltipElement = this;
      const rect = tooltipElement.getBoundingClientRect();
      
      // Tooltip dimensions
      const tooltipWidth = 400; // max-width from CSS
      const tooltipHeight = 150; // estimated height (increased for safety)
      const gap = 10;
      const arrowSize = 8;
      
      // Calculate horizontal position (centered by default)
      let left = rect.left + (rect.width / 2);
      let translateX = -50;
      
      // Check right boundary
      if (left + (tooltipWidth / 2) > window.innerWidth - 20) {
        left = window.innerWidth - tooltipWidth - 20;
        translateX = 0;
      }
      
      // Check left boundary
      if (left - (tooltipWidth / 2) < 20) {
        left = 20;
        translateX = 0;
      }
      
      // Calculate vertical position
      let top = rect.bottom + gap;
      let arrowTop = rect.bottom;
      let flipAbove = false;
      
      // Check if tooltip would go below viewport
      if (top + tooltipHeight > window.innerHeight - 20) {
        // Flip to show above
        top = rect.top - gap;
        arrowTop = rect.top - arrowSize;
        flipAbove = true;
        
        tooltipElement.style.setProperty('--tooltip-transform', `translate(${translateX}%, -100%)`);
        tooltipElement.style.setProperty('--arrow-transform', `translate(-50%, 0)`);
        tooltipElement.style.setProperty('--flip-above', '1');
      } else {
        // Show below (default)
        top = rect.bottom + gap;
        arrowTop = rect.bottom + gap / 2;
        
        tooltipElement.style.setProperty('--tooltip-transform', `translate(${translateX}%, 0)`);
        tooltipElement.style.setProperty('--arrow-transform', `translate(-50%, -100%)`);
        tooltipElement.style.removeProperty('--flip-above');
      }
      
      // Set all CSS custom properties
      tooltipElement.style.setProperty('--tooltip-top', `${top}px`);
      tooltipElement.style.setProperty('--tooltip-left', `${left}px`);
      tooltipElement.style.setProperty('--arrow-top', `${arrowTop}px`);
      tooltipElement.style.setProperty('--arrow-left', `${rect.left + (rect.width / 2)}px`);
    });
    
    // Clean up on mouse leave
    tooltip.addEventListener('mouseleave', function() {
      this.style.removeProperty('--tooltip-top');
      this.style.removeProperty('--tooltip-left');
      this.style.removeProperty('--tooltip-transform');
      this.style.removeProperty('--arrow-top');
      this.style.removeProperty('--arrow-left');
      this.style.removeProperty('--arrow-transform');
      this.style.removeProperty('--flip-above');
    });
  });
}