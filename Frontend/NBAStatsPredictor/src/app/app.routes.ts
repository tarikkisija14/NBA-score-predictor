
import { Routes } from '@angular/router';
import { StandingsComponent } from './components/standings/standings';
import { LeagueLeadersComponent } from './components/league-leaders/league-leaders';
import { TeamLeadersComponent } from './components/team-leaders/team-leaders';
import { PredictorComponent } from './components/predictor/predictor';


export const routes: Routes = [
  { path: '', pathMatch: 'full', redirectTo: 'standings' },
  {
    path: 'standings',
    loadComponent: () => import('./components/standings/standings')
      .then(m => m.StandingsComponent)
  },
  {
    path: 'league-leaders',
    loadComponent: () => import('./components/league-leaders/league-leaders')
      .then(m => m.LeagueLeadersComponent)
  },
  {
    path: 'team-leaders',
    loadComponent: () => import('./components/team-leaders/team-leaders')
      .then(m => m.TeamLeadersComponent)
  },
  {
    path: 'predictor',
    loadComponent: () => import('./components/predictor/predictor')
      .then(m => m.PredictorComponent)
  },
  { path: '**', redirectTo: 'standings' }
];
