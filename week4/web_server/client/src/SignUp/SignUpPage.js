import React from 'react';
import SignUpForm from './SignUpForm';

class SignUpPage extends React.Component{
	constructor(props){
		super(props);

		this.state = {
			errors:{},
			user: {
				email:'',
				password:'',
				confirm_password:''
			}
		};
	}
	processForm(event){
		event.preventDefault();

		const email = this.state.user.email;
		const password = this.state.user.password;
		const confirm_password = this.state.user.confirm_password;

		console.log('email',email);
		console.log('password',password);
		console.log('confirm_password',confirm_password);

		if(password !== confirm_password){
			return;
		}

		//to do

	}
	changeUser(event){
		const field = event.target.name;
		const user = this.state.user;
		user[field] = event.target.value;

		this.setState({user});

		const errors = this.state.errors;
		if (this.state.user.password !== this.state.user.confirm_password){
			errors.password = "password and confirmed password don't match"
		}else{
			errors.password = '';
		}
		this.setState({errors});
	}


	render(){
		return (
			<SignUpForm
				onSubmit={(e)=> this.processForm(e)}
				onChange={(e)=> this.changeUser(e)}
				errors={this.state.errors}
			/>
			)
	}
}

export default SignUpPage;