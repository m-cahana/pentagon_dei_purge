<script lang="ts">
    import * as d3 from 'd3';
    import { onMount } from 'svelte';
    import Scrolly from "$lib/components/helpers/scrolly.svelte";
    import { getFullPath } from '$lib/utils/paths';
    
    // Props for customization
    let {
        dataPath = '/data/cleaned_titles_with_themes_and_types.csv', // Path to the data file
        colorScheme = {
            "Women": "#FF5A5F",           // Pink-red
            "Black": "#484848",           // Dark grey
            "Hispanic": "#FFB400",        // Amber/gold
            "Asian or Pacific Islander": "#00A699", // Teal
            "Native American": "#FC642D", // Orange
            "LGBTQ+": "#7B0051",          // Purple
            "Generic DEI": "#00D1C1",     // Light teal
            "Other": "#8F8F8F"            // Medium grey
            // Add more mappings as needed
        },
        // Fallback colors if no mapping exists for a category
        fallbackColorArray = [
            "#98abc5", "#8a89a6", "#7b6888", "#6b486b", "#a05d56", "#d0743c", "#ff8c00"
        ],
        // New prop to specify which column to use for grouping
        groupByColumn = 'theme', // Default to 'theme', can be changed to 'type' or any other column
        // New prop to add a suffix to CSS class names to avoid conflicts
        classSuffix = '', // Default to empty string (no suffix)
        // New props for scrolly content
        scrollContent = {
            0: "The largest groups targeted by the Pentagon's DEI purge are women and Black people.",
            1: "Asian Americans, Pacific Islanders, and Hispanic people trail not too far behind.",
            2: "Native Americans and LGBTQ+ people are also significant targets.",
            3: 'There are a fair amount of websites that relate to generic DEI content, like websites that discuss "diversity" or "inclusion" without mentioning any specific groups.',
            4: "And there's a large segment of websites that don't belong to any of the defined groups. These websites' titles alone aren't very informative. If their full content wasn't already purged, I suspect we'd find these websites were targeted because they related to a specific group."
        },
        // Add highlightMap prop to specify which items to highlight at each step
        highlightMap = {
            0: ["Women", "Black"], // Example: highlight "Women" and "Black" themes
            1: ["Hispanic", "Asian or Pacific Islander"], // Example: highlight Hispanic and API themes
            2: ["Native American", "LGBTQ+"], // Example: highlight Native American and LGBTQ+ themes
            3: ["Generic DEI"], 
            4: ["Other"]
        }
    } = $props();
    
    // Extract section indices from scrollContent
    let sectionIndices = $derived(Object.keys(scrollContent).map(Number).sort((a, b) => a - b));
    
    // Add proper type for container to fix "implicit any" error
    let container: HTMLDivElement;
    let width: number;
    let height: number;
    
    // Define proper type for data structure
    interface DataItem {
        label: string;
        value: number;
        percentage: string;
        formattedCount: string;
    }
    
    let data: DataItem[] = [];
    let value = $state(0);
    let svg: any;
    let pie: any;
    let arc: any;
    let outerArc: any;
    let radius: number;
    let color: d3.ScaleOrdinal<string, string, never>;
    
    // Define type for color scheme
    type ColorSchemeType = string[] | {[key: string]: string};
    
    interface RawDataItem {
        title: string;
        theme: string;
        type: string;
        [key: string]: any;
    }
    
    // Function to handle window resize
    function handleResize() {
        updateVisualizationSize();
        if (data.length > 0) {
            createVisualization();
        }
    }
    
    // Function to update visualization dimensions based on container size
    function updateVisualizationSize() {
        if (!container) return;
        
        const containerRect = container.getBoundingClientRect();
        width = containerRect.width;
        height = containerRect.height;
        
        // Ensure minimum dimensions
        width = Math.max(width, 300);
        height = Math.max(height, 400);
        
        // Calculate radius based on container size
        radius = Math.min(width, height) / 2 * 0.8;
    }

    // Helper function to calculate label distance factor based on screen size
    function getLabelDistanceFactor(): number {
        // On smaller screens, bring labels closer to the donut
        if (width < 480) {
            return 0.7; // Much closer to donut on very small screens
        } else if (width < 768) {
            return 0.8; // Closer to donut on small screens
        } else {
            return 1.0; // Normal distance on larger screens
        }
    }

    // Helper function to format numbers with commas
    function formatNumber(num: number): string {
        return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    }

    onMount(() => {
        // Initialize size based on container
        updateVisualizationSize();
        
        // Add resize listener
        window.addEventListener('resize', handleResize);
        
        // Use our utility function to handle the path from props
        const fullDataPath = getFullPath(dataPath);
        console.log(`Loading data from: ${fullDataPath}`);
        
        // Load and process the data
        d3.csv(fullDataPath)
            .then(processData)
            .then(createVisualization)
            .catch((error: any) => {
                console.error("Error loading CSV:", error);
            });
            
        // Clean up event listeners on component destruction
        return () => {
            window.removeEventListener('resize', handleResize);
        };
    });

    // Process the CSV data into format for donut chart
    function processData(csvData: RawDataItem[]) {
        // Group titles by the specified column
        const dataGroups = d3.group(csvData, (d: RawDataItem) => d[groupByColumn] || "Unknown");

        const totalItems = csvData.length;
        
        // Convert to array structure for pie chart
        data = Array.from(dataGroups, ([groupValue, items]) => ({
            label: groupValue,
            value: items.length,
            percentage: (items.length / totalItems * 100).toFixed(1),
            formattedCount: formatNumber(items.length)
        }));
        
        // Sort by size (descending)
        data.sort((a, b) => b.value - a.value);
        
        return data;
    }

    // Function to normalize group names for CSS class names
    function normalizeForCSS(name: string): string {
        // Replace spaces with hyphens, remove + character, and convert to lowercase
        return name.replace(/\s+/g, '-').replace(/\+/g, '').toLowerCase();
    }
    
    // Function to create a CSS class name with optional suffix
    function createClassName(prefix: string, name: string): string {
        const normalizedName = normalizeForCSS(name);
        // Add suffix if provided, otherwise just use the normalized name
        return `${prefix}-${normalizedName}${classSuffix ? `-${classSuffix}` : ''}`;
    }

    // Helper function to calculate middle angle of a pie slice
    function midAngle(d: any): number {
        return d.startAngle + (d.endAngle - d.startAngle) / 2;
    }

    // Function to prevent label overlapping
    function preventLabelOverlap(labels: any[], radius: number, maxLabelWidth: number): void {
        // First, estimate how many lines each label will need
        labels.forEach(label => {
            const text = `${label.data.label} (${label.data.formattedCount} websites - ${label.data.percentage}%)`;
            const words = text.split(/\s+/);
            
            // Create a temporary text element to measure text dimensions
            const tempText = document.createElement('span');
            // Use the same font properties as defined in CSS
            tempText.style.font = 'var(--label-font-weight, 500) var(--label-font-size, 12px) var(--label-font-family, "Helvetica Neue", Arial, sans-serif)';
            tempText.style.position = 'absolute';
            tempText.style.visibility = 'hidden';
            tempText.style.whiteSpace = 'nowrap';
            document.body.appendChild(tempText);
            
            // Estimate how many lines this text will need
            let currentLine = '';
            let lineCount = 1;
            
            for (const word of words) {
                const testLine = currentLine + (currentLine ? ' ' : '') + word;
                tempText.textContent = testLine;
                
                // If this line is too long, start a new line
                if (tempText.offsetWidth > maxLabelWidth) {
                    if (currentLine === '') {
                        // Even a single word is too long, but we have to keep it
                        currentLine = word;
                    } else {
                        currentLine = word;
                        lineCount++;
                    }
                } else {
                    currentLine = testLine;
                }
            }
            
            // Clean up
            document.body.removeChild(tempText);
            
            // Store estimated line count
            label.estimatedLines = lineCount;
            // Calculate estimated height based on line count and line height
            // Get computed font size from CSS variable or use default
            const fontSize = parseInt(getComputedStyle(document.documentElement).getPropertyValue('--label-font-size') || '12px');
            const lineHeight = parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--label-line-height') || '1.3');
            label.estimatedHeight = lineCount * lineHeight * fontSize;
        });
        
        // Now sort labels by vertical position
        const leftLabels = labels.filter(l => l.x < 0).sort((a, b) => a.y - b.y);
        const rightLabels = labels.filter(l => l.x > 0).sort((a, b) => a.y - b.y);
        
        // Process each side separately
        [leftLabels, rightLabels].forEach(sidedLabels => {
            // Adjust overlapping labels
            for (let i = 0; i < sidedLabels.length - 1; i++) {
                const currentLabel = sidedLabels[i];
                const nextLabel = sidedLabels[i + 1];
                
                // Calculate vertical space needed
                const currentHeight = currentLabel.estimatedHeight;
                const nextHeight = nextLabel.estimatedHeight;
                
                // Minimum vertical distance needed between label centers
                const minDistance = (currentHeight + nextHeight) / 2 + 8; // 8px extra padding
                
                // Calculate actual distance
                const actualDistance = nextLabel.y - currentLabel.y;
                
                // If labels are too close
                if (actualDistance < minDistance) {
                    // Move the next label down by the required amount
                    const offset = minDistance - actualDistance;
                    nextLabel.y += offset;
                    
                    // If the adjusted position goes outside the chart area,
                    // try to adjust both labels (move current up, next down)
                    const maxY = radius * 0.9;
                    if (Math.abs(nextLabel.y) > maxY) {
                        // Calculate how much we need to adjust
                        const excess = Math.abs(nextLabel.y) - maxY;
                        // Move current label up and next label down to distribute the adjustment
                        currentLabel.y -= excess / 2;
                        nextLabel.y = Math.sign(nextLabel.y) * maxY;
                    }
                }
            }
        });
    }

    // Function to wrap text into multiple lines
    function wrapText(text: d3.Selection<any, any, any, any>, maxWidth: number) {
        text.each(function(d: any) {
            const text = d3.select(this);
            const words = text.text().split(/\s+/);
            // Use CSS variable or default to 1.3
            const lineHeight = parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--label-line-height') || '1.3');
            
            let line: string[] = [];
            let lineNumber = 0;
            let tspan = text.text(null).append("tspan")
                .attr("x", 0)
                .attr("dy", 0);
            
            for (const word of words) {
                line.push(word);
                tspan.text(line.join(" "));
                
                if (tspan.node()?.getComputedTextLength() > maxWidth) {
                    line.pop(); // Remove the word that caused overflow
                    
                    // If there are words in line, create a line with them
                    if (line.length) {
                        tspan.text(line.join(" "));
                        line = [word]; // Start a new line with the overflow word
                    } else {
                        // If no words, this single word is too long, add it anyway and truncate with ellipsis later if needed
                        line = [word];
                    }
                    
                    // Create a new line for the next set of words
                    lineNumber++;
                    tspan = text.append("tspan")
                        .attr("x", 0)
                        .attr("dy", `${lineHeight}em`)
                        .text(line.join(" "));
                }
            }
            
            // Center the text vertically based on number of lines
            const totalLines = lineNumber + 1;
            if (totalLines > 1) {
                text.selectAll("tspan")
                    .attr("dy", (_: any, i: number) => `${i === 0 ? -(totalLines - 1) * lineHeight / 2 : lineHeight}em`);
            }
            
            // Store actual line count for future reference
            d.actualLines = totalLines;
        });
    }

    // Function to highlight groups based on current scroll position
    function highlightGroups(currentValue: number) {
        if (!svg) return;
        
        // Get groups to highlight for this scroll position
        const groupsToHighlight = getGroupsToHighlight(currentValue);
        
        // Reset all slices and labels to non-highlighted state
        svg.selectAll(".slice")
            .classed("highlighted", false)
            .classed("dimmed", true);
            
        svg.selectAll("text.label")
            .classed("highlighted", false)
            .classed("dimmed", true);
            
        svg.selectAll("path.connector")
            .classed("highlighted", false)
            .classed("dimmed", true);
        
        // Then, highlight the specific groups
        if (groupsToHighlight.length > 0) {
            groupsToHighlight.forEach(groupName => {
                // Highlight slices
                svg.selectAll(`.${createClassName('slice', groupName)}`)
                    .classed("highlighted", true)
                    .classed("dimmed", false);
                    
                // Highlight labels
                svg.selectAll(`.${createClassName('label', groupName)}`)
                    .classed("highlighted", true)
                    .classed("dimmed", false);
                    
                // Highlight connecting lines
                svg.selectAll(`.${createClassName('polyline', groupName)}`)
                    .classed("highlighted", true)
                    .classed("dimmed", false);
            });
        }
    }
    
    // Get groups to highlight from props based on current scroll value
    function getGroupsToHighlight(currentValue: number): string[] {
        // Use items from highlightMap prop if available, or return empty array
        return highlightMap[currentValue] || [];
    }

    function createVisualization() {
        // Clear any existing SVG
        d3.select(container).selectAll("svg").remove();
        
        // Create the SVG container
        svg = d3.select(container)
            .append("svg")
            .attr("width", width)
            .attr("height", height)
            .attr("viewBox", [0, 0, width, height])
            .attr("style", "max-width: 100%; height: auto; font: 10px sans-serif;")
            .append("g")
            .attr("transform", `translate(${width / 2},${height / 2})`);
        
        // Create groups for slices, labels, and lines
        svg.append("g").attr("class", "slices");
        svg.append("g").attr("class", "lines");
        svg.append("g").attr("class", "labels");
        
        // Create a color scale based on the type of colorScheme provided
        if (typeof colorScheme === 'object' && !Array.isArray(colorScheme)) {
            // If colorScheme is a mapping object
            const fallbackScale = d3.scaleOrdinal<string>()
                .domain(data.map(d => d.label))
                .range(fallbackColorArray);
                
            color = d3.scaleOrdinal<string>()
                .domain(data.map(d => d.label))
                .unknown("#CCCCCC") // Default color for unknown categories
                .range(data.map(d => {
                    // Use the mapped color if available, otherwise use fallback scale
                    return colorScheme[d.label] || fallbackScale(d.label);
                }));
        } else if (Array.isArray(colorScheme)) {
            // Backward compatibility: if colorScheme is an array
            color = d3.scaleOrdinal<string>()
                .domain(data.map(d => d.label))
                .range(colorScheme);
        } else {
            // Default case
            color = d3.scaleOrdinal<string>()
                .domain(data.map(d => d.label))
                .range(fallbackColorArray);
        }
            
        // Create pie layout
        pie = d3.pie()
            .sort(null)
            .value((d: any) => d.value);
            
        // Create arcs for slices and labels
        arc = d3.arc()
            .outerRadius(radius * 0.8)
            .innerRadius(radius * 0.4);
            
        outerArc = d3.arc()
            .innerRadius(radius * 0.9)
            .outerRadius(radius * 0.9);
        
        // Create the donut chart slices
        const slice = svg.select(".slices").selectAll("path.slice")
            .data(pie(data), (d: any) => d.data.label);
            
        slice.enter()
            .insert("path")
            .attr("class", (d: any) => `slice ${createClassName('slice', d.data.label)}`)
            .attr("fill", (d: any) => color(d.data.label))
            .attr("d", arc)
            .classed("dimmed", true);
            
        // Calculate max width for label text based on chart size
        const maxLabelWidth = radius * 0.6;
        
        // Get label distance factor based on screen size
        const labelDistanceFactor = getLabelDistanceFactor();
            
        // Generate label positions and process them to prevent overlaps
        const pieData = pie(data);
        const labelPositions = pieData.map((d: any) => {
            const pos = outerArc.centroid(d);
            // Extend the position out to the label location - adjusted by screen size
            pos[0] = radius * labelDistanceFactor * (midAngle(d) < Math.PI ? 1 : -1);
            return {
                data: d.data,
                angle: midAngle(d),
                x: pos[0],
                y: pos[1],
                anchor: midAngle(d) < Math.PI ? "start" : "end"
            };
        });
        
        // Apply the overlap prevention algorithm with the max label width
        preventLabelOverlap(labelPositions, radius, maxLabelWidth);
        
        // Create the connecting curved lines using paths instead of polylines
        const line = svg.select(".lines").selectAll("path.connector")
            .data(labelPositions, (d: any) => d.data.label);
            
        line.enter()
            .append("path")
            .attr("class", (d: any) => `connector ${createClassName('polyline', d.data.label)}`)
            .attr("d", (d: any) => {
                // Calculate centroid of arc for start point
                const arcCentroid = arc.centroid(pieData.find((p: any) => p.data.label === d.data.label));
                // Calculate outer arc centroid for middle control point
                const outerCentroid = outerArc.centroid(pieData.find((p: any) => p.data.label === d.data.label));
                
                // Determine control points for the curve
                // This creates an S-curve from arc to label
                const controlPoint1 = [
                    arcCentroid[0] + (outerCentroid[0] - arcCentroid[0]) * 0.5,
                    arcCentroid[1] + (outerCentroid[1] - arcCentroid[1]) * 0.5
                ];
                
                const controlPoint2 = [
                    outerCentroid[0] + (d.x - outerCentroid[0]) * 0.5,
                    outerCentroid[1] + (d.y - outerCentroid[1]) * 0.5
                ];
                
                // Create SVG path with cubic Bezier curve
                return `M ${arcCentroid[0]},${arcCentroid[1]} 
                        C ${controlPoint1[0]},${controlPoint1[1]} 
                          ${controlPoint2[0]},${controlPoint2[1]} 
                          ${d.x},${d.y}`;
            })
            .classed("dimmed", true);

        // Create the text labels using the processed positions
        const text = svg.select(".labels").selectAll("text")
            .data(labelPositions, (d: any) => d.data.label);
            
        text.enter()
            .append("text")
            .attr("class", (d: any) => `label ${createClassName('label', d.data.label)}`)
            .attr("transform", (d: any) => `translate(${d.x},${d.y})`)
            .style("text-anchor", (d: any) => d.anchor)
            .classed("dimmed", true)
            .text((d: any) => `${d.data.label} (${d.data.formattedCount} websites - ${d.data.percentage}%)`)
            .each(function(d: any) {
                // Store the original text before wrapping
                d.originalText = d3.select(this).text();
            })
            .call(wrapText, maxLabelWidth);
            
        // Initial highlight based on current value
        highlightGroups(value);
    }
    
    // Replace legacy reactive statement with $effect
    $effect(() => {
        if (value !== undefined && svg) {
            highlightGroups(value);
        }
    });
