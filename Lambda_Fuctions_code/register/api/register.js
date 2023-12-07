const dbConnection = require('../database');
const {error} = require("joi/lib/annotate");
const bcrypt = require('bcryptjs');
const uuid = require('uuid');

module.exports = async (event) => {
    var result = {};
    try {
        var data = event;
        var rds_reponse = new Promise((resolve, reject) => {
            try {
                var sql = 'SELECT * FROM users_info WHERE username=?';
                dbConnection.query(sql, [data.username], (err, results, _) => {
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
                })
            } catch (code_err) {
                reject(code_err);
            }
        });

        const rds_result = await rds_reponse;

        if (rds_result.length == 0) {
            var insert_users_reponse = new Promise((resolve, reject) => {
                try {
                    var sql = 'INSERT INTO users_info value(null, ?, ?, ?, ?)';
                    // encrypt password
                    data.password = bcrypt.hashSync(event.password, 10);
                    dbConnection.query(sql, [data.email, data.username, data.password, uuid.v4()], (err, results, _) => {
                        try {
                            if (err) {
                                reject(err);
                                return;
                            }
                            if (results.affectedRows === 1) {
                                console.log('user insert done');
                                result = {
                                    status: 0,
                                    msg: 'account is created'
                                };
                                resolve(result);
                            }
                            else {
                                result = {
                                    status: 1,
                                    msg: 'account creation failed'
                                };
                                resolve(result);
                            }
                        } catch (code_err) {
                            reject(code_err);
                        }
                    });
                } catch (code_err) {
                    reject(code_err);
                }
            });

            const insert_result = await insert_users_reponse;
            return insert_result;

        } else {
            throw new Error('username existed');
        }
    }
    catch (err) {
        console.log("**ERROR", err.message);
        return {
            status: 1,
            msg: err.message,
        };
    }
};