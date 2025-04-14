craetePie('game-info-top-graphLeft', '<span>172<br/>GAME</span>', 
[
    { name: '패', y: 63, color: '#8B0000' },
    { name: '무효', y: 49, color: '#7D91A5' },
    { name: '승', y: 65, color: '#002063' },
]);

createColumn('game-info-top-graphCenter', '', ['GOAL'], [
    { name: '득점', data: [45], color: '#FF6600' },
    { name: '실점', data: [31] }
]
);

createBar('game-info-top-graphRight', '', 
    ['홈런', '안타', '타점', '득점권 타율'], [27, 148, 91, 6.298], true);
    
createBar('game-info-top-graphRight2', '', 
    ['홈런', '안타', '타점', '득점권 타율'], [14, 58, 121, 11], false);
