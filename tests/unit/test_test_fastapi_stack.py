import aws_cdk as core
import aws_cdk.assertions as assertions

from test_fastapi.test_fastapi_stack import TestFastapiStack

# example tests. To run these tests, uncomment this file along with the example
# resource in test_fastapi/test_fastapi_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = TestFastapiStack(app, "test-fastapi")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
