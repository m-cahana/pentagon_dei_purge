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

    <TitleScrolly 
    titlesList={
      [
        'Observance for Black History Month',
        'Quantico celebrates Black History Month at prayer breakfast',
        'Tuskegee Airman describes service, time as POW during virtual call with 332nd AEW',
        'Marine Corps Observes African American / Black History Month', 
        'African American/Black Innovations ... where would we be without them?',
        'Gospel celebration',
        'FACES of MCIPAC - African American U.S. Marines share their stories',
        'African American Heritage Open Mic Night',
        'Airmen sample soul food',
        'Goodfellow Celebrates Juneteenth',
        'Martin Luther King Jr. special observance',
        '2nd Annual Soul Food Taste',
        'Vance Marchbanks Jr.',
        'Civil rights activist shares legacy of love, community and action amid anecdotes of working with Dr. Martin Luther King Jr.',
        "Respecting slaves' value at Mount Vernon",
        'Miramar pauses to acknowledge selfless service of Tuskegee Airmen',
        'Elayne Arrington'
      ]}
    highlightMap={{
      0: [
        'Observance for Black History Month',
        'Quantico celebrates Black History Month at prayer breakfast',
        'Marine Corps Observes African American / Black History Month', 
        'African American Heritage Open Mic Night',
        'Goodfellow Celebrates Juneteenth',
        'Martin Luther King Jr. special observance',
      ],
      1: [
        'African American/Black Innovations ... where would we be without them?',
        'FACES of MCIPAC - African American U.S. Marines share their stories',
      ],
      2: [
        'Airmen sample soul food',
        'Gospel celebration',
        '2nd Annual Soul Food Taste',
      ],
      3: [
         "Respecting slaves' value at Mount Vernon",
         'Civil rights activist shares legacy of love, community and action amid anecdotes of working with Dr. Martin Luther King Jr.',

      ],
      4: [
         'Miramar pauses to acknowledge selfless service of Tuskegee Airmen',
        'Elayne Arrington',
        'Vance Marchbanks Jr.',
      ]
    }}
    highlightText={{
      0: "Mentions of cultural celebrations like Black History Month, Juneteenth, and MLK Day are gone.",
      1: "So are mentions of soliders that call out their Blackness",
      2: "Artifacts of Black culture, like soul food and gospel music, are also removed.",
      3: "And the purge has even extended to basic facts of Black history, like slavery and civil rights activism.",
      4: "Again, military heroes have been erased simply for being Black."
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