</script>

<section id="theme-donut-chart">
    <!-- Fixed visualization that stays in the background -->
    <div class="visualization-container">
        <div class="theme-donut-chart__container" bind:this={container}>
            <!-- Donut chart visualization rendered here -->
        </div>
    </div>

    <div class="spacer"></div>
    
    <!-- Scrolly component for scroll-activated content -->
    <Scrolly bind:value>
        {#each sectionIndices as section}
            {@const active = value === section}
            <div class="step" class:active>
                <div class="step-content">
                    <p>{scrollContent[section]}</p>
                </div>
            </div>
        {/each}
    </Scrolly>
    
    <div class="spacer"></div>
</section>

<style>
    /* Define label font variables at the component level - 
       These can be customized by parent components or global CSS */
    :global(:root) {
        --label-font-family: "Helvetica", Arial, sans-serif;
        --label-font-size: 16px;
        --label-font-weight: 350;
        --label-line-height: 1.3;
        --label-highlighted-font-weight: 500;
        --label-max-width-factor: 0.6; /* Controls how much width labels can use */
    }
    
    #theme-donut-chart {
        position: relative;
        width: 100%;
        max-width: 1000px;
        margin: 0 auto;
    }
    
    .visualization-container {
        position: sticky;
        top: calc(50vh - 40vh); /* Position to center the chart vertically */
        z-index: 1;
        width: 100%;
        height: auto;
        background-color: white;
        padding: 0 10px; /* Add some padding to prevent edge cutting */
        display: flex;
        justify-content: center;
        align-items: center;
    }
    
    .theme-donut-chart__container {
        width: 100%;
        height: 80vh;
        min-height: 400px;
        border: none;
        overflow: hidden;
        display: flex;
        justify-content: center;
        align-items: center;
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
        z-index: 5;
        position: relative;
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
    
    .step p {
        margin: 0;
        font-family: "Arial";
        font-weight: 200;
    }
    
    .active {
        font-weight: bold;
    }
    
    /* Styling for donut chart elements */
    :global(path.slice) {
        stroke-width: 2px;
        stroke: white;
        transition: opacity 0.3s ease;
    }
    
    :global(path.slice.dimmed) {
        opacity: 0.3;
    }
    
    :global(path.slice.highlighted) {
        opacity: 1;
        stroke-width: 3px;
    }
    
    /* Improved label styling with CSS variables */
    :global(text.label) {
        font-family: var(--label-font-family);
        font-size: var(--label-font-size);
        font-weight: var(--label-font-weight);
        transition: opacity 0.3s ease, font-weight 0.3s ease;
        fill: #333;
    }
    
    :global(text.label.dimmed) {
        opacity: 0.3;
    }
    
    :global(text.label.highlighted) {
        opacity: 1;
        font-weight: var(--label-highlighted-font-weight);
        fill: #000;
    }
    
    /* Styled curved connector paths */
    :global(path.connector) {
        fill: none;
        stroke: #222;
        stroke-width: 1px;
        opacity: 0.3;
        transition: opacity 0.3s ease, stroke-width 0.3s ease;
        stroke-linejoin: round;
        stroke-linecap: round;
    }
    
    :global(path.connector.dimmed) {
        opacity: 0.1;
    }
    
    :global(path.connector.highlighted) {
        opacity: 0.8;
        stroke-width: 2px;
    }
    
    /* Make sure the Scrolly component has proper z-index */
    :global(.scrolly-container) {
        position: relative;
        z-index: 10; /* Higher than both visualization and steps */
    }
    
    /* Media query for small screens */
    @media (max-width: 768px) {
        .visualization-container {
            top: calc(50vh - 30vh); /* Adjusted to center the 60vh container */
        }
        
        .theme-donut-chart__container {
            height: 60vh;
        }
        
        .step-content {
            max-width: 280px;
            padding: 15px;
        }
        
        :global(:root) {
            --label-font-size: 11px;
            --label-max-width-factor: 0.5; /* Less width for labels on small screens */
        }

        /* Reduce vertical space between steps on smaller screens */
        .spacer {
            height: 60vh;
        }
    }
    
    /* Media query for very small screens */
    @media (max-width: 480px) {
        .visualization-container {
            top: calc(50vh - 25vh); /* Adjusted to center the 50vh container */
        }
        
        .theme-donut-chart__container {
            height: 50vh;
        }
        
        .step-content {
            max-width: 240px;
            padding: 12px;
        }
        
        :global(:root) {
            --label-font-size: 9px;
            --label-max-width-factor: 0.4; /* Even less width for labels on tiny screens */
        }
        
        /* Further reduce vertical space on tiny screens */
        .spacer {
            height: 50vh;
        }
    }
</style> 