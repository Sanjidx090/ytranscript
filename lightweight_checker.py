#!/usr/bin/env python3
"""
LIGHTWEIGHT TRANSCRIPT AVAILABILITY CHECKER
Only checks IF transcripts exist - doesn't download them
Much faster and less likely to trigger rate limits
"""

# !pip -q install youtube-transcript-api
import pandas as pd
import time
import random
import os
from youtube_transcript_api import YouTubeTranscriptApi
import youtube_transcript_api._errors as yt_errors

# ==============================
# CONFIG - EDIT THESE
# ==============================
INPUT_CSV = "video_ids.csv"  # Your input CSV file
OUTPUT_CSV = "transcript_availability.csv"  # Results will be saved here
VIDEO_ID_COLUMN = "video_id"  # Column name containing video IDs

# Which batch to process (for splitting across platforms)
START_INDEX = 0    # Start from this video (0 = first video)
END_INDEX = None   # End at this video (None = process all remaining)
BATCH_SIZE = 100   # Process this many videos then stop (None = no limit)

# Safety settings
MIN_WAIT = 2.0
MAX_WAIT = 4.0
SAVE_EVERY = 10  # Save progress every N videos

# ==============================
# LOAD DATA
# ==============================
print("=" * 70)
print("📋 TRANSCRIPT AVAILABILITY CHECKER")
print("=" * 70)
print()

df = pd.read_csv(INPUT_CSV)
all_video_ids = df[VIDEO_ID_COLUMN].dropna().astype(str).unique().tolist()
print(f"📌 Total videos in CSV: {len(all_video_ids)}")

# ==============================
# DETERMINE WHAT TO PROCESS
# ==============================
# Check for existing results
already_checked = set()
results = []

if os.path.exists(OUTPUT_CSV):
    print(f"📁 Found existing results: {OUTPUT_CSV}")
    existing_df = pd.read_csv(OUTPUT_CSV)
    already_checked = set(existing_df['video_id'].astype(str).tolist())
    results = existing_df.to_dict('records')
    print(f"✅ Already checked: {len(already_checked)} videos")

# Filter to unchecked videos
unchecked_videos = [vid for vid in all_video_ids if vid not in already_checked]

# Apply batch limits
if END_INDEX:
    unchecked_videos = unchecked_videos[START_INDEX:END_INDEX]
elif BATCH_SIZE:
    unchecked_videos = unchecked_videos[START_INDEX:START_INDEX + BATCH_SIZE]
else:
    unchecked_videos = unchecked_videos[START_INDEX:]

if len(unchecked_videos) == 0:
    print("\n✅ All videos already checked!")
    exit(0)

print(f"📝 Will check: {len(unchecked_videos)} videos in this batch")
print(f"   Starting from index: {START_INDEX}")
print()

# ==============================
# CREATE API INSTANCE
# ==============================
api = YouTubeTranscriptApi()

