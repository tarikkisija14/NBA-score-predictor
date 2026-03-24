import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import {StandingsService} from '../../services/standings';
import {TeamRow,StandingsData,SortKey,SortDir} from '../../models/Nba.models';


const TEXT_SORT_KEYS: SortKey[] = ['team', 'home', 'away', 'div', 'conf'];

@Component({
  selector: 'app-standings',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './standings.html',
  styleUrl: './standings.css',
})
export class StandingsComponent implements OnInit {
  activeConference: 'east' | 'west' = 'east';
  east: TeamRow[] = [];
  west: TeamRow[] = [];
  loading = false;
  error: string | null = null;

  sortKey: SortKey = 'wins';
  sortDir: SortDir = 'desc';

  readonly columns: { key: SortKey; label: string }[] = [
    { key: 'team',   label: 'Team' },
    { key: 'wins',   label: 'W'    },
    { key: 'losses', label: 'L'    },
    { key: 'pct',    label: 'PCT'  },
    { key: 'gb',     label: 'GB'   },
    { key: 'conf',   label: 'CONF' },
    { key: 'home',   label: 'HOME' },
    { key: 'away',   label: 'AWAY' },
    { key: 'div',    label: 'DIV'  },
  ];

  constructor(private standingsService: StandingsService) {}

  ngOnInit(): void {
    this.fetchStandings();
  }

  fetchStandings(): void {
    this.loading = true;
    this.error   = null;

    this.standingsService.getStandings().subscribe({
      next: (response: StandingsData) => {
        this.east    = response.east    ?? [];
        this.west    = response.west    ?? [];
        this.loading = false;
      },
      error: (err: unknown) => {
        console.error('Error fetching standings:', err);
        this.error   = 'Failed to load standings';
        this.loading = false;
      },
    });
  }

  setConference(side: 'east' | 'west'): void {
    this.activeConference = side;
  }

  get activeRows(): TeamRow[] {
    const rows = [...(this.activeConference === 'east' ? this.east : this.west)];
    return rows.sort((a, b) => {
      const av   = a[this.sortKey];
      const bv   = b[this.sortKey];
      const aNum = parseFloat(String(av));
      const bNum = parseFloat(String(bv));
      const cmp  = isNaN(aNum) || isNaN(bNum)
        ? String(av).localeCompare(String(bv))
        : aNum - bNum;
      return this.sortDir === 'asc' ? cmp : -cmp;
    });
  }

  sort(key: SortKey): void {
    if (this.sortKey === key) {
      this.sortDir = this.sortDir === 'asc' ? 'desc' : 'asc';
    } else {
      this.sortKey = key;
      this.sortDir = TEXT_SORT_KEYS.includes(key) ? 'asc' : 'desc';
    }
  }

  sortIcon(key: SortKey): string {
    if (this.sortKey !== key) return '↕';
    return this.sortDir === 'asc' ? '↑' : '↓';
  }

  trackByTeam = (_: number, row: TeamRow) => row.team;
}
