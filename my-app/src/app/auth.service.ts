import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { tap } from 'rxjs/operators';
import { BehaviorSubject, Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  private user = new BehaviorSubject<any>(null);
  private loggedIn = new BehaviorSubject<boolean>(false);

  isLoggedIn$ = this.loggedIn.asObservable();
  user$ = this.user.asObservable();

  constructor(private httpClient: HttpClient) {
    // Fetch user information if already authenticated
    this.fetchUser();
  }

  login(user: any) {
    return this.httpClient.post('http://127.0.0.1:8000/users/api/login/', user)
      .pipe(tap((res: any) => {
        this.fetchUser(); // Fetch user details after successful login
        this.loggedIn.next(true);
      }));
  }

  logout() {
    // Remove authentication cookie on the server side
    return this.httpClient.post('http://127.0.0.1:8000/users/api/logout/', {})
      .pipe(tap(() => {
        this.user.next(null);
        this.loggedIn.next(false); // Also set loggedIn to false
      }));
  }

  private fetchUser() {
    this.httpClient.get('http://127.0.0.1:8000/users/api/me/', { withCredentials: true })
      .subscribe(user => {
        this.user.next(user);
      });
  }
}
