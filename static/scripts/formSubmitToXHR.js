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
            var errors;
            try {
                errors = JSON.parse(responseObj.error);
            } catch (e) {}

            if (!Array.isArray(errors)) {
                if (responseObj.error) {
                    errors = [ responseObj.error, ];
                } else {
                    errors = [];
                }
            }

            errors.forEach(function each(err) {
                var li = document.createElement('li');
                li.textContent = err;
                error.appendChild(li);
            });

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
