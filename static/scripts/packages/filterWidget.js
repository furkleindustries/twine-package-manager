(function () {
    var orderingField = document.querySelector('.packages-ordering-field');
    var orderingDirection = document.querySelector('.packages-ordering-direction');
    var updateButton = document.querySelector('.packages-update');
    var offset = (location.href.match(/\/[^/]+(offset=\d+)/) || [])[1];
    updateButton.addEventListener('click', function () {
        var direction = orderingDirection.value === 'ascending' ? '' : '-'; 
        var pathname = '/packages/?' +
            'ordering=' + direction + orderingField.value;

        if (offset) {
            pathname += '&' + offset;
        }

        location.href = pathname;
    });
})();