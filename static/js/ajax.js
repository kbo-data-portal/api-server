function getMatch(gameId) {
  $.ajax({
    url: "/get_match",
    method: "POST",
    contentType: "application/json",
    data: JSON.stringify({ game_id: gameId }),
    success: function (response) {
      $('.stat-button').data('season-id', response.season_id);
      $('.stat-button').data('home-name', response.home_team_name);
      $('.stat-button').data('away-name', response.away_team_name);

      updateMatchBox(response);
      updateTeamInfo(response);
      updateMatchGraph(response);
      updateMatchList(response);

      $(".stat-button.active").trigger("click");
    },
    error: function (e) {
      console.error(e);
    }
  });
}

function getTeamStats(playerType, seasonId, homeName, awayName) {
  $.ajax({
    url: "/get_team_stats",
    method: "POST",
    contentType: "application/json",
    data: JSON.stringify({
      player_type: playerType,
      season_id: seasonId,
      home_name: homeName,
      away_name: awayName
    }),
    success: function (response) {
      updateStats(response);
    },
    error: function (e) {
      console.error(e);
    }
  });
}
