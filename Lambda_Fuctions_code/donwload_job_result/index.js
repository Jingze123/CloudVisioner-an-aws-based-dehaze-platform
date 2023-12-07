const dbConnection = require('./database.js')
const { GetObjectCommand, S3Client} = require('@aws-sdk/client-s3');
const fs = require('fs');
const ini = require('ini');
const config = require("./config");
const configText = fs.readFileSync(config.photoapp_config, 'utf-8');
const config_text = ini.parse(configText);

const client = new S3Client({
    region: "us-east-2",
    credentials: {
        accessKeyId: config_text.s3readwrite.aws_access_key_id,
        secretAccessKey:config_text.s3readwrite.aws_secret_access_key ,
    }
});

const jwt = require('jsonwebtoken');


exports.handler = async (event, context) => {
    try {
        // fetch input data
        // const data = JSON.parse(event.body);
        const headers = event.headers;
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
        // const jobid = data.jobid;
        const jobid = event.pathParameters.jobid;


        // check whether the jobid belongs to user
        const rds_reponse = new Promise((resolve, reject) => {
            try {
                const sql = 'SELECT * FROM jobs WHERE userid=? AND jobid=?';
                dbConnection.query(sql, [userid, jobid], (err, results, _) => {
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

        // wait for rds_reponse
        const rds_result = await rds_reponse;

        // jobid does not belong to user
        if (rds_result.length == 0) {
            throw new Error("Invalid jobid");
        }

        const download_key = rds_result[0].resultsfilekey;
        const result_file_name = rds_result[0].originaldatafile;

        const input = {
            // "Bucket": "new-bucket-photoapp-ruiyangpeng",
            "Bucket": config_text.s3.bucket_name,
            "Key": download_key
        };

        const command = new GetObjectCommand(input);
        console.log('here0');
        const s3_response = await client.send(command);
        console.log(s3_response);
        const result_data = await s3_response.Body.transformToString("base64");

        const responseData = {
            message: "download success",
            result_data: result_data,
            filename: result_file_name
        };

        return {
            statusCode: 200,
            body: JSON.stringify(responseData)
        }
    }// try
    catch (err) {
        console.log("**ERROR:", err.message);
        return {
            statusCode: 400,
            body: err.message
        }
    }// catch
};
