<template>
  <v-layout
    align-center
    justify-center
    full-width
    fill-height
  >
    <v-flex
      xs12
      sm8
      md3
      xl2
      fill-height
      align-content-center
    >
      <div>
        <h1 v-if="error.statusCode === 404">Page not found custom</h1>
        <h1 v-else>An error occurred</h1>
        {{error}}
        <nuxt-link to="/">Home page</nuxt-link>
      </div>
    </v-flex>
  </v-layout>

</template>

<script>
export default {
	props: ['error'],
};
</script>
