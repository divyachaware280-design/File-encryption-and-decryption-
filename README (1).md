# File Encryption & Decryption System

A simple, secure command-line tool to encrypt and decrypt any file using a password. Built with Python and the `cryptography` library, with a Windows `.bat` launcher for easy use.

## Features

- Encrypts and decrypts any file type (documents, images, PDFs, videos, etc.)
- AES-256-GCM encryption (confidential and tamper-proof)
- Password-based key derivation using Scrypt with a random salt per file
- Detects wrong passwords and modified or corrupted files
- Menu-driven Windows launcher with drag-and-drop support
- Passwords are hidden while typing

## Project Structure

```
file-encryption-system/
├── file_crypto.py        # Core encryption/decryption program
├── run_file_crypto.bat   # Windows menu launcher
└── README.md             # Project documentation
```

## Requirements

- Python 3.8 or higher
- `cryptography` package

```
pip install cryptography
```

(The `.bat` file installs this automatically if it is missing.)

## Usage

### Option 1: Windows launcher (easiest)

1. Keep all files in the same folder.
2. Double-click `run_file_crypto.bat`.
3. Choose **1** to encrypt or **2** to decrypt.
4. Type or drag and drop the file path, then enter a password.

### Option 2: Command line

```
# Encrypt  (creates report.pdf.enc)
python file_crypto.py encrypt report.pdf

# Decrypt  (restores report.pdf)
python file_crypto.py decrypt report.pdf.enc

# Custom output name
python file_crypto.py encrypt notes.txt -o secret.enc
python file_crypto.py decrypt secret.enc -o notes_restored.txt
```

## How It Works

**Encryption**

1. The user enters a password (confirmed twice).
2. A random 16-byte salt and a random 12-byte nonce are generated.
3. Scrypt derives a 256-bit key from the password and salt.
4. AES-256-GCM encrypts the file contents.
5. The output is saved as: `MAGIC | salt | nonce | ciphertext + auth tag`.

**Decryption**

1. The header is read to get the salt and nonce.
2. The key is re-derived from the entered password.
3. AES-GCM decrypts the data and verifies the authentication tag.
4. If the password is wrong or the file was altered, decryption fails with an error and no output is produced.

## Encrypted File Format

| Field        | Size     | Purpose                          |
|--------------|----------|----------------------------------|
| Magic header | 5 bytes  | Identifies the file (`FENC1`)    |
| Salt         | 16 bytes | Used for key derivation          |
| Nonce        | 12 bytes | Unique value for AES-GCM         |
| Ciphertext   | Variable | Encrypted data + 16-byte auth tag|

## Security Notes

- Use a strong, unique password. There is no recovery if it is forgotten.
- The original file is not deleted after encryption. Delete it yourself if needed.
- The entire file is loaded into memory, so very large files (over a few hundred MB) may be slow.
- This project is for learning and personal use. It has not been independently audited.

## Test Cases

| Test                          | Expected Result                              |
|-------------------------------|----------------------------------------------|
| Encrypt then decrypt          | Restored file identical to original          |
| Wrong password                | Error: wrong password or tampered file       |
| Corrupted .enc file           | Error: wrong password or tampered file       |
| Non-encrypted file as input   | Error: invalid header                        |
| Empty file                    | Encrypts and decrypts successfully           |
| Passwords do not match        | Encryption cancelled                         |

## Future Improvements

- GUI using Tkinter
- Chunked encryption for very large files
- Folder encryption (zip and encrypt)
- Password strength checker
- Hybrid encryption with RSA
- Secure deletion of original files

## Technologies Used

- Python 3
- cryptography (AES-GCM, Scrypt)
- Windows Batch scripting

## Author

Divya Chaware
B.Tech, Information Technology
Priyadarshini College of Engineering
