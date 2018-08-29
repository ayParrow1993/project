const jwt = require('jsonwebtoken');
const User = require('mongoose').model('User');
const PassportLocalStrategy = require('passport-local').Strategy;
 // we need jwtSecret as a seed of password
const config = require('../config/config.json');
module.exports = new PassportLocalStrategy({
 // email and password should match the login form sent from client
 	usernameField: 'email',
 	passwordField: 'password',
 	session: false, // default value
 	passReqToCallback: true // default value
 // done: callback
}, (req, email, password, done) => {
 	const userData = {
 	email: email.trim(),
 	password: password
 	};

  	return User.findOne({ email: userData.email }, (err, user) => {
 		if (err) { return done(err); }
 		if (!user) {
 // when user not found, set error message
 			const error = new Error('Incorrect email or password');
 			error.name = 'IncorrectCredentialsError';
 			return done(error);
 		}
 // check if a hashed user's password is equal to a value saved

 		return user.comparePassword(userData.password, (passwordErr,isMatch) => {
 			if (passwordErr) { return done(passwordErr); }
 			if (!isMatch) {
 // when password not match, set error message
 				const error = new Error('Incorrect email or password');
 				error.name = 'IncorrectCredentialsError';
 				return done(error);
 			}

		const payload = {
 			sub: user._id // mongodb internal id
 		};
 // create a token string
 		const token = jwt.sign(payload, config.jwtSecret);
 		return done(null, token, null);
 		});
 	});
});