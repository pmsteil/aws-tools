// Use this code snippet in your app.
// If you need more information about configurations or implementing the sample code, visit the AWS docs:
// https://docs.aws.amazon.com/sdk-for-javascript/v3/developer-guide/getting-started.html

// import {
//     SecretsManagerClient,
//     GetSecretValueCommand,
//   } from "@aws-sdk/client-secrets-manager";

const { SecretsManagerClient, GetSecretValueCommand } = require("@aws-sdk/client-secrets-manager");

const secret_name = "rds-db-credentials/cluster-QLGIYIGN4C7WR4I4GWSCOMU7EE/patricksteil";


  const client = new SecretsManagerClient({
    region: "us-east-1",
  });
  
  let response;
  
  try {
    response =  client.send(
      new GetSecretValueCommand({
        SecretId: secret_name,
        VersionStage: "AWSCURRENT", // VersionStage defaults to AWSCURRENT if unspecified
      }))    
    .finally( ( response ) => {
      console.log( "Response: " + response)
    })
  .catch( (error) => {
    // For a list of exceptions thrown, see
    // https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
    throw error;
  });
} catch (err) {
  console.log(err);
}
  
  const secret = response.SecretString;

  //only ever returned undefined... pita
  console.log( "Secret: " + secret) ;

