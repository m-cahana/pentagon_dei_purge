<script>
	import TitleScrolly from "$lib/components/title_scrolly.svelte";
    import Footer from "$lib/components/footer.svelte";
    import TopWordList from "$lib/components/top_word_list.svelte";
    
    import ThemeCirclePack from "$lib/components/theme_circle_pack.svelte";
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
	<h1>What Exactly Is the Trump Administration Trying to Erase Through Its DEI Purge?</h1>
    <div class="subtitle">March 2025</div>

    <p>
        On the first day of his second term in office, President Trump signed an <a href = 'https://www.whitehouse.gov/presidential-actions/2025/01/ending-radical-and-wasteful-government-dei-programs-and-preferencing/'>executive order</a> calling for an end to government DEI programs, which he categorized as "radical", "wasteful", and the cause of "shameful discrimination". In turn, the Pentagon released a <a href = 'https://www.defense.gov/News/News-Releases/News-Release-View/Article/260000/pentagon-to-end-radical-and-wasteful-dei-programs-and-preferencing-in-the-defense-department/'>memorandum</a> calling for a "digital content refresh" across all Department of Defense public platforms. Any articles, photos, and videos promoting DEI were ordered to be removed by March 5th.
    </p>

    <p>
        By March 7th, the Pentagon had flagged 26,000 images for removal across websites from every branch of the military. Outlets quickly noted that websites about the <a href = 'https://apnews.com/article/dei-purge-images-pentagon-diversity-women-black-8efcfaec909954f4a24bad0d49c78074'>Tuskegee Airmen</a>, <a href = 'https://www.washingtonpost.com/investigations/2025/03/17/pentagon-dei-native-american-iwo-jima/'>Navajo code talkers</a> and <a href = 'https://www.axios.com/2025/03/19/jackie-robinson-military-service-webpage-dod-dei'>Jackie Robinson</a> were among the sites purged. Websites about <a href = 'https://www.forbes.com/sites/conormurray/2025/03/07/enola-gay-aircraft-and-other-historic-items-inaccurately-targeted-under-pentagons-anti-dei-purge/'>Enola Gay</a> - the aircraft that dropped an atomic bomb on Hiroshima - were also removed, presumably because they were mistakenly flagged as LGBTQ+ content. 
    </p>

    <p>
        I thought I'd take a closer look into all the websites that were purged, to categorize the kind of content the Pentagon is targeting for removal, and systematically determine what kinds of stories the Trump administration considers unfitting for the military. Most website urls are now defunct, so I investigated website titles, which were preserved in an <a href = 'https://flo.uri.sh/visualisation/21970718/embed?auto=1'>AP database</a>. I started by checking the most common phrases in titles:
    </p>

    <br>

    <TopWordList />

    <p>
        Looking through these top phrases and some additional, less common ones, it seems that websites can be grouped into a handful of different themes: 
    </p>

    <ol>
        <li>Websites related to <span class = 'highlight'>women</span></li>
        <li>Websites related to <span class = 'highlight'>Black</span> people</li>
        <li>Websites related to <span class = 'highlight'>Hispanic</span> people</li>
        <li>Websites related to <span class = 'highlight'>Asian Americans or Pacific Islanders</span></li>
        <li>Websites related to <span class = 'highlight'>Native Americans</span></li>
        <li>Websites related to <span class = 'highlight'>LGBTQ+</span> people</li>
        <li>Websites related to <span class = 'highlight'>other ethnicities & religions</span></li>
        <li>Websites related to <span class = 'highlight'>generic DEI</span> content</li>
        <li>Websites belonging to some <span class = 'highlight'>other</span> category.</li>
        
    </ol>

    <p>

    To classify each website into one of these themes, I used OpenAI's large language model, GPT-4o-mini. This LLM has enough contextual knowledge to recognize that titles like "Jackie Robinson" or "Tuskegee Airmen" are related to Black people, even though they don't explicitly have "black" in their text. After manually reviewing a sample of 100 classifications, I found that the LLM was consistently choosing the themes that I would have chosen myself. Here are all websites, classified by theme according to their title: 

    </p>    


    <ThemeCirclePack />

    <p>
        It's instructive to dig into a sample of websites that all fall under the same theme. What you find is that there are a few different types of content within a thematic category. Consider this sample of websites about Black people, for example:
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
      0: ["Erasure of Cultural Celebrations", "Mentions of cultural celebrations like Black History Month, Juneteenth, and MLK Day are gone."],
      1: ["Black Soldiers Removed", "So are mentions of soldiers that call out their Blackness"],
      2: ["Cultural References Purged", "Artifacts of Black culture, like soul food and gospel music, are also removed."],
      3: ["Historical Facts Deleted", "And the purge has even extended to basic facts of Black history, like slavery and civil rights activism."],
      4: ["Military Heroes Erased", "Again, military heroes have been erased simply for being Black."]
    }}
  />

  <p>
    These few types of content come up again and again when you investigate websites of specific themes. I classified each website into one of these types to understand how frequently each one comes up. Here are websites by content type:
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

    ol {
        text-align: left;
        margin-left: 2rem;
        font-family: "Helvetica";
        font-weight: 300;
    }
    
    ol li {
        margin-bottom: 0.75rem;
    }

    .highlight {
        font-weight: 550;
        text-decoration: underline;
        padding: 0 1px;
    }

</style>
