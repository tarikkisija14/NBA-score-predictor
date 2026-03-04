import { Component } from '@angular/core';
import { NgIf, NgClass } from '@angular/common';
import { PredictorService, PredictionResponse } from '../../services/predictor';

interface Team {
  name: string;
  logo: string;
}

@Component({
  selector: 'app-predictor',
  imports: [NgIf, NgClass],
  templateUrl: './predictor.html',
  styleUrl: './predictor.css',
  standalone: true,
})
export class PredictorComponent {

  teams: Team[] = [
    { name: 'Atlanta Hawks',           logo: 'https://cdn.nba.com/logos/nba/1610612737/primary/L/logo.svg' },
    { name: 'Boston Celtics',          logo: 'https://cdn.nba.com/logos/nba/1610612738/primary/L/logo.svg' },
    { name: 'Brooklyn Nets',           logo: 'https://cdn.nba.com/logos/nba/1610612751/primary/L/logo.svg' },
    { name: 'Charlotte Hornets',       logo: 'https://cdn.nba.com/logos/nba/1610612766/primary/L/logo.svg' },
    { name: 'Chicago Bulls',           logo: 'https://cdn.nba.com/logos/nba/1610612741/primary/L/logo.svg' },
    { name: 'Cleveland Cavaliers',     logo: 'https://cdn.nba.com/logos/nba/1610612739/primary/L/logo.svg' },
    { name: 'Dallas Mavericks',        logo: 'https://cdn.nba.com/logos/nba/1610612742/primary/L/logo.svg' },
    { name: 'Denver Nuggets',          logo: 'https://cdn.nba.com/logos/nba/1610612743/primary/L/logo.svg' },
    { name: 'Detroit Pistons',         logo: 'https://cdn.nba.com/logos/nba/1610612765/primary/L/logo.svg' },
    { name: 'Golden State Warriors',   logo: 'https://cdn.nba.com/logos/nba/1610612744/primary/L/logo.svg' },
    { name: 'Houston Rockets',         logo: 'https://cdn.nba.com/logos/nba/1610612745/primary/L/logo.svg' },
    { name: 'Indiana Pacers',          logo: 'https://cdn.nba.com/logos/nba/1610612754/primary/L/logo.svg' },
    { name: 'LA Clippers',             logo: 'https://cdn.nba.com/logos/nba/1610612746/primary/L/logo.svg' },
    { name: 'Los Angeles Lakers',      logo: 'https://cdn.nba.com/logos/nba/1610612747/primary/L/logo.svg' },
    { name: 'Memphis Grizzlies',       logo: 'https://cdn.nba.com/logos/nba/1610612763/primary/L/logo.svg' },
    { name: 'Miami Heat',              logo: 'https://cdn.nba.com/logos/nba/1610612748/primary/L/logo.svg' },
    { name: 'Milwaukee Bucks',         logo: 'https://cdn.nba.com/logos/nba/1610612749/primary/L/logo.svg' },
    { name: 'Minnesota Timberwolves',  logo: 'https://cdn.nba.com/logos/nba/1610612750/primary/L/logo.svg' },
    { name: 'New Orleans Pelicans',    logo: 'https://cdn.nba.com/logos/nba/1610612740/primary/L/logo.svg' },
    { name: 'New York Knicks',         logo: 'https://cdn.nba.com/logos/nba/1610612752/primary/L/logo.svg' },
    { name: 'Oklahoma City Thunder',   logo: 'https://cdn.nba.com/logos/nba/1610612760/primary/L/logo.svg' },
    { name: 'Orlando Magic',           logo: 'https://cdn.nba.com/logos/nba/1610612753/primary/L/logo.svg' },
    { name: 'Philadelphia 76ers',      logo: 'https://cdn.nba.com/logos/nba/1610612755/primary/L/logo.svg' },
    { name: 'Phoenix Suns',            logo: 'https://cdn.nba.com/logos/nba/1610612756/primary/L/logo.svg' },
    { name: 'Portland Trail Blazers',  logo: 'https://cdn.nba.com/logos/nba/1610612757/primary/L/logo.svg' },
    { name: 'Sacramento Kings',        logo: 'https://cdn.nba.com/logos/nba/1610612758/primary/L/logo.svg' },
    { name: 'San Antonio Spurs',       logo: 'https://cdn.nba.com/logos/nba/1610612759/primary/L/logo.svg' },
    { name: 'Toronto Raptors',         logo: 'https://cdn.nba.com/logos/nba/1610612761/primary/L/logo.svg' },
    { name: 'Utah Jazz',               logo: 'https://cdn.nba.com/logos/nba/1610612762/primary/L/logo.svg' },
    { name: 'Washington Wizards',      logo: 'https://cdn.nba.com/logos/nba/1610612764/primary/L/logo.svg' },
  ];

  team1Index = 0;
  team2Index = 1;

  predictionResult: PredictionResponse | null = null;
  errorMessage: string | null = null;
  loading = false;


  constructor(private predictorService: PredictorService) {}

  get team1(): Team { return this.teams[this.team1Index]; }
  get team2(): Team { return this.teams[this.team2Index]; }



  private skip(current: number, delta: number, blocked: number): number {
    let next = (current + delta + this.teams.length) % this.teams.length;
    if (next === blocked) {
      next = (next + delta + this.teams.length) % this.teams.length;
    }
    return next;
  }

  nextTeam1() { this.team1Index = this.skip(this.team1Index, +1, this.team2Index); }
  prevTeam1() { this.team1Index = this.skip(this.team1Index, -1, this.team2Index); }
  nextTeam2() { this.team2Index = this.skip(this.team2Index, +1, this.team1Index); }
  prevTeam2() { this.team2Index = this.skip(this.team2Index, -1, this.team1Index); }

  predict() {
    this.loading = true;
    this.predictionResult = null;
    this.errorMessage = null;


    this.predictorService.predictGame(this.team1.name, this.team2.name).subscribe({
      next: (response) => {
        this.predictionResult = response;
        this.loading = false;
      },
      error: (err) => {
        console.error(err);
        this.errorMessage = 'Prediction failed. Please try again.';
        this.loading = false;
      }
    });
  }
}
