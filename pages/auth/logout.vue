<template>

</template>

<script>
export default {
	fetch({ app, req, store }) {
		store.commit('setToken', null);
		app.$cookies.remove('token');
	}
};
</script>

<style>
</style>
