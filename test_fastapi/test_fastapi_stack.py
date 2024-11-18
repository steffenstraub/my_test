import aws_cdk as cdk
from aws_cdk import aws_apigateway as apigateway
from constructs import Construct

from aws_cdk import (
    Duration,
    Stack,
    aws_lambda as _lambda,
    aws_iam as _iam,
    aws_lambda_python_alpha as _aLambda,
    aws_ec2 as _ec2
)

class TestFastapiStack(cdk.Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        testExecutionRole = _iam.Role(self,
                                      id="testExecutionRoleFAST",
                                      role_name="testExecutionRoleFAST",
                                      assumed_by=_iam.ServicePrincipal("lambda.amazonaws.com"),
                                      managed_policies=[_iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole"),
                                                        _iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaVPCAccessExecutionRole"),
                                                        _iam.ManagedPolicy.from_aws_managed_policy_name("AmazonVPCFullAccess"),
                                                        _iam.ManagedPolicy.from_aws_managed_policy_name("SecretsManagerReadWrite")]
                                      )

        uaPortalVpc = _ec2.Vpc.from_lookup(self,id="vpc-098616615f44e68bc", vpc_name="UaPortalDbStack/portal-db-vpc")

        privateSubnets = _ec2.SubnetSelection(
            subnet_type=_ec2.SubnetType.PRIVATE_ISOLATED
        )

        fastapi_lambda = _aLambda.PythonFunction(
            self, 
            'FastApiFunction',
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler='handler',
            entry="./fastapi_app/",
            index="app.py",
            role=testExecutionRole,
            timeout=cdk.Duration.seconds(30),
            memory_size=512,
            vpc=uaPortalVpc,
            vpc_subnets=privateSubnets,
            security_groups=[_ec2.SecurityGroup.from_lookup_by_id(scope=self,id="mySecGroup",security_group_id="sg-0397d4e23a3788a8a")]
        )

        # Define the API Gateway
        api = apigateway.LambdaRestApi(
            self, 'FastApiEndpoint',
            handler=fastapi_lambda,
            proxy=True,
        )

