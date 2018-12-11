(function () {
    var input = document.querySelector('.package-delete .confirmation');
    var submit = document.querySelector('.package-delete .submit');
    if (input && submit) {
        input.addEventListener('keyup', function () {
            if (input.value && input.value === input.dataset.packageName) {
                submit.removeAttribute('disabled');
            } else {
                submit.setAttribute('disabled', '');
            }
        });
    }
})();
