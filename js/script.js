document.addEventListener("DOMContentLoaded", function() {
    const treeItems = document.querySelectorAll('.tree_label');

    treeItems.forEach(item => {
        // Find the hidden tooltip content element
        const tooltipContentElement = item.querySelector('.tooltip-content');
        if (tooltipContentElement) {
            // Split text content for each section based on a semicolon delimiter
            const [text1, text2, text3] = tooltipContentElement.innerHTML.split(';');

            // Create a tooltip element with three sections
            const tooltip = document.createElement('div');
            tooltip.className = 'tooltip';

            const section1 = document.createElement('div');
            section1.className = 'tooltip-section';
            section1.innerHTML = text1 || '';

            const section2 = document.createElement('div');
            section2.className = 'tooltip-section';
            section2.innerHTML = text2 || '';

            const section3 = document.createElement('div');
            section3.className = 'tooltip-section';
            section3.innerHTML = text3 || '';

            tooltip.appendChild(section1);
            tooltip.appendChild(section2);
            tooltip.appendChild(section3);

            item.appendChild(tooltip);
        }

        item.addEventListener('mouseenter', function() {
            // Highlight the current item
            item.classList.add('current-highlight');

            // Highlight current item's parents
            let currentElement = item.closest('li');
            while (currentElement) {
                const parentLabel = currentElement.querySelector('.tree_label');
                if (parentLabel && parentLabel !== item) {
                    parentLabel.classList.add('parent-highlight');
                }
                currentElement = currentElement.parentElement.closest('li');
            }

            // Highlight children
            let childLabels = item.parentElement.querySelectorAll('.tree_label');
            childLabels.forEach(child => {
                if (child !== item) {
                    child.classList.add('child-highlight');
                }
            });

            // Show the tooltip
            const tooltip = item.querySelector('.tooltip');
            if (tooltip) {
                tooltip.style.visibility = 'visible';
                tooltip.style.opacity = '1';
            }
        });

        item.addEventListener('mouseleave', function() {
            // Remove all highlight classes
            const highlighted = document.querySelectorAll('.parent-highlight, .child-highlight, .current-highlight');
            highlighted.forEach(el => el.classList.remove('parent-highlight', 'child-highlight', 'current-highlight'));

            // Hide the tooltip
            const tooltip = item.querySelector('.tooltip');
            if (tooltip) {
                tooltip.style.visibility = 'hidden';
                tooltip.style.opacity = '0';
            }
        });
    });
});
