
const totalPages = Math.ceil($(".game-cont").length / 5)
let currentPage = (totalPages + 5) % 10

$(document).ready(function () {
  updateSlider()

  const firstGame = $(".game-list-n .game-cont").eq((10 - totalPages) * 5);
  firstGame.addClass("on");
  getMatch(firstGame.data("game-id"));
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

  $(".game-cont").removeClass("on");
  $(this).addClass("on");
  
  getMatch(gameId);
});

$(document).on("click", ".stat-button", function () {
  const seasonId = $(this).data("season-id");
  const homeId = $(this).data("home-id");
  const awayId = $(this).data("away-id");
  const playerType = $(this).data("player-type");

  $(".stat-button").removeClass("active");
  $(this).addClass("active");

  getTeamStats(playerType, seasonId, homeId, awayId);
});
