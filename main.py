from fastapi import FastAPI
from simple_salesforce import Salesforce
from dotenv import load_dotenv
import os
app = FastAPI()


load_dotenv()  # take environment variables from .env.

username = os.getenv('username') 
password = os.getenv('password')
security_token = os.getenv('security_token')
domain = os.getenv('domain')
 #Connect to salesforce
sf = Salesforce(
        username=username,
        password=password,
        security_token=security_token,
        domain=domain
            )


@app.get("/health")
async def root():
    return {"message": "alive"}

#New route to get case details from salesforce
@app.get("/cases")
async def read_item():
   
    #Query the cases
    case = sf.query("SELECT Id, CaseNumber, Subject, Description, Status, RecordType.Name FROM Case WHERE IsClosed = false AND RecordType.Name = 'KAR Global Arbitration' ORDER BY CreatedDate DESC LIMIT 1000")
    #Return the case
    return case



#New route to get case details from salesforce
@app.get("/case/{case_id}")
async def read_item(case_id):
    #Query the cases
    case = sf.query("SELECT Id, CaseNumber, (select Id, LastModifiedDate from Attachments), (Select Id, LastModifiedDate from Tasks), (Select Id, TextBody, Subject, ContentDocumentIds, LastModifiedDate from EmailMessages), (Select Id,LastModifiedDate, CommentBody FROM CaseComments) from Case WHERE Id =  '" + case_id + "'")
    #Return the case
    return case

@app.get("/evaluate/{VIN}")
async def read_item(VIN):
    return {"item_id": VIN}
