<template>
	<v-container>
		<remote-table
		 api="/users"
		 select-all
		 :headers="tableHeaders"
		 :actions="tableActions"
		 item-key="username"
		 ref="table"
		 v-model="selected"
		>
			<template
			 slot="items"
			 slot-scope="props"
			>
				<td>{{props.item.last_name}}</td>
				<td>{{props.item.first_name}}</td>
				<td>{{props.item.email}}</td>
				<td
				 v-for="key in ['is_superuser', 'is_staff', 'is_active']"
				 :key="key"
				>
					<v-icon v-if="props.item[key]">check</v-icon>
					<v-icon
					 v-else
					 table
					>close</v-icon>
				</td>
				<td>
					<v-icon @click="$router.push(props.item.pk+'/edit')">edit</v-icon>
					<v-icon @click="deleteUser(props.item)">delete</v-icon>
				</td>
				<context-menu>
					<context-menu-item
					 @click="$router.push(props.item.pk+'/edit')"
					 text="Edit"
					 icon="edit"
					/>
					<context-menu-item
					 @click="deleteUser(props.item)"
					 text="Delete"
					 icon="delete"
					/>
				</context-menu>
			</template>
			<template slot="controls">
				<v-btn
				 outline
				 color="primary"
				 to="add"
				>Add</v-btn>
			</template>
		</remote-table>
		<nuxt-child />
	</v-container>
</template>

<script>
require('~/assets/js/util');
export default {
	data() {
		return {
			selected: [],
			tableHeaders: [
				{
					text: 'Lastname',
					value: 'last_name'
				},
				{
					text: 'Firstname',
					value: 'first_name'
				},
				{
					text: 'Email',
					value: 'email'
				},
				{
					text: 'Admin',
					value: 'is_superuser'
				},
				{
					text: 'Staff',
					value: 'is_staff'
				},
				{
					text: 'Active',
					value: 'is_active'
				},
				{
					text: 'Actions'
				}
			],
			tableActions: [
				{
					key: 'delete',
					text: 'Delete',
					async callback() {
						const respone = await this.$axios.post('/users/mdelete/', {
							ids: this.selected.map(e => e.pk)
						});
						if (respone.status == 200) {
							const ids = selected.map(e => e.pk);
							const items = this.getItems();
							ids.forEach(id => {
								const index = items.findIndex(e => e.pk == id);
								items.splice(index, 1);
							});
						}
					},
					hide: false
				},
				{
					key: 'activate',
					text: 'Activate',
					callback() {
						this.activateUsers(this.selected, true);
					},
					hide: true
				},
				{
					key: 'deactivate',
					text: 'Deactivate',
					callback() {
						this.activateUsers(this.selected, false);
					},
					hide: true
				}
			]
		};
	},
	mounted() {
		const vm = this;
		vm.$bus.$on('user-added', newUser => {
			const items = this.$refs.table.items;
			items.push(newUser);
		});
		vm.$bus.$on('user-updated', user => {
			const items = this.$refs.table.items;
			const index = items.findIndex(e => e.pk == user.pk);
			items.splice(index, 1, user);
		});
	},
	methods: {
		hideAction(key, flag) {
			const index = this.tableActions.findIndex(e => e.key == key);
			this.tableActions[index].hide = flag;
		},
		async activateUsers(selected, flag) {
			const respone = await this.$axios.post('/users/mactivate/', {
				ids: selected.map(e => e.pk),
				flag
			});
			if (respone.status == 200) {
				selected.forEach(e => (e.is_active = flag));
				const count = respone.data.result;
				this.$toast.success(
					`${count} User${count > 1 ? 's' : ''} has been ${
						flag ? 'Activated' : 'Deactivated'
					}`
				);
			}
		},
		async deleteUser(user) {
			const response = await this.$axios.delete('/users/' + user.pk);
			if (response.status == 204) {
				this.$toast.success('User Deleted');
			}
		},
		getItems() {
			return this.$refs.table.items;
		}
	},
	watch: {
		selected(val) {
			const status = Array.from(new Set(val.map(e => e.is_active)));
			if (status.length == 1) {
				this.hideAction('activate', status[0]);
				this.hideAction('deactivate', !status[0]);
			} else {
				this.hideAction('activate', true);
				this.hideAction('deactivate', true);
			}
		}
	}
};
</script>

