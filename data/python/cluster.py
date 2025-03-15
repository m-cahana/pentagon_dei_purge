import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from collections import Counter

# **************
# data read-in
# **************

# read the JSON file
df = pd.read_json('../raw/photos.json')

# **************
# data cleaning
# **************

# convert the 'columns' arrays into separate columns
df = pd.DataFrame(df['rows'].tolist())
df = pd.DataFrame(df['columns'].tolist(), columns=['filename', 'title', 'url'])

# clean up the URLs by removing the markdown formatting
df['url'] = df['url'].str.extract(r'\[(.*?)\]')[0]

# mark and remove numeric titles
df['numeric_title'] = df['title'].str.match(r'^\d{6}-[A-Z]-[A-Z0-9]+-\d+$') | df['title'].str.match(r'^\d{6}-[a-z]-[a-z0-9]+-\d+(\.[a-z]+)?$')

clean_df = df[~df['numeric_title']]

# remove duplicate titles
clean_df_no_duplicates = clean_df.drop_duplicates(subset=['title'])

print(f"Total titles after cleaning: {clean_df.shape[0]}")
print(f"Unique titles: {clean_df_no_duplicates.shape[0]}")

# **************
# TF-IDF based clustering
# **************

print("\nPerforming TF-IDF based clustering...")

# Create TF-IDF vectorizer
tfidf_vectorizer = TfidfVectorizer(
    min_df=2,              # Minimum document frequency
    max_df=0.9,            # Maximum document frequency
    stop_words='english',  # Remove English stopwords
    lowercase=True,        # Convert to lowercase
    use_idf=True,          # Use inverse document frequency
    ngram_range=(1, 2)     # Use both unigrams and bigrams
)

# Fit and transform the titles
tfidf_matrix = tfidf_vectorizer.fit_transform(clean_df_no_duplicates['title'])
print(f"TF-IDF matrix shape: {tfidf_matrix.shape}")

# Determine optimal number of clusters using the elbow method
def find_optimal_clusters(tfidf_matrix, max_clusters=20):
    inertia = []
    for k in range(2, max_clusters + 1):
        km = KMeans(n_clusters=k, random_state=42, n_init=10)
        km.fit(tfidf_matrix)
        inertia.append(km.inertia_)
    
    # Plot the elbow curve
    plt.figure(figsize=(10, 6))
    plt.plot(range(2, max_clusters + 1), inertia, 'bo-')
    plt.xlabel('Number of Clusters')
    plt.ylabel('Inertia')
    plt.title('Elbow Method for Optimal Number of Clusters')
    plt.savefig('../processed/elbow_curve.png')
    plt.close()
    print("Elbow curve saved to '../processed/elbow_curve.png'")
    
    return inertia

# Try to find optimal number of clusters
try:
    inertia = find_optimal_clusters(tfidf_matrix)
except Exception as e:
    print(f"Could not create elbow curve: {e}")

# Number of clusters (you can adjust this based on the elbow curve)
num_clusters = 11
print(f"Using {num_clusters} clusters for K-means")

# Apply K-means clustering
km = KMeans(n_clusters=num_clusters, random_state=42, n_init=10)
km.fit(tfidf_matrix)

# Add the cluster labels to the DataFrame
clean_df_no_duplicates['cluster'] = km.labels_

# Get the top terms per cluster
def get_top_terms_per_cluster(km, tfidf_vectorizer, n_terms=15):
    # Get cluster centroids
    centroids = km.cluster_centers_.argsort()[:, ::-1]
    terms = tfidf_vectorizer.get_feature_names_out()
    
    # For each cluster, get the top terms
    cluster_terms = {}
    for i in range(num_clusters):
        top_term_indices = centroids[i, :n_terms]
        top_terms = [terms[idx] for idx in top_term_indices]
        cluster_terms[i] = top_terms
    
    return cluster_terms

# Get and print top terms for each cluster
print("\nCluster Analysis:")
top_terms = get_top_terms_per_cluster(km, tfidf_vectorizer)
for cluster_id, terms in top_terms.items():
    print(f"\nCluster {cluster_id}: {', '.join(terms)}")
    # Count titles in this cluster
    cluster_size = sum(clean_df_no_duplicates['cluster'] == cluster_id)
    print(f"Number of titles: {cluster_size}")
    # Print a few example titles
    examples = clean_df_no_duplicates[clean_df_no_duplicates['cluster'] == cluster_id]['title'].head(5).tolist()
    print(f"Examples: {examples}")

