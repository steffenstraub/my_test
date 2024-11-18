#!/usr/bin/env python3
import os

import aws_cdk as cdk

from test_fastapi.test_fastapi_stack import TestFastapiStack


app = cdk.App()
TestFastapiStack(app, "TestFastapiStack",
                 env=cdk.Environment(
                            account="429113693686",
                            region="eu-central-1"
                        )
                )

app.synth()
