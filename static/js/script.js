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

      
      craetePie('graph-all-match-left', '<span>172<br/>GAME</span>',
        [
          { name: `${response.HOME_NM} 승`, y: 65, color: response.HOME_COLOR },
          { name: '무', y: 49, color: '#666666' },
          { name: `${response.AWAY_NM} 승`, y: 63, color:response.AWAY_COLOR },
        ]
      );

      createColumn('graph-all-match-right', '', ['득점'],
        [
          { name: response.AWAY_NM, data: [45], color: response.AWAY_COLOR },
          { name: response.HOME_NM, data: [31], color: response.HOME_COLOR }
        ]
      );

      craetePie('graph-match-left', '<span>10<br/>GAME</span>',
        [
          { name: `${response.HOME_NM} 승`, y: 4, color: response.HOME_COLOR },
          { name: '무', y: 3, color: '#666666' },
          { name: `${response.AWAY_NM} 승`, y: 3, color: response.AWAY_COLOR },
        ]
      );

      createColumn('graph-match-right', '', ['득점'],
        [
          { name: response.AWAY_NM, data: [45], color: response.AWAY_COLOR },
          { name: response.HOME_NM, data: [31], color: response.HOME_COLOR }
        ]
      );

      craeteButterflyBar('graph-stat-leftL', 'graph-stat-leftR', '',
        ['안타', '홈런', '타점', '득점'],
        [{
          data: [27, 148, 91, 6.298],
          color: response.AWAY_COLOR
        }], [{
          data: [14, 58, 121, 11],
          color: response.HOME_COLOR
        }]
      );

      craeteButterflyBar('graph-stat-rightL', 'graph-stat-rightR', '',
        ['볼넷', '도루', '삼진', '장타'],
        [{
          data: [27, 148, 91, 6.298],
          color: response.AWAY_COLOR
        }], [{
          data: [14, 58, 121, 11],
          color: response.HOME_COLOR
        }]
      );

      const matchList = $(".match-list");
      matchList.empty();
      response.matches.forEach(match => {
        const li = `
            <li>
              <span class="match-name away-name" style="color: ${match.away_color};">${match.away}</span>
              <span class="match-score away-score" style="background: ${match.away_color};">${match.away_score}</span>
              <span class="match-date">${match.date}</span>
              <span class="match-score home-score" style="background: ${match.home_color};">${match.home_score}</span>
              <span class="match-name home-name" style="color: ${match.home_color};">${match.home}</span>
            </li>
          `;
        matchList.append(li);
      });
    },
    error: function (e) {
      console.error(e);
    }
  });
});