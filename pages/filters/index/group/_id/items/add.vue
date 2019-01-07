<template>
  <modal title="Create User" width="500">
    <v-form @submit.prevent="save">
      <v-text-field
        v-model="formData.content"
        name="Content"
        label="Content"
        v-validate="'required'"
        :error="errors.has('Content')"
        :error-messages="errors.first('Content')"
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
        group: vm.$route.params.id
      },
      group: {}
    };
  },
  async created() {
    const response = await this.$axios.get(
      "/filter-group/" + this.formData.group
    );
    if ((response.status = 200)) {
      this.group = response.data;
    }
  },
  methods: {
    async save() {
      const response = await this.$axios.post("/filter-item/", this.formData);
      if (response.status == 201) {
        this.$bus.$emit("add-item", response.data);
        this.$toast.success(
          `Item ${this.formData.content} has beend added to ${this.group.name}`
        );
        this.$router.go(-1);
      }
    }
  }
};
</script>