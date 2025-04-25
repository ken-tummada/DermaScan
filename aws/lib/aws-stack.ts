import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as lambda from "aws-cdk-lib/aws-lambda";

export class AwsStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const dockerFunc = new lambda.DockerImageFunction(this, "DockerFunc", {
      functionName: "dermascan-backend",
      code: lambda.DockerImageCode.fromImageAsset("./image"),
      memorySize: 512,
      timeout: cdk.Duration.minutes(2),
      architecture: lambda.Architecture.ARM_64,
    });

    const functionUrl = dockerFunc.addFunctionUrl({
      authType: lambda.FunctionUrlAuthType.NONE,
      cors: {
        allowedMethods: [lambda.HttpMethod.POST],
        allowedHeaders: ["*"],
        allowedOrigins: ["*"],
      }
    });

    new cdk.CfnOutput(this, "FunctionUrlValue", {
      value: functionUrl.url
    });
  }
}
