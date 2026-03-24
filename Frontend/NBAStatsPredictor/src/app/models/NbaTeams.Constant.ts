/**
 * nba-teams.constant.ts
 *
 * The canonical list of 30 NBA teams with their official logo URLs.
 * Extracted from predictor.ts to make it reusable and independently testable.
 */

import {NbaTeam} from './Nba.models';

const NBA_LOGO_BASE = 'https://cdn.nba.com/logos/nba';

function teamLogo(id: number): string {
  return `${NBA_LOGO_BASE}/${id}/primary/L/logo.svg`;
}

export const NBA_TEAMS: NbaTeam[] = [
  { name: 'Atlanta Hawks',          logo: teamLogo(1610612737) },
  { name: 'Boston Celtics',         logo: teamLogo(1610612738) },
  { name: 'Brooklyn Nets',          logo: teamLogo(1610612751) },
  { name: 'Charlotte Hornets',      logo: teamLogo(1610612766) },
  { name: 'Chicago Bulls',          logo: teamLogo(1610612741) },
  { name: 'Cleveland Cavaliers',    logo: teamLogo(1610612739) },
  { name: 'Dallas Mavericks',       logo: teamLogo(1610612742) },
  { name: 'Denver Nuggets',         logo: teamLogo(1610612743) },
  { name: 'Detroit Pistons',        logo: teamLogo(1610612765) },
  { name: 'Golden State Warriors',  logo: teamLogo(1610612744) },
  { name: 'Houston Rockets',        logo: teamLogo(1610612745) },
  { name: 'Indiana Pacers',         logo: teamLogo(1610612754) },
  { name: 'LA Clippers',            logo: teamLogo(1610612746) },
  { name: 'Los Angeles Lakers',     logo: teamLogo(1610612747) },
  { name: 'Memphis Grizzlies',      logo: teamLogo(1610612763) },
  { name: 'Miami Heat',             logo: teamLogo(1610612748) },
  { name: 'Milwaukee Bucks',        logo: teamLogo(1610612749) },
  { name: 'Minnesota Timberwolves', logo: teamLogo(1610612750) },
  { name: 'New Orleans Pelicans',   logo: teamLogo(1610612740) },
  { name: 'New York Knicks',        logo: teamLogo(1610612752) },
  { name: 'Oklahoma City Thunder',  logo: teamLogo(1610612760) },
  { name: 'Orlando Magic',          logo: teamLogo(1610612753) },
  { name: 'Philadelphia 76ers',     logo: teamLogo(1610612755) },
  { name: 'Phoenix Suns',           logo: teamLogo(1610612756) },
  { name: 'Portland Trail Blazers', logo: teamLogo(1610612757) },
  { name: 'Sacramento Kings',       logo: teamLogo(1610612758) },
  { name: 'San Antonio Spurs',      logo: teamLogo(1610612759) },
  { name: 'Toronto Raptors',        logo: teamLogo(1610612761) },
  { name: 'Utah Jazz',              logo: teamLogo(1610612762) },
  { name: 'Washington Wizards',     logo: teamLogo(1610612764) },
];
