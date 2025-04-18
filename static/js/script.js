craetePie('graph-all-match-left', '<span>172<br/>GAME</span>',
  [
    { name: 'KT 위즈 승', y: 65, color: homeColor },
    { name: '무', y: 49, color: '#666666' },
    { name: '삼성 라이온즈 승', y: 63, color: awayColor },
  ]
);

createColumn('graph-all-match-right', '', ['득점'],
  [
    { name: '삼성 라이온즈', data: [45], color: awayColor },
    { name: 'KT 위즈', data: [31], color: homeColor }
  ]
);

craetePie('graph-match-left', '<span>10<br/>GAME</span>',
  [
    { name: 'KT 위즈 승', y: 4, color: homeColor },
    { name: '무', y: 3, color: '#666666' },
    { name: '삼성 라이온즈 승', y: 3, color: awayColor },
  ]
);

createColumn('graph-match-right', '', ['득점'],
  [
    { name: '삼성 라이온즈', data: [45], color: awayColor },
    { name: 'KT 위즈', data: [31], color: homeColor }
  ]
);

craeteButterflyBar('graph-stat-leftL', 'graph-stat-leftR', '',
  ['홈런', '안타', '타점', '득점권 타율'],
  [{
    data: [27, 148, 91, 6.298],
    color: awayColor
  }], [{
    data: [14, 58, 121, 11],
    color: homeColor
  }]
);

craeteButterflyBar('graph-stat-rightL', 'graph-stat-rightR', '',
  ['홈런', '안타', '타점', '득점권 타율'],
  [{
    data: [27, 148, 91, 6.298],
    color: awayColor
  }], [{
    data: [14, 58, 121, 11],
    color: homeColor
  }]
);