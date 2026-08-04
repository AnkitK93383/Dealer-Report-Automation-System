# Dealer Report Automation System
A Streamlit-based web application that automates dealer report generation and email distribution.

The application allows users to upload sales data and dealer information, automatically generates dealer-wise Excel reports, emails each report to the corresponding dealer, displays real-time progress, and cleans up temporary files after completion.

## Features

- Upload Sales Excel file
- Upload Dealer Details Excel file
- Automatic dealer-wise report generation
- Email reports to dealers
- Real-time progress tracking
- Temporary file cleanup
- Simple Streamlit interface
- Error handling and validation

Dealer-Report-Automation-System/
│
├── app.py
├── modules/
│   └── dashboard.py
├── utils/
│   ├── excel_reader.py
│   ├── report_generator.py
│   ├── email_sender.py
│   └── ...
├── uploads/
├── output/
├── requirements.txt
├── README.md
└── .gitignore

## Technologies

- Python 3.11
- Streamlit
- Pandas
- OpenPyXL
- SMTP (Email)

## How It Works

1. Launch the Streamlit application.
2. Upload the Sales Excel file.
3. Upload the Dealer Details Excel file.
4. Enter sender email credentials.
5. Click "Generate & Send Reports".
6. The application:
   - Generates dealer-wise reports
   - Sends reports via email
   - Displays live progress
   - Deletes temporary files after completion

## Screenshots
![alt text](<Screenshot 2026-08-04 141452.png>)
![alt text](<Screenshot 2026-08-04 141718.png>)
![alt text](<Screenshot 2026-08-04 141733.png>)
![alt text](<Screenshot 2026-08-04 141804.png>)

## Requirements

- Python 3.11+
- Internet connection
- Gmail App Password

## Author

Ankit Kumar

GitHub:
https://github.com/AnkitK93383

## Workflow

Upload Sales File
        │
        ▼
Read Excel Files
        │
        ▼
Generate Dealer Reports
        │
        ▼
Send Email
        │
        ▼
Show Progress
        │
        ▼
Delete Temporary Files