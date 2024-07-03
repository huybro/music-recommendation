async function getRecommendations() {
    const spfUrl = document.getElementById('spotify-url').value
    if (!spotifyUrl) {
        alert('Please enter a Spotify URL');
        return;
    }
    playlist_id = extractPlaylistId(spfUrl)
    if (!spotifyId) {
        alert('Invalid Spotify URL');
        return;
    }
    try {
        const reponse =  await fetch('http://your-api-url/recommend', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ spotify_id: playlist_id, num_recommendations: 5 })
        });
    }
}


    function extractPlaylistId(url) {
        const match = url.match(/playlist\/([a-zA-Z0-9]{22})/);
        return match ? match[1] : null;
    }

