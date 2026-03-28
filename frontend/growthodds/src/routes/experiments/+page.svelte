<script lang="ts">
	import { resolve } from '$app/paths';

	import AppNavbar from '$lib/components/AppNavbar.svelte';

	import type { PageProps } from './$types';

	let { data }: PageProps = $props();
</script>

<svelte:head>
	<title>GrowthOdds - Experiments</title>
	<meta name="viewport" content="width=device-width, initial-scale=1" />
</svelte:head>

<div class="min-h-screen text-[var(--color-foreground)]">
	<AppNavbar activeItem="Experiments" />

	<main class="pt-20">
		<div class="mx-auto max-w-6xl px-6 py-14 md:px-10 md:py-20">
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
					<div class="space-y-3">
						<p class="text-label text-black/45">Experiments</p>
						<h1
							class="font-display text-3xl leading-tight font-extrabold tracking-tight text-[var(--color-primary)] md:text-[2.75rem]"
						>
							All experiments
						</h1>
					</div>

					{#if data.initialError}
						<section class="rounded-[1.5rem] border border-rose-200 bg-rose-50 px-5 py-4">
							<p class="text-sm font-semibold text-rose-700">{data.initialError}</p>
						</section>
					{:else if data.experiments.length === 0}
						<section
							class="rounded-[1.5rem] bg-white/85 px-6 py-10 text-center shadow-[0_18px_45px_rgba(25,28,28,0.05)]"
						>
							<p class="text-lg font-semibold text-black/65">No experiments yet.</p>
						</section>
					{:else}
						<section class="grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
							{#each data.experiments as experiment (experiment.id)}
								<a
									href={resolve(`/experiments/${experiment.id}`)}
									class="group rounded-[1.5rem] bg-white/88 px-6 py-8 text-center shadow-[0_18px_45px_rgba(25,28,28,0.05)] transition-transform duration-200 hover:-translate-y-1 hover:shadow-[0_24px_60px_rgba(25,28,28,0.1)]"
								>
									<p
										class="font-display text-xl leading-tight font-bold tracking-tight text-[var(--color-primary)] transition-colors group-hover:text-[var(--color-primary-soft)]"
									>
										{experiment.title?.trim() || experiment.id}
									</p>
								</a>
							{/each}
						</section>
					{/if}
				</div>
			</section>
		</div>
	</main>
</div>
