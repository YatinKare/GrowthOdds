<script lang="ts">
	import { goto } from '$app/navigation';
	import { resolve } from '$app/paths';

	import AppNavbar from '$lib/components/AppNavbar.svelte';
	import {
		getApiErrorMessage,
		type CreateExperimentRequest,
		type CreateExperimentResponse
	} from '$lib/experiments';

	type IconName =
		| 'dashboard'
		| 'actions'
		| 'experiments'
		| 'spark'
		| 'arrow'
		| 'notifications'
		| 'settings'
		| 'users'
		| 'engagement'
		| 'science'
		| 'swipe'
		| 'close'
		| 'info'
		| 'trend'
		| 'refresh'
		| 'copy'
		| 'send'
		| 'command';

	type StatCard = {
		label: string;
		value: string;
		description: string;
		icon: IconName;
		change?: string;
	};

	type SubmitState = 'idle' | 'submitting' | 'error';

	const statCards: StatCard[] = [
		{
			label: 'Growth Base',
			value: '142',
			description: 'New users this cycle',
			icon: 'users',
			change: '+12%'
		},
		{
			label: 'Social Depth',
			value: '1,234',
			description: 'X engagement (aggregated)',
			icon: 'engagement'
		},
		{
			label: 'Active Bets',
			value: '3',
			description: 'Live growth experiments',
			icon: 'science'
		}
	];

	const actionTitle = 'Post comparison of your product and its top competitor on X';
	const actionReason = 'Reason: High engagement on competitor threads';
	const actionOdds = 'Odds: 84.2% Success';
	const steeringPlaceholder =
		'Describe the specifics of your move here (e.g., focus on new features, highlight pricing, or set a specific tone)...';

	let isModalOpen = $state(false);
	let experimentMode = $state<'single' | 'ab'>('ab');
	let userNote = $state('');
	let submitState = $state<SubmitState>('idle');
	let submitError = $state<string | null>(null);

	const mappedExperimentType = $derived(experimentMode === 'single' ? 'single' : 'ab_test');
	const trimmedUserNote = $derived(userNote.trim());
	const isSubmitting = $derived(submitState === 'submitting');
	const submitButtonLabel = $derived(
		isSubmitting
			? 'Starting experiment...'
			: experimentMode === 'single'
				? 'Run Single Post'
				: 'Run A/B Test'
	);
	const activeModeLabel = $derived(experimentMode === 'single' ? 'Single Post' : 'A/B Test');

	$effect(() => {
		const previousOverflow = document.body.style.overflow;
		document.body.style.overflow = isModalOpen ? 'hidden' : '';

		return () => {
			document.body.style.overflow = previousOverflow;
		};
	});

	function openModal() {
		submitState = 'idle';
		submitError = null;
		isModalOpen = true;
	}

	function closeModal() {
		if (isSubmitting) {
			return;
		}

		isModalOpen = false;
	}

	async function submitExperiment(event: SubmitEvent) {
		event.preventDefault();

		if (isSubmitting) {
			return;
		}

		submitState = 'submitting';
		submitError = null;

		const payload: CreateExperimentRequest = {
			product_id: 'prod_123',
			created_by: '1',
			experiment_title: actionTitle,
			experiment_type: mappedExperimentType,
			goal: 'increase signups',
			channel: 'x',
			user_note: trimmedUserNote
		};

		try {
			const response = await fetch('/api/experiment', {
				method: 'POST',
				headers: {
					'content-type': 'application/json',
					accept: 'application/json'
				},
				body: JSON.stringify(payload)
			});
			const responseBody = await response.json().catch(() => null);

			if (!response.ok) {
				submitState = 'error';
				submitError = getApiErrorMessage(responseBody, 'Unable to create experiment.');
				return;
			}

			const createdExperiment = responseBody as CreateExperimentResponse;

			if (!createdExperiment?.experiment_id) {
				submitState = 'error';
				submitError = 'The create response did not include an experiment ID.';
				return;
			}

			userNote = '';
			submitState = 'idle';
			submitError = null;
			isModalOpen = false;

			await goto(resolve(`/experiments/${createdExperiment.experiment_id}`));
		} catch {
			submitState = 'error';
			submitError = 'Unable to create experiment.';
		}
	}

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
		spark: ['M12 4.5 13.9 8.1 17.5 10 13.9 11.9 12 15.5 10.1 11.9 6.5 10 10.1 8.1Z'],
		arrow: ['M5.75 12h12.5', 'M13.5 6.75 18.75 12 13.5 17.25'],
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
		],
		users: [
			'M9.25 10.25a2.75 2.75 0 1 0 0-5.5 2.75 2.75 0 0 0 0 5.5Z',
			'M16 11.5a2.25 2.25 0 1 0 0-4.5 2.25 2.25 0 0 0 0 4.5Z',
			'M4.75 18c.933-2.37 2.991-3.75 5.5-3.75S14.817 15.63 15.75 18',
			'M14.25 17.75c.577-1.486 1.876-2.5 3.5-2.5 1.246 0 2.32.597 3 1.75'
		],
		engagement: ['M5 17.5 9 13.5 12 15.5 19 8.5', 'M14.5 8.5H19v4.5', 'M5 7.5h5', 'M5 11.5h2.5'],
		science: [
			'M9 4.75v4.5l-3.5 6.25A3 3 0 0 0 8.12 20h7.76a3 3 0 0 0 2.62-4.5L15 9.25v-4.5',
			'M8.25 4.75h7.5',
			'M9.5 15c1 .9 2.091 1.35 3.273 1.35 1.027 0 1.936-.25 2.727-.75'
		],
		swipe: [
			'M6.5 8.25h5.25V3.75',
			'M17.5 15.75h-5.25v4.5',
			'M11.75 4.25 5.25 10.75',
			'M12.25 19.75 18.75 13.25'
		],
		close: ['M6 6l12 12', 'M18 6 6 18'],
		info: ['M12 17v-5', 'M12 8.5h.01', 'M12 3.75a8.25 8.25 0 1 1 0 16.5 8.25 8.25 0 0 1 0-16.5Z'],
		trend: ['M5.75 16.25 10 12l3 3 5.25-6.25', 'M14.75 8.75h3.5v3.5'],
		refresh: [
			'M16.75 9.25A5.5 5.5 0 0 0 7.5 8.1',
			'M7.25 14.75A5.5 5.5 0 0 0 16.5 15.9',
			'M16.75 5.75v3.5h-3.5',
			'M7.25 18.25v-3.5h3.5'
		],
		copy: [
			'M9.25 9.25h7.5a1 1 0 0 1 1 1v7.5a1 1 0 0 1-1 1h-7.5a1 1 0 0 1-1-1v-7.5a1 1 0 0 1 1-1Z',
			'M7.5 14.75h-1.25a1 1 0 0 1-1-1v-7.5a1 1 0 0 1 1-1h7.5a1 1 0 0 1 1 1V7.5'
		],
		send: ['M4.75 12h12.5', 'M13.75 7 19 12l-5.25 5'],
		command: [
			'M8.5 7.25a2.25 2.25 0 1 0 0 4.5h7a2.25 2.25 0 1 1 0 4.5h-7a2.25 2.25 0 1 0 0 4.5',
			'M12 6v12'
		]
	};
