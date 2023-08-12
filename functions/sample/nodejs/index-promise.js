/**
 * Get all dealerships
 */

const { CloudantV1 } = require('@ibm-cloud/cloudant');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');

function main(params) {

    const authenticator = new IamAuthenticator({ apikey: params.IAM_API_KEY })
    const cloudant = CloudantV1.newInstance({
      authenticator: authenticator
    });
    cloudant.setServiceUrl(params.COUCH_URL);

    // const cloudant = CloudantV1({
    //     url: params.COUCH_URL,
    //     plugins: { iamauth: { iamApiKey: params.IAM_API_KEY } }
    // });

    let dbListPromise = getDbs(cloudant);
    // console.log("kfakfdskjfdskajf");
    // console.log(`inside ${dbListPromise}`);
    // dbListPromise.then(
    //     (data) => {console.log(data);}
    // )
    return dbListPromise;
}

function getDbs(cloudant) {
     return new Promise((resolve, reject) => {
         cloudant.getAllDbs()
             .then(body => {
                 resolve({ dbs: body.result });
             })
             .catch(err => {
                  console.log(err);
                 reject({ err: err });
             });
     });
 }
 
 
 /*
 Sample implementation to get the records in a db based on a selector. If selector is empty, it returns all records. 
 eg: selector = {state:"Texas"} - Will return all records which has value 'Texas' in the column 'State'
 */
 function getMatchingRecords(cloudant,dbname, selector) {
     return new Promise((resolve, reject) => {
         cloudant.postFind({db:dbname,selector:selector})
                 .then((result)=>{
                   resolve({result:result.result.docs});
                 })
                 .catch(err => {
                    console.log(err);
                     reject({ err: err });
                 });
          })
 }
 
                        
 /*
 Sample implementation to get all the records in a db.
 */
 function getAllRecords(cloudant,dbname) {
     return new Promise((resolve, reject) => {
         cloudant.postAllDocs({ db: dbname, includeDocs: true, limit: 10 })            
             .then((result)=>{
               resolve({result:result.result.rows});
             })
             .catch(err => {
                console.log(err);
                reject({ err: err });
             });
         })
 }

 const params={
    IAM_API_KEY:"fda",
    COUCH_URL:"fdaf"
}
// console.log(params.IAM_API_KEY)
// console.log(params.COUCH_URL)
main(params)
.then(data => console.log(data))
.catch(err=>console.log(err.toString()))