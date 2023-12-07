const dbConnection = require('./database.js')
const jwt = require('jsonwebtoken');

exports.handler = async (event, context) => {
    try {
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
        const token_data = jwt.verify(token,"jwttoken",(error,decoded)=>{
            if(error){
                return {
                    statusCode: 401,
                    body: error.message
                }
            }
            return decoded;
        })

        // token error
        if (token_data.statusCode) {
            return {
                statusCode:token_data.statusCode,
                body: token_data.body
            }
        }

        const userid = token_data.userid;

        // get this users' jobs
        const rds_reponse = new Promise((resolve, reject) => {
            try {
                const sql = 'SELECT * FROM jobs WHERE userid=?';
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

        return {
            statusCode: 200,
            body: JSON.stringify(rds_result)
        }
    }
    catch (err) {
        console.log("**ERROR:", err.message);
        return {
            statusCode: 400,
            body: err.message
        }
    }//catch
};
