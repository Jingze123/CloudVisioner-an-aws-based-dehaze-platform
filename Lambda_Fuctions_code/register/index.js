const express = require('express');
const app = express();
const register_validation = require('./middleware/register_valid');
const register_schema = require('./schema/register_schema');
const register = require('./api/register');

exports.handler = async (event, context) => {
    const data = JSON.parse(event.body);
    const valid_result = register_validation(register_schema, data);
    if (valid_result === 1) {
        const register_result = await register(data);
        console.log(register_result);
        // error occurs
        if (register_result.status === 1) {
            return {
                statusCode: 400,
                body: register_result.msg
            }
        }
        // no error
        return {
            statusCode: 200,
            body: register_result.msg };
    }
    return {
        statusCode: 400,
        body: valid_result.msg[1]
    };
};