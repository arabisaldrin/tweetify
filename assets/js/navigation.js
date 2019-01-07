export default [
	{ title: 'Dashboard', icon: 'dashboard', to: '/dashboard' },
	{
		title: 'Administration',
		icon: 'security',
		prefix: '/administration',
		children: [{ title: 'System Users', icon: 'people', to: '/users/' }]
	},
	{ title: 'About', icon: 'question_answer', to: '/about' }
];
