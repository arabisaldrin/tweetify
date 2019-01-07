<template>
	<modal
	 title="Edit User"
	 width="500"
	>
		<v-form>
			<v-text-field
			 v-model="formData.first_name"
			 name="first name"
			 label="First name"
			 v-validate="'required'"
			 :error="errors.has('first name')"
			 :error-messages="errors.first('first name')"
			></v-text-field>
			<v-text-field
			 v-model="formData.last_name"
			 name="last name"
			 label="Last name"
			 v-validate="'required'"
			 :error="errors.has('last name')"
			 :error-messages="errors.first('last name')"
			></v-text-field>
			<v-text-field
			 v-model="formData.username"
			 name="username"
			 label="Username"
			 v-validate="'required'"
			 :error="errors.has('username')"
			 :error-messages="errors.first('username')"
			></v-text-field>
			<v-text-field
			 v-model="formData.email"
			 type="email"
			 name="email"
			 label="Emai"
			 autocomplete="new-password"
			 v-validate="'required|email'"
			 :error="errors.has('email')"
			 :error-messages="errors.first('email')"
			 data-vv-validate-on="blur"
			></v-text-field>
			<v-layout
			 row
			 wrap
			>
				<v-checkbox
				 label="Superuser"
				 v-model="formData.is_superuser"
				></v-checkbox>
				<v-checkbox
				 label="Staff"
				 v-model="formData.is_staff"
				></v-checkbox>
				<v-checkbox
				 label="Active"
				 v-model="formData.is_active"
				></v-checkbox>
			</v-layout>
		</v-form>
		<template slot="actions">
			<v-btn
			 color="primary"
			 flat
			 @click="$router.go(-1)"
			>
				Cancel
			</v-btn>
			<v-btn
			 color="primary"
			 outline
			 @click="save"
			>
				Save
			</v-btn>
		</template>
	</modal>
</template>

<script>
export default {
	data: () => ({
		formData: {}
	}),
	async created() {
		let userId = this.$route.params.id;

		const { data } = await this.$axios.get('/users/' + userId);
		this.formData = data;
	},
	methods: {
		async save() {
			let vm = this,
				userId = vm.$route.params.id;
			const valid = await vm.$validator.validateAll();
			if (valid) {
				vm.$axios
					.patch('/users/' + userId + '/', vm.formData)
					.then(response => {
						if (response.status == 200 && response.data) {
							vm.$toast.success('User successduly updated');
							vm.$bus.$emit('user-updated', response.data);
							vm.$router.go(-1);
						} else {
							vm.$toast.error(
								'Some error occured while trying to update user!'
							);
						}
					})
					.catch(err => {
						vm.$toast.error(response.statusText);
					});
			}
		}
	}
};
</script>
