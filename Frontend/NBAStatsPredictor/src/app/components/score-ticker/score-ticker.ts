import { Component } from '@angular/core';
import { CommonModule, AsyncPipe } from '@angular/common';
import { Observable } from 'rxjs';
import {ScoresService,ScoresResponse,LiveGame} from '../../services/scorers-service';

const LIVE_STATUS_KEYWORDS     = ['qtr', 'half', 'ot'];
const FINISHED_STATUS_KEYWORDS = ['final', 'pm', 'am'];

@Component({
  selector: 'app-score-ticker',
  standalone: true,
  imports: [CommonModule, AsyncPipe],
  templateUrl: './score-ticker.html',
  styleUrl: './score-ticker.css',
})
export class ScoreTickerComponent {
  readonly scores$: Observable<ScoresResponse>;

  constructor(private scoresService: ScoresService) {
    this.scores$ = this.scoresService.scores$;
  }

  isLive(game: LiveGame): boolean {
    const status     = game.status.toLowerCase();
    const hasLiveKw  = LIVE_STATUS_KEYWORDS.some(kw => status.includes(kw));
    const isFinished = FINISHED_STATUS_KEYWORDS.some(kw => status.includes(kw));
    return hasLiveKw || (game.period > 0 && !isFinished);
  }

  trackByGame = (_: number, game: LiveGame) => game.game_id;
}
