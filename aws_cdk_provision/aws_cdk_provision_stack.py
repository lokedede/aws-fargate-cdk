from aws_cdk import (
    core,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_ecs_patterns as ecs_patterns
)


class AwsCdkProvisionStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

       # Defines vpc to host Fargate SLB

        vpc = ec2.Vpc(
            self, 'cdkVPC', 
            cidr = "10.0.0.0/24",
            # two azs required to host alb 
            max_azs = 2,
            subnet_configuration=[
                # create private subnet to host fargate service
                ec2.SubnetConfiguration(
                    subnet_type = ec2.SubnetType.PRIVATE,
                    name = "cdkPrivate",
                    cidr_mask = 28
                ),
                # create public subnet to host nat-gateway for private subnet so that amazon-ecs-sample image can be pulled from internet"
                ec2.SubnetConfiguration(
                    subnet_type = ec2.SubnetType.PUBLIC,
                    name = "cdkPublic",
                    cidr_mask = 28
                ),                      
            ]
        )
        # create cluster to host fargate
        cluster = ecs.Cluster(self, "CDKCluster", vpc=vpc)
        # create fargate and service and alb
        ecs_patterns.ApplicationLoadBalancedFargateService(self, "MyFargateService",
            assign_public_ip= False,
            cluster = cluster,                           
            desired_count = 1,            
            task_image_options=ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
                image=ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample")
            ), 
            public_load_balancer = False
            )  
