<template>
	<modal
	 title="Create User"
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
			<!-- <v-text-field
			 v-model="formData.password"
			 type="password"
			 name="password"
			 label="Password"
			 autocomplete="new-password"
			 v-validate="'required'"
			 :error="errors.has('password')"
			 :error-messages="errors.first('password')"
			 ref="password"
			></v-text-field>
			<v-text-field
			 v-model="tempData.confirmPassword"
			 type="password"
			 name="confirm password"
			 label="Confirm Password"
			 autocomplete="new-password"
			 v-validate="'required|confirmed:password'"
			 :error="errors.has('confirm password')"
			 :error-messages="errors.first('confirm password')"
			></v-text-field> -->
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
				 :value="true"
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
		formData: {},
		tempData: {}
	}),
	methods: {
		async save() {
			let vm = this;
			const valid = await vm.$validator.validateAll();
			if (valid) {
				vm.$axios
					.post('/users/', vm.formData)
					.then(response => {
						if (response.status == 201 && response.data) {
							vm.$toast.success('User successduly created');
							vm.$bus.$emit('user-added', response.data);
							vm.$router.go(-1);
						} else {
							vm.$toast.error('Some error occured while trying to creat user!');
						}
					})
					.catch(err => {
						if (err.status == 409) {
							vm.errors.add({
								field: 'username',
								msg: 'Username already in used!'
							});
						}
					});
			}
		}
	}
};
</script>
