const express = require('express');
const app = express();
const port = 3000;
// const Cloudant = require('@cloudant/cloudant');

const { CloudantV1 } = require('@ibm-cloud/cloudant');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');
let params= require('./.creds.json');
const authenticator = new IamAuthenticator({ apikey: params.IAM_API_KEY })
const cloudant = CloudantV1.newInstance({
  authenticator: authenticator
});
cloudant.setServiceUrl(params.COUCH_URL);

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

let databases, dealershipDB, reviewDB;
getDbs(cloudant)
.then((data)=>{
    databases=data;
    dealershipDB=databases["dbs"].filter((dbname)=>dbname==='dealerships')[0];
    reviewDB=databases["dbs"].filter((dbname)=>dbname==='reviews')[0];
    console.log(databases, dealershipDB, reviewDB);
})
.catch((err)=>{ throw err;})
 
 /*
 Sample implementation to get the records in a db based on a selector. If selector is empty, it returns all records. 
 eg: selector = {state:"Texas"} - Will return all records which has value 'Texas' in the column 'State'
 */
 function getMatchingRecords(cloudant,dbname, selector) {
     return new Promise((resolve, reject) => {
         cloudant.postFind({db:dbname,selector:selector})
                 .then((result)=>{
                    if (result.result.docs.length == 0) {
                        resolve({404:'The state or id does not exist'});}
                    else{
                        resolve(result.result.docs);
                    }
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
        // cloudant.postAllDocs({ db: dbname, includeDocs: true})
             .then((result)=>{
                if (result.result.rows.length == 0) {
                    resolve({404:'The database is empty'});}
                else{
                    resolve(result.result.rows.map((r)=>{return r.doc}));
                    // resolve(result.result.rows);
                }
             })
             .catch(err => {
                console.log(err);
                reject({ err: err });
             });
         })
 }
 
app.use(express.json());
 
// Define a route to get all dealerships with optional state and ID filters
app.get('/api/dealership', (req, res) => {
    const { state, id } = req.query;
    let selector={}
    if (state) selector.state=state;
    if (id) selector.id=parseInt(id);
    if (state || id){
        console.log('specific dealer:'); 
        getMatchingRecords(cloudant, dealershipDB, selector)
        .then(data => res.json(data))
        .catch(err => res.status(500).send({ error: "Error while quering the database" }));
    } else {
        console.log('all dealer')
        getAllRecords(cloudant, dealershipDB)
        .then(data => res.json(data))
        .catch(err=>res.status(500).send({ error: "Error while quering the database" }));
    }

})

app.listen(port, () => {
    console.log("listening to port " + port)
})