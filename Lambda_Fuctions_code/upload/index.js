const dbConnection = require('./database.js')
const { PutObjectCommand } = require('@aws-sdk/client-s3');
const { s3, s3_bucket_name, s3_region_name } = require('./aws.js');
const uuid = require('uuid');
const jwt = require('jsonwebtoken');

exports.handler = async (event, context) => {
    try {
        // fetch input data
        const data = JSON.parse(event.body);  // data => JS object
        const headers = event.headers;
        const bytes = Buffer.from(data.image, 'base64');
        const originaldatafile = data.originaldatafile;
        const token = headers?.Authorization?.substring(7);

        // Validate that the token is present
        if (!token) {
            return {
                statusCode: 401,
                body: "Token not provided",
            };
        }

        // decode token
        const token_data = jwt.verify(token,"jwttoken",(error,decoded)=>{
            if(error){
                return {
                    statusCode: 401,
                    body: error.message
                }
            }
            return decoded;
        });

        // token error
        if (token_data.statusCode) {
            return {
                statusCode:token_data.statusCode,
                body: token_data.body
            }
        }

        const userid = token_data.userid;

        // get the username's bucketkey
        const rds_reponse = new Promise((resolve, reject) => {
            try {
                const sql = 'SELECT * FROM users_info WHERE userid=?';
                dbConnection.query(sql, [userid], (err, results, _) => {
                    try {
                        if (err) {
                            reject(err);
                            return;
                        }
                        console.log('user query done');
                        resolve(results);
                    } catch (code_err) {
                        reject(code_err);
                    }
                });
            }
            catch (code_err) {
                reject(code_err);
            }
        });

        // wait for rds_response
        const rds_result = await rds_reponse;


        // user in users_info table

        // upload to s3 bucket
        const key = rds_result[0].bucketfolder + '/' + 'image' + '/' + uuid.v4() + '.jpg';
        const input = {
            "Bucket": s3_bucket_name,
            "Key": key,
            "Body": bytes,
            "ContentType": "image/jpg"
        }
        const command = new PutObjectCommand(input);

        // insert into jobs table
        const rds_reponse_1 = new Promise((resolve, reject) => {
            try {
                const sql_1 = 'INSERT INTO jobs VALUES(null, ?, ?, ?, ?, ?)';
                dbConnection.query(sql_1, [userid, "pending", originaldatafile, key, ""], (err, results, _) => {
                    try {
                        if (err) {
                            reject(err);
                            return;
                        }
                        console.log('jobs insert done');
                        resolve(results);
                    } catch (code_err) {
                        reject(code_err);
                    }
                });
            }
            catch (code_err) {
                reject(code_err);
            }
        });

        const response = await s3.send(command);
        const insert_response = await rds_reponse_1;
        console.log("upload done")

        return {
            statusCode: 200,
            body: "upload success"
        }

    }//try
    catch (err) {
        console.log("**ERROR:", err.message);
        return {
            statusCode: 400,
            body: err.message
        }
    }//catch
};//post