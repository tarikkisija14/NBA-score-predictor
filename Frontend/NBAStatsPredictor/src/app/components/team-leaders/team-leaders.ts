import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import {TeamLeadersService} from '../../services/team-leaders';
import {LeadersMap} from '../../models/Nba.models';
import {TEAM_LEADER_CATEGORIES} from '../../models/StatCategories.Constant';

@Component({
  selector: 'app-team-leaders',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './team-leaders.html',
  styleUrl: './team-leaders.css',
})
export class TeamLeadersComponent implements OnInit {
  data: LeadersMap = {};
  loading = false;
  error: string | null = null;

  readonly categories = TEAM_LEADER_CATEGORIES;

  constructor(private teamLeadersService: TeamLeadersService) {}

  ngOnInit(): void {
    this.loading = true;
    this.teamLeadersService.getTeamLeaders().subscribe({
      next: (res) => {
        this.data    = res ?? {};
        this.loading = false;
      },
      error: (err: unknown) => {
        console.error(err);
        this.error   = 'Failed to load team leaders';
        this.loading = false;
      },
    });
  }

  trackByIndex = (i: number) => i;
}
