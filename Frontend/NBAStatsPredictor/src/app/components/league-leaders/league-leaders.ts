import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import {LeagueLeadersService} from '../../services/league-leaders';
import {LeadersMap} from '../../models/Nba.models';
import {LEAGUE_LEADER_CATEGORIES} from '../../models/StatCategories.Constant';

@Component({
  selector: 'app-league-leaders',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './league-leaders.html',
  styleUrl: './league-leaders.css',
})
export class LeagueLeadersComponent implements OnInit {
  data: LeadersMap = {};
  loading = false;
  error: string | null = null;

  readonly categories = LEAGUE_LEADER_CATEGORIES;

  constructor(private leagueLeadersService: LeagueLeadersService) {}

  ngOnInit(): void {
    this.loading = true;
    this.leagueLeadersService.getLeagueLeaders().subscribe({
      next: (res) => {
        this.data    = res ?? {};
        this.loading = false;
      },
      error: (err: unknown) => {
        console.error(err);
        this.error   = 'Failed to load league leaders';
        this.loading = false;
      },
    });
  }

  trackByIndex = (i: number) => i;
}
