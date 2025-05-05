# Guardian AI Chrome Extension

Guardian AI-Protech is a Chrome Extension that allows you to analyze and protect your data using AI-powered tools. This extension provides functionalities to analyze text data and files, anonymize sensitive information, redact confidential content, and identify personally identifiable information (PII).

## How to Use

### Installation

1.  Clone or download the repository to your local machine.

    ```bash
    git clone https://github.com/prasad-chinthalapudi/data-guardian/tree/dev
    ```
2.  Enable Developer Mode in Chrome Extensions.
    Open Chrome browser.
    Go to chrome://extensions/.
    Toggle on the "Developer mode" switch in the top right corner.
3.  Load the Extension.
    Click on "Load unpacked" button.
    Choose the frontend folder from the downloaded repository.

The Guardian AI-Protech extension should now appear in your Chrome browser.



## Backend Setup

## app.py(Flask server)

1.  This Flask server provides functionality for anonymizing, redacting and reviewing the text files or CSV     files containing text data as well as text input. It utilizes the Presidio Toolkit for anonymization, redaction and identification purposes. Additionally, it supports changing the guardian for the anonymization process.

2.  Before starting the Flask server it is suggested to create a new virtual environment.

2.  After cloning the repository navigate to the data-guardian/backend folder.

3.  Install all the dependencies by running the following command
    ````
    pip3 install -r requirements.txt
    ````

## Starting server

1.  Run the following command to start the server
    ````
    python3 app.py
    ````
    By default, the server runs on http://localhost:5000/.

### API Endpoints

##  Change the default guardian
    URL: /change_guardian?guardian='Presidio'
    Method: POST
    Description: Change the guardian for the data processing.
    Parameters:
    guardian: The guardian to be set (LLM, Presidio, Bedrock).

##  Anonymize CSV
    URL: /anonymize_csv
    Method: POST
    Description: Anonymize a CSV file containing text data.
    Parameters:
        file: The CSV file to be anonymized.
    Anonymize Text File

##  Anonymize Text File
    URL: /anonymize_text_file
    Method: POST
    Description: Anonymize a text file.
    Parameters:
        file: The text file to be anonymized.

##  Redact Text File
    URL: /redact_text_file
    Method: POST
    Description: Redact sensitive information from a text file.
    Parameters:
        file: The text file to be redacted.

##  Review Text File
    URL: /review_text_file
    Method: POST
    Description: Identify and review sensitive information in a text file.
    Parameters:
        file: The text file to be reviewed.

##  Anonymize Text
    URL: /anonymize_text?text
    Method: POST
    Description: Anonymize a given text string.
    Parameters:
        text: The text to be anonymized.

##  Redact Text
    URL: /redact_text?text
    Method: POST
    Description: Redact sensitive information from a given text string.
    Parameters:
        text: The text to be redacted.

##  Review Text
    URL: /review_text?text
    Method: POST
    Description: Identify and review sensitive information in a given text string.
    Parameters:
        text: The text to be reviewed.
