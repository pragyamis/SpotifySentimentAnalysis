import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { LoginComponent } from './login/login.component';
import { MainComponent } from './main/main.component';
import { AboutComponent } from './about/about.component';


const routes: Routes = [
  {path :"login", component : LoginComponent},
  {path : "main", component : MainComponent},
  {path : "about", component : AboutComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
export const routingComponents = [LoginComponent, MainComponent, AboutComponent];
