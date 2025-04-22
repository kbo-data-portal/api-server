$(document).on("click", ".game-cont", function () {
  const gameId = $(this).data("game-id");

  $.ajax({
    url: "/get_match",
    method: "POST",
    contentType: "application/json",
    data: JSON.stringify({ game_id: gameId }),
    success: function (response) {
      const matchBox = $(".match-box");
      matchBox.empty();
      matchBox.append(`
        <span class="match-box-title">장소</span>
        <span class="match-box-txt">${response.S_NM}</span>
        <span class="match-box-title">경기일자</span>
        <span class="match-box-txt">${response.G_DT_TXT}</span>
        <span class="match-box-title">방송중계</span>
        <span class="match-box-txt">${response.TV_IF}</span>
      `);

      const teamHome = $(".team.home.info");
      teamHome.empty();
      teamHome.append(`
        <div class="name" style="color: ${response.HOME_COLOR};">${response.HOME_NM}</div>
        <div class="score">${response.HOME_SCORE}</div>
        <div class="emb">
          <img src="//6ptotvmi5753.edge.naverncp.com/KBO_IMAGE/KBOHome/resources/images/emblem/regular/2022/${response.HOME_ID}.png" alt="" />
        </div>
      `);

      const teamAway = $(".team.away.info");
      teamAway.empty();
      teamAway.append(`
        <div class="emb">
          <img src="//6ptotvmi5753.edge.naverncp.com/KBO_IMAGE/KBOHome/resources/images/emblem/regular/2022/${response.AWAY_ID}.png" alt="" />
        </div>
        <div class="score">${response.AWAY_SCORE}</div>
        <div class="name" style="color: ${response.AWAY_COLOR};">${response.AWAY_NM}</div>
      `);

      craetePie('graph-all-match-left', `<span>${response.OP_SCORE[0] + response.OP_SCORE[1] + response.OP_SCORE[2]}<br/>GAME</span>`,
        [
          { name: `${response.HOME_NM} 승`, y: response.OP_SCORE[0], color: response.HOME_COLOR },
          { name: '무', y: response.OP_SCORE[1], color: '#666666' },
          { name: `${response.AWAY_NM} 승`, y: response.OP_SCORE[2], color: response.AWAY_COLOR },
        ]
      );

      createColumn('graph-all-match-right', '', ['득점'],
        [
          { name: response.AWAY_NM, data: [45], color: response.AWAY_COLOR },
          { name: response.HOME_NM, data: [31], color: response.HOME_COLOR }
        ]
      );

      const matchList = $(".match-list");
      matchList.empty();
      response.MATCH_SCORE.forEach(match => {
        const li = `
            <li>
              <span class="match-name away-name" style="color: ${response.AWAY_COLOR};">${match.AWAY_NM}</span>
              <span class="match-score away-score" style="background: ${response.AWAY_COLOR};">${match.AWAY_SCORE}</span>
              <span class="match-date">${match.G_DT}</span>
              <span class="match-score home-score" style="background: ${response.HOME_COLOR};">${match.HOME_SCORE}</span>
              <span class="match-name home-name" style="color: ${response.HOME_COLOR};">${match.HOME_NM}</span>
            </li>
          `;
        matchList.append(li);
      });

      craetePie('graph-match-left', `<span>${response.SS_OP_SCORE[0] + response.SS_OP_SCORE[1] + response.SS_OP_SCORE[2]}<br/>GAME</span>`,
        [
          { name: `${response.HOME_NM} 승`, y: response.SS_OP_SCORE[0], color: response.HOME_COLOR },
          { name: '무', y: response.SS_OP_SCORE[1], color: '#666666' },
          { name: `${response.AWAY_NM} 승`, y: response.SS_OP_SCORE[2], color: response.AWAY_COLOR },
        ]
      );

      createColumn('graph-match-right', '', ['득점'],
        [
          { name: response.AWAY_NM, data: [45], color: response.AWAY_COLOR },
          { name: response.HOME_NM, data: [31], color: response.HOME_COLOR }
        ]
      );
      
      craeteButterflyBar('graph-stat-leftL', 'graph-stat-leftR', '',
        ['득점', '안타', '홈런', '타점'],
        [{
          name : response.AWAY_NM,
          data: response.A_HITTER_INFO.slice(0, 4),
          color: response.AWAY_COLOR
        }], [{
          name : response.HOME_NM,
          data: response.H_HITTER_INFO.slice(0, 4),
          color: response.HOME_COLOR
        }]
      );

      craeteButterflyBar('graph-stat-rightL', 'graph-stat-rightR', '',
        ['2루타', '3루타', '볼넷', '삼진'],
        [{
          name : response.AWAY_NM,
          data: response.A_HITTER_INFO.slice(4, 8),
          color: response.AWAY_COLOR
        }], [{
          name : response.HOME_NM,
          data: response.H_HITTER_INFO.slice(4, 8),
          color: response.HOME_COLOR
        }]
      );
    },
    error: function (e) {
      console.error(e);
    }
  });
});