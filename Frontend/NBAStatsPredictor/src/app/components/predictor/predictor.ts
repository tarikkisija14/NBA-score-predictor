import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import {NgIf} from '@angular/common';

interface Team {
  name: string;
  logo: string;
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
    { name: 'Atlanta Hawks', logo: 'assets/logos/hawks.png' },
    { name: 'Boston Celtics', logo: 'assets/logos/celtics.png' },
    { name: 'Brooklyn Nets', logo: 'assets/logos/nets.png' },
    { name: 'Charlotte Hornets', logo: 'assets/logos/hornets.png' },
    { name: 'Chicago Bulls', logo: 'assets/logos/bulls.png' },
    { name: 'Cleveland Cavaliers', logo: 'assets/logos/cavaliers.png' },
    { name: 'Dallas Mavericks', logo: 'assets/logos/mavericks.png' },
    { name: 'Denver Nuggets', logo: 'assets/logos/nuggets.png' },
    { name: 'Detroit Pistons', logo: 'assets/logos/pistons.png' },
    { name: 'Golden State Warriors', logo: 'assets/logos/warriors.png' },
    { name: 'Houston Rockets', logo: 'assets/logos/rockets.png' },
    { name: 'Indiana Pacers', logo: 'assets/logos/pacers.png' },
    { name: 'Los Angeles Clippers', logo: 'assets/logos/clippers.png' },
    { name: 'Los Angeles Lakers', logo: 'assets/logos/lakers.png' },
    { name: 'Memphis Grizzlies', logo: 'assets/logos/grizzlies.png' },
    { name: 'Miami Heat', logo: 'assets/logos/heat.png' },
    { name: 'Milwaukee Bucks', logo: 'assets/logos/bucks.png' },
    { name: 'Minnesota Timberwolves', logo: 'assets/logos/timberwolves.png' },
    { name: 'New Orleans Pelicans', logo: 'assets/logos/pelicans.png' },
    { name: 'New York Knicks', logo: 'assets/logos/knicks.png' },
    { name: 'Oklahoma City Thunder', logo: 'assets/logos/thunder.png' },
    { name: 'Orlando Magic', logo: 'assets/logos/magic.png' },
    { name: 'Philadelphia 76ers', logo: 'assets/logos/76ers.png' },
    { name: 'Phoenix Suns', logo: 'assets/logos/suns.png' },
    { name: 'Portland Trail Blazers', logo: 'assets/logos/blazers.png' },
    { name: 'Sacramento Kings', logo: 'assets/logos/kings.png' },
    { name: 'San Antonio Spurs', logo: 'assets/logos/spurs.png' },
    { name: 'Toronto Raptors', logo: 'assets/logos/raptors.png' },
    { name: 'Utah Jazz', logo: 'assets/logos/jazz.png' },
    { name: 'Washington Wizards', logo: 'assets/logos/wizards.png' }
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
      team1: this.team1Name,
      team2: this.team2Name
    };

    this.http.post<{ result: string }>('http://localhost:5000/predict', payload)
      .subscribe({
        next: (response) => {
          this.predictionResult = response.result;
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

