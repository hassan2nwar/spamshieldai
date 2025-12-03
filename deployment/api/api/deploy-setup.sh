#!/bin/bash
set -e

# Install Python dependencies
pip install -r api/requirements-api.txt

# Print success message
cat <<EOF

✅ SpamShield API setup complete!
Run with:
  python api/app.py
Or deploy to Railway/Heroku with Procfile.
EOF
