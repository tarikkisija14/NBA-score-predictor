import { Component, signal } from '@angular/core';
import {StandingsComponent} from './components/standings/standings';
import {LeagueLeadersComponent} from './components/league-leaders/league-leaders';
import {TeamLeadersComponent} from './components/team-leaders/team-leaders';
import {PredictorComponent} from './components/predictor/predictor';



@Component({
  selector: 'app-root',
  imports: [
    StandingsComponent,
    LeagueLeadersComponent,
    TeamLeadersComponent,
    PredictorComponent,

  ],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  //standings will be default component when page loads
  activeSection: string = 'standings';
 //method to change which section is displayed
  showSection(sectionId: string) {
    this.activeSection = sectionId;
  }
}
