#!/usr/bin/env python3
"""
Merge results from all platforms into one final CSV
"""

import pandas as pd
import glob
import os

print("=" * 70)
print("RESULTS MERGER")
print("=" * 70)
print()

# ==============================
# METHOD 1: Auto-detect result files
# ==============================
print("Looking for result files...")

# Look for files named results_*.csv or transcript_availability.csv
result_files = []

# Pattern 1: results_0.csv, results_1.csv, etc.
pattern1 = glob.glob("results_*.csv")
result_files.extend(pattern1)

# Pattern 2: Any transcript_availability.csv
if os.path.exists("transcript_availability.csv"):
    result_files.append("transcript_availability.csv")

# Pattern 3: batch results
pattern3 = glob.glob("batch_*_result.csv") # Changed 'results' to 'result'
result_files.extend(pattern3)

# Remove duplicates
result_files = list(set(result_files))
result_files.sort()

print(f"Found {len(result_files)} result files:")
for f in result_files:
    print(f"  - {f}")
print()

if len(result_files) == 0:
    print("❌ No result files found!")
    print()
    print("Make sure you have files named:")
    print("  - results_0.csv, results_1.csv, etc.")
    print("  OR")
    print("  - transcript_availability.csv")
    print()
    print("Place them in the same directory as this script.")
    exit(1)

# ==============================
# LOAD AND MERGE
# ==============================
print("Merging files...")

all_results = []
total_videos = 0

for filename in result_files:
    df = pd.read_csv(filename)
    all_results.append(df)
    total_videos += len(df)
    print(f"  ✅ {filename}: {len(df)} videos")

# Combine all dataframes
merged_df = pd.concat(all_results, ignore_index=True)

# Remove duplicates (in case same video checked on multiple platforms)
original_count = len(merged_df)
merged_df = merged_df.drop_duplicates(subset=['video_id'], keep='first')
final_count = len(merged_df)

if original_count > final_count:
    print(f"\n⚠️  Removed {original_count - final_count} duplicate entries")

print()
print(f"📊 Total unique videos: {final_count}")

# ==============================
# SAVE MERGED RESULTS
# ==============================
output_file = "final_transcript_availability.csv"
merged_df.to_csv(output_file, index=False)

print(f"💾 Saved to: {output_file}")
print()

# ==============================
# STATISTICS
# ==============================
print("=" * 70)
print("FINAL STATISTICS")
print("=" * 70)
print()

# Status breakdown
if 'status' in merged_df.columns:
    print("Status breakdown:")
    status_counts = merged_df['status'].value_counts()
    for status, count in status_counts.items():
        pct = 100 * count / len(merged_df)
        print(f"  {status}: {count} ({pct:.1f}%)")
    print()

# Transcript availability
if 'has_transcript' in merged_df.columns:
    has_transcript = merged_df['has_transcript'].sum()
    print(f"✅ Has transcripts: {has_transcript}/{len(merged_df)} ({100*has_transcript/len(merged_df):.1f}%)")

# Language breakdown
if 'has_bangla' in merged_df.columns:
    has_bangla = merged_df['has_bangla'].sum()
    print(f"🇧🇩 Has Bangla: {has_bangla}/{len(merged_df)} ({100*has_bangla/len(merged_df):.1f}%)")

if 'has_english' in merged_df.columns:
    has_english = merged_df['has_english'].sum()
    print(f"🌐 Has English: {has_english}/{len(merged_df)} ({100*has_english/len(merged_df):.1f}%)")

print()

# ==============================
# CREATE FILTERED CSVS
# ==============================
print("Creating filtered CSVs...")
print()

if 'has_bangla' in merged_df.columns:
    bangla_df = merged_df[merged_df['has_bangla'] == True]
    bangla_file = "videos_with_bangla.csv"
    bangla_df.to_csv(bangla_file, index=False)
    print(f"🇧🇩 Videos with Bangla: {bangla_file} ({len(bangla_df)} videos)")

if 'has_transcript' in merged_df.columns:
    available_df = merged_df[merged_df['has_transcript'] == True]
    available_file = "videos_with_transcripts.csv"
    available_df.to_csv(available_file, index=False)
    print(f"✅ Videos with any transcript: {available_file} ({len(available_df)} videos)")

    no_transcript_df = merged_df[merged_df['has_transcript'] == False]
    no_transcript_file = "videos_without_transcripts.csv"
    no_transcript_df.to_csv(no_transcript_file, index=False)
    print(f"❌ Videos without transcripts: {no_transcript_file} ({len(no_transcript_df)} videos)")

print()
print("=" * 70)
print("✅ MERGE COMPLETE!")
print("=" * 70)
print()
print("Files created:")
print(f"  1. {output_file} - All results")
if 'has_bangla' in merged_df.columns:
    print(f"  2. videos_with_bangla.csv - Only Bangla videos")
if 'has_transcript' in merged_df.columns:
    print(f"  3. videos_with_transcripts.csv - All videos with transcripts")
    print(f"  4. videos_without_transcripts.csv - Videos without transcripts")
print()
