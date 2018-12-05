(function defaultVersionSelector() {
    var select = document.querySelector('#default_version');
    if (select) {
        var versionIdentifiers = Array.prototype.slice.call(
            document.querySelectorAll('.semver_identifier[data-semver-identifier]'));
        if (versionIdentifiers) {
            select.onchange = function select(e) {
                versionIdentifiers.forEach(function each(versionIdentifier) {
                    if (versionIdentifier.dataset.versionIdentifier === e.target.value) {
                        versionIdentifier.classList.add('default');
                    } else {
                        versionIdentifier.classList.remove('default');
                    }
                });
            };
        }
    }
})();