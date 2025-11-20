// Wrap everything in DOMContentLoaded to ensure elements exist
document.addEventListener('DOMContentLoaded', function() {
  
  // Divider resize functionality
  const divider = document.getElementById('divider');
  const left = document.getElementById('left');
  const right = document.getElementById('right');
  const container = document.getElementById('container');

  if (divider && left && right && container) {
    let isResizing = false;

    divider.addEventListener('mousedown', () => {
      isResizing = true;
      document.addEventListener('mousemove', resize);
      document.addEventListener('mouseup', stopResize);
    });

    function stopResize() {
      isResizing = false;
      document.removeEventListener('mousemove', resize);
      document.removeEventListener('mouseup', stopResize);
    }

    function resize(e) {
      if (!isResizing) return;
      const containerWidth = container.offsetWidth;
      const leftWidth = e.clientX / containerWidth * 100;
      left.style.flex = leftWidth;
      right.style.flex = 100 - leftWidth;
    }
  }

  // Toggle content functionality
  window.toggleContent = function(id) {
    const sections = ['start', 'element', 'channel', 'code'];
    sections.forEach(section => {
      const el = document.getElementById(section);
      if (el) el.style.display = 'none';
    });
    const target = document.getElementById(id);
    if (target) target.style.display = 'block';
  }

  // Initialize tooltips
  initializeTooltips();

  // Setup observer for dynamically added toggle buttons
  setupToggleObserver();
});

// Observer to handle dynamically added elements
function setupToggleObserver() {
  const observer = new MutationObserver(function(mutations) {
    mutations.forEach(function(mutation) {
      mutation.addedNodes.forEach(function(node) {
        if (node.nodeType === 1) { // Element node
          // Check if the added node contains toggleText
          const toggleText = node.id === 'toggleText' ? node : node.querySelector('#toggleText');
          if (toggleText) {
            attachToggleListener(toggleText);
          }
          
          // Also check for elements with IDs starting with 'activity'
          const activityDivs = node.querySelectorAll ? node.querySelectorAll('[id^="activity"]') : [];
          if (node.id && node.id.startsWith('activity')) {
            activityDivs.push(node);
          }
          
          // Find matching pairs of toggleText and activity divs
          document.querySelectorAll('[id^="toggleText"]').forEach(toggle => {
            const suffix = toggle.id.replace('toggleText', '');
            const activityDiv = document.getElementById('activity' + suffix);
            if (activityDiv && !toggle.dataset.listenerAttached) {
              attachToggleListener(toggle, activityDiv);
            }
          });
        }
      });
    });
  });

  observer.observe(document.body, {
    childList: true,
    subtree: true
  });
}

function attachToggleListener(toggleElement, targetDiv) {
  // Prevent attaching multiple listeners
  console.log('Attaching listener to', toggleElement.id);
  if (toggleElement.dataset.listenerAttached) {
    return;
  }
  
  // If targetDiv not provided, try to find it based on suffix
  if (!targetDiv) {
    const suffix = toggleElement.id.replace('toggleText', '');
    targetDiv = document.getElementById('activity' + suffix);
  }
  
  if (!targetDiv) {
    // Fallback to original ID
    targetDiv = document.getElementById('activity_test');
  }
  
  if (targetDiv) {
    toggleElement.addEventListener('click', function() {
      if (targetDiv.style.display === 'none') {
        targetDiv.style.display = 'block';
        toggleElement.textContent = 'Hide';
      } else {
        targetDiv.style.display = 'none';
        toggleElement.textContent = 'Show';
      }
    });
    
    // Mark as having listener attached
    toggleElement.dataset.listenerAttached = 'true';
    
    // Set initial state to hidden
    targetDiv.style.display = 'none';
    toggleElement.textContent = 'Show';
  }
}

function initializeTooltips() {
  document.querySelectorAll('.fs-tooltip').forEach(tooltip => {
    tooltip.addEventListener('mouseenter', function(e) {
      const tooltipElement = this;
      const rect = tooltipElement.getBoundingClientRect();
      
      // Tooltip dimensions
      const tooltipWidth = 400;
      const tooltipHeight = 150;
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
      
      // Check if tooltip would go below viewport
      if (top + tooltipHeight > window.innerHeight - 20) {
        // Flip to show above
        top = rect.top - gap;
        arrowTop = rect.top - arrowSize;
        
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