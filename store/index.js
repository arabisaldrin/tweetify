import Vuex from "vuex";

const store = () => {
	return new Vuex.Store({
		state: () => ({
			tweets: [],
			streaming: false,
			socketConnected: false,
			tweetReceived: false
		}),
		mutations: {
			onTweet(state, tweet) {
				state.tweets.unshift(tweet);
				if (!state.streaming) state.streaming = true;
			},
			setStreamingStatus(state, flag) {
				state.streaming = flag;
			},
			setSocketConnected(state, flag) {
				state.socketConnected = flag;
			},
			tweetReceived(state) {
				state.tweetReceived = true;
			}
		}
	});
};

export default store;
