(function editOnBeforeUnloadHandler() {
    var inputs = Array.prototype.slice.call(
        document.querySelectorAll('input, select, textarea'));

    var submitter = document.querySelector('#submit');

    if (inputs.length > 0 && submitter) {
        inputs.forEach(function each(input) {
            input.addEventListener('change', function change(e) {
                if (!window.onbeforeunload) {
                    window.onbeforeunload = onbeforeunload;
                }
            });
        });

        /* Remove the event listener after the form is submitted. */
        submitter.addEventListener('click', function submit(e) {
            window.onbeforeunload = function noop() {
                /* In some cases, deleting or setting to null the
                 * onbeforeunload property does not prevent the function from
                 * firing. This, however, replaces it with a no-op. */
            };
        });
    }

    function onbeforeunload(e) {
        var retVal = 'You have made modifications, but they have not been ' +
                     'saved to the database, and will be lost if you ' +
                     'navigate away from the page.';
        e.returnValue = retVal;
        return retVal;
    }
})();