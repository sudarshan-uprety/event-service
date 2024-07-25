import boto3

aws_lambda = boto3.client('lambda', region_name='ap-south-1')
aws_lambda_function = 'lambda_function_name'


def lambda_invoke(*args, **kwargs):
    print(args)
    print(kwargs)
    return aws_lambda.invoke()
