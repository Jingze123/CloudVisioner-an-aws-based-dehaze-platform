const dbConnection = require('../database');
const bcrypt = require('bcryptjs')
const jwt = require('jsonwebtoken');


module.exports = async (event) => {
    let data = event;
    let result = {};
    try {
        // whether the username is in the db
        let rds_response = new Promise((resolve, reject) => {
            try {
                let sql = 'SELECT * from users_info WHERE username=?';
                dbConnection.query(sql, [data.username], (err, results, _) => {
                    try {
                        if (err) {
                            reject(err);
                            return;
                        }
                        console.log('user query done');
                        resolve(results);
                    }
                    catch (code_err) {
                        reject(code_err);
                    }
                })
            }
            catch (code_err) {
                reject(code_err);
            }
        });

        const rds_result = await rds_response;

        // username not in db
        if (rds_result.length == 0) {
            return {
                status: 1,
                msg: 'username does not exist'
            }
        }
        // username is in db
        else {
            let password_compare = await bcrypt.compare(data.password, rds_result[0].password);
            // password correct
            if (password_compare && data.email === rds_result[0].email) {
                // generate token
                const userid = rds_result[0].userid;
                const token = jwt.sign({userid},'jwttoken',{expiresIn:"1h"});
                return {
                    status: 0,
                    msg: token
                }
            }

            // password incorrect
            else {
                return {
                    status: 1,
                    msg: 'password/email is incorrect'
                }
            }
        }
    }
    catch (err) {
        console.log("**ERROR", err.message);
        return {
            status: 1,
            msg: err.message
        };
    }
}