# ==============================
# LIGHTWEIGHT CHECK FUNCTION
# ==============================
def check_transcript_availability(video_id):
    """
    LIGHTWEIGHT check - only determines if transcripts exist
    Returns: dict with availability info
    """
    try:
        # Just list available transcripts (doesn't download them!)
        transcript_list = api.list(video_id)
        
        # Collect available languages
        languages = []
        has_bangla = False
        has_english = False
        manual_count = 0
        auto_count = 0
        
        for transcript in transcript_list:
            lang_code = transcript.language_code
            languages.append(lang_code)
            
            if lang_code == 'bn':
                has_bangla = True
            if lang_code == 'en':
                has_english = True
            
            if transcript.is_generated:
                auto_count += 1
            else:
                manual_count += 1
        
        return {
            'video_id': video_id,
            'has_transcript': True,
            'has_bangla': has_bangla,
            'has_english': has_english,
            'total_languages': len(languages),
            'manual_count': manual_count,
            'auto_count': auto_count,
            'languages': ','.join(languages),
            'status': 'Available'
        }
        
    except yt_errors.TranscriptsDisabled:
        return {
            'video_id': video_id,
            'has_transcript': False,
            'has_bangla': False,
            'has_english': False,
            'total_languages': 0,
            'manual_count': 0,
            'auto_count': 0,
            'languages': '',
            'status': 'Disabled'
        }
    except yt_errors.VideoUnavailable:
        return {
            'video_id': video_id,
            'has_transcript': False,
            'has_bangla': False,
            'has_english': False,
            'total_languages': 0,
            'manual_count': 0,
            'auto_count': 0,
            'languages': '',
            'status': 'Unavailable'
        }
    except Exception as e:
        error_msg = str(e)
        
        # Detect rate limiting
        if "429" in error_msg or "Too Many Requests" in error_msg:
            status = "RateLimited"
        elif "Could not retrieve" in error_msg:
            status = "Blocked"
        else:
            status = "Error"
        
        return {
            'video_id': video_id,
            'has_transcript': False,
            'has_bangla': False,
            'has_english': False,
            'total_languages': 0,
            'manual_count': 0,
            'auto_count': 0,
            'languages': '',
            'status': status
        }

# ==============================
# MAIN CHECKING LOOP
# ==============================
print("🚀 Starting checks...")
print("=" * 70)
print()

processed = 0
consecutive_failures = 0

for i, video_id in enumerate(unchecked_videos):
    current_index = START_INDEX + i
    total_processed = len(already_checked) + processed + 1
    
    print(f"🔍 [{total_processed}/{len(all_video_ids)}] Index {current_index}: {video_id}")
    
    result = check_transcript_availability(video_id)
    
    # Display result
    status = result['status']
    if result['has_transcript']:
        bangla_emoji = "🇧🇩" if result['has_bangla'] else ""
        print(f"   ✅ {status} - {result['total_languages']} languages {bangla_emoji}")
        consecutive_failures = 0
    else:
        print(f"   ❌ {status}")
        
        # Track consecutive failures
        if status in ['Blocked', 'RateLimited', 'Error']:
            consecutive_failures += 1
            if consecutive_failures >= 5:
                print(f"\n⚠️  {consecutive_failures} consecutive failures - stopping")
                results.append(result)
                processed += 1
                break
        else:
            consecutive_failures = 0
    
    results.append(result)
    processed += 1
    
    # Save progress
    if processed % SAVE_EVERY == 0:
        pd.DataFrame(results).to_csv(OUTPUT_CSV, index=False)
        print(f"   💾 Saved progress ({total_processed} total)")
    
    # Delay before next request
    if i < len(unchecked_videos) - 1:
        wait_time = random.uniform(MIN_WAIT, MAX_WAIT)
        time.sleep(wait_time)

# Final save
pd.DataFrame(results).to_csv(OUTPUT_CSV, index=False)

# ==============================
# SUMMARY
# ==============================
print("\n" + "=" * 70)
print("✅ BATCH COMPLETE")
print("=" * 70)

df_results = pd.DataFrame(results)

print(f"📊 This session: {processed} videos")
print(f"📊 Total checked: {len(results)}/{len(all_video_ids)}")
print()

# Count by status
status_counts = df_results['status'].value_counts()
print("Status breakdown:")
for status, count in status_counts.items():
    print(f"  {status}: {count}")
print()

# Key metrics
available = df_results['has_transcript'].sum()
bangla = df_results['has_bangla'].sum()
english = df_results['has_english'].sum()

print(f"✅ Has transcripts: {available}/{len(results)} ({100*available/len(results):.1f}%)")
print(f"🇧🇩 Has Bangla: {bangla}/{len(results)} ({100*bangla/len(results):.1f}%)")
print(f"🌐 Has English: {english}/{len(results)} ({100*english/len(results):.1f}%)")

print()
print(f"💾 Results saved to: {OUTPUT_CSV}")
print("=" * 70)
