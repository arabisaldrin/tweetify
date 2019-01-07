<template>
  <v-container fluid grid-list-lg>
    <v-layout row wrap></v-layout>
    <v-toolbar flat color="white">
      <v-toolbar-title>Stream Filters</v-toolbar-title>
      <v-divider class="mx-2" inset vertical></v-divider>
      <v-spacer></v-spacer>
      <v-btn color="blue" to="add" class="white--text">Add Group</v-btn>
    </v-toolbar>
    <v-data-table :headers="headers" :items="items" hide-actions class="elevation-1" item-key="pk">
      <template slot="items" slot-scope="props">
        <tr @click="props.expanded = !props.expanded">
          <td>{{props.item.pk}}</td>
          <td>{{props.item.name}}</td>
          <td>{{props.item.description}}</td>
          <td align="center" @click.stop>
            <v-btn icon color="white" :to="`group/${props.item.pk}/items/add`">
              <v-icon small color="green">mdi mdi-plus</v-icon>
            </v-btn>
            <v-btn icon color="white" :to="`group/${props.item.pk}/edit`">
              <v-icon small color="blue">mdi mdi-pencil</v-icon>
            </v-btn>
            <v-btn icon color="white" @click="deleteGroup(props.item)">
              <v-icon small color="red">mdi mdi-delete</v-icon>
            </v-btn>
          </td>
        </tr>
      </template>
      <template slot="expand" slot-scope="props">
        <v-card flat>
          <v-card-text>
            <v-chip
              close
              v-for="item in props.item.items"
              @input="removeItem(item)"
              :key="item.pk"
              color="blue"
              text-color="white"
            >{{item.content}}</v-chip>
          </v-card-text>
        </v-card>
      </template>
    </v-data-table>
    <nuxt-child/>
  </v-container>
</template>
<script>
export default {
  data() {
    return {
      headers: [
        {
          text: "ID",
          value: "pk"
        },
        {
          text: "Name",
          value: "name"
        },
        {
          text: "Description",
          value: "description"
        },
        {
          text: "Actions",
          value: "actions",
          align: "center",
          width: "250px"
        }
      ],
      items: [],
      search: "",
      fab: false
    };
  },
  async created() {
    const resposne = await this.$axios.get("/filter-group");
    this.items = resposne.data.results;
    this.$bus.$on("add-group", e => {
      this.items.push(e);
      this.$bus.$emit("socket-command", "restart");
    });
    this.$bus.$on("update-group", e => {
      const groupIndex = this.items.findIndex(g => g.pk == e.pk);
      this.items.splice(groupIndex, 1, e);
    });
    this.$bus.$on("add-item", e => {
      const group = this.items.find(g => g.pk == e.group);
      group.items.push(e);
      this.$bus.$emit("socket-command", "restart");
    });
  },
  methods: {
    async removeItem(item) {
      const respone = await this.$axios.delete("/filter-item/" + item.pk);
      if (respone.status == 204) {
        const group = this.items.find(e => e.pk == item.group);
        const itemIndex = group.items.findIndex(i => i.pk == item.pk);
        group.items.splice(itemIndex, 1);
        this.$bus.$emit("socket-command", "restart");
        this.$toast.success(
          `Item (${item.content}) from group (${group.name}) has been removed`
        );
      }
    },

    async deleteGroup(group) {
      const response = await this.$axios.delete("/filter-group/" + group.pk);
      if (response.status == 204) {
        const groupIndex = this.items.findIndex(g => g.pk == group.pk);
        this.items.splice(groupIndex, 1);
        this.$toast.success(`Group (${group.name}) has been removed`);
        this.$bus.$emit("socket-command", "restart");
      }
    }
  }
};
</script>
