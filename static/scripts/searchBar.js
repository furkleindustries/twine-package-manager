(function iife() {
    function searchRedirect(query) {
        location.assign('/packages/search?query=' + encodeURIComponent(query));
    }

    var searchBar = document.querySelector('.search-bar');
    searchBar.addEventListener('keydown', function (e) {
        if (searchBar.value && e.keyCode === 13) {
            searchRedirect(searchBar.value);
        }
    });

    var searchButton = document.querySelector('.search-button');
    searchButton.addEventListener('click', function () {
        if (searchBar.value) {
            searchRedirect(searchBar.value);
        }
    });
})();
