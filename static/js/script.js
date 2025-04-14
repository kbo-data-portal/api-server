craetePie('game-info-top-graphLeft', '<span>172<br/>GAME</span>',
  [
    { name: '패', y: 63, color: '#000000' },
    { name: '무효', y: 49, color: '#666666' },
    { name: '승', y: 65, color: '#0072CE' },
  ]);

createColumn('game-info-top-graphCenter', '', ['GOAL'],
  [
    { name: '득점', data: [45], color: '#0072CE' },
    { name: '실점', data: [31], color: '#000000' }
  ]
);


craeteButterflyBar('game-info-top-graphRight', 'game-info-top-graphRight2', '',
  ['홈런', '안타', '타점', '득점권 타율'],
  [{
    data: [27, 148, 91, 6.298],
    color: '#0072CE',
  }], [{
    data: [14, 58, 121, 11],
    color: '#000000',
  }]);
