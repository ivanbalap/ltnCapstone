/**
 * Get all dealerships
 */

const { CloudantV1 } = require('@ibm-cloud/cloudant');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');

async function main(params) {
      const authenticator = new IamAuthenticator({ apikey: params.IAM_API_KEY })
      const cloudant = CloudantV1.newInstance({
          authenticator: authenticator
      });
      cloudant.setServiceUrl(params.COUCH_URL);
      try {
        let dbList = await cloudant.getAllDbs();
        return { "dbs": dbList.result };
      } catch (error) {
          return { error: error.description };
      }
}

// const params={
//     IAM_API_KEY:"fda",
//     COUCH_URL:"fdaf"
// }
const params= require('../../.creds.json');
// console.log(params.IAM_API_KEY)
// console.log(params.COUCH_URL)
// main(params).catch(err=>console.log(err.toString()));
main(params).then(
    (data) => {console.log(data)}
)