<script>
	import TitleScrolly from "$lib/components/title_scrolly.svelte";
    import Footer from "$lib/components/footer.svelte";
    import TopWordList from "$lib/components/top_word_list.svelte";
    import TitleSearch from "$lib/components/title_search.svelte";
    import PieChart from "$lib/components/pie_chart.svelte";
    import { themeColors, typeColors } from '$lib/utils/color_schemes';

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

<svelte:head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</svelte:head>

<main>
	<h1>What's the Trump Administration Trying to Erase Through Its DEI Purge?</h1>
    <div class="subtitle">March 2025</div>

    <p>
        On the first day of his second term in office, President Trump signed an <a href = 'https://www.whitehouse.gov/presidential-actions/2025/01/ending-radical-and-wasteful-government-dei-programs-and-preferencing/' target="_blank" rel="noopener noreferrer">executive order</a> calling for an end to government DEI programs, which he categorized as "radical", "wasteful", and the cause of "shameful discrimination". In turn, the Pentagon released a <a href = 'https://www.defense.gov/News/News-Releases/News-Release-View/Article/260000/pentagon-to-end-radical-and-wasteful-dei-programs-and-preferencing-in-the-defense-department/' target="_blank" rel="noopener noreferrer">memorandum</a> calling for a "digital content refresh" across all Department of Defense public platforms. Any articles, photos, and videos promoting DEI were ordered to be removed by March 5th.
    </p>

    <p>
        By March 7th, the Pentagon had flagged 26,000 images for removal across websites from every branch of the military. Outlets quickly noted that websites about the <a href = 'https://apnews.com/article/dei-purge-images-pentagon-diversity-women-black-8efcfaec909954f4a24bad0d49c78074' target="_blank" rel="noopener noreferrer">Tuskegee Airmen</a>, <a href = 'https://www.washingtonpost.com/investigations/2025/03/17/pentagon-dei-native-american-iwo-jima/' target="_blank" rel="noopener noreferrer">Navajo code talkers</a> and <a href = 'https://www.axios.com/2025/03/19/jackie-robinson-military-service-webpage-dod-dei' target="_blank" rel="noopener noreferrer">Jackie Robinson</a> were among the sites purged. Websites about <a href = 'https://www.forbes.com/sites/conormurray/2025/03/07/enola-gay-aircraft-and-other-historic-items-inaccurately-targeted-under-pentagons-anti-dei-purge/' target="_blank" rel="noopener noreferrer">Enola Gay</a> - the aircraft that dropped an atomic bomb on Hiroshima - were also removed, presumably because they were mistakenly flagged as LGBTQ+ content. 
    </p>

    <p>
        Although these examples have captured attention, to my knowledge someone's yet to run a comprehensive analysis to categorize purged websites. I try to do that here. By systematically categorizing websites the Trump administration has purged, I think we can better understand the full breadth of stories the administration considers unfitting for the military. 
    </p>

    <p>
        Since most website urls are now defunct, this analysis relies on website titles, which were preserved in an <a href = 'https://flo.uri.sh/visualisation/21970718/embed?auto=1' target="_blank" rel="noopener noreferrer">AP database</a>. To start simply, I checked the most common phrases among website titles:
    </p>

    <br>

    <TopWordList />

    <p>
        Looking through these top phrases and some additional, less common ones, I figured that websites could be categorized into a handful of different identity groups: 
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

    To classify each website into one of these groups, I used a large language model, which has enough contextual knowledge to recognize that titles like "Jackie Robinson" or "Tuskegee Airmen" are related to Black people, even though they don't explicitly have "black" in their text. After manually reviewing a sample of 100 classifications, I found that the model was consistently choosing groups I would have chosen myself. Here are all websites, classified by identity group according to their title: 

    </p>    


    <PieChart
        colorScheme = {themeColors}
     />

    <p>
        It's instructive to dig into a sample of websites that all relate to the same group. What you find is that there are a few different types of content within each group. Consider this sample of websites about Black people, for example:
      </p>

    <TitleScrolly 
    titlesList={
      [
        'Observance for Black History Month',
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
        "Respecting slaves' value at Mount Vernon",
        'Miramar pauses to acknowledge selfless service of Tuskegee Airmen',
        'Elayne Arrington'
      ]}
    highlightMap={{
      0: [
        'Observance for Black History Month',
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
         'Display About Slavery',
         'Americans of all colors contributed to civil rights movement',
      ],
    }}
    highlightText={{
      0: ["Explicit heritage events", "Mentions of holidays like Black History Month, Juneteenth, and MLK Day are gone."],
      1: ["Everyday celebrations of heritage and identity", "So are artifacts of Black cultural celebration, like soul food and gospel music."],
      2: ["Mentions of personnel that highlight their identity", "Soldiers referred to in a way that calls out their Blackness are removed."],
      3: ["Personel whose identity isn't explicitly mentioned", "And even when their Blackness isn't mentioned soldiers have been erased from web records seemingly just for being Black."],
      4: ["Facts of history that relate to Black people", "The administration's DEI purge has extended to basic facts of Black history as well, like slavery and civil rights activism."],
    }}
  />
  
    <p>
    These few types of content come up again and again when you investigate websites of a specific identity group. To state the categories more generally, they are:
    
    </p>

    <ol>
        <li><span class = 'highlight'>Explicit heritage and DEI events</span></li>
        <li><span class = 'highlight'>Everyday celebrations</span> of heritage and identity</li>
        <li>Mentions of <span class = 'highlight'>military personnel that highlight their identity</span> </li>
        <li>Mentions of <span class = 'highlight'>military personnel that belong to a specific identity group</span>, even though that's <span class = 'highlight'>not explicitly mentioned</span> </li>
        <li><span class = 'highlight'>Facts of history</span> that relate to a specific identity group</li>
        <li>Content belonging to some <span class = 'highlight'>other</span> category</li>
        
    </ol>

    <p>
    To better understand the scope of the adminsitration's purge, I categorized each website into one of these content types as well. Again, I used a large language model to do this. Here are websites broken down by content type:

    </p>

    <PieChart 
        classSuffix = 'type'
        groupByColumn = 'type' 
        colorScheme = {typeColors}
        highlightMap = {{
            0: ["Explicit heritage and DEI events"], 
            1: ["Other"], 
            2: ["Everyday celebrations", "Military personnel - identity mentioned"], 
            3: ["Military personnel - no stated identity", "Facts of history"]
        }}
        scrollContent = {{
            0: "Heritage and DEI events are by far the most common content type targeted for removal.",
            1: "And there's a large share of websites that don't belong to any predefined type.",
            2: "But there are also a meaningful number of sites taken down, seemingly, because they describe people as belonging to minority identity groups.",
            3: 'And hundreds of sites taken down, seemingly, because they simply mention soldiers that happen to have certain identities, or mention facts relating to the history of certain identity groups.',
        }}
    />

    <p>
    These last two categories - facts of history, and military personnel with no identity stated - are the most striking. They suggest that for the Trump administration, purging DEI content isn't just about erasing programming that celebrates diversity, strives for equity, or promotes inclusion. It seems to be about erasing the footprints of certain types of people, many of whose lives played out long before DEI programs entered the military. Consider these purged websites, for example, about military personnel whose identity isn't explicitly stated:

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
        'Maj. Gen. Marcelite Harris',
        'Cmdr. John Herrington'
      ]}
    highlightMap={{
      0: [
        'Vance Marchbanks Jr.',
        'Clarence D. "Lucky" Lester',
        'Roy LaGrone',
        'Maj. Gen. Alfred K. Flowers', 
      ],
      1: [
        'Army Pfc. Joe Nishimoto',
      ],
      2: [
        'Marine Corps Heroes: Lt. Kurt Chew-Een Lee',
      ],
      3: [
        'The 442nd',
      ],
      4: [
        'Hazel Ying Lee',
      ],
      5: [
        'Marine Corps Heroes: Pfc. Harold Gonsalves',
      ],
      6: [
         'SECDEF Chief of Staff Chief of Staff Eric Fanning at DIA',
      ],
      7: [
        'Cmdr. John Herrington'
      ],
      8: [
        'Maj. Gen. Marcelite Harris'
      ],
    }}
    highlightText={{
      0: ["", "Vance Marchbanks Jr., Clarence D. Lester, Roy Lagrone, and Alfred K. Flowers were all Tuskegee Airmen - the first Black aviators in the U.S. military, who fought during WWII."],
      1: ["", "Joe Nishimoto - born to Japanese immigrant parents - died in 1944, and received the Medal of Honor posthumously."],
      2: ["", "Kurt Chew-Een Lee fought in World War II, the Korean War, and the Vietnam War, and was the first Asian American to be a commissioned as a regular officer in the Marine Corps."],
      3: ["", "The 442nd regiment was a WWII unit that consisted almost entirely of Japanese Americans."],
      4: ["", "Hazel Ying Lee was one of only two Chinese American Women Airforce Service Pilots during WWII."],
      5: ["", "Harold Gonsalves was a Portugese-American, and among the earliest Hispanic Marines to receive the Medal of Honor. He received the award for jumping on a grenade to save the lives of two fellow Marines."],
      6: ["", "Eric Fanning was Secretary of the Army under President Obama, and the first openly gay leader of a U.S. military service. This website described him attending a meeting at the Defense Intelligence Agency."],
      7: ["", "John Herrington is a retired Naval aviator and former NASA astronaut, who in 2002 became the first Native American to fly in space."],
      8: ["", "Marcelite Harris served in Vietnam, and became the first Black female General Officer in the U.S. Air Force."],
    }}
  />

  <p>
    As people have started to notice military heroes gone missing online, outrage has grown, and in some cases the Pentagon has retraced its steps. Websites about Jackie Robinson, the Navajo code talkers, and the Tuskegee Airmen, for example, have been <a href = 'https://www.npr.org/2025/03/20/nx-s1-5334461/pentagon-black-veterans-navajo-code-talkers-website-diversity' target="_blank" rel="noopener noreferrer">restored</a>. But the purge is quite widespread in its reach, erasing digital traces of hundreds of soldiers, many of whom haven't received attention yet. 
  </p>

  <p>
    And you can see here that even when the Administration buckles and restores some websites, it keeps other related content erased. Some websites about Jackie Robinson were restored, for example, but the database below shows that other websites describing Jackie Robinson movies remain defunct (as of March 21st at least).
  </p>

  <p>
    This database displays all of the Pentagon's purged websites, broken down by identity group and content type (this dataset's also available for download as a <a href = 'https://github.com/m-cahana/pentagon_dei_purge/blob/main/static/data/cleaned_titles_with_themes_and_types.csv' target="_blank" rel="noopener noreferrer" >csv</a>). There are many more striking examples of purged content to be found in it - too many to list comprehensively. But here are a few: websites about Vietnamese refugees, immigrants-turned-soldiers, and Holocaust survivors. All have been purged, suggesting that this administration doesn't think these stories, and these people, belong in the military.

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
