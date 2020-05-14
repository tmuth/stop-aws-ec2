import boto3
from botocore.exceptions import ClientError
import json

# Use the following article to verify the SENDER email address
# https://docs.aws.amazon.com/ses/latest/DeveloperGuide/verify-email-addresses-procedure.html

SENDER = "AWS lambda tmuth <tmuth@nowhere.com>"
RECIPIENT = "tmuth@nowhere.com"
# If necessary, replace us-west-2 with the AWS Region you're using for Amazon SES.
AWS_REGION = "us-east-1"

def lambda_handler(event, context):
    ec2 = boto3.resource('ec2')
    filters = [
        {
        'Name': 'instance-state-name', 
        'Values': ['running']                 # pending | running | shutting-down | terminated | stopping | stopped
        }
    ]
    
    instances = ec2.instances.filter(Filters = filters)
    instanceJSON = []
    RunningInstances = []
    instanceList = []
    subject = ""
    for instance in instances:
        instancename = ''
        try:
            for tags in instance.tags:
                if tags["Key"] == 'Name':
                    instancename = 'Name: '+tags["Value"]+', '
        except:
            pass
        
        RunningInstances.append(instancename+"ID: "+instance.id)
        #instanceList.append(instance.id)
        
    if len(RunningInstances):
        subject = str(len(RunningInstances)) + " AWS instances running"
        send_email(subject,RunningInstances)
    
    #instanceJSON = json.dumps(RunningInstances)
    return {
        "statusCode": 200,
        "body": "yep"
    }

def send_email(subject, instanceList = []):
    # The subject line for the email.
    SUBJECT = subject
    
    # The email body for recipients with non-HTML email clients.
    BODY_TEXT = ("The following AWS instances are currently running:\r\n")
    
    body_html_instances=""
    
    for instance in instanceList: 
        BODY_TEXT=BODY_TEXT+instance+"\r\n"
        body_html_instances=body_html_instances+instance+"<br />"
                
    # The HTML body of the email.
    BODY_HTML = """<html>
    <head></head>
    <body>
      <h1>The following AWS instances are currently running:</h1>
      <p>"""+body_html_instances+"""</p>
    </body>
    </html>
                """            
    
    # The character encoding for the email.
    CHARSET = "UTF-8"
    
    # Create a new SES resource and specify a region.
    client = boto3.client('ses',region_name=AWS_REGION)
    
    # Try to send the email.
    try:
        #Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
            # If you are not using a configuration set, comment or delete the
            # following line
            #ConfigurationSetName=CONFIGURATION_SET,
        )
    # Display an error if something goes wrong.	
    except ClientError as e:
        return {
            "statusCode": 200,
            "body": "Error: "+e.response['Error']['Message']
        }
        # print(e.response['Error']['Message'])
    else:
        return {
            "statusCode": 200,
            "body": "Email sent! Message ID:"+response['MessageId']
        }
