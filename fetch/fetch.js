const buddyList = require('spotify-buddylist')

async function main () {
    const spDcCookie = 'AQACDtT1pV6dAd3vWPY1Z5ovqkKu-KRqzyx-k4JorMU9P7Mt-Vp1qcFQ8BcX19Ilpoj9tXa7unByx4Mhz9QM-dFY5n61eF_ynLwR8oBw6j53_IgH977oj6U9CzCP2-rhhBLvtKoVh3PcOZ6sfu4YK0UwqK1zHXk' 
    
    const response = await buddyList.getWebAccessToken(spDcCookie)
    const friendActivity = await buddyList.getFriendActivity(response.accessToken)

    const result = friendActivity.friends.map(friend => ({
        timestamp: friend.timestamp,
        userName: friend.user.name,
        trackName: friend.track.name,
        albumName: friend.track.album.name,
        artistName: friend.track.artist.name,
        contextName: friend.track.context.name
    }));

    // console.log(JSON.stringify(friendActivity, null, 2));
    // console.log(JSON.stringify(response, null, 2));
    console.log(result);
}

main()