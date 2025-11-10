const divider = document.getElementById('divider');
const left = document.getElementById('left');
const right = document.getElementById('right');
const container = document.getElementById('container');

fetch('crumbs.html')
  .then(response => response.text())
  .then(html => { document.getElementById('breadcrumb-container').innerHTML = html; });

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

function makeDraggable(element, handleSelector) {
  let pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;
  let isFirstDrag = true;
  
  const dragHandle = element.querySelector(handleSelector);
  
  if (dragHandle) {
    dragHandle.onmousedown = dragMouseDown;
  }
  
  function dragMouseDown(e) {
    e = e || window.event;
    e.preventDefault();
    
    // On first drag, remove transform and set absolute position
    if (isFirstDrag) {
      const rect = element.getBoundingClientRect();
      element.style.top = rect.top + 'px';
      element.style.left = rect.left + 'px';
      element.style.transform = 'none';
      isFirstDrag = false;
    }
    
    // Get the mouse cursor position at startup
    pos3 = e.clientX;
    pos4 = e.clientY;
    
    document.onmouseup = closeDragElement;
    document.onmousemove = elementDrag;
  }
  
  function elementDrag(e) {
    e = e || window.event;
    e.preventDefault();
    
    // Calculate the new cursor position
    pos1 = pos3 - e.clientX;
    pos2 = pos4 - e.clientY;
    pos3 = e.clientX;
    pos4 = e.clientY;
    
    // Get current position
    const currentTop = parseInt(element.style.top) || element.offsetTop;
    const currentLeft = parseInt(element.style.left) || element.offsetLeft;
    
    // Calculate new position
    let newTop = currentTop - pos2;
    let newLeft = currentLeft - pos1;
    
    // Get element dimensions
    const elementWidth = element.offsetWidth;
    const elementHeight = element.offsetHeight;
    
    // Get viewport dimensions
    const viewportWidth = window.innerWidth;
    const viewportHeight = window.innerHeight;
    
    // Constrain to viewport bounds
    newTop = Math.max(0, Math.min(newTop, viewportHeight - elementHeight));
    newLeft = Math.max(0, Math.min(newLeft, viewportWidth - elementWidth));
    
    // Set the element's new position
    element.style.top = newTop + "px";
    element.style.left = newLeft + "px";
  }
  
  function closeDragElement() {
    document.onmouseup = null;
    document.onmousemove = null;
  }
}

window.addEventListener('load', function() {
  setTimeout(function() {
    // Find all elements with the 'draggable-card' class
    const draggableElements = document.querySelectorAll('.draggable-card');
    
    draggableElements.forEach(function(element) {
      makeDraggable(element, '.drag-handle');
    });
  }, 1000);
});