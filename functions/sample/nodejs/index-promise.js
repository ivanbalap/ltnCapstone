/**
 * Get all dealerships
 */

const { CloudantV1 } = require('@ibm-cloud/cloudant');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');
let params= require('../../.creds.json');
params.state="Texas";

function main(params) {

    const authenticator = new IamAuthenticator({ apikey: params.IAM_API_KEY })
    const cloudant = CloudantV1.newInstance({
      authenticator: authenticator
    });
    cloudant.setServiceUrl(params.COUCH_URL);

    // let dbListPromise = getDbs(cloudant);
    // return dbListPromise;

    getDbs(cloudant)
    .then((databases)=>{
        console.log({state:params.state});
        console.log(databases["dbs"][0]);
        if (params.state){
            console.log('specific dealer:'); 
            getMatchingRecords(cloudant, databases["dbs"][0],{state:params.state})
            .then(data => console.log(data))
            .catch(err=>console.log(err.toString()));
        } else {
            console.log('all dealer')
            getAllRecords(cloudant, databases["dbs"][0])
            .then(data => console.log(data))
            .catch(err=>console.log(err.toString()));
        }
    })
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
            //    resolve({result:result.result.docs});
             })
             .catch(err => {
                console.log(err);
                reject({ err: err });
             });
         })
 }

//  const params={
//     IAM_API_KEY:"fda",
//     COUCH_URL:"fdaf"
// }


// console.log(params.IAM_API_KEY)
// console.log(params.COUCH_URL)

function dealership(selector) {

    const authenticator = new IamAuthenticator({ apikey: params.IAM_API_KEY })
    const cloudant = CloudantV1.newInstance({
      authenticator: authenticator
    });
    cloudant.setServiceUrl(params.COUCH_URL);

    // let dbListPromise = getDbs(cloudant);
    // dbListPromise
    getDbs(cloudant)
    .then((databases)=>{
        console.log(selector);
        console.log(databases["dbs"][0]);
        if (selector.state){
            console.log('specific dealer:'); 
            console.log(selector)
            // return getMatchingRecords(cloudant, databases["dbs"][0],selector);
            getMatchingRecords(cloudant, databases["dbs"][0],selector)
            .then(data => console.log(data))
            .catch(err=>console.log(err.toString()));
        } else {
            console.log('all dealer')
            // return getAllRecords(cloudant, databases["dbs"][0])
            getAllRecords(cloudant, databases["dbs"][0])
            .then(data => console.log(data))
            .catch(err=>console.log(err.toString()));
        }
    })
    // return ret_dealership;
}

main(params)
// .then(data => console.log(data))
// .catch(err=>console.log(err.toString()))

// selector = {state:"Texas"}
// dealership(selector)
// .then(data => console.log(data))
// .catch(err=>console.log(err.toString()))

// selector = {}
// dealership(selector)