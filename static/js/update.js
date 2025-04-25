function updateSlider() {
  if (currentPage === 1) {
    $(".bx-prev").css('display', 'none')
  } else {
    $(".bx-prev").css('display', 'block')
  }
  if (currentPage === totalPages) {
    $(".bx-next").css('display', 'none')
  } else {
    $(".bx-next").css('display', 'block')
  }

  const offset = (currentPage - 1) * 1050
  $(".game-list-n").css('transform', `translateX(-${offset}px)`)
}

function updateMatchBox(response) {
  const matchBox = $(".match-box");
  matchBox.empty();
  matchBox.append(`
    <span class="match-box-title">장소</span>
    <span class="match-box-txt">${response.stadium_name}</span>
    <span class="match-box-title">경기일자</span>
    <span class="match-box-txt">${response.game_date}</span>
    <span class="match-box-title">방송중계</span>
    <span class="match-box-txt">${response.tv_channel}</span>
  `);
}

function updateTeamInfo(response) {
  const teamHomeInfo = $(".team.home.info");
  teamHomeInfo.empty();
  teamHomeInfo.append(`
    <div class="name" style="color: ${response.home_team_color};">${response.home_team_full_name}</div>
    <div class="score">${response.home_team_record}</div>
    <div class="emb">
      <img src="//6ptotvmi5753.edge.naverncp.com/KBO_IMAGE/KBOHome/resources/images/emblem/regular/2022/${response.home_team_id}.png" alt="" />
    </div>
  `);

  const teamAwayInfo = $(".team.away.info");
  teamAwayInfo.empty();
  teamAwayInfo.append(`
    <div class="emb">
      <img src="//6ptotvmi5753.edge.naverncp.com/KBO_IMAGE/KBOHome/resources/images/emblem/regular/2022/${response.away_team_id}.png" alt="" />
    </div>
    <div class="score">${response.away_team_record}</div>
    <div class="name" style="color: ${response.away_team_color};">${response.away_team_full_name}</div>
  `);
}

function updatePlayerRank(response) {
  const matchBox = $(".match-box");
  matchBox.empty();
  matchBox.append(`
    <span class="match-box-title">장소</span>
    <span class="match-box-txt">${response.stadium_name}</span>
    <span class="match-box-title">경기일자</span>
    <span class="match-box-txt">${response.game_date}</span>
    <span class="match-box-title">방송중계</span>
    <span class="match-box-txt">${response.tv_channel}</span>
  `);
}

function updateMatchGraph(response) {
  createPie('graph-all-match-left', `${response.overall_vs_record[0] + response.overall_vs_record[1] + response.overall_vs_record[2]}<br/>GAME`,
    [
      { name: `${response.home_team_full_name} 승`, y: response.overall_vs_record[0], color: response.home_team_color },
      { name: '무', y: response.overall_vs_record[1], color: '#666666' },
      { name: `${response.away_team_full_name} 승`, y: response.overall_vs_record[2], color: response.away_team_color }
    ]
  );

  createColumn('graph-all-match-right', '', ['득점'],
    [
      { name: response.away_team_full_name, data: [response.overall_vs_record[4]], color: response.away_team_color },
      { name: response.home_team_full_name, data: [response.overall_vs_record[3]], color: response.home_team_color }
    ]
  );

  createPie('graph-match-left', `${response.season_vs_record[0] + response.season_vs_record[1] + response.season_vs_record[2]}<br/>GAME`,
    [
      { name: `${response.home_team_full_name} 승`, y: response.season_vs_record[0], color: response.home_team_color },
      { name: '무', y: response.season_vs_record[1], color: '#666666' },
      { name: `${response.away_team_full_name} 승`, y: response.season_vs_record[2], color: response.away_team_color }
    ]
  );

  createColumn('graph-match-right', '', ['득점'],
    [
      { name: response.away_team_full_name, data: [response.season_vs_record[4]], color: response.away_team_color },
      { name: response.home_team_full_name, data: [response.season_vs_record[3]], color: response.home_team_color }
    ]
  );
}

function updateMatchList(response) {
  const matchList = $(".match-list");
  matchList.empty();
  response.recent_match_results.forEach(match => {
    const li = `
      <li>
        <span class="match-name away-name" style="color: ${response.away_team_color};">${match.away_team_name}</span>
        <span class="match-score away-score" style="background: ${response.away_team_color};">${match.away_team_score}</span>
        <span class="match-date">${match.game_date}</span>
        <span class="match-score home-score" style="background: ${response.home_team_color};">${match.home_team_score}</span>
        <span class="match-name home-name" style="color: ${response.home_team_color};">${match.home_team_name}</span>
      </li>
    `;
    matchList.append(li);
  });
}

function updateStats(response) {
  createButterflyBar('graph-stat-left-away', 'graph-stat-left-home', '',
    response.columns.slice(0, 4),
    [{
      name: response.away_team_full_name,
      data: response.away_team_stats.slice(0, 4),
      color: response.away_team_color
    }], [{
      name: response.home_team_full_name,
      data: response.home_team_stats.slice(0, 4),
      color: response.home_team_color
    }]
  );

  createButterflyBar('graph-stat-right-away', 'graph-stat-right-home', '',
    response.columns.slice(4, 8),
    [{
      name: response.away_team_full_name,
      data: response.away_team_stats.slice(4, 8),
      color: response.away_team_color
    }], [{
      name: response.home_team_full_name,
      data: response.home_team_stats.slice(4, 8),
      color: response.home_team_color
    }]
  );
}
