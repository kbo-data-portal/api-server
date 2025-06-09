
const totalPages = Math.ceil($(".game-cont").length / 5)
let currentPage = 1

$(document).ready(function () {
  const today = $(".game-list-n").data("today")

  let firstGame = $(".game-list-n .game-cont").first();
  let page = 0;
  $(".game-list-n .game-cont").each(function () {
    const date = $(this).data("game-id");
    page += 1;

    if (date.startsWith(today)) {
      firstGame = $(this);
      currentPage += Math.round(page / 5);
      return false;
    }
  });
  console.log("First game found:", firstGame, "Current page:", currentPage);

  updateSlider();

  firstGame.addClass("on");
  getMatch(firstGame.data("game-id"));

  getTeamPlayers(NaN);
});

$(document).on("click", ".bx-prev", function (e) {
  e.preventDefault();
  if (currentPage > 1) {
    currentPage--;
    updateSlider();
  }
})

$(document).on("click", ".bx-next", function (e) {
  e.preventDefault();
  if (currentPage < totalPages) {
    currentPage++;
    updateSlider();
  }
})

$(document).on("click", ".game-cont", function () {
  const gameId = $(this).data("game-id");

  $(".game-cont").removeClass("on");
  $(this).addClass("on");
  
  getMatch(gameId);
});

$(document).on("click", ".stat-button", function () {
  const seasonId = $(this).data("season-id");
  const homeName = $(this).data("home-name");
  const awayName = $(this).data("away-name");
  const playerType = $(this).data("player-type");

  $(".stat-button").removeClass("active");
  $(this).addClass("active");

  getTeamStats(playerType, seasonId, homeName, awayName);
});


$(document).on("click", ".rank-info", function () {
  if ($(this).hasClass('on')) {
    $(".rank-info").removeClass("on");
    getTeamPlayers(NaN);
  }
  else {
    $(".rank-info").removeClass("on");
    $(this).addClass("on");

    const teamName = $(this).data("team-name");
    getTeamPlayers(teamName);
  }
});