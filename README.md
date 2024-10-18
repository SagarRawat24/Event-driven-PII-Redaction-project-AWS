#              PII-Resume-Redaction-Using-AWS 

Project Overview: This project aims to automate the process of redacting personally identifiable information (PII), such as phone numbers and email addresses, from resumes using AWS services. The redaction process is powered by Python's regex capabilities and the PyMuPDF library for handling PDF files. The project leverages AWS Lambda for serverless execution, Amazon S3 for storing resumes and redacted files, and AWS Cognito for user authentication.


## AWS-Services
AWS Lambda: Handles the processing of uploaded resumes, including scanning for PII using regex and redacting information using PyMuPDF. It provides scalable, serverless computing without the need for infrastructure management.

Amazon S3: Serves as the storage location for both the original resumes and the redacted versions. Users upload resumes to S3, and the processed redacted documents are also saved in S3.

AWS Cognito: Manages user authentication and access control to the system. Only authenticated users can upload resumes and access redacted documents.

PyMuPDF and Regex: PyMuPDF is used to manipulate PDF files, while regular expressions (regex) are employed to detect PII, including phone numbers and email addresses. These are then redacted from the resumes before the final document is stored in S3.

AWS IAM (Identity and Access Management): Controls access to AWS services by assigning permissions to users, Lambda functions, and S3 buckets. IAM ensures that only authenticated and authorized users can access specific resources and services.

AWS CloudWatch: Provides monitoring and logging capabilities. CloudWatch logs are used to track the execution of Lambda functions, capture any errors during redaction, and monitor overall system performance.
## Project-Workflow 

1. Simple Webpage for Resume Upload: A simple webpage is provided where authenticated users can upload their resumes. The webpage is integrated with AWS Cognito for authentication and uses a secure API to upload the resume directly to an S3 bucket. Once the user is logged in, the webpage generates a pre-signed URL or uses an API Gateway to securely upload the resume to S3.

2. Resume Upload (S3): The resume uploaded via the webpage is stored in an S3 bucket. This triggers a Lambda function for processing and redaction. 


3. User Authentication (Cognito): Users sign up or log in through AWS Cognito, ensuring secure access to the system.


4. Resume Upload (S3): The resume uploaded via the webpage is stored in an S3 bucket. This triggers a Lambda function for processing and redaction.


5. IAM Policies: AWS IAM policies are used to secure the S3 bucket, Lambda functions, and restrict access to only authorized users based on Cognito authentication and permissions.

6. Redaction Process (Lambda, PyMuPDF, Regex): The AWS Lambda function is automatically triggered when a resume is uploaded to the S3 bucket. It:

Downloads the resume from S3.
Uses Python's regex to scan the document for personally identifiable information (PII) such as phone numbers and email addresses.
Redacts the detected PII using the PyMuPDF library to modify the PDF file.
Saves the redacted version back to the S3 bucket.

7. Storing Redacted Resume (S3): The redacted version of the resume is saved in a dedicated folder in S3.

8. Access Redacted Resumes (S3): Users can securely retrieve the redacted versions of their resumes from S3 using a pre-signed URL or API.

9. Monitoring & Logging (CloudWatch): AWS CloudWatch is used to track the execution of the Lambda function, monitor errors, and log performance metrics for continuous improvement.
## Diagram


## Package and deploy on lambda 
Ensure you're in the pdf-redactor-lambda directory:
  ```

    cd /path/to/pdf-redactor-lambda
  ```


Activate your virtual environment (if not already activated):
```

   source venv/bin/activate
```


Create the package directory inside pdf-redactor-lambda:
```

   mkdir package
```


Install the required libraries into the package directory:

```

  pip install --target ./package PyMuPDF boto3
```


Copy your Lambda function into the package directory:
```

cp lambda_function.py package
```


Create the deployment ZIP file:
```

   cd package

  zip -r ../deployment-package.zip .
```
 

-  after that create lambda functiomn and upload package to lambda function

- create s3 trigger with s3 bucket where your resume store from upload 
 
- Run your html webpage and upload your resume 



