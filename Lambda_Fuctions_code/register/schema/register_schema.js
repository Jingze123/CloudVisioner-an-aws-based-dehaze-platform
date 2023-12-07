const Joi = require('joi')

const registerSchema = Joi.object({
    username: Joi.string().required(),
    email: Joi.string().email().required(),
    password: Joi.string().required()
    // passwordConfirm: Joi.ref('password')
})

module.exports = registerSchema;