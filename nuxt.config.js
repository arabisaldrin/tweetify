const pkg = require("./package");
const nodeExternals = require("webpack-node-externals");

module.exports = {
	/* server: {
		port: 3000, // default: 3000
		host: '0.0.0.0' // default: localhost
	}, */
	mode: "universal",
	router: {
		middleware: ["auth"]
	},
	/*
  ** Headers of the page
  */
	head: {
		title: pkg.name,
		meta: [
			{ charset: "utf-8" },
			{
				name: "viewport",
				content: "width=device-width, initial-scale=1"
			},
			{
				hid: "description",
				name: "description",
				content: pkg.description
			}
		],
		link: [
			{ rel: "icon", type: "image/x-icon", href: "/favicon.ico" },
			{
				rel: "stylesheet",
				href:
					"https://fonts.googleapis.com/css?family=Roboto:300,400,500,700|Material+Icons"
			}
		]
	},

	/*
	** Customize the progress-bar color
	*/
	loading: { color: "#fff" },

	/*
	** Global CSS
	*/
	css: ["~/assets/style/app.styl"],

	/*
	** Plugins to load before mounting the App
	*/
	plugins: ["@/plugins/vue", "@/plugins/vuetify", "@/plugins/axios"],

	/*
	** Nuxt.js modules
	*/
	modules: [
		// Doc: https://github.com/nuxt-community/axios-module#usage
		[
			"@nuxtjs/axios",
			{
				baseURL: "http://localhost:8000/api"
			}
		],
		"@nuxtjs/auth",
		"@nuxtjs/proxy",
		"@nuxtjs/toast",
		"nuxt-validate",
		"cookie-universal-nuxt"
	],
	axios: {
		/*  */
	},
	auth: {
		strategies: {
			local: {
				endpoints: {
					login: {
						url: "/auth/token/login/",
						method: "post",
						propertyName: "auth_token"
					},
					user: {
						url: "/auth/me",
						method: "get",
						propertyName: false
					},
					logout: {
						url: "/auth/token/logout",
						method: "post"
					}
				},
				tokenType: "Token"
			}
		},
		plugins: ["~/plugins/auth.js"]
	},
	/**
	 *
	 */
	toast: {
		position: "top-right",
		duration: 2000
	},
	/*
  ** Build configuration
  */
	build: {
		transpile: [/\bvue-echarts\b/, /\bresize-detector\b/],
		/*
    ** You can extend webpack config here
    */
		extend(config, { isServer }) {
			if (isServer) {
				config.externals = [
					nodeExternals({
						// default value for `whitelist` is
						// [/es6-promise|\.(?!(?:js|json)$).{1,5}$/i]
						whitelist: [
							/es6-promise|\.(?!(?:js|json)$).{1,5}$/i,
							/^vue-echarts/
						]
					})
				];
			}
		}
	}
};
