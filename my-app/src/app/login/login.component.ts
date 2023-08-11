import { Component } from '@angular/core';
import { faEye, faEyeSlash } from '@fortawesome/free-solid-svg-icons';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';

interface LoginResponse {
  token: string;
  // add other properties if needed
}

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent {
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

  constructor(private http: HttpClient, private router: Router) { }

  login() {
    const formData = {
      email: this.email,
      password: this.password
    };
  
    this.http.post<LoginResponse>('http://127.0.0.1:8000/users/api/login/', formData).subscribe(
      response => {
        // Handle response
        console.log(response);
        localStorage.setItem('token', response.token);  // Store the token in local storage
        this.router.navigate(['/']);
      },
      error => {
        // Handle error
        console.error(error);
      }
    );
  } 
}
