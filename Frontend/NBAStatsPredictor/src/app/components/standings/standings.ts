import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Standings } from '../../services/standings';

interface TeamRow {
  logo: string;
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

type SortKey = keyof TeamRow;
type SortDir = 'asc' | 'desc';

@Component({
  selector: 'app-standings',
  imports: [CommonModule],
  templateUrl: './standings.html',
  styleUrl: './standings.css',
  standalone: true
})
export class StandingsComponent implements OnInit {
  activeConference: 'east' | 'west' = 'east';
  east: TeamRow[] = [];
  west: TeamRow[] = [];
  loading = false;
  error: string | null = null;

  sortKey: SortKey = 'wins';
  sortDir: SortDir = 'desc';

  columns: { key: SortKey; label: string }[] = [
    { key: 'team',   label: 'Team'  },
    { key: 'wins',   label: 'W'     },
    { key: 'losses', label: 'L'     },
    { key: 'pct',    label: 'PCT'   },
    { key: 'gb',     label: 'GB'    },
    { key: 'conf',   label: 'CONF'  },
    { key: 'home',   label: 'HOME'  },
    { key: 'away',   label: 'AWAY'  },
    { key: 'div',    label: 'DIV'   },
  ];

  constructor(private standingsService: Standings) {}

  ngOnInit(): void { this.fetch(); }

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

  setConference(side: 'east' | 'west') { this.activeConference = side; }

  get activeRows(): TeamRow[] {
    const rows = this.activeConference === 'east' ? [...this.east] : [...this.west];
    return rows.sort((a, b) => {
      const av = a[this.sortKey];
      const bv = b[this.sortKey];
      const aNum = parseFloat(String(av));
      const bNum = parseFloat(String(bv));
      const compared = isNaN(aNum) || isNaN(bNum)
        ? String(av).localeCompare(String(bv))
        : aNum - bNum;
      return this.sortDir === 'asc' ? compared : -compared;
    });
  }

  sort(key: SortKey) {
    if (this.sortKey === key) {
      this.sortDir = this.sortDir === 'asc' ? 'desc' : 'asc';
    } else {
      this.sortKey = key;
      // Numeric cols default desc, text cols asc
      this.sortDir = ['team', 'home', 'away', 'div', 'conf'].includes(key) ? 'asc' : 'desc';
    }
  }

  sortIcon(key: SortKey): string {
    if (this.sortKey !== key) return '↕';
    return this.sortDir === 'asc' ? '↑' : '↓';
  }

  trackByTeam = (_: number, row: TeamRow) => row.team;
}
