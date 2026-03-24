

import {StatCategory} from './Nba.models';

export const LEAGUE_LEADER_CATEGORIES: StatCategory[] = [
  { key: 'PTS', label: 'Points Per Game (PPG)'  },
  { key: 'AST', label: 'Assists Per Game (APG)'  },
  { key: 'REB', label: 'Rebounds Per Game (RPG)' },
  { key: 'STL', label: 'Steals Per Game (SPG)'   },
  { key: 'BLK', label: 'Blocks Per Game (BPG)'   },
  { key: 'MIN', label: 'Minutes Per Game (MIN)'   },
];

export const TEAM_LEADER_CATEGORIES: StatCategory[] = [
  { key: 'PTS',    label: 'Points Per Game (PPG)'  },
  { key: 'AST',    label: 'Assists Per Game (APG)'  },
  { key: 'REB',    label: 'Rebounds Per Game (RPG)' },
  { key: 'STL',    label: 'Steals Per Game (SPG)'   },
  { key: 'BLK',    label: 'Blocks Per Game (BPG)'   },
  { key: 'FG_PCT', label: 'Field Goal % (FG%)'      },
];
