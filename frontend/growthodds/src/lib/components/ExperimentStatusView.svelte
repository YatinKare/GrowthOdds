<script lang="ts">
	import { resolve } from '$app/paths';

	import AppNavbar from '$lib/components/AppNavbar.svelte';
	import {
		getApiErrorMessage,
		getExperimentStatusMessage,
		isTerminalExperimentStatus,
		type ExperimentGetResponse,
		type ExperimentStatus
	} from '$lib/experiments';

	type FetchState = 'idle' | 'polling' | 'error';

	const POLL_INTERVAL_MS = 3000;

	let {
		experimentId,
		initialResponse,
		initialError
	}: {
		experimentId: string;
		initialResponse: ExperimentGetResponse | null;
		initialError: string | null;
	} = $props();

	let latestResponse = $state.raw<ExperimentGetResponse | null>(null);
	let fetchState = $state<FetchState>('idle');
	let fetchError = $state<string | null>(null);
	let isFetching = $state(false);
	let pollingBlocked = $state(false);
	let dismissedInitialError = $state(false);
	let lastUpdatedAt = $state<string | null>(null);

	const experimentResponse = $derived(latestResponse ?? initialResponse);
	const activeError = $derived(fetchError ?? (dismissedInitialError ? null : initialError));
	const experimentTitle = $derived(experimentResponse?.experiment.title || null);
	const displayName = $derived(experimentTitle ?? experimentId);
	const currentStatus = $derived<ExperimentStatus | null>(experimentResponse?.experiment.status ?? null);
	const statusMessage = $derived(getExperimentStatusMessage(currentStatus));
	const shouldPoll = $derived(
		!pollingBlocked && (currentStatus === 'queued' || currentStatus === 'running')
	);
	const isPolling = $derived(fetchState === 'polling');
	const statusBadgeClass = $derived([
		'inline-flex items-center gap-2 rounded-full px-4 py-2 text-xs font-bold tracking-[0.18em] uppercase',
		currentStatus === 'completed'
			? 'bg-emerald-100 text-emerald-700'
			: currentStatus === 'failed'
				? 'bg-rose-100 text-rose-700'
				: currentStatus === 'running'
					? 'bg-amber-100 text-amber-700'
					: 'bg-[var(--color-primary-fixed)] text-[var(--color-primary)]'
	]);
	const debugPayload = $derived(
		experimentResponse ? JSON.stringify(experimentResponse, null, 2) : 'No response available yet.'
	);
	const lastUpdatedLabel = $derived(
		lastUpdatedAt
			? new Date(lastUpdatedAt).toLocaleTimeString([], {
					hour: 'numeric',
					minute: '2-digit',
					second: '2-digit'
				})
			: experimentResponse
				? 'Initial load'
			: 'Never'
	);
	const retryButtonLabel = $derived(isFetching ? 'Retrying...' : 'Retry fetch');

	async function refetchExperiment(manual = false) {
		if (isFetching) {
			return;
		}

		isFetching = true;
		fetchState = manual ? 'idle' : 'polling';

		try {
			const response = await fetch(`/api/experiment/${experimentId}`, {
				headers: {
					accept: 'application/json'
				}
			});
			const payload = await response.json().catch(() => null);

			if (!response.ok) {
				pollingBlocked = true;
				fetchState = 'error';
				fetchError = getApiErrorMessage(payload, 'Unable to load experiment.');
				return;
			}

			latestResponse = payload as ExperimentGetResponse;
			dismissedInitialError = true;
			fetchError = null;
			fetchState = 'idle';
			lastUpdatedAt = new Date().toISOString();
			pollingBlocked = isTerminalExperimentStatus(latestResponse.experiment.status);
		} catch {
			pollingBlocked = true;
			fetchState = 'error';
			fetchError = 'Unable to load experiment.';
		} finally {
			isFetching = false;
		}
	}

	$effect(() => {
		if (!shouldPoll) {
			return;
		}

		const interval = window.setInterval(() => {
			void refetchExperiment();
		}, POLL_INTERVAL_MS);

		return () => {
			window.clearInterval(interval);
		};
	});
</script>

<svelte:head>
	<title>GrowthOdds - {displayName}</title>
	<meta name="viewport" content="width=device-width, initial-scale=1" />
</svelte:head>

