import querystring from "querystring";

export default ({ $axios, store }) => {
	$axios.onError(error => {
		return Promise.reject(error.response);
	});
};
