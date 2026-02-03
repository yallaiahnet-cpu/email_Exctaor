#!/bin/bash

# Create a safe package with sanitized email.json (no real passwords)

echo "========================================"
echo "Creating SAFE Package (Sanitized)"
echo "========================================"
echo ""
echo "This will create a package with example email.json"
echo "(no real passwords - friend needs to add their own)"
echo ""

# First create the regular package
./package_for_sharing.sh

# Get the package directory (most recent one)
PACKAGE_DIR=$(ls -td Email_Notifications_Package_* 2>/dev/null | head -1)

if [ -z "$PACKAGE_DIR" ]; then
    echo "Error: Package directory not found"
    exit 1
fi

echo ""
echo "Creating sanitized email.json.example..."
echo ""

# Create email.json.example with placeholder data
cat > "$PACKAGE_DIR/email.json.example" << 'EOF'
{
    "example@gmail.com": [
        {
            "name": "Your Name",
            "phone_number": "1234567890",
            "smtp_username": "example@gmail.com",
            "smtp_password": "YOUR_APP_PASSWORD_HERE",
            "years_of_experience": "10+ years",
            "linkedin_url": ""
        }
    ]
}
EOF

# Remove the real email.json and rename example
if [ -f "$PACKAGE_DIR/email.json" ]; then
    echo "Removing real email.json (contains sensitive data)..."
    rm "$PACKAGE_DIR/email.json"
    echo ""
    echo "IMPORTANT: Your friend needs to:"
    echo "  1. Copy email.json.example to email.json"
    echo "  2. Add their own email credentials"
fi

echo ""
echo "========================================"
echo "Safe package created!"
echo "========================================"
echo ""
echo "Package: $PACKAGE_DIR"
echo ""
echo "Your friend should:"
echo "  1. Copy email.json.example to email.json"
echo "  2. Add their own email credentials to email.json"
echo "  3. Create .env file from env_example.txt"
echo ""