<div class="min-h-screen text-[var(--color-foreground)]">
	<AppNavbar activeItem="Experiments" />

	<main class="pt-20">
		<div class="mx-auto max-w-5xl px-6 py-14 md:px-10 md:py-20">
			<section
				class="relative overflow-hidden rounded-[2rem] border border-black/5 bg-[linear-gradient(180deg,rgba(255,255,255,0.95),rgba(243,244,243,0.92))] px-6 py-8 shadow-[0_24px_60px_rgba(25,28,28,0.06)] md:px-10 md:py-10"
			>
				<div
					class="absolute top-[-5rem] left-[-4rem] h-40 w-40 rounded-full bg-[rgba(10,77,60,0.11)] blur-3xl"
				></div>
				<div
					class="absolute right-[-5rem] bottom-[-6rem] h-56 w-56 rounded-full bg-[rgba(178,239,216,0.45)] blur-3xl"
				></div>

				<div class="relative space-y-8">
					<div class="flex flex-col gap-5 md:flex-row md:items-start md:justify-between">
						<div class="space-y-4">
							<nav
								class="flex flex-wrap items-center gap-2 text-[0.72rem] font-semibold tracking-[0.24em] text-black/42 uppercase"
							>
								<a
									href={resolve('/dashboard')}
									class="transition-colors hover:text-[var(--color-primary)]"
								>
									Dashboard
								</a>
								<span class="text-black/25">/</span>
								<span class="text-[var(--color-primary)]">Experiment</span>
							</nav>

							<div>
								<p class="text-label text-black/45">Experiment</p>
								<h1
									class="mt-3 font-display text-3xl leading-tight font-extrabold tracking-tight text-[var(--color-primary)] md:text-[2.75rem]"
								>
									{displayName}
								</h1>
								<p class="mt-1.5 text-xs font-medium tracking-wide text-black/35 break-all">{experimentId}</p>
							</div>
						</div>

						<div class="space-y-3 md:text-right">
							<div class={statusBadgeClass} data-testid="status-badge">
								<span class="h-2.5 w-2.5 rounded-full bg-current opacity-70"></span>
								<span>{currentStatus ?? 'unavailable'}</span>
							</div>
							<p class="text-sm font-semibold text-black/55">{statusMessage}</p>
							<p class="text-xs text-black/42">Last fetched: {lastUpdatedLabel}</p>
						</div>
					</div>

					<section class="grid gap-5 md:grid-cols-[minmax(0,1fr)_18rem]">
						<article class="rounded-[1.5rem] bg-white/85 p-6 shadow-[0_18px_45px_rgba(25,28,28,0.05)]">
							<p class="text-label text-black/42">Run State</p>
							<p class="mt-4 text-lg leading-8 text-black/70">
								This screen mirrors the backend response directly for the first integrated slice.
								When the experiment is <span class="font-bold text-[var(--color-primary)]">queued</span>
								or <span class="font-bold text-[var(--color-primary)]">running</span>, it polls every 3
								seconds. Polling stops automatically after <span class="font-bold">completed</span> or
								<span class="font-bold">failed</span>.
							</p>

							<div class="mt-6 flex flex-wrap gap-3 text-xs font-semibold">
								<span class="rounded-full bg-[var(--color-surface-low)] px-3 py-2 text-black/55">
									Polling: {isPolling ? 'active' : 'idle'}
								</span>
								<span class="rounded-full bg-[var(--color-surface-low)] px-3 py-2 text-black/55">
									Auto refresh: {shouldPoll ? 'enabled' : 'stopped'}
								</span>
							</div>
						</article>

						<article class="rounded-[1.5rem] bg-white/85 p-6 shadow-[0_18px_45px_rgba(25,28,28,0.05)]">
							<p class="text-label text-black/42">Quick Actions</p>
							<div class="mt-4 space-y-3 text-sm text-black/60">
								<p>Manual refetch is only needed after a failed GET request or a network issue.</p>

								{#if activeError}
									<button
										type="button"
										data-testid="retry-fetch"
										onclick={() => void refetchExperiment(true)}
										disabled={isFetching}
										class="inline-flex w-full items-center justify-center rounded-xl bg-[var(--color-primary)] px-4 py-3 font-bold text-white transition hover:bg-[var(--color-primary-soft)] disabled:cursor-not-allowed disabled:opacity-65"
									>
										{retryButtonLabel}
									</button>
								{:else}
									<p class="rounded-xl bg-[var(--color-surface-low)] px-4 py-3 font-semibold text-black/50">
										No retry needed right now.
									</p>
								{/if}
							</div>
						</article>
					</section>

					{#if activeError}
						<section class="rounded-[1.5rem] border border-rose-200 bg-rose-50 px-5 py-4">
							<p class="text-sm font-semibold text-rose-700">{activeError}</p>
						</section>
					{/if}

					<section class="rounded-[1.6rem] bg-[#101716] p-5 shadow-[0_18px_45px_rgba(10,15,15,0.18)]">
						<div class="mb-4 flex items-center justify-between gap-4">
							<div>
								<p class="text-label text-white/45">Debug Payload</p>
								<p class="mt-1 text-sm text-white/55">
									Latest successful GET response from `/api/experiment/{experimentId}`
								</p>
							</div>
							<span class="rounded-full bg-white/8 px-3 py-1 text-xs font-semibold text-white/65">
								JSON
							</span>
						</div>

						<pre
							class="modal-scroll overflow-x-auto rounded-[1.2rem] bg-black/25 p-4 text-xs leading-6 text-[#d7f2e6]"
							data-testid="debug-payload"
						><code>{debugPayload}</code></pre>
					</section>
				</div>
			</section>
		</div>
	</main>
</div>