# Visualize clusters with PCA
def visualize_clusters(tfidf_matrix, km):
    # Reduce dimensions to 2D using PCA
    pca = PCA(n_components=2, random_state=42)
    reduced_features = pca.fit_transform(tfidf_matrix.toarray())
    
    # Create a scatter plot
    plt.figure(figsize=(14, 10))
    
    # Plot each cluster with a different color
    for cluster_id in range(num_clusters):
        # Get points in this cluster
        cluster_points = reduced_features[km.labels_ == cluster_id]
        
        # Skip if no points in this cluster
        if len(cluster_points) == 0:
            continue
            
        # Plot points
        plt.scatter(
            cluster_points[:, 0], 
            cluster_points[:, 1],
            label=f'Cluster {cluster_id}',
            alpha=0.7
        )
    
    plt.title('TF-IDF Clusters Visualization (PCA)')
    plt.xlabel('PCA Component 1')
    plt.ylabel('PCA Component 2')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig('../processed/tfidf_clusters.png')
    plt.close()

# Try to visualize clusters
print("\nVisualizing clusters...")
try:
    visualize_clusters(tfidf_matrix, km)
    print("Cluster visualization saved to '../processed/tfidf_clusters.png'")
except Exception as e:
    print(f"Could not create visualization: {e}")

# Add cluster information to the main DataFrame
clean_df = clean_df.merge(
    clean_df_no_duplicates[['title', 'cluster']], 
    on='title', 
    how='left'
)

# **************
# Analyze clusters for keywords
# **************

# Define keywords of interest
keywords = [
    'black', 'women', 'woman', 'hispanic', 'pacific', 'asian', 'native',
    'islander', 'diversity', 'dei', 'unconscious bias', 'equal employment',
    'pride', 'inclusion', 'inclusive', 'included', 'african', 'indian',
    'aapi', 'female', 'lgbt', 'gender', 'gay', 'heritage', 'juneteenth',
    'deia', 'tuskegee', 'disability', 'disabilities', 'martin luther king', 
    'mlk', 'indigenous', 'bhm', 'aahm', 'aahc', 'apahm', 'aanhpi', 'nahm', 
    'naih', 'naihm', 'hahm', 'whm', 'culture', 'cultural', 'multicultural', 
    'multi-cultural', 'immigrant', 'refugee', 'slave', 'gospel', 'yasuke',
    'latin', 'unidos', 'soul food', 'code talker', 'navajo', 'cherokee', 
    'powwow', 'lumbee', 'barrier', 'contraceptive'
]

# Create a column that checks if any keyword is present
clean_df['has_keywords'] = clean_df['title'].str.lower().apply(
    lambda x: any(keyword in x.lower() for keyword in keywords)
)

# Create a column that lists all present keywords
clean_df['keywords_present'] = clean_df['title'].str.lower().apply(
    lambda x: ', '.join([keyword for keyword in keywords if keyword in x.lower()])
)

# Analyze keyword distribution across clusters
print("\nKeyword Distribution Across Clusters:")
cluster_keyword_counts = {}
for cluster_id in range(num_clusters):
    cluster_df = clean_df[clean_df['cluster'] == cluster_id]
    keyword_count = cluster_df['has_keywords'].sum()
    total_count = len(cluster_df)
    percentage = (keyword_count / total_count * 100) if total_count > 0 else 0
    cluster_keyword_counts[cluster_id] = {
        'total': total_count,
        'with_keywords': keyword_count,
        'percentage': percentage
    }
    print(f"Cluster {cluster_id}: {keyword_count}/{total_count} titles contain keywords ({percentage:.2f}%)")

# Find clusters with highest keyword density
sorted_clusters = sorted(cluster_keyword_counts.items(), 
                         key=lambda x: x[1]['percentage'], 
                         reverse=True)
print("\nClusters Ranked by Keyword Density:")
for cluster_id, stats in sorted_clusters:
    print(f"Cluster {cluster_id}: {stats['percentage']:.2f}% ({stats['with_keywords']}/{stats['total']})")

# **************
# save the clustered data
# **************

# Save the full dataset with cluster information
clean_df.to_csv('../processed/clustered_photos.csv', index=False)

# Save a summary of clusters
cluster_summary = pd.DataFrame({
    'cluster': range(num_clusters),
    'size': [cluster_keyword_counts[i]['total'] for i in range(num_clusters)],
    'with_keywords': [cluster_keyword_counts[i]['with_keywords'] for i in range(num_clusters)],
    'keyword_percentage': [cluster_keyword_counts[i]['percentage'] for i in range(num_clusters)],
    'top_terms': [', '.join(top_terms[i][:5]) for i in range(num_clusters)]
})
cluster_summary.to_csv('../processed/cluster_summary.csv', index=False)

print("\nAnalysis complete. Results saved to '../processed/' directory.")


