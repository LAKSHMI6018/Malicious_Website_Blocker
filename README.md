# Malicious Website Blocker

## Project Overview

The Malicious Website Blocker is a desktop application developed using Python and Tkinter. It helps users identify malicious websites using the VirusTotal API and blocks only malicious websites by updating the Windows Hosts file. The application also includes password verification, email registration, and logging features.

---

## Features

- User Registration
- Password Authentication
- Website Scanning using VirusTotal API
- Detects Safe and Malicious Websites
- Blocks Only Malicious Websites
- Unblocks Websites
- Stores Activity Logs
- Simple and User-Friendly GUI
- Email Registration Support

---

## Technologies Used

- Python
- Tkinter
- VirusTotal API
- Requests Library
- SMTP (Email)
- Windows Hosts File
- Git & GitHub

---

## Requirements

- Windows 10 or Windows 11
- Python 3.x
- Internet Connection
- VirusTotal API Key

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/LAKSHMI6018/Malicious_Website_Blocker.git
```

2. Open the project folder.

3. Install the required package:

```bash
pip install requests
```

4. Run the application:

```bash
python main.py
```

---

## How to Use

1. Register your email.
2. Generate or enter the password.
3. Scan a website using the VirusTotal API.
4. If the website is detected as malicious, click **Block Website**.
5. Enter the password to confirm.
6. View logs of all scanned and blocked websites.

---

## Project Structure

```
Malicious_Website_Blocker/
│
├── build/
├── dist/
├── main.py
├── passwords.txt
├── registered_emails.txt
├── logs.txt
├── README.md
└── MaliciousWebsiteBlocker.spec
```

---

## Screenshots

Add screenshots of your application here.

Example:

- Home Screen
- Scan Website Window
- Block Website Window
- Reports Window

---

## Future Enhancements

- Machine Learning Based Website Detection
- Real-Time URL Monitoring
- Browser Extension Integration
- Multi-User Authentication
- Cloud Database Support
- Automatic Threat Updates

---

## GitHub Repository

https://github.com/LAKSHMI6018/Malicious_Website_Blocker

---

## Author

**Bandaru Lakshmi**

B.Tech - Computer Science Engineering (Cyber Security)

Madanapalle Institute of Technology & Science

---

## License

This project is developed for educational and learning purposes.