<footer>
    <div class="line"></div>
    <div class="footer-content">
        <p class = 'attribution'>Created by Michael Cahana. All code for this project can be viewed on <a href = 'https://github.com/m-cahana/pentagon_dei_purge'>GitHub</a>.</p>

        <h2>Methodology</h2>
        <p class = 'methodology'>
            Photo data was scraped as a .json file from the AP's <a href = 'https://flo.uri.sh/visualisation/21970718/embed?auto=1'>database</a>. You can see the raw dataset at <a href = 'https://github.com/m-cahana/pentagon_dei_purge/blob/main/data/raw/photos.json'>this link</a>.
        </p>

        <p class = 'methodology'>
            To clean the dataset, I ommitted titles that had no meaningful text in them. In practice, that meant removing titles that only consisted of a single word, filled with numbers, like "141006-M-RY817-003". These titles could never be interpreted in any meaningful way. To compute top keywords, I simply counted the number of times each word, or word combinations, appeared in website titles. 
        </p>

        <p class = 'methodology'>
            To classify websites into identity groups and content types, I used Open AI's large language model, GPT-4o-mini, accessed via Python through the <a href = 'https://openai.com/api/'>OpenAI API</a>. I developed prompts to classify websites appropriately, which can be found <a href = 'https://github.com/m-cahana/pentagon_dei_purge/blob/main/data/python/cluster.py'>here</a>. I then manually reviewed a sample of 100 classifications to ensure the LLM was performing as expected. I also, separately, tried a few more traditional text clustering methods (like generating text embeddings, measuring distances between titles, and grouping titles using k-means clustering), but found the LLM to be far more accurate, especially when it came to classifying titles whose meanings weren't immediately obvious (like "Eric Fanning", the former Secretary of the Army, and first openly gay leader of a U.S. military service).
        </p>

        <p class = 'methodology'>
            To put together scrolling tiles that move against a fixed background, I used a <a href = 'https://github.com/the-pudding/svelte-starter'>Svelte starter template developed by the Pudding</a>. 
        </p>
    </div>
</footer>

<style>
    footer {
        padding: 2rem 5%;
        margin-top: 2rem;
    }

    p {
        font-size: 14px;
        text-align: left;
    }

    .attribution {
        font-style: italic;
    }

    .methodology {
        padding-left: 1rem;
    }

    h2 {
        font-size: 18px;
        font-family: "Helvetica";
        font-weight: 300;
        font-style: italic;
        margin-bottom: 1rem;
        text-align: left;
    }

    .line {
        border-top: 1px solid black;
        width: 100%;
        margin-bottom: 1rem;
    }

    .footer-content {
        font-family: "Helvetica";
        font-weight: 300;
        text-align: center;
    }

</style> 