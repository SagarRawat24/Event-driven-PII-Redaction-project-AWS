import json
import boto3
import fitz  # PyMuPDF
import re
import os

class Redactor:
    @staticmethod
    def get_sensitive_data(text):
        """ Function to get phone numbers and email addresses """
        PHONE_REG_1 = r"\b(?:\+?1[-.\s]?)?(?:\(?[2-9]\d{2}\)?[-.\s]?)?[2-9]\d{2}[-.\s]?\d{4}\b"
        PHONE_REG_2 = r"\+91\.\d{10}"
        EMAIL_REG = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
        
        phones_1 = re.findall(PHONE_REG_1, text)
        phones_2 = re.findall(PHONE_REG_2, text)
        emails = re.findall(EMAIL_REG, text)
        
        return phones_1 + phones_2 + emails

    def __init__(self, path):
        self.path = path

    def redaction(self):
        """ Main redactor code """
        doc = fitz.open(self.path)
         
        for page in doc:
            page.wrap_contents()
            text = page.get_text("text")
            sensitive_data = self.get_sensitive_data(text)
            
            for data in sensitive_data:
                areas = page.search_for(data)
                [page.add_redact_annot(area, fill=(0, 0, 0)) for area in areas]
                 
            page.apply_redactions()
             
        redacted_path = '/tmp/redacted_output.pdf'
        doc.save(redacted_path)
        print("Successfully redacted phone numbers and email addresses")
        return redacted_path

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    
    # Get the source bucket and key from the event
    source_bucket = event['Records'][0]['s3']['bucket']['name']
    source_key = event['Records'][0]['s3']['object']['key']
    
    # Download the file from the source bucket
    input_path = '/tmp/input.pdf'
    s3.download_file(source_bucket, source_key, input_path)
    
    # Perform redaction
    redactor = Redactor(input_path)
    redacted_path = redactor.redaction()
    
    # Upload the redacted file to the destination bucket
    destination_bucket = 'redactedfile'
    destination_key = 'redacted_' + os.path.basename(source_key)
    s3.upload_file(redacted_path, destination_bucket, destination_key)
    
    return {
        'statusCode': 200,
        'body': json.dumps('PDF redacted and uploaded successfully')
    }