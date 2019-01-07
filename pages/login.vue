<template>
	<v-layout
	 align-center
	 justify-center
	 full-width
	>
		<v-flex
		 xs12
		 sm8
		 md3
		 xl2
		>
			<v-card class="elevation-12">
				<v-toolbar
				 dark
				 color="primary"
				>
					<v-toolbar-title>Login form</v-toolbar-title>
					<v-spacer></v-spacer>
				</v-toolbar>
				<v-card-text>
					<v-form>
						<!-- username -->
						<v-text-field
						 v-validate="'required'"
						 data-vv-name="username"
						 :error="errors.has('username')"
						 :error-messages="errors.collect('username')"
						 :disabled="isLoading"
						 v-model="username"
						 autocomplete="off"
						 prepend-icon="person"
						 name="username"
						 label="Login"
						 type="text"
						 @keydown.enter="login"
						>
						</v-text-field>
						<!-- password -->
						<v-text-field
						 v-validate="'required'"
						 data-vv-name="password"
						 :error="errors.has('password')"
						 :error-messages="errors.collect('password')"
						 :disabled="isLoading"
						 v-model="password"
						 autocomplete="off"
						 prepend-icon="lock"
						 name="password"
						 label="Password"
						 type="password"
						 @keydown.enter="login"
						>
						</v-text-field>
					</v-form>
				</v-card-text>
				<v-card-actions>
					<v-spacer></v-spacer>
					<v-btn
					 ref="loginButton"
					 color="primary"
					 :loading="isLoading"
					 @click.stop="login"
					>Login</v-btn>
				</v-card-actions>
			</v-card>
		</v-flex>
	</v-layout>
</template>

<script>
export default {
	data() {
		return {
			username: '',
			password: '',
			isLoading: false
		};
	},
	redirect() {
		return (
			this.$route.query.redirect &&
			decodeURIComponent(this.$route.query.redirect)
		);
	},
	methods: {
		async login() {
			let vm = this;
			vm.$auth.loginWith('local', {
				data: {
					username: vm.username,
					password: vm.password
				}
			});
		}
	},
	layout: 'fullpage'
};
</script>
