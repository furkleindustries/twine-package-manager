function formSubmitToXHR(form) {
    var csrfTokenInput = form.querySelector('[name=csrfmiddlewaretoken]');
    var csrfToken = csrfTokenInput ? csrfTokenInput.value : null;

    var errorContainer = form.querySelector('.error-container');

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

        if (this.status.toString()[0] === '2') {
            /* Redirect back to the account page. */
            if (form.dataset.redirectUrl) {
                window.location = form.dataset.redirectUrl;
            } else {
                window.location.reload();
            }
        } else if (errorContainer) {
            var errKeys = Object.keys(responseObj);
            if (errKeys.length) {
                for (var ii = 0; ii < errKeys.length; ii += 1) {
                    var errs = responseObj[errKeys[ii]];
                    var li = document.createElement('li');
                    var pre = document.createElement('pre');
                    var text = errKeys[ii] + ':\n';
                    if (errs && errs.length) {
                        for (var jj = 0; jj < errs.length; jj += 1) {
                            var err = responseObj[errKeys[ii]][jj];
                            if (typeof err === 'string') {
                                text += err + '\n';
                            } else {
                                text += JSON.stringify(err) + '\n';
                            }
                        }
                    } else {
                        text += JSON.stringify(errs) + '\n';
                    }
    
                    pre.textContent = text;
                    li.appendChild(pre);
                    errorContainer.appendChild(li);
                }
            } else {
                var li = document.createElement('li');
                var pre = document.createElement('pre');
                pre.textContent = 'Unknown error.';
                li.appendChild(pre);
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