</script>

<svelte:head>
	<title>GrowthOdds - Growth Command</title>
	<meta name="viewport" content="width=device-width, initial-scale=1" />
</svelte:head>

<div class="min-h-screen text-[var(--color-foreground)]">
	<AppNavbar activeItem="Home" />

	<main class="pt-20">
		<div class="mx-auto max-w-6xl px-6 py-16 md:px-12 md:py-24">
			<section class="relative overflow-hidden rounded-[2rem] px-6 py-16 md:px-12 md:py-20">
				<div
					class="absolute inset-0 -z-10 bg-[linear-gradient(180deg,rgba(255,255,255,0.96),rgba(243,244,243,0.92))]"
				></div>
				<div
					class="absolute top-[-5rem] left-[-6rem] -z-10 h-48 w-48 rounded-full bg-[rgba(10,77,60,0.12)] blur-3xl"
				></div>
				<div
					class="absolute right-[-4rem] bottom-[-8rem] -z-10 h-64 w-64 rounded-full bg-[rgba(178,239,216,0.4)] blur-3xl"
				></div>

				<div class="mx-auto flex max-w-4xl flex-col items-center text-center">
					<div
						class="mb-8 inline-flex items-center gap-3 rounded-full border border-black/5 bg-white/75 px-4 py-2 shadow-[0_10px_30px_rgba(25,28,28,0.04)]"
					>
						<span
							class="inline-flex h-9 w-9 items-center justify-center rounded-full bg-[var(--color-primary-fixed)] text-[var(--color-primary)]"
						>
							<svg
								viewBox="0 0 24 24"
								fill="none"
								stroke="currentColor"
								stroke-width="1.7"
								stroke-linecap="round"
								stroke-linejoin="round"
								class="h-4 w-4"
								aria-hidden="true"
							>
								{#each iconPaths.spark as path (`spark-${path}`)}
									<path d={path}></path>
								{/each}
							</svg>
						</span>
						<span class="font-display text-label text-[var(--color-primary)]">
							Recommended Move
						</span>
					</div>

					<h1
						class="max-w-4xl font-display text-4xl leading-[1.05] font-extrabold tracking-tight text-[var(--color-foreground)] sm:text-5xl md:text-6xl"
					>
						Next Best Action: Post a comparison of your product and its top competitor on X.
					</h1>

					<p class="mt-5 max-w-2xl text-sm leading-7 text-black/55 md:text-base">
						One clear move, timed for the current cycle. This first merged slice now submits the
						action into the backend experiment pipeline and follows the run on the detail page.
					</p>

					<div class="mt-10 flex flex-col items-center gap-6">
						<button
							type="button"
							data-testid="open-create-modal"
							onclick={openModal}
							class="group inline-flex items-center gap-3 rounded-xl bg-primary-gradient px-8 py-4 font-display text-lg font-bold text-white shadow-[0_24px_50px_-20px_rgba(0,53,40,0.45)] transition-transform duration-300 hover:-translate-y-0.5"
						>
							<span>Run Action</span>
							<svg
								viewBox="0 0 24 24"
								fill="none"
								stroke="currentColor"
								stroke-width="1.75"
								stroke-linecap="round"
								stroke-linejoin="round"
								class="h-5 w-5 transition-transform duration-300 group-hover:translate-x-1"
								aria-hidden="true"
							>
								{#each iconPaths.arrow as path (`arrow-${path}`)}
									<path d={path}></path>
								{/each}
							</svg>
						</button>

						<div
							class="flex items-center gap-3 text-xs font-medium tracking-[0.04em] text-black/55"
						>
							<span class="relative flex h-3 w-3">
								<span
									class="absolute inline-flex h-full w-full animate-ping rounded-full bg-emerald-400 opacity-70"
								></span>
								<span class="relative inline-flex h-3 w-3 rounded-full bg-emerald-500"></span>
							</span>
							<span>System Ready: All platforms synced.</span>
						</div>
					</div>
				</div>
			</section>

			<section class="mt-18 md:mt-24">
				<div class="mb-8 flex items-center gap-6">
					<h2 class="font-display text-2xl font-bold text-[var(--color-primary)]">Your Stats</h2>
					<div class="h-px flex-1 bg-black/7"></div>
					<button
						type="button"
						class="text-sm font-semibold text-black/45 transition-colors hover:text-[var(--color-primary)]"
					>
						Full Report
					</button>
				</div>

				<div class="grid gap-6 md:grid-cols-3">
					{#each statCards as card (card.label)}
						<article
							class="group rounded-[1.5rem] bg-white p-8 shadow-[0_22px_50px_rgba(25,28,28,0.05)] transition-transform duration-300 hover:-translate-y-1"
						>
							<div class="mb-8 flex items-start justify-between gap-4">
								<p class="text-label text-black/45">{card.label}</p>
								<span
									class="inline-flex h-10 w-10 items-center justify-center rounded-full bg-[var(--color-surface-low)] text-black/40 transition-colors group-hover:text-[var(--color-primary)]"
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
										{#each iconPaths[card.icon] as path (`${card.label}-${path}`)}
											<path d={path}></path>
										{/each}
									</svg>
								</span>
							</div>

							<div class="flex items-end gap-3">
								<p class="font-display text-4xl font-black text-[var(--color-foreground)]">
									{card.value}
								</p>
								{#if card.change}
									<span
										class="theme-badge theme-badge-primary rounded-full px-2.5 py-1 text-[0.7rem] font-bold"
									>
										{card.change}
									</span>
								{/if}
							</div>

							<p class="mt-3 text-sm text-black/50">{card.description}</p>
						</article>
					{/each}
				</div>
			</section>
		</div>
	</main>

	{#if isModalOpen}
		<button
			type="button"
			class="fixed inset-0 z-50 bg-[rgba(25,28,28,0.22)] backdrop-blur-sm"
			aria-label="Close popup overlay"
			onclick={closeModal}
		></button>

		<section class="fixed inset-0 z-[60] overflow-y-auto" aria-modal="true" role="dialog">
			<div class="flex min-h-full items-center justify-center p-4 md:p-6">
				<form
					class="w-full max-w-[36rem] overflow-hidden rounded-[1.6rem] border border-black/6 bg-white/88 shadow-[0_28px_70px_rgba(25,28,28,0.22)] backdrop-blur-xl"
					onsubmit={submitExperiment}
					aria-busy={isSubmitting}
					data-testid="create-modal"
				>
					<header
						class="flex items-center justify-between border-b border-black/6 px-6 py-5 md:px-7"
					>
						<div class="flex items-center gap-3">
							<span
								class="inline-flex h-11 w-11 items-center justify-center rounded-xl bg-[var(--color-primary)] text-white shadow-[0_12px_24px_rgba(0,53,40,0.2)]"
							>
								<svg
									viewBox="0 0 24 24"
									fill="none"
									stroke="currentColor"
									stroke-width="1.8"
									stroke-linecap="round"
									stroke-linejoin="round"
									class="h-5 w-5"
									aria-hidden="true"
								>
									{#each iconPaths.swipe as path (`modal-swipe-${path}`)}
										<path d={path}></path>
									{/each}
								</svg>
							</span>

							<div>
								<h2
									class="font-display text-[1.9rem] font-extrabold tracking-tight text-[var(--color-primary)]"
								>
									Execute Move
								</h2>
								<p class="mt-1 text-xs font-semibold tracking-[0.18em] text-black/42 uppercase">
									{activeModeLabel}
								</p>
							</div>
						</div>

						<button
							type="button"
							aria-label="Close popup"
							onclick={closeModal}
							disabled={isSubmitting}
							class="inline-flex h-10 w-10 items-center justify-center rounded-full text-black/55 transition-colors hover:bg-[var(--color-surface-low)] hover:text-[var(--color-foreground)] disabled:cursor-not-allowed disabled:opacity-45"
						>
							<svg
								viewBox="0 0 24 24"
								fill="none"
								stroke="currentColor"
								stroke-width="1.8"
								stroke-linecap="round"
								stroke-linejoin="round"
								class="h-5 w-5"
								aria-hidden="true"
							>
								{#each iconPaths.close as path (`close-${path}`)}
									<path d={path}></path>
								{/each}
							</svg>
						</button>
					</header>

					<div class="modal-scroll max-h-[44rem] space-y-8 overflow-y-auto px-6 py-6 md:px-7">
						<section class="space-y-4">
							<div class="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
								<p class="text-[0.68rem] font-bold tracking-[0.24em] text-black/45 uppercase">
									Experiment: Social Post (X)
								</p>

								<div
									class="inline-flex w-fit items-center gap-1 rounded-xl border border-black/6 bg-[var(--color-surface-low)] p-1"
								>
									<button
										type="button"
										onclick={() => (experimentMode = 'single')}
										disabled={isSubmitting}
										class={[
											'rounded-[0.7rem] px-4 py-2 text-xs font-bold transition disabled:cursor-not-allowed disabled:opacity-45',
											experimentMode === 'single'
												? 'bg-white text-[var(--color-primary)] shadow-sm'
												: 'text-black/45 hover:text-[var(--color-foreground)]'
										]}
									>
										Single Post
									</button>
									<button
										type="button"
										onclick={() => (experimentMode = 'ab')}
										disabled={isSubmitting}
										class={[
											'rounded-[0.7rem] px-4 py-2 text-xs font-bold transition disabled:cursor-not-allowed disabled:opacity-45',
											experimentMode === 'ab'
												? 'bg-white text-[var(--color-primary)] shadow-sm'
												: 'text-black/45 hover:text-[var(--color-foreground)]'
										]}
									>
										A/B Test
									</button>
								</div>
							</div>

							<div
								class="rounded-[1.25rem] border border-black/5 bg-[var(--color-surface-low)] p-5 shadow-[inset_0_1px_0_rgba(255,255,255,0.65)]"
							>
								<div class="flex gap-4">
									<div class="w-1 rounded-full bg-[var(--color-primary)]"></div>

									<div class="flex-1">
										<h3
											class="font-display text-[1.35rem] leading-tight font-extrabold text-[var(--color-primary)]"
										>
											{actionTitle}
										</h3>

										<div class="mt-4 flex flex-wrap gap-3">
											<div
												class="inline-flex items-center gap-2 rounded-full border border-black/6 bg-white px-3 py-2 text-xs font-semibold text-black/55 shadow-sm"
											>
												<svg
													viewBox="0 0 24 24"
													fill="none"
													stroke="currentColor"
													stroke-width="1.65"
													stroke-linecap="round"
													stroke-linejoin="round"
													class="h-3.5 w-3.5"
													aria-hidden="true"
												>
													{#each iconPaths.info as path (`info-${path}`)}
														<path d={path}></path>
													{/each}
												</svg>
												<span>{actionReason}</span>
											</div>

											<div
												class="inline-flex items-center gap-2 rounded-full bg-[var(--color-primary-fixed)] px-3 py-2 text-xs font-bold text-[var(--color-primary)] shadow-sm"
											>
												<svg
													viewBox="0 0 24 24"
													fill="none"
													stroke="currentColor"
													stroke-width="1.75"
													stroke-linecap="round"
													stroke-linejoin="round"
													class="h-3.5 w-3.5"
													aria-hidden="true"
												>
													{#each iconPaths.trend as path (`trend-${path}`)}
														<path d={path}></path>
													{/each}
												</svg>
												<span>{actionOdds}</span>
											</div>
										</div>
									</div>
								</div>
							</div>
						</section>

						<section class="space-y-4">
							<div class="flex items-center justify-between gap-4 px-1">
								<p class="text-[0.68rem] font-bold tracking-[0.24em] text-black/45 uppercase">
									Input
								</p>
								<p class="text-xs text-black/45">Optional free-text steering</p>
							</div>

							<div
								class="rounded-[1.25rem] border border-black/6 bg-white p-5 shadow-[0_18px_40px_rgba(25,28,28,0.04)] transition focus-within:ring-2 focus-within:ring-[var(--color-primary)]/10"
							>
								<label class="sr-only" for="user-note">Manual steering note</label>
								<textarea
									id="user-note"
									bind:value={userNote}
									data-testid="user-note-input"
									placeholder={steeringPlaceholder}
									spellcheck="false"
									disabled={isSubmitting}
									class="modal-scroll min-h-48 w-full resize-none border-0 bg-transparent p-0 text-sm leading-7 font-medium text-[var(--color-foreground)] outline-none disabled:cursor-not-allowed disabled:opacity-70"
								></textarea>

								<div class="mt-4 flex items-center justify-end gap-3 border-t border-black/6 pt-4">
									<span class="text-[0.62rem] font-bold tracking-[0.18em] text-black/35 uppercase">
										Manual Steering
									</span>

									<button
										type="button"
										aria-label="Manual steering shortcut"
										disabled={isSubmitting}
										class="inline-flex h-8 w-8 items-center justify-center rounded-full text-black/45 transition hover:bg-[var(--color-surface-low)] hover:text-[var(--color-primary)] disabled:cursor-not-allowed disabled:opacity-45"
									>
										<svg
											viewBox="0 0 24 24"
											fill="none"
											stroke="currentColor"
											stroke-width="1.7"
											stroke-linecap="round"
											stroke-linejoin="round"
											class="h-4 w-4"
											aria-hidden="true"
										>
											{#each iconPaths.command as path (`command-${path}`)}
												<path d={path}></path>
											{/each}
										</svg>
									</button>
								</div>
							</div>
						</section>

						{#if submitError}
							<p
								class="rounded-2xl border border-[var(--color-secondary)]/12 bg-[var(--color-secondary-soft)] px-4 py-3 text-sm font-semibold text-[var(--color-secondary)]"
								data-testid="create-error"
							>
								{submitError}
							</p>
						{/if}
					</div>

					<footer
						class="flex items-center justify-between bg-[linear-gradient(180deg,rgba(243,244,243,0.55),rgba(243,244,243,0.8))] px-6 py-5 md:px-7"
					>
						<button
							type="button"
							onclick={closeModal}
							disabled={isSubmitting}
							class="text-sm font-bold text-black/65 transition hover:text-[var(--color-foreground)] disabled:cursor-not-allowed disabled:opacity-45"
						>
							Cancel
						</button>

						<button
							type="submit"
							data-testid="submit-create"
							disabled={isSubmitting}
							class="inline-flex items-center gap-2 rounded-[0.85rem] bg-[linear-gradient(135deg,var(--color-primary),var(--color-primary-soft))] px-6 py-3.5 text-sm font-bold text-white shadow-[0_18px_32px_rgba(0,53,40,0.28)] transition hover:-translate-y-0.5 disabled:cursor-not-allowed disabled:opacity-80 disabled:hover:translate-y-0"
						>
							<span>{submitButtonLabel}</span>
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
								{#each isSubmitting ? iconPaths.refresh : iconPaths.send as path (`submit-${path}`)}
									<path d={path}></path>
								{/each}
							</svg>
						</button>
					</footer>
				</form>
			</div>
		</section>
	{/if}
</div>
