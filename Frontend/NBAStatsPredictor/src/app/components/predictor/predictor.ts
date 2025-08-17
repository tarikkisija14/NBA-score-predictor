import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import {NgIf} from '@angular/common';

interface Team {
  name: string;
  logo: string;
}

interface PredictionResponse {
  winner: string;
  winner_points: number;
  loser: string;
  loser_points: number;
}

@Component({
  selector: 'app-predictor',
  imports: [
    NgIf
  ],
  templateUrl: './predictor.html',
  styleUrl: './predictor.css',
  standalone: true,
})
export class PredictorComponent {
  teams: Team[] = [
    { name: 'Atlanta Hawks', logo: 'https://cdn.nba.com/logos/nba/1610612737/primary/L/logo.svg' },
    { name: 'Boston Celtics', logo: 'https://cdn.nba.com/logos/nba/1610612738/primary/L/logo.svg' },
    { name: 'Brooklyn Nets', logo: 'https://cdn.nba.com/logos/nba/1610612751/primary/L/logo.svg' },
    { name: 'Charlotte Hornets', logo: 'https://cdn.nba.com/logos/nba/1610612766/primary/L/logo.svg' },
    { name: 'Chicago Bulls', logo: 'https://cdn.nba.com/logos/nba/1610612741/primary/L/logo.svg' },
    { name: 'Cleveland Cavaliers', logo: 'https://cdn.nba.com/logos/nba/1610612739/primary/L/logo.svg' },
    { name: 'Dallas Mavericks', logo: 'https://cdn.nba.com/logos/nba/1610612742/primary/L/logo.svg' },
    { name: 'Denver Nuggets', logo: 'https://cdn.nba.com/logos/nba/1610612743/primary/L/logo.svg' },
    { name: 'Detroit Pistons', logo: 'https://cdn.nba.com/logos/nba/1610612765/primary/L/logo.svg' },
    { name: 'Golden State Warriors', logo: 'https://cdn.nba.com/logos/nba/1610612744/primary/L/logo.svg' },
    { name: 'Houston Rockets', logo: 'https://cdn.nba.com/logos/nba/1610612745/primary/L/logo.svg' },
    { name: 'Indiana Pacers', logo: 'https://cdn.nba.com/logos/nba/1610612754/primary/L/logo.svg' },
    { name: 'LA Clippers', logo: 'https://cdn.nba.com/logos/nba/1610612746/primary/L/logo.svg' },
    { name: 'Los Angeles Lakers', logo: 'https://cdn.nba.com/logos/nba/1610612747/primary/L/logo.svg' },
    { name: 'Memphis Grizzlies', logo: 'https://cdn.nba.com/logos/nba/1610612763/primary/L/logo.svg' },
    { name: 'Miami Heat', logo: 'https://cdn.nba.com/logos/nba/1610612748/primary/L/logo.svg' },
    { name: 'Milwaukee Bucks', logo: 'https://cdn.nba.com/logos/nba/1610612749/primary/L/logo.svg' },
    { name: 'Minnesota Timberwolves', logo: 'https://cdn.nba.com/logos/nba/1610612750/primary/L/logo.svg' },
    { name: 'New Orleans Pelicans', logo: 'https://cdn.nba.com/logos/nba/1610612740/primary/L/logo.svg' },
    { name: 'New York Knicks', logo: 'https://cdn.nba.com/logos/nba/1610612752/primary/L/logo.svg' },
    { name: 'Oklahoma City Thunder', logo: 'https://cdn.nba.com/logos/nba/1610612760/primary/L/logo.svg' },
    { name: 'Orlando Magic', logo: 'https://cdn.nba.com/logos/nba/1610612753/primary/L/logo.svg' },
    { name: 'Philadelphia 76ers', logo: 'https://cdn.nba.com/logos/nba/1610612755/primary/L/logo.svg' },
    { name: 'Phoenix Suns', logo: 'https://cdn.nba.com/logos/nba/1610612756/primary/L/logo.svg' },
    { name: 'Portland Trail Blazers', logo: 'https://cdn.nba.com/logos/nba/1610612757/primary/L/logo.svg' },
    { name: 'Sacramento Kings', logo: 'https://cdn.nba.com/logos/nba/1610612758/primary/L/logo.svg' },
    { name: 'San Antonio Spurs', logo: 'https://cdn.nba.com/logos/nba/1610612759/primary/L/logo.svg' },
    { name: 'Toronto Raptors', logo: 'https://cdn.nba.com/logos/nba/1610612761/primary/L/logo.svg' },
    { name: 'Utah Jazz', logo: 'https://cdn.nba.com/logos/nba/1610612762/primary/L/logo.svg' },
    { name: 'Washington Wizards', logo: 'https://cdn.nba.com/logos/nba/1610612764/primary/L/logo.svg' }
  ];


  team1Index = 0;
  team2Index = 1;

  predictionResult: string | null = null;
  loading = false;

  constructor(private http: HttpClient) {}

  get team1Name(): string {
    return this.teams[this.team1Index].name;
  }

  get team2Name(): string {
    return this.teams[this.team2Index].name;
  }

  get team1Logo(): string {
    return this.teams[this.team1Index].logo;
  }

  get team2Logo(): string {
    return this.teams[this.team2Index].logo;
  }

  nextTeam1() {
    this.team1Index = (this.team1Index + 1) % this.teams.length;
  }

  prevTeam1() {
    this.team1Index = (this.team1Index - 1 + this.teams.length) % this.teams.length;
  }

  nextTeam2() {
    this.team2Index = (this.team2Index + 1) % this.teams.length;
  }

  prevTeam2() {
    this.team2Index = (this.team2Index - 1 + this.teams.length) % this.teams.length;
  }

  predict() {
    this.loading = true;
    this.predictionResult = null;

    const payload = {
      HomeTeam: this.team1Name,
      AwayTeam: this.team2Name
    };

    this.http.post<PredictionResponse>('https://localhost:7042/api/prediction/predict', payload)
      .subscribe({
        next: (response) => {
          this.predictionResult = `${response.winner} ${response.winner_points} - ${response.loser_points} ${response.loser}`;
          this.loading = false;
        },
        error: (err) => {
          console.error(err);
          this.predictionResult = 'Error while predicting.';
          this.loading = false;
        }
      });

  }

}

