<template>
  <modal title="Create User" width="500">
    <v-form @submit.prevent="save">
      <v-text-field
        v-model="formData.name"
        name="Group Name"
        label="Group Name"
        v-validate="'required'"
        :error="errors.has('Group Name')"
        :error-messages="errors.first('Group Name')"
      ></v-text-field>
      <v-text-field
        v-model="formData.description"
        name="Description"
        label="Description"
        v-validate="'required'"
        :error="errors.has('Description')"
        :error-messages="errors.first('Description')"
      ></v-text-field>
    </v-form>
    <template slot="actions">
      <v-btn color="primary" flat @click="$router.go(-1)">Cancel</v-btn>
      <v-btn color="primary" outline @click="save">Save</v-btn>
    </template>
  </modal>
</template>

<script>
export default {
  data() {
    let vm = this;
    return {
      formData: {
        user: vm.$auth.user.id
      }
    };
  },
  methods: {
    async save() {
      const response = await this.$axios.post("/filter-group/", this.formData);
      if (response.status == 201) {
        this.$bus.$emit("add-group", response.data);
        this.$router.go(-1);
      }
    }
  }
};
</script>

<style>
</style>
