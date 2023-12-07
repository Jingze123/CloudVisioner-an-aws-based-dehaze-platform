const login = require('./api/login')


exports.handler = async (event, context) => {
    const data = JSON.parse(event.body);
    const login_result = await login(data);
    if (login_result.status === 1) {
        return {
            statusCode: 400,
            body: login_result.msg
        }
    }
    return {
        statusCode: 200,
        body: login_result.msg
    }
};
