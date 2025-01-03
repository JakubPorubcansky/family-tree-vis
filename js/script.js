document.addEventListener("DOMContentLoaded", function() {
    const treeItems = document.querySelectorAll('.tree_label');

    treeItems.forEach(item => {
        item.addEventListener('mouseenter', function() {

            // Highlight current item differently
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
        });

        item.addEventListener('mouseleave', function() {
            const highlighted = document.querySelectorAll('.parent-highlight, .child-highlight, .current-highlight');
            highlighted.forEach(el => el.classList.remove('parent-highlight', 'child-highlight', 'current-highlight'));
        });
    });
});
