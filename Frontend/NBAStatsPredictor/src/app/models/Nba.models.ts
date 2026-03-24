
// ---------------------------------------------------------------------------
// Standings
// ---------------------------------------------------------------------------

export interface TeamRow {
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

export interface StandingsData {
  east: TeamRow[];
  west: TeamRow[];
}

export type SortKey = keyof TeamRow;
export type SortDir = 'asc' | 'desc';

// ---------------------------------------------------------------------------
// Scores / Live ticker
// ---------------------------------------------------------------------------

export interface LiveGame {
  game_id: string;
  status: string;
  period: number;
  home_team: string;
  home_tricode: string;
  home_score: number;
  home_logo: string;
  away_team: string;
  away_tricode: string;
  away_score: number;
  away_logo: string;
}

export interface ScoresResponse {
  games: LiveGame[];
  count: number;
  error?: string;
}

// ---------------------------------------------------------------------------
// League / Team leaders
// ---------------------------------------------------------------------------

export interface LeaderEntry {
  player?: string;
  team?: string;
  value?: number;
  error?: string;
}

export type LeadersMap = Record<string, LeaderEntry[]>;

export interface StatCategory {
  key: string;
  label: string;
}

// ---------------------------------------------------------------------------
// Predictor
// ---------------------------------------------------------------------------

export interface H2HGame {
  season: string;
  home: string;
  away: string;
  home_pts: number;
  away_pts: number;
  winner: string;
}

export interface HeadToHead {
  games: H2HGame[];
  team1_wins: number;
  team2_wins: number;
  total: number;
}

export interface PredictionResponse {
  winner: string;
  winner_points: number;
  loser: string;
  loser_points: number;
  confidence: number;
  head_to_head: HeadToHead;
}

export interface PredictRequest {
  HomeTeam: string;
  AwayTeam: string;
}

export interface NbaTeam {
  name: string;
  logo: string;
}
