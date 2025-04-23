
const totalPages = Math.ceil($(".game-cont").length / 5)
let currentPage = 1

$(document).ready(function () {
  updateSlider()
});

$(document).on("click", ".bx-prev", function (e) {
  e.preventDefault()
  if (currentPage > 1) {
    currentPage--
    updateSlider()
  }
})

$(document).on("click", ".bx-next", function (e) {
  e.preventDefault()
  if (currentPage < totalPages) {
    currentPage++
    updateSlider()
  }
})

$(document).on("click", ".game-cont", function () {
  const gameId = $(this).data("game-id");

  $.ajax({
    url: "/get_match",
    method: "POST",
    contentType: "application/json",
    data: JSON.stringify({ game_id: gameId }),
    success: function (response) {
      $('.stat-button').data('season-id', response.season_id);
      $('.stat-button').data('home-id', response.home_team_id);
      $('.stat-button').data('away-id', response.away_team_id);

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
});

$(document).on("click", ".stat-button", function () {
  const seasonId = $(this).data("season-id");
  const homeId = $(this).data("home-id");
  const awayId = $(this).data("away-id");
  const playerType = $(this).data("player-type");

  $(".stat-button").removeClass("active");
  $(this).addClass("active");

  $.ajax({
    url: "/get_team_stats",
    method: "POST",
    contentType: "application/json",
    data: JSON.stringify({
      player_type: playerType,
      season_id: seasonId,
      home_id: homeId,
      away_id: awayId
    }),
    success: function (response) {
      updateStats(response);
    },
    error: function (e) {
      console.error(e);
    }
  });
});
