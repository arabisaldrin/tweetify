<template>
	<v-dialog
	 :value="true"
	 v-bind="$attrs"
	 persistent
	>
		<v-card>
			<v-card-title
			 primary-title
			 v-text="title"
			>
			</v-card-title>
			<v-divider></v-divider>

			<v-card-text>
				<slot></slot>
			</v-card-text>

			<v-divider></v-divider>

			<v-card-actions>
				<v-spacer></v-spacer>
				<slot name="actions"></slot>
			</v-card-actions>
		</v-card>
	</v-dialog>
</template>

<script>
export default {
	props: {
		title: {
			type: String,
			default: ''
		}
	}
};
</script>

<style>
</style>
