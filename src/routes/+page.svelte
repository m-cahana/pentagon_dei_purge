<script>
	import TitleScrolly from "$lib/components/title_scrolly.svelte";
    import Footer from "$lib/components/footer.svelte";
    import TopWordList from "$lib/components/top_word_list.svelte";

    import CirclePackScroll from "$lib/components/circle_pack_scroll.svelte";
    import CirclePack from "$lib/components/circle_packing.svelte";
    import { onMount } from 'svelte';
    
    onMount(() => {
        // Ensure page starts at the top when refreshed
        window.onbeforeunload = function() {
            window.scrollTo(0, 0);
        };
        
        // Also scroll to top immediately when component mounts
        window.scrollTo(0, 0);
    });
</script>

<main>
	<h1>What gets erased in a Pentagon DEI purge?</h1>
    <div class="subtitle">March 2025</div>

    <p>
        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
    </p>

    <p>
        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
    </p>


    <TopWordList />

    <p>
        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
    </p>


    <CirclePack />

    <p>
        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
    </p>

    <TitleScrolly 
      titlesList={
        ["Women's History Month",
        "A story to tell: MCSC celebrates Women's History Month",
        "WASPs receiving Congressional Gold Medal", 
        "Marines Honor Women's History Month",
        "First female shuttle commander",
        "We can do it! - Female Marines gather to show support for each other", 
        "Discussing Women's History Month",
        "Kurze's rise to DLA Executive Director: A testament to women",
        "WASP recalls her World War II experiences",
        "Staff Sgt. Betty Blake: First female in AF",
        "Honoring SixTripleEight",
        "The First Female Marine - Opha May Johnson",
        "571 MSAS launches inaugural WPS seminar in El Salvador"]}
      highlightMap={{
        0: [
            "Women's History Month",
            "Kurze's rise to DLA Executive Director: A testament to women","Discussing Women's History Month",
            "A story to tell: MCSC celebrates Women's History Month", 
            "We can do it! - Female Marines gather to show support for each other", 
        ],
        1: [ "Honoring SixTripleEight"],
        2: [
            "First female shuttle commander", 
            "Staff Sgt. Betty Blake: First female in AF",
             "The First Female Marine - Opha May Johnson",
        ],
        3: [
            "WASP recalls her World War II experiences",
            "WASPs receiving Congressional Gold Medal",
            "571 MSAS launches inaugural WPS seminar in El Salvador",
        ]
      }}
      highlightText={{
        0: "Any mention of women's history month has been purged, along with celebration of women in the military.",
        1: "Cultural media that celebrates women - like the movie Six Triple Eight, which highlights the contributions an all-black women's battalion during WWII - has been removed too.",
        2: "Female figures from history have been erased.",
        3: "So too have female-oriented military organizations, like the Women Air Force Service Pilots (WASPS), and the Women's Peace Service (WPS)."
      }}
    />
    
    <p>
        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
    </p>
</main>

<Footer />

<style>
	main {
		margin: 0 auto;
		max-width: 800px;
		padding: 1rem;
        font-family: "Helvetica";
		text-align: center;
	}


	h1 {
		font-size: 36px;
        font-style: italic;
        font-weight: 300;
        margin-bottom: 0.2rem;
	}

    p {
        font-size: 16px;
        text-align: left;
        font-weight: 300;
    }

    .subtitle {
        font-size: 20px;
        font-style: italic;
        font-weight: 300;
        margin-top: 0;
    }
</style>
