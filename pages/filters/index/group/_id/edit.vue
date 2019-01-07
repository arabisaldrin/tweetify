<template>
  <modal title="Create User" width="500">
    <v-form>
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
  async created() {
    const groupId = this.$route.params.id,
      response = await this.$axios.get(`/filter-group/${groupId}`);
    if (response.status == 200) {
      this.formData = response.data;
    }
  },
  methods: {
    async save() {
      const groupId = this.$route.params.id,
        response = await this.$axios.patch(
          `/filter-group/${groupId}/`,
          this.formData
        );
      if (response.status == 200) {
        this.$bus.$emit("update-group", response.data);
        this.$router.go(-1);
      }
    }
  }
};
</script>

<style>
</style>
