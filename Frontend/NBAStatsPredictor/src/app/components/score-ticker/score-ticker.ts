import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule, AsyncPipe } from '@angular/common';
import{ScoresService,LiveGame,ScoresResponse} from '../../services/scorers-service';
import { Observable, Subscription } from 'rxjs';

@Component({
  selector: 'app-score-ticker',
  imports: [CommonModule, AsyncPipe],
  templateUrl: './score-ticker.html',
  styleUrl: './score-ticker.css',
  standalone: true,
})
export class ScoreTickerComponent {
  scores$: Observable<ScoresResponse>;

  constructor(private scoresService: ScoresService) {
    this.scores$ = this.scoresService.scores$;
  }

  isLive(game: LiveGame): boolean {
    const s = game.status.toLowerCase();
    return s.includes('qtr') || s.includes('half') || s.includes('ot') || game.period > 0 && !s.includes('final') && !s.includes('pm') && !s.includes('am');
  }

  trackByGame = (_: number, g: LiveGame) => g.game_id;
}
