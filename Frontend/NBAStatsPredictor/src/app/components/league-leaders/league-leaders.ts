import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { LeagueLeaders } from '../../services/league-leaders';

type LeadersMap = Record<string, { player?: string; team?: string; value?: number; error?: string }[]>;


@Component({
  selector: 'app-league-leaders',
  imports: [CommonModule],
  templateUrl: './league-leaders.html',
  styleUrl: './league-leaders.css',
  standalone:true

})
export class LeagueLeadersComponent implements OnInit {
   data: LeadersMap={};
   loading = false;
   error: string | null = null;

  categories = [
    { key: 'PTS', label: 'Points Per Game (PPG)' },
    { key: 'AST', label: 'Assists Per Game (APG)' },
    { key: 'REB', label: 'Rebounds Per Game (RPG)' },
    { key: 'STL', label: 'Steals Per Game (SPG)' },
    { key: 'BLK', label: 'Blocks Per Game (BPG)' },
    { key: 'MIN', label: 'Minutes Per Game (MIN)' }
  ];

  constructor(private leadersService: LeagueLeaders) {}

  ngOnInit(): void {
    this.loading = true;
    this.leadersService.getLeagueLeaders().subscribe({
      next: (res) => { this.data = res || {}; this.loading = false; },
      error: (err) => { this.error = 'Failed to load league leaders'; console.error(err); this.loading = false; }
    });
  }
  trackByIndex = (i: number) => i;
}
