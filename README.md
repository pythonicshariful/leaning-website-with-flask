# leaning-website-with-flask

## Setup

Install dependencies:

```powershell
pip install -r requirements.txt
```

Configure the admin login using environment variables before starting the app.
Choose a unique, strong password and set a stable random `SECRET_KEY` in
production. For local development in PowerShell:

```powershell
$env:SECRET_KEY = (python -c "import secrets; print(secrets.token_hex(32))")
$env:ADMIN_USERNAME = "admin"
$env:ADMIN_PASSWORD = "replace-with-a-strong-unique-password"
python app.py
```

The app generates a temporary session key if `SECRET_KEY` is unset, so sessions
will be invalidated when the process restarts. Admin login is unavailable until
both `ADMIN_USERNAME` and `ADMIN_PASSWORD` are set.

## Checkout and payment verification

Checkout currently records a student's selected manual payment method and
transaction reference as a pending order. It does not collect money or verify
transactions automatically. Before paying, students must contact support for
the current official payment instructions. An admin must verify the transfer
outside the app and approve the pending order from the admin dashboard before
course access is enabled. Connect and verify a payment provider before treating
this prototype flow as automated checkout.
