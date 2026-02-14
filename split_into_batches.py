#!/usr/bin/env python3
"""
Split your video CSV into batches for parallel processing
"""

import pandas as pd
import math

# ==============================
# CONFIG
# ==============================
INPUT_CSV = "video_ids_metadata_Bengali - Sanjid.csv"  # Your original CSV
VIDEO_ID_COLUMN = "video_id"  # Column with video IDs
VIDEOS_PER_BATCH = 100  # Split into batches of this size

# ==============================
# LOAD AND SPLIT
# ==============================
print("=" * 70)
print("CSV BATCH SPLITTER")
print("=" * 70)
print()

# Load CSV
df = pd.read_csv(INPUT_CSV)
video_ids = df[VIDEO_ID_COLUMN].dropna().astype(str).unique().tolist()

print(f"📌 Total unique video IDs: {len(video_ids)}")
print(f"📦 Batch size: {VIDEOS_PER_BATCH} videos")

# Calculate number of batches needed
num_batches = math.ceil(len(video_ids) / VIDEOS_PER_BATCH)
print(f"📊 Will create: {num_batches} batches")
print()

# Create batches
for i in range(num_batches):
    start_idx = i * VIDEOS_PER_BATCH
    end_idx = min((i + 1) * VIDEOS_PER_BATCH, len(video_ids))
    
    batch_ids = video_ids[start_idx:end_idx]
    batch_df = pd.DataFrame({VIDEO_ID_COLUMN: batch_ids})
    
    filename = f"batch_{i}.csv"
    batch_df.to_csv(filename, index=False)
    
    print(f"✅ Created {filename}")
    print(f"   Videos {start_idx} to {end_idx-1} ({len(batch_ids)} videos)")
    print()

# ==============================
# CREATE PLATFORM ASSIGNMENT
# ==============================
platform_assignments = []

platforms = [
    "Kaggle (Notebook 1)",
    "Google Colab (Account 1)",
    "GitHub Codespaces",
    "Google Colab (Account 2)",
    "Kaggle (Notebook 2)",
    "Any other platform"
]

for i in range(num_batches):
    platform = platforms[i] if i < len(platforms) else f"Platform {i+1}"
    start_idx = i * VIDEOS_PER_BATCH
    end_idx = min((i + 1) * VIDEOS_PER_BATCH, len(video_ids))
    count = end_idx - start_idx
    
    platform_assignments.append({
        'Batch': i,
        'File': f'batch_{i}.csv',
        'Videos': f'{start_idx}-{end_idx-1}',
        'Count': count,
        'Platform': platform
    })

assignment_df = pd.DataFrame(platform_assignments)
assignment_df.to_csv('batch_assignments.csv', index=False)

print("=" * 70)
print("PLATFORM ASSIGNMENTS")
print("=" * 70)
print(assignment_df.to_string(index=False))
print()
print("💾 Saved to: batch_assignments.csv")
print()

# ==============================
# NEXT STEPS
# ==============================
print("=" * 70)
print("NEXT STEPS")
print("=" * 70)
print()
print("1. You now have these batch files:")
for i in range(num_batches):
    print(f"   - batch_{i}.csv")
print()
print("2. Upload each batch to its assigned platform")
print("3. Run lightweight_checker.py on each platform")
print("4. Download the results (rename to results_0.csv, results_1.csv, etc.)")
print("5. Run merge_results.py to combine everything")
print()
print("See STRATEGY.txt for detailed instructions!")
print("=" * 70)
