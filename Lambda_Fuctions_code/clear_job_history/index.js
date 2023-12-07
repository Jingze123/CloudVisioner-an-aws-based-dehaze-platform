const dbConnection = require('./database.js')
const jwt = require('jsonwebtoken');

exports.handler = async (event, context) => {
    try {
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
        console.log(userid);

        // delete
        const rds_reponse = new Promise((resolve, reject) => {
            try {
                const sql = 'DELETE FROM jobs WHERE userid=?';
                dbConnection.query(sql, [userid], (err, results, _) => {
                    try {
                        if (err) {
                            reject(err);
                            return;
                        }
                        console.log('jobs delete done');
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

        const rds_result = await rds_reponse;

        return {
            statusCode: 200,
            body: "delete success"
        }

    }
    catch (err) {
        console.log("**ERROR:", err.message);
        return {
            statusCode: 400,
            body: err.message
        };
    }

};
