
const totalPages = Math.ceil($(".game-cont").length / 5)
let currentPage = (totalPages + 5) % 10

$(document).ready(function () {
  updateSlider();

  const firstGame = $(".game-list-n .game-cont").eq((currentPage - 1) * 5);
  firstGame.addClass("on");
  getMatch(firstGame.data("game-id"));
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
  const teamName = $(this).data("team-name");
  console.log(teamName);
});