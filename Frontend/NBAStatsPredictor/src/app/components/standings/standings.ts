import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Standings } from '../../services/standings';

interface TeamRow {
  team: string;
  wins: number;
  losses: number;
  pct: number;
  gb: string | number;
  home: string;
  away: string;
  div: string;
  conf: string;
}

interface StandingsData {
  east: TeamRow[];
  west: TeamRow[];
}

@Component({
  selector: 'app-standings',
  imports: [CommonModule],
  templateUrl: './standings.html',
  styleUrl: './standings.css',
  standalone:true
})
export class StandingsComponent implements OnInit {
  activeConference: 'east' | 'west' = 'east';
  east: TeamRow[] = [];
  west: TeamRow[] = [];
  loading = false;
  error: string | null = null;

  constructor(private standingsService: Standings) {}

  ngOnInit(): void {
    this.fetch();
  }

  fetch(): void {
    this.loading = true;
    this.error = null;

    this.standingsService.getStandings().subscribe({
      next: (response: StandingsData) => {
        this.east = response.east || [];
        this.west = response.west || [];
        this.loading = false;
      },
      error: (error: any) => {
        this.error = 'Failed to load standings';
        console.error('Error fetching standings:', error);
        this.loading = false;
      }
    });
  }

  setConference(side: 'east' | 'west') {
    this.activeConference = side;
  }

  trackByTeam = (_: number, row: TeamRow) => row.team;
}


