import { Component } from '@angular/core';
import { NgIf } from '@angular/common';
import { StandingsComponent }    from './components/standings/standings';
import { LeagueLeadersComponent } from './components/league-leaders/league-leaders';
import { TeamLeadersComponent }  from './components/team-leaders/team-leaders';
import { PredictorComponent }    from './components/predictor/predictor';
import { ScoreTickerComponent }  from './components/score-ticker/score-ticker';

@Component({
  selector: 'app-root',
  imports: [
    StandingsComponent,
    LeagueLeadersComponent,
    TeamLeadersComponent,
    PredictorComponent,
    ScoreTickerComponent,
    NgIf,
  ],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  activeSection: string = 'standings';
  showSection(sectionId: string) { this.activeSection = sectionId; }
}
