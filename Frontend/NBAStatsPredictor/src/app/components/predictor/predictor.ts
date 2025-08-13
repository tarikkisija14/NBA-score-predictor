import { Component, ElementRef, ViewChild } from '@angular/core';


@Component({
  selector: 'app-predictor',
  imports: [],
  templateUrl: './predictor.html',
  styleUrl: './predictor.css',
  standalone: true,
})
export class PredictorComponent {
  @ViewChild('predictionResult') predictionResult!: ElementRef;

  selectTeam(teamName: string): void {
    alert(`Select Team ${teamName}`);
  }

  cycleTeam(teamName: string, direction: string): void {
    alert(`Cycle Team ${teamName} ${direction}`);
  }

  predictGame(): void {
    this.predictionResult.nativeElement.innerText = 'Prediction: Team 1 vs Team 2 - Processing...';
  }
}

