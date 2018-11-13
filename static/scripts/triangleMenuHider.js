(function hider() {
    Array.prototype.slice.call(document.querySelectorAll('.hider')).forEach(function each(hider) {
        var parent = hider.parentElement;
        var hideable = parent.querySelector('.hideable');
        if (parent && hideable) {
            hider.addEventListener('click', function click() {
                if (hideable.classList.contains('hidden')) {
                    hideable.classList.remove('hidden');
                    hider.textContent = '▼';   
                } else {
                    hideable.classList.add('hidden');
                    hider.textContent = '▶';
                }
            });
        }
    });
})();