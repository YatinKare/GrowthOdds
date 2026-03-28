<script lang="ts">
	type NavLabel = 'Home' | 'Actions' | 'Experiments';
	type IconName = 'dashboard' | 'actions' | 'experiments' | 'notifications' | 'settings';
	type NavItem = {
		label: NavLabel;
		icon: IconName;
		href: string;
		active?: boolean;
	};

	let { activeItem = 'Home' }: { activeItem?: NavLabel } = $props();

	const profileImage =
		'https://lh3.googleusercontent.com/aida-public/AB6AXuB5f0msn_ts-N8uqykhCiSmY7nCvduNGKaAOMnxA2xmKVyrljuPeQUufIG3mybPvhVW14cxaH2W4P0xOydEo0lTGj4XZxsx8y_CjIvc15jA1ga7smYIsAV7RGBVdL9KLpElh7j_7fq0JHGweBU_VV4m6malxmRwF8JUc_gHaxQein14duB6T5_PBuIKoqSOZGCNvFyVwapXzthKXrlweScPIolbkkBIaAACNhLIYy7wjg3zHxISJb93vy8y-kcPT35HjOjzt5wTwI-2';

	const navItems = $derived([
		{ label: 'Home', icon: 'dashboard', href: '/dashboard', active: activeItem === 'Home' },
		{ label: 'Actions', icon: 'actions', href: '/actions', active: activeItem === 'Actions' },
		{
			label: 'Experiments',
			icon: 'experiments',
			href: '/experiements',
			active: activeItem === 'Experiments'
		}
	] satisfies NavItem[]);

	const iconPaths: Record<IconName, string[]> = {
		dashboard: [
			'M4.75 4.75h5.5v5.5h-5.5z',
			'M13.75 4.75h5.5v5.5h-5.5z',
			'M4.75 13.75h5.5v5.5h-5.5z',
			'M13.75 13.75h5.5v5.5h-5.5z'
		],
		actions: [
			'M6 12c0-3.314 2.686-6 6-6 2.376 0 4.43 1.38 5.402 3.384',
			'M18 12c0 3.314-2.686 6-6 6-2.376 0-4.43-1.38-5.402-3.384',
			'M16.75 5.75 17.75 9.25 14.25 10.25',
			'M7.25 18.25 6.25 14.75 9.75 13.75'
		],
		experiments: [
			'M9 4.75v4.5l-3.5 6.25A3 3 0 0 0 8.12 20h7.76a3 3 0 0 0 2.62-4.5L15 9.25v-4.5',
			'M8.25 4.75h7.5',
			'M9.25 13.5h5.5'
		],
		notifications: [
			'M12 5.25a4 4 0 0 0-4 4v2.02c0 .72-.2 1.425-.578 2.038l-1.172 1.9h11.5l-1.172-1.9A3.89 3.89 0 0 1 16 11.27V9.25a4 4 0 0 0-4-4Z',
			'M10.25 18a1.75 1.75 0 0 0 3.5 0'
		],
		settings: [
			'M12 8.25a3.75 3.75 0 1 0 0 7.5 3.75 3.75 0 0 0 0-7.5Z',
			'M12 3.75v2.5',
			'M12 17.75v2.5',
			'M20.25 12h-2.5',
			'M6.25 12h-2.5',
			'M17.834 6.166 16.066 7.934',
			'M7.934 16.066 6.166 17.834',
			'M17.834 17.834 16.066 16.066',
			'M7.934 7.934 6.166 6.166'
		]
	};
</script>

<header class="fixed inset-x-0 top-0 z-40 border-b border-black/5 bg-white/80 backdrop-blur-xl">
	<div class="mx-auto flex h-20 max-w-7xl items-center justify-between px-6 md:px-8">
		<div class="flex shrink-0 items-center gap-3">
			<div class="hidden sm:block">
				<p
					class="font-display text-lg font-extrabold tracking-[0.35em] text-[var(--color-primary)] uppercase"
				>
					GrowthOdds
				</p>
			</div>
		</div>

		<nav class="flex items-center gap-1 rounded-full bg-white/60 p-1 md:gap-2">
			{#each navItems as item (item.label)}
				<a
					href={item.href}
					aria-current={item.active ? 'page' : undefined}
					class={[
						'inline-flex items-center gap-2 rounded-full px-3 py-2 text-sm transition-colors md:px-4',
						item.active
							? 'bg-[var(--color-primary-fixed)] font-semibold text-[var(--color-primary)]'
							: 'text-black/45 hover:text-[var(--color-primary-soft)]'
					]}
				>
					<span
						class={[
							'inline-flex h-8 w-8 items-center justify-center rounded-full',
							item.active
								? 'bg-white text-[var(--color-primary)]'
								: 'bg-[var(--color-surface-low)] text-black/55'
						]}
					>
						<svg
							viewBox="0 0 24 24"
							fill="none"
							stroke="currentColor"
							stroke-width="1.65"
							stroke-linecap="round"
							stroke-linejoin="round"
							class="h-4 w-4"
							aria-hidden="true"
						>
							{#each iconPaths[item.icon] as path (`${item.icon}-${path}`)}
								<path d={path}></path>
							{/each}
						</svg>
					</span>
					<span class="font-display text-sm font-bold">{item.label}</span>
				</a>
			{/each}
		</nav>

		<div class="flex items-center gap-3 md:gap-4">
			<div
				class="hidden items-center gap-2 rounded-full bg-[var(--color-surface-low)] px-3 py-1.5 lg:flex"
			>
				<span class="h-2 w-2 rounded-full bg-emerald-500"></span>
				<span class="text-xs font-semibold text-[var(--color-foreground)]">Connected</span>
			</div>

			<button
				type="button"
				aria-label="Notifications"
				class="inline-flex h-10 w-10 items-center justify-center rounded-full text-black/50 transition-colors hover:bg-[var(--color-surface-low)] hover:text-[var(--color-primary)]"
			>
				<svg
					viewBox="0 0 24 24"
					fill="none"
					stroke="currentColor"
					stroke-width="1.65"
					stroke-linecap="round"
					stroke-linejoin="round"
					class="h-5 w-5"
					aria-hidden="true"
				>
					{#each iconPaths.notifications as path (`notifications-${path}`)}
						<path d={path}></path>
					{/each}
				</svg>
			</button>

			<button
				type="button"
				aria-label="Settings"
				class="inline-flex h-10 w-10 items-center justify-center rounded-full text-black/50 transition-colors hover:bg-[var(--color-surface-low)] hover:text-[var(--color-primary)]"
			>
				<svg
					viewBox="0 0 24 24"
					fill="none"
					stroke="currentColor"
					stroke-width="1.65"
					stroke-linecap="round"
					stroke-linejoin="round"
					class="h-5 w-5"
					aria-hidden="true"
				>
					{#each iconPaths.settings as path (`settings-${path}`)}
						<path d={path}></path>
					{/each}
				</svg>
			</button>

			<button
				type="button"
				aria-label="Profile"
				class="h-10 w-10 overflow-hidden rounded-full border border-black/8 shadow-sm transition-transform hover:-translate-y-0.5"
			>
				<img src={profileImage} alt="User profile" class="h-full w-full object-cover" />
			</button>
		</div>
	</div>
</header>
