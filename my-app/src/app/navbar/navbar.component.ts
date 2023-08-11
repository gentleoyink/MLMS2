import { Component, OnInit } from '@angular/core';
import { faBars, faUser, faShoppingCart, faSearch, faAngleDown, faUserCircle, faAngleRight, faShop } from '@fortawesome/free-solid-svg-icons';
import { BreakpointObserver, Breakpoints } from '@angular/cdk/layout';
import { Router } from '@angular/router';
import { Observable } from 'rxjs';
import { map, shareReplay } from 'rxjs/operators';
import { AuthService } from '../auth.service'; // Update the path based on your project structure
import { ChangeDetectorRef } from '@angular/core';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.scss']
})
export class NavbarComponent implements OnInit {
  faBars = faBars;
  faUser = faUser;
  faShoppingCart = faShoppingCart;
  faAngleRight = faAngleRight;
  faSearch = faSearch;
  faAngleDown = faAngleDown;
  faUserCircle = faUserCircle;
  faShop = faShop;
  isLoggedIn$: Observable<boolean>;
  isInstructor: boolean = false;
  showNavbar = false;
  isMobileView = false;
  userInitials: string = "U";
  user: any = null;

  isHandset$: Observable<boolean> = this.breakpointObserver.observe(Breakpoints.Handset)
    .pipe(
      map(result => result.matches),
      shareReplay()
    );

    constructor(
      public authService: AuthService,
      private breakpointObserver: BreakpointObserver, 
      private router: Router
    ) {
      this.authService.user$.subscribe(user => {
        this.user = user;
        if (user) {
          this.userInitials = user.first_name ? user.first_name.charAt(0) : 'U';
        }
      });
    
      this.isLoggedIn$ = this.authService.isLoggedIn$; // Add this line to initialize isLoggedIn$
    }
    

  ngOnInit(): void {
    this.checkMobileView();
    window.onresize = () => {
      this.checkMobileView();
    };
  }

  checkMobileView() {
    this.isMobileView = window.innerWidth <= 768;
  }

  toggleNavbar() {
    this.showNavbar = !this.showNavbar;
  }

  logIn(): void {
    this.router.navigate(['/login']);
  }

  signUp(): void {
    this.router.navigate(['/signup']);
  }

  becomeInstructor(): void {
    this.router.navigate(['/instructor']);
  }

  logOut(): void {
    this.authService.logout().subscribe(() => {
      this.router.navigate(['/']);
    });
  }
}
