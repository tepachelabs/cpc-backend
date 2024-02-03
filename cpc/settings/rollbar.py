from cpc.settings import DEBUG, BASE_DIR

ROLLBAR = {
    "access_token": "ac5b23ebfc5f4cd19b38af9d423c29b1",
    "environment": "development" if DEBUG else "production",
    "code_version": "1.0",
    "root": BASE_DIR,
}
