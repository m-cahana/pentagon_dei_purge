<script lang="ts">
	import * as d3 from 'd3';
	import { onMount } from 'svelte';
	import Scrolly from "$lib/components/helpers/scrolly.svelte";
	import { getDataPath } from '$lib/utils/paths';
	
	// Props for customization

	let {
		highlightMap = { // Customizable highlight mapping
			0: ["Women's History Month",
				"Black History Month"],
			1: ["Asian American and Pacific Islander Heritage Month",
				"LGBTQ+ History Month"],
			2: ["National Disability Employment Awareness Month",
				"National Hispanic Heritage Month"],
		}, 
		highlightText = {
			0: ["Section 1 Title", "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."],
			1: ["Section 2 Title", "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."],
			2: ["Section 3 Title", "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."],
		}, 
		titlesList = [
			"Women's History Month",
			"Black History Month",
			"Asian American and Pacific Islander Heritage Month",
			"LGBTQ+ History Month",
			"National Disability Employment Awareness Month",
			"National Hispanic Heritage Month"
		]
	} = $props();
	
	let sectionIndices = $derived(Object.keys(highlightMap).map(Number).sort((a, b) => a - b));

	let sampleTitles = $state([]);

	onMount(() => {
		// Use our utility function to get the proper path
		const dataFilePath = getDataPath('cleaned_titles_with_keywords.csv');
		
		d3.csv(dataFilePath).then((data) => {
			sampleTitles = data.filter(website => titlesList.includes(website.title));
			// remove duplicates based on title only
			sampleTitles = sampleTitles.filter((value, index, self) =>
				index === self.findIndex((t) => t.title === value.title)
			);
		});
	});

	let value = $state(0);
	
	// Define which titles to highlight for each value
	function getTitlesToHighlight(currentValue) {
		// Return the array of indices to highlight, or empty array if not found
		return highlightMap[currentValue] || [];
	}
	
	// Function to check if a title should be highlighted
	function shouldHighlight(index, currentValue) {
		return getTitlesToHighlight(currentValue).includes(sampleTitles[index].title);
	}

</script>

<section id="scrolly">
	<!-- Display each title as a separate paragraph -->
	<div class="titles-container">
		{#each sampleTitles as title, i}
			<p>
				<span class="title-text" class:highlighted={shouldHighlight(i, value)}>
					{title.title}
				</span>
			</p>
		{/each}
	</div>
	
	<div class="spacer"></div>
	<Scrolly bind:value>
		{#each sectionIndices as section}
			{@const active = value === section}
			<div class="step" class:active>
				<div class="step-content">
					{#if highlightText[section][0] && highlightText[section][0].trim() !== ''}
						<h3>{highlightText[section][0]}</h3>
					{/if}
					<p>{highlightText[section][1]}</p>
				</div>
			</div>
		{/each}
	</Scrolly>
	<div class="spacer"></div>
</section>

<style>
	p {
		margin: 0.2em 0;
		font-family: "Arial";
		font-weight: 200 !important;
		text-align: left;
	}
	
	.title-text {
		transition: background-color 0.5s ease;
		border-radius: 2px;
		padding: 1px 0;
		/* Remove z-index from individual text spans */
	}
	
	/* Highlighted title style */
	.highlighted {
		background-color: var(--color-military-green);
		font-weight: 400 !important;
		padding: 1px 2px;
		box-decoration-break: clone;
		-webkit-box-decoration-break: clone;
	}
	
	/* Container for all titles */
	.titles-container {
		position: sticky;
		top: 0;
		height: 100vh; /* Take full viewport height */
		display: flex;
		flex-direction: column;
		justify-content: center; /* Center content vertically */
		z-index: 1;
		background-color: white;
		padding: 10px 0;
		/* Ensure there's room for overflow if many titles */
		overflow-y: auto;
		/* Add compact spacing */
		gap: 0.1em; /* Small gap between title items */
		max-height: 100vh;
	}

	.spacer {
		height: 75vh;
	}

	.step {
		height: 100vh;
        display: flex;
        align-items: center;
        justify-content: flex-end;
        padding: 0 20px;
		z-index: 5; /* Increase z-index to ensure it's above titles */
		position: relative; /* Add positioning context for z-index to work */
	}

	.step-content {
		background-color: rgba(255, 255, 255, 0.9);
        border-radius: 8px;
        padding: 20px;
        max-width: 350px;
        pointer-events: auto;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-right: 5%;
	}
	
	.step-content h3 {
		margin-top: 0;
		margin-bottom: 0.5em;
		font-weight: 550;
		font-size: 18px;
	}
	
	.step-content p {
		margin: 0;
	}
	
	/* Make sure the Scrolly component has proper z-index */
	:global(.scrolly-container) {
		position: relative;
		z-index: 10; /* Higher than both titles and steps */
	}

</style>