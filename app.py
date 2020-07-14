#!/usr/bin/env python3

from aws_cdk import core

from aws_cdk_provision.aws_cdk_provision_stack import AwsCdkProvisionStack


app = core.App()
AwsCdkProvisionStack(app, "aws-cdk-provision")

app.synth()
