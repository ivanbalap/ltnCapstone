/**
 * Get all databases
 */

 const { CloudantV1 } = require("@ibm-cloud/cloudant");
 const { IamAuthenticator } = require("ibm-cloud-sdk-core");
 
 function main(params) {
   const authenticator = new IamAuthenticator({ apikey: params.IAM_API_KEY });
   const cloudant = CloudantV1.newInstance({
     authenticator: authenticator,
   });
   cloudant.setServiceUrl(params.COUCH_URL);
 
   let dbList = getDbs(cloudant);
   console.log("kfakfdskjfdskajf");
   console.log(dbList);
   return { dbs: dbList };
 }
 
 function getDbs(cloudant) {
   cloudant
     .getAllDbs()
     .then((body) => {
       body.forEach((db) => {
         dbList.push(db);
       });
     })
     .catch((err) => {
       console.log(err);
     });
 }

 let params={
     "IAM_API_KEY":"fdaf",
     "COUCH_URL":"fdas"
 }
 main(params)