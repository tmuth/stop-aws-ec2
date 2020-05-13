# stop-aws-ec2
Code to automatically stop AWS EC2 instances using a lambda function or local python script. The idea is based on this article: https://aws.amazon.com/premiumsupport/knowledge-center/start-stop-lambda-cloudwatch/
but instead of having to manually update the list of IDs, this loops over all of your running instances and shuts them all down.
