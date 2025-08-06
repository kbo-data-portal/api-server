function getMatch(gameId) {
  $.ajax({
    url: "/web/match_info",
    method: "POST",
    contentType: "application/json",
    data: JSON.stringify({ game_id: gameId }),
    success: function (response) {
      $(".stat-button").data("season-id", response.season_id);
      $(".stat-button").data("home-name", response.home_team_name);
      $(".stat-button").data("away-name", response.away_team_name);

      updateMatchBox(response);
      updateTeamInfo(response);
      updateMatchGraph(response);
      updateMatchList(response);

      $(".stat-button.active").trigger("click");
    },
    error: function (e) {
      console.error(e);
    },
  });
}

function getTeamStats(playerType, seasonId, homeName, awayName) {
  $.ajax({
    url: "/web/team_stats",
    method: "POST",
    contentType: "application/json",
    data: JSON.stringify({
      player_type: playerType,
      season_id: seasonId,
      home_name: homeName,
      away_name: awayName,
    }),
    success: function (response) {
      updateStats(response);
    },
    error: function (e) {
      console.error(e);
    },
  });
}

function getTeamPlayers(teamName) {
  $.ajax({
    url: "/web/team_players",
    method: "POST",
    contentType: "application/json",
    data: JSON.stringify({
      team_name: teamName,
    }),
    success: function (response) {
      $(".tbl th").css("background", response.color);

      updateTopPlayer(response.hitter[0], "hitter", ["타율", "득점", "안타"]);
      updatePlayerRank(response.hitter.slice(1, 5), "hitter");
      updateTopPlayer(response.pitcher[0], "pitcher", [
        "평균자책점",
        "승리",
        "탈삼진",
      ]);
      updatePlayerRank(response.pitcher.slice(1, 5), "pitcher");
    },
    error: function (e) {
      console.error(e);
    },
  });
}
