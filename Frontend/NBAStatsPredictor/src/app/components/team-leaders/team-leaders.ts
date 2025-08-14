import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { TeamLeaders } from '../../services/team-leaders';


type TeamLeadersMap = Record<string, { team?: string; value?: number }[]>;

@Component({
  selector: 'app-team-leaders',
  imports: [CommonModule],
  templateUrl: './team-leaders.html',
  styleUrl: './team-leaders.css',
  standalone:true
})
export class TeamLeadersComponent implements OnInit  {
   data: TeamLeadersMap = {};
   loading = false;
   error: string | null = null;

  categories = [
    { key: 'PTS', label: 'Points Per Game (PPG)' },
    { key: 'AST', label: 'Assists Per Game (APG)' },
    { key: 'REB', label: 'Rebounds Per Game (RPG)' },
    { key: 'STL', label: 'Steals Per Game (SPG)' },
    { key: 'BLK', label: 'Blocks Per Game (BPG)' },
    { key: 'FG_PCT', label: 'Field Goal % (FG%)' }
  ];

  constructor(private service: TeamLeaders) {}

  ngOnInit(): void {
    this.loading = true;
    this.service.getTeamLeaders().subscribe({
      next: (res) => { this.data = res || {}; this.loading = false; },
      error: (err) => { this.error = 'Failed to load team leaders'; console.error(err); this.loading = false; }
    });
  }

  trackByIndex = (i: number) => i;

}
