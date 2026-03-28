<script lang="ts">
	import AppNavbar from '$lib/components/AppNavbar.svelte';
	import type { PageProps } from './$types';

	type IconName = 'chevron' | 'spark' | 'launch' | 'reply' | 'split';

	type MetricCard = {
		label: string;
		value: string;
		delta: string;
		eyebrow: string;
	};

	type TimelineItem = {
		title: string;
		description: string;
		date: string;
		status: string;
		icon: IconName;
		active?: boolean;
	};

	let { params }: PageProps = $props();

	const metrics: MetricCard[] = [
		{
			label: 'Total Clicks',
			value: '14,802',
			delta: '+12%',
			eyebrow: 'Across both active variants'
		},
		{
			label: 'Unique Users',
			value: '8,440',
			delta: '+4.2%',
			eyebrow: 'Qualified ICP responders'
		}
	];

	const insightTags = ['Direct style', 'Urgency hooks', 'Data-first'];

	const timeline: TimelineItem[] = [
		{
			title: 'Initial Post Deployment',
			description: 'Targeted at Series A founders in FinTech',
			date: 'Oct 12',
			status: 'Completed',
			icon: 'launch'
		},
		{
			title: 'Follow-up Thread Reply',
			description: 'Automated response based on high engagement',
			date: 'Oct 14',
			status: 'Completed',
			icon: 'reply'
		},
		{
			title: 'A/B Test Variant B Launch',
			description: 'Testing aggressive vs subtle CTAs',
			date: 'Oct 15',
			status: 'Active',
			icon: 'split',
			active: true
		}
	];

	const iconPaths: Record<IconName, string[]> = {
		chevron: ['M9 6.75 14.25 12 9 17.25'],
		spark: ['M12 4.5 13.9 8.1 17.5 10 13.9 11.9 12 15.5 10.1 11.9 6.5 10 10.1 8.1Z'],
		launch: ['M14.75 7.25 9.75 12l5 4.75', 'M9.75 12h8'],
		reply: ['M9.25 8 5 12.25l4.25 4.25', 'M5.5 12.25h8.75a4.25 4.25 0 0 1 4.25 4.25'],
		split: ['M8.25 5.25h7.5', 'M8.25 18.75h7.5', 'M12 5.25v13.5', 'M7.5 10.5h9']
	};

	function formatExperimentLabel(id: string) {
		return id
			.split('-')
			.filter(Boolean)
			.map((segment) => {
				if (segment.length <= 2) {
					return segment.toUpperCase();
				}

				return `${segment[0]?.toUpperCase()}${segment.slice(1)}`;
			})
			.join(' ');
	}

	const experimentLabel = $derived(formatExperimentLabel(params.id));
</script>

<svelte:head>
	<title>GrowthOdds - {experimentLabel}</title>
	<meta name="viewport" content="width=device-width, initial-scale=1" />
</svelte:head>

