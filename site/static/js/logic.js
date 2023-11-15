const dataGrid = new gridjs.Grid({
    columns: [ {
        id: 'player_id',
        hidden: true
    }, {
        id: 'player_name',
        name: 'Player Name',
        width: '15%'
    }, {
        id: 'team',
        name: 'Team',
        width: '13%'
    }, {
        id: 'position',
        name: 'Position',
        width: '9%'
    }, {
        id: 'goals',
        name: 'Goals',
        width: '7%'
    }, {
        id: 'assists',
        name: 'Assists',
        width: '7%'
    }, {
        id: 'shots',
        name: 'Shots',
        width: '7%'
    }, {
        id: 'shots_on_goal',
        name: 'Shots On Goal',
        width: '7%'
    }, {
        id: 'saves',
        name: 'Saves',
        width: '7%'
    }, {
        id: 'goals_against',
        name: 'Goals Against',
        width: '7%'
    }, {
        id: 'clean_sheets',
        name: 'Clean Sheets',
        width: '7%'
    }, {
        id: 'yellow_cards',
        name: 'Yellow Cards',
        width: '7%'
    }, {
        id: 'red_cards',
        name: 'Red Cards',
        width: '7%'
    }],
    data: [],
    style: {
        container: {
            'max-height': '400px',
            'overflow-y':'auto',
            'overflow-x': 'auto'
        },
        th: {
            'font-size': '12px',
            'padding': '5px',
            'font-family': 'Arial'
        },
        td: {
            'font-size': '12px',
            'padding': '5px',
            'font-family': 'Arial'
        }
    }
}).render(document.getElementById('playerStatsGrid'));

dataGrid.on('rowClick', (e, row) => selectPlayerData(row, row.cell(0).data));

d3.json('http://127.0.0.1:8000/api/v1.0/leagues').then(function(data) {
    let leagueDropDown = d3.select('#selLeague')

    data.forEach (l => {
        leagueDropDown.append('option').text(l['league']).property('value', l['league_id'])
        
    });

    leagueDropDown.property('selectedIndex', -1)
});

d3.json('http://127.0.0.1:8000/api/v1.0/positions').then(function(data) {
    let positionDropDown = d3.select('#selPosition')

    data.forEach(p => {
        positionDropDown.append('option').text(p['position']).property('value', p['position_id'])
    });

    positionDropDown.property('selectedIndex', -1)
});

function selLeagueChange(leagueId) {
    d3.json(`http://127.0.0.1:8000/api/v1.0/leagues/${leagueId}/teams`).then(function(data) {
        let teamDropDown = d3.select('#selTeam')
        teamDropDown.selectAll('*').remove();
        
        data.forEach(t => {
            teamDropDown.append('option').text(t['team']).property('value', t['team_id'])
        });

        teamDropDown.property('selectedIndex', -1)
    });

    
};

function selTeamChange() {
    selectPlayerStats();
};

function selPositionChange() {
    selectPlayerStats();
};


function selectPlayerStats() {
    let leagueDropDown = d3.select('#selLeague')
    let teamDropDown = d3.select('#selTeam')
    let positionDropDown = d3.select('#selPosition')

    if (leagueDropDown.property('selectedIndex') > -1 && teamDropDown.property('selectedIndex') > -1 && positionDropDown.property('selectedIndex') > -1) {
        let leagueId = leagueDropDown.property('value')
        let teamId = teamDropDown.property('value')
        let positionId = positionDropDown.property('value')
        d3.json(`http://127.0.0.1:8000/api/v1.0/player_stats/${leagueId}/${teamId}/${positionId}`).then(function(data) {
            dataGrid.updateConfig({
                data: data,
                sort: true
            }).forceRender();

        });

        clearSelectedPlayer();


    };
};

function setRowSelected(row) {
    // reset all of the rows to normal
    for (const tr of document.querySelectorAll('tr')) {
        tr.style.fontStyle = 'normal';
        tr.style.fontWeight = 'normal';
    };

    // find the selected row element and style it
    for (const td of document.querySelectorAll("td")) {
        if (td.textContent.includes(row.cell(1).data)) {
          td.parentElement.style.fontStyle = 'italic';
          td.parentElement.style.fontWeight = 'bold';
        }
      };
    
}

function selectPlayerData(row, playerId) {
    setRowSelected(row);

    d3.json(`http://127.0.0.1:8000/api/v1.0/player_data/${playerId}`).then(function(data) {
        let playerImg = d3.select('#playerPhoto')
        if (data[0]['photo_url'] == 'N/A') {
            playerImg.property('src', '/static/img/no_picture.png')
        }
        else {
            playerImg.property('src', data[0]['photo_url']);
        }
        

        d3.select('#playerBirthdate').text(`Birthdate: ${data[0]['birthdate']}`);
        d3.select('#playerHeight').text(`Height (inches): ${data[0]['height']}`);
        d3.select('#playerNumber').text(`Jersey Number: ${data[0]['jersey_number']}`);
        d3.select('#playerNationality').text(`Nationality: ${data[0]['nationality']}`);
        d3.select('#playerWeight').text(`Weight (lbs): ${data[0]['weight']}`);
    });
};

function clearSelectedPlayer() {
    d3.select('#playerPhoto').attr('src', null)
    d3.select('#playerBirthdate').text('');
    d3.select('#playerHeight').text('');
    d3.select('#playerNumber').text('');
    d3.select('#playerNationality').text('');
    d3.select('#playerWeight').text('');
};
