function formSubmitToXHR(form) {
    var csrfTokenInput = form.querySelector('[name=csrfmiddlewaretoken]');
    var csrfToken = csrfTokenInput ? csrfTokenInput.value : null;

    var errorContainer = form.querySelector('.error_container');

    var method = (form.attributes.method || {}).value;
    if (!method) {
        throw new Error('No HTTP method attribute was found on the form.')
    }

    var action = form.action;
    var xhr = new XMLHttpRequest();

    var formData = new FormData(form);
    delete formData.name;
    delete formData.date_created;
    delete formData.date_modified;

    xhr.withCredentials = true;
    xhr.open(method, action);
    xhr.setRequestHeader('X-CSRFToken', csrfToken);

    xhr.onload = function onload(e) {
        var responseObj = {};
        try {
            responseObj = JSON.parse(this.responseText);
        } catch (e) {}

        if (this.status === 200) {
            /* Redirect back to the account page. */
            if (form.dataset.redirectUrl) {
                window.location = form.dataset.redirectUrl;
            } else {
                window.location.reload();
            }
        } else if (errorContainer) {
            var errKeys = Object.keys(responseObj);
            for (var ii = 0; ii < errKeys.length; ii += 1) {
                var li = document.createElement('li');
                var errs = responseObj[errKeys[ii]];
                var text = errKeys[ii] + ':\n';
                for (var jj = 0; jj < errs.length; jj += 1) {
                    text += responseObj[errKeys[ii]][jj] + '\n';
                }

                li.textContent = text;
                errorContainer.appendChild(li);
            }

            /* Clear the error after a timeout. */
            setTimeout(function timeout() {
                errorContainer.innerHTML = '';
            }, 6000);
        } else {
            console.log('Could not find error element. Error was:');
            console.log(responseObj.error);
        }
    };

    xhr.send(formData);

    return false;
}
