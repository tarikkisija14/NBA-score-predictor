import { Component } from '@angular/core';
import { NgIf, NgClass, NgFor } from '@angular/common';
import {PredictorService,PredictionResponse} from '../../services/predictor';
import {NbaTeam} from '../../models/Nba.models';
import {NBA_TEAMS} from '../../models/NbaTeams.Constant';

const CONFIDENCE_HIGH_THRESHOLD   = 75;
const CONFIDENCE_MEDIUM_THRESHOLD = 60;
const CONFIDENCE_COLOR_HIGH       = '#22c55e';
const CONFIDENCE_COLOR_MEDIUM     = '#fdb927';
const CONFIDENCE_COLOR_LOW        = '#c8102e';

@Component({
  selector: 'app-predictor',
  standalone: true,
  imports: [NgIf, NgClass, NgFor],
  templateUrl: './predictor.html',
  styleUrl: './predictor.css',
})
export class PredictorComponent {
  readonly teams: NbaTeam[] = NBA_TEAMS;

  team1Index  = 0;
  team2Index  = 1;
  team1IsHome = true;

  predictionResult: PredictionResponse | null = null;
  errorMessage: string | null = null;
  loading = false;

  constructor(private predictorService: PredictorService) {}

  get team1(): NbaTeam { return this.teams[this.team1Index]; }
  get team2(): NbaTeam { return this.teams[this.team2Index]; }

  get homeTeam(): NbaTeam { return this.team1IsHome ? this.team1 : this.team2; }
  get awayTeam(): NbaTeam { return this.team1IsHome ? this.team2 : this.team1; }

  get homeTeamName(): string { return this.homeTeam.name; }
  get awayTeamName(): string { return this.awayTeam.name; }

  get confidenceBar(): number {
    return this.predictionResult
      ? Math.min(this.predictionResult.confidence, 100)
      : 0;
  }

  get confidenceColor(): string {
    const c = this.confidenceBar;
    if (c >= CONFIDENCE_HIGH_THRESHOLD)   return CONFIDENCE_COLOR_HIGH;
    if (c >= CONFIDENCE_MEDIUM_THRESHOLD) return CONFIDENCE_COLOR_MEDIUM;
    return CONFIDENCE_COLOR_LOW;
  }

  swapHomeAway(): void {
    this.team1IsHome      = !this.team1IsHome;
    this.predictionResult = null;
    this.errorMessage     = null;
  }

  nextTeam1(): void { this.team1Index = this.advanceIndex(this.team1Index, +1, this.team2Index); this.clearResult(); }
  prevTeam1(): void { this.team1Index = this.advanceIndex(this.team1Index, -1, this.team2Index); this.clearResult(); }
  nextTeam2(): void { this.team2Index = this.advanceIndex(this.team2Index, +1, this.team1Index); this.clearResult(); }
  prevTeam2(): void { this.team2Index = this.advanceIndex(this.team2Index, -1, this.team1Index); this.clearResult(); }

  predict(): void {
    this.loading          = true;
    this.predictionResult = null;
    this.errorMessage     = null;

    this.predictorService.predictGame(this.homeTeamName, this.awayTeamName).subscribe({
      next: (response) => {
        this.predictionResult = response;
        this.loading          = false;
      },
      error: (err: unknown) => {
        console.error(err);
        this.errorMessage = 'Prediction failed. Please try again.';
        this.loading      = false;
      },
    });
  }


  private clearResult(): void {
    this.predictionResult = null;
  }

  private advanceIndex(current: number, delta: number, blocked: number): number {
    let next = (current + delta + this.teams.length) % this.teams.length;
    if (next === blocked) {
      next = (next + delta + this.teams.length) % this.teams.length;
    }
    return next;
  }
}
