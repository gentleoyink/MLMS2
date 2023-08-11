import { Component } from '@angular/core';
import { faEye, faEyeSlash } from '@fortawesome/free-solid-svg-icons';

@Component({
  selector: 'app-signup',
  templateUrl: './signup.component.html',
  styleUrls: ['./signup.component.scss']
})
export class SignupComponent {
  email = '';
  password = '';
  hide = true;
  invalidEmail = false;
  invalidPassword = false;
  faEye = faEye;
  faEyeSlash = faEyeSlash;

  validateEmail() {
    this.invalidEmail = !this.email.includes('@');
  }

  validatePassword() {
    const pattern = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
    this.invalidPassword = !pattern.test(this.password);
  }  

  toggleVisibility() {
    this.hide = !this.hide;
  }

  signup() {
    const formData = {
      email: this.email,
      password: this.password
    };
    // Send formData to your server...
  }
  
}
