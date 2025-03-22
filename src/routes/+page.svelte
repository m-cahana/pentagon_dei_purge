<script>
	import TitleScrolly from "$lib/components/title_scrolly.svelte";
    import Footer from "$lib/components/footer.svelte";
    import TopWordList from "$lib/components/top_word_list.svelte";
    import TitleSearch from "$lib/components/title_search.svelte";
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
	<h1>What's the Trump Administration Trying to Erase Through Its DEI Purge?</h1>
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
        Looking through these top phrases and some additional, less common ones, I figured that websites can be grouped into a handful of different identity groups: 
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

    To classify each website into one of these groups, I used a large language model, which has enough contextual knowledge to recognize that titles like "Jackie Robinson" or "Tuskegee Airmen" are related to Black people, even though they don't explicitly have "black" in their text. After manually reviewing a sample of 100 classifications, I found that the LLM was consistently choosing groups that I would have chosen myself. Here are all websites, classified by identity group according to their title: 

    </p>    


    <ThemeCirclePack
        maxScaleValue = 10_000
     />

    <p>
        It's instructive to dig into a sample of websites that all relate to the same group. What you find is that there are a few different types of content within each group. Consider this sample of websites about Black people, for example:
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
        'Americans of all colors contributed to civil rights movement',
        'Martin Luther King Jr. special observance',
        '2nd Annual Soul Food Taste',
        'Vance Marchbanks Jr.',
        'Display About Slavery',
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
        'Airmen sample soul food',
        'Gospel celebration',
        '2nd Annual Soul Food Taste',
      ],
      2: [
        'African American/Black Innovations ... where would we be without them?',
        'FACES of MCIPAC - African American U.S. Marines share their stories',
      ],
      3: [
         'Miramar pauses to acknowledge selfless service of Tuskegee Airmen',
        'Elayne Arrington',
        'Vance Marchbanks Jr.',
      ],
      4: [
         "Respecting slaves' value at Mount Vernon",
         'Civil rights activist shares legacy of love, community and action amid anecdotes of working with Dr. Martin Luther King Jr.',
         'Display About Slavery',
         'Americans of all colors contributed to civil rights movement',
      ],
    }}
    highlightText={{
      0: ["Explicit heritage events", "Mentions of holidays like Black History Month, Juneteenth, and MLK Day are gone."],
      1: ["Everyday celebrations of heritage and identity", "So are artifacts of Black culture, like soul food and gospel music."],
      2: ["Mentions of personnel that highlight their identity", "When soldiers are referred to in a way that calls out their Blackness, their web footprint is removed."],
      3: ["Personel whose identity isn't explicitly mentioned", "And even when their Blackness isn't mentioned, military heroes have been erased simply for being Black."],
      4: ["Facts of history that relate to Black people", "The administration's DEI purge has extended to basic facts of Black history as well, like slavery and civil rights activism."],
    }}
  />
  
    <p>
    These few types of content come up again and again when you investigate websites of specific group:
    
    </p>

    <ol>
        <li><span class = 'highlight'>Explicit heritage and DEI events</span></li>
        <li><span class = 'highlight'>Everyday celebrations</span> of heritage and identity</li>
        <li>Mentions of <span class = 'highlight'>military personnel that highlight their identity</span> </li>
        <li>Mentions of <span class = 'highlight'>military personnel that belong to a specific identity group</span>, even though that's <span class = 'highlight'>not explicitly mentioned</span> </li>
        <li><span class = 'highlight'>Facts of history</span> that relate to a specific identity group</li>
        
    </ol>

    <p>
    So, I figured I'd classify websites based on whether their content belongs to one of these types. Again, I used a large language model to do this. Here are websites broken downby content type:

    </p>

    <ThemeCirclePack 
        classSuffix = 'type'
        groupByColumn = 'type' 
        highlightMap = {{
            0: ["Explicit heritage and DEI events"], 
            1: ["Other"], 
            2: ["Everyday celebrations", "Military personnel - identity mentioned"], 
            3: ["Military personnel - no stated identity", "Facts of history"]
        }}
        scrollContent = {{
            0: "Heritage and DEI events are by far the most common content type targeted for removal.",
            1: "And there's a large share of websites that don't belong to any predefined type.",
            2: "But there are also a meaningful number of sites taken down, seemingly, just because they describe people as belonging to minority groups.",
            3: 'And a fair amount of sites taken down simply for mentioning people that happen to be members of minority groups, or mentioning facts that relate to the history of minority groups.',
        }}
    />

    <p>
    These last two categories - facts of history, and military personnel with no identity stated - are the most striking. They suggest for the Trump administration, purging DEI content isn't just about erasing programming that celebrates diversity. It's about cutting down on the footprint of certain types of people. Consider purged websites about military personnel whose identity isn't explicitly stated:

    </p>

    <TitleScrolly 
    titlesList={
      [
        'Vance Marchbanks Jr.',
        'Clarence D. "Lucky" Lester',
        'Roy LaGrone',
        'Maj. Gen. Alfred K. Flowers', 
        'Hazel Ying Lee',
        'Army Pfc. Joe Nishimoto',
        'The 442nd',
        'Marine Corps Heroes: Lt. Kurt Chew-Een Lee',
        'Marine Corps Heroes: Pfc. Harold Gonsalves',
        'SECDEF Chief of Staff Chief of Staff Eric Fanning at DIA',
        'Jason Strong',
        'Brig. Gen. Stayce Harris',
        'Maj. Gen. Marcelite Harris'
      ]}
    highlightMap={{
      0: [
        'Vance Marchbanks Jr.',
        'Clarence D. "Lucky" Lester',
        'Roy LaGrone',
        'Maj. Gen. Alfred K. Flowers', 
      ],
      1: [
        'Hazel Ying Lee',
        'Army Pfc. Joe Nishimoto',
      ],
      2: [
        'The 442nd',
        'Marine Corps Heroes: Lt. Kurt Chew-Een Lee',
      ],
      3: [
        'Marine Corps Heroes: Pfc. Harold Gonsalves',
      ],
      4: [
         'SECDEF Chief of Staff Chief of Staff Eric Fanning at DIA',
      ],
      5: [
        'Maj. Gen. Marcelite Harris'
      ],
    }}
    highlightText={{
      0: ["", "Vance Marchbanks Jr., Clarence D. Lester, Roy Lagrone, and Alfred K. Flowers were all Tuskegee Airmen - the first Black aviators force in the U.S. military."],
      1: ["", "Joe Nishimoto - born to Japaense immigrant parents - won the Medal of Honor; Kurt Chew-Een Lee was the first Asian American to be a commissioned as a regular officer in the Marine Corps."],
      2: ["", "Hazel Ying Lee was one of only two Chinese American Women Airforce Service Pilots during WWII; the 442nd regiment consisted almost entirely of Japanese Americans."],
      3: ["", "Harold Gonsalves was a Portugese-American, and among the earliest Hispanic Marines to receive the Medal of Honor."],
      4: ["", "Eric Fanning was the first openly gay leader of a U.S. military service. This website describes him attending a meeting at the Defense Intelligence Agency."],
      5: ["", "Marcelite Harris became the first Black female General Officer in the U.S. Air Force."],
    }}
  />

  <p>
    As people have started to notice military heroes gone missing online, outrage has grown, and in some cases the Pentagon has retracted its steps. Some websites about Jackie Robinson, the Navajo code talkers, and the Tuskegee Airmen, for example, have been <a href = 'https://www.npr.org/2025/03/20/nx-s1-5334461/pentagon-black-veterans-navajo-code-talkers-website-diversity'>restored</a>. But the purge is quite widespread in its reach, erasing the memories of hundreds of soldiers, many of whom have received less attention so far. And the purge itself tells of what this administration does when uninhibited - which military stories it seeks to erase before public backlash forces some reversals. 
  </p>

  <p>
    You can see too that, even when the Administration buckles and restores some websites, it keeps others erased. Some websites about Jackie Robinson were restored, for example, but you can see in the database below that other websites describing Jackie Robinson movies remain dead (as of March 21st at least).
  </p>

  <p>
    The database below displays all of the Pentagon's purged websites, broken down by group and content type (this dataset's also available for download as a <a href = 'https://github.com/m-cahana/pentagon_dei_purge/blob/main/static/data/cleaned_titles_with_themes.csv'>csv</a>). There are many more striking examples of purged content to be found here - too many to list comprehensively. But by way of example, it's worth noting that a number of websites related to Holocaust survivors (content type: facts of history)have been removed. All have been purged, suggesting that this administration doesn't think these stories, and these people, belong in the military.
    </p>

    <TitleSearch />

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