<div class="min-h-screen text-[var(--color-foreground)]">
	<AppNavbar activeItem="Experiments" />

	<main class="pt-20">
		<div class="mx-auto max-w-6xl px-6 py-14 md:px-12 md:py-20">
			<section
				class="relative overflow-hidden rounded-[2rem] border border-black/5 bg-[linear-gradient(180deg,rgba(255,255,255,0.94),rgba(243,244,243,0.92))] px-6 py-8 shadow-[0_24px_60px_rgba(25,28,28,0.06)] md:px-10 md:py-12"
			>
				<div
					class="absolute top-[-5rem] left-[-4rem] h-40 w-40 rounded-full bg-[rgba(10,77,60,0.11)] blur-3xl"
				></div>
				<div
					class="absolute right-[-5rem] bottom-[-6rem] h-56 w-56 rounded-full bg-[rgba(178,239,216,0.45)] blur-3xl"
				></div>

				<div class="relative mx-auto max-w-5xl">
					<div class="flex flex-col gap-8 md:gap-10">
						<div class="flex flex-col gap-5">
							<nav
								class="flex flex-wrap items-center gap-2 text-[0.72rem] font-semibold tracking-[0.24em] text-black/42 uppercase"
							>
								<a href="/experiments" class="transition-colors hover:text-[var(--color-primary)]">
									Experiments
								</a>
								<svg
									viewBox="0 0 24 24"
									fill="none"
									stroke="currentColor"
									stroke-width="1.8"
									stroke-linecap="round"
									stroke-linejoin="round"
									class="h-3.5 w-3.5 text-black/25"
									aria-hidden="true"
								>
									{#each iconPaths.chevron as path (`crumb-${path}`)}
										<path d={path}></path>
									{/each}
								</svg>
								<span class="text-[var(--color-primary)]">{experimentLabel}</span>
							</nav>

							<div class="flex flex-col gap-5 md:flex-row md:items-end md:justify-between">
								<div>
									<h1
										class="max-w-3xl font-display text-4xl leading-none font-extrabold tracking-tight text-[var(--color-primary)] sm:text-5xl md:text-[3.6rem]"
									>
										Competitive Comparison
									</h1>
								</div>
							</div>
						</div>

						<section class="grid gap-5 md:grid-cols-2">
							{#each metrics as metric (metric.label)}
								<article
									class="theme-card rounded-[1.6rem] border border-white/75 bg-[rgba(255,255,255,0.8)] p-7 shadow-[0_18px_45px_rgba(25,28,28,0.05)] md:p-8"
								>
									<p class="text-label text-black/45">{metric.label}</p>
									<p class="mt-3 text-sm text-black/42">{metric.eyebrow}</p>
									<div class="mt-6 flex items-end gap-3">
										<p
											class="font-display text-5xl font-black tracking-tight text-[var(--color-primary)] md:text-6xl"
										>
											{metric.value}
										</p>
										<span
											class="pb-2 text-sm font-bold text-[var(--color-primary-soft)] md:text-base"
										>
											{metric.delta}
										</span>
									</div>
								</article>
							{/each}
						</section>

						<section
							class="relative overflow-hidden rounded-[1.8rem] border border-white/80 glass-panel p-8 md:p-10"
						>
							<div
								class="absolute top-5 right-5 flex h-16 w-16 items-center justify-center rounded-full bg-white/70 text-[var(--color-primary)] opacity-15"
							>
								<svg
									viewBox="0 0 24 24"
									fill="none"
									stroke="currentColor"
									stroke-width="1.8"
									stroke-linecap="round"
									stroke-linejoin="round"
									class="h-8 w-8"
									aria-hidden="true"
								>
									{#each iconPaths.spark as path (`hero-spark-${path}`)}
										<path d={path}></path>
									{/each}
								</svg>
							</div>

							<div class="relative max-w-4xl">
								<div class="mb-5 flex items-center gap-3 text-[var(--color-primary)]">
									<span
										class="inline-flex h-10 w-10 items-center justify-center rounded-full bg-[var(--color-primary-fixed)]"
									>
										<svg
											viewBox="0 0 24 24"
											fill="none"
											stroke="currentColor"
											stroke-width="1.75"
											stroke-linecap="round"
											stroke-linejoin="round"
											class="h-4.5 w-4.5"
											aria-hidden="true"
										>
											{#each iconPaths.spark as path (`spark-${path}`)}
												<path d={path}></path>
											{/each}
										</svg>
									</span>
									<h2 class="font-display text-2xl font-bold">Strategic Outcome</h2>
								</div>

								<p class="max-w-3xl text-lg leading-8 text-black/70 md:text-xl">
									The data reveals a decisive shift in user sentiment.
									<span class="font-bold text-[var(--color-primary)]">
										Variation A outperformed Variation B by 22%
									</span>, specifically when utilizing a direct, high-urgency messaging style. Users
									engaged 3x more frequently with data-backed claims than with purely
									narrative-driven hooks.
								</p>

								<div class="mt-8 flex flex-wrap gap-3">
									{#each insightTags as tag (tag)}
										<span
											class="rounded-xl bg-[var(--color-surface-low)] px-4 py-2 text-[0.72rem] font-bold tracking-[0.16em] text-black/55 uppercase"
										>
											{tag}
										</span>
									{/each}
								</div>
							</div>
						</section>

						<section>
							<div class="mb-6">
								<div>
									<h2
										class="font-display text-2xl font-bold text-[var(--color-primary)] md:text-[2rem]"
									>
										Execution Timeline
									</h2>
									<p class="mt-2 text-sm text-black/50">
										A static recap of the steps that fed this experiment run.
									</p>
								</div>
							</div>

							<div class="space-y-4">
								{#each timeline as item (item.title)}
									<article
										class={[
											'group flex flex-col gap-4 rounded-[1.4rem] border border-white/80 bg-white/88 p-5 shadow-[0_16px_40px_rgba(25,28,28,0.04)] transition-transform duration-300 hover:-translate-y-0.5 md:flex-row md:items-center md:justify-between md:p-6',
											item.active && 'ring-1 ring-[rgba(0,53,40,0.08)]'
										]}
									>
										<div class="flex items-center gap-4 md:gap-5">
											<div
												class={[
													'inline-flex h-12 w-12 shrink-0 items-center justify-center rounded-full',
													item.active
														? 'bg-[var(--color-primary)] text-white shadow-[0_14px_32px_rgba(0,53,40,0.2)]'
														: 'bg-[var(--color-surface-low)] text-[var(--color-primary)]'
												]}
											>
												<svg
													viewBox="0 0 24 24"
													fill="none"
													stroke="currentColor"
													stroke-width="1.75"
													stroke-linecap="round"
													stroke-linejoin="round"
													class="h-5 w-5"
													aria-hidden="true"
												>
													{#each iconPaths[item.icon] as path (`${item.title}-${path}`)}
														<path d={path}></path>
													{/each}
												</svg>
											</div>

											<div>
												<h3
													class="font-display text-lg font-bold text-[var(--color-primary)] md:text-xl"
												>
													{item.title}
												</h3>
												<p class="mt-1 text-sm text-black/48">{item.description}</p>
											</div>
										</div>

										<div class="text-left md:text-right">
											<p class="font-display text-lg font-bold text-[var(--color-primary)]">
												{item.date}
											</p>
											<p
												class={[
													'mt-1 text-[0.68rem] font-bold tracking-[0.22em] uppercase',
													item.active ? 'text-emerald-600' : 'text-black/35'
												]}
											>
												{item.status}
											</p>
										</div>
									</article>
								{/each}
							</div>
						</section>
					</div>
				</div>
			</section>
		</div>
	</main>
</div>
