const Joi = require('joi');
const { ValidationError } = require('joi/lib/errors');

module.exports =  (schema, data) => {
    // Joi type of error
    console.log(data);
    const { error } = schema.validate(data);
    if (error) {
        if (error instanceof ValidationError) {
            return {
                status: 1,
                msg: [error.details[0].context.label, error.details[0].message]
            }
        }

        // other type of errors
        return {
            status: 1,
            msg: error.message || error
        }
    }
    return 1;
}
