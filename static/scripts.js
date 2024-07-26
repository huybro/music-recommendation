async function getRecommendations() {
    const spfUrl = document.getElementById('spotify-url').value
    const songName = document.getElementById('song-name').value
    document.getElementById('recommendations').innerHTML = ''
    if (!spfUrl) {
        alert('Please enter a Spotify URL');
        return;
    }
    playlist_id = extractPlaylistId(spfUrl)
    console.log(playlist_id)
    if (!playlist_id) {
        alert('Invalid Spotify URL');
        return;
    }
    try {
        const response =  await fetch('http://127.0.0.1:5000/recommend', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ spotify_id: playlist_id,song_name: songName})
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const recommendations = await response.json();
        displayRecommendations(recommendations);

    } catch (error) {
        console.error('Error fetching recommendations:', error);
        alert('Error fetching recommendations. Please try again later.');
    }
}


function extractPlaylistId(url) {
    const match = url.match(/playlist\/([a-zA-Z0-9]{22})/);
    return match ? match[1] : null;
}

function displayRecommendations(recommendations) {
    const recommendationsDiv = document.getElementById('recommendations');
    recommendationsDiv.innerHTML = '';

    recommendations.forEach(song => {
        const songDiv = document.createElement('div');
        songDiv.className = 'song';

        const songName = document.createElement('h3');
        songName.textContent = song['Track Name'];
        songDiv.appendChild(songName);

        const songArtists = document.createElement('p');
        songArtists.textContent = `Artists: ${song['Artists']}`;
        songDiv.appendChild(songArtists);

        const songAlbum = document.createElement('p');
        songAlbum.textContent = `Album: ${song['Album Name']}`;
        songDiv.appendChild(songAlbum);

        recommendationsDiv.appendChild(songDiv);
    });
}

