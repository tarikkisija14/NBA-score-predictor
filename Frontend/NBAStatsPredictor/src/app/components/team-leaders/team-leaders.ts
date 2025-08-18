import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { TeamLeaders } from '../../services/team-leaders';

//map type definition for data returned from the API
type TeamLeadersMap = Record<string, { team?: string; value?: number }[]>;

@Component({
  selector: 'app-team-leaders',
  imports: [CommonModule],
  templateUrl: './team-leaders.html',
  styleUrl: './team-leaders.css',
  standalone:true
})
export class TeamLeadersComponent implements OnInit  {
  //hold api data structured by given stat categories
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
    //start loading
    this.loading = true;
    this.service.getTeamLeaders().subscribe({
      //if request succeeds, update data and stop loading
      next: (res) => { this.data = res || {}; this.loading = false; },
      error: (err) => { this.error = 'Failed to load team leaders'; console.error(err); this.loading = false; }
    });
  }

  trackByIndex = (i: number) => i;

}
