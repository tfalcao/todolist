__author__ = 'cody'

REQUEST_EMPTY = "Request contains no data"
MALFORMED_JSON = "Request contains malformed JSON"

EXPECTED_JSON_OBJECT = "Expected a JSON Object, not a JSON Array."
INSUFFICIENT_FIELDS = "Required fields missing. Fields required are: {}"

RESOURCE_ALREADY_EXISTS = "Resource already exists"
RESOURCE_NOT_FOUND = "Resource not found"
RESOURCE_DELETED = "Resource deleted"
RESOURCE_UPDATED = "Resource updated"
RESOURCE_CREATED = "Resource created"

INTERNAL_EXCEPTION = "There has been an internal exception."
AUTHENTICATION_FAILURE = "Authentication failed"

EMPTY_USERNAME_OR_PASSWORD = "Username or password is missing"
EMPTY_CAPTCHA = "You seem to have forgotten to fill out the reCAPTCHA"
INCORRECT_USERNAME_OR_PASSWORD = "Incorrect username or password"
DUMMY_FIELD_DATA = "You seem to have put data into the dummy fields. Please leave these fields empty on submission"
NOT_ALL_REQUIRED_FIELDS_RECEIVED = "Not all required fields have been filled in"
PASSWORDS_NOT_MATCH = "The supplied passwords do not match"

USER_ALREADY_EXISTS = "User already exists"
USER_NOT_FOUND = "User not found"
USER_CREATED = "New user created successfully. You may now log in"
USER_DELETED = "User deleted"

TASK_ALREADY_EXISTS = "Task already exists"
TASK_NOT_FOUND = "Task not found"
TASK_CREATED = "New task created successfully"
TASK_DELETED = "Task deleted"

LOGIN_SUCCESSFUL = "Login successful"
UPDATE_SUCCESSFUL = "Update successful"
PASSWORDS_CHANGED_SUCCESSFULLY = "Passwords changed successfully"

recaptcha_messages = {
    "invalid-site-private-key": "ReCAPTCHA Error",
    "invalid-request-cookie": "ReCAPTCHA Error",
    "incorrect-captcha-sol": "You seem to have mistyped the ReCAPTCHA text",
    "captcha-timeout": "This ReCAPTCHA text is no longer valid",
    "recaptcha-not-reachable": "Could not reach reCAPTCHA servers. Check your connection and try again",
    "success": "Recaptcha was successful"
}

