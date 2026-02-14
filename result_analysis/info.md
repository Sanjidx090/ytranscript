======================================================================
RESULTS MERGER
======================================================================

Looking for result files...
Found 6 result files:
  - /kaggle/working/ytranscript/result/batch_0_result.csv
  - /kaggle/working/ytranscript/result/batch_1_result.csv
  - /kaggle/working/ytranscript/result/batch_2_result.csv
  - /kaggle/working/ytranscript/result/batch_3_result.csv
  - /kaggle/working/ytranscript/result/batch_4_result.csv
  - /kaggle/working/ytranscript/result/batch_5_result.csv

Merging files...
  ✅ /kaggle/working/ytranscript/result/batch_0_result.csv: 100 videos
  ✅ /kaggle/working/ytranscript/result/batch_1_result.csv: 100 videos
  ✅ /kaggle/working/ytranscript/result/batch_2_result.csv: 100 videos
  ✅ /kaggle/working/ytranscript/result/batch_3_result.csv: 100 videos
  ✅ /kaggle/working/ytranscript/result/batch_4_result.csv: 100 videos
  ✅ /kaggle/working/ytranscript/result/batch_5_result.csv: 5 videos

📊 Total unique videos: 505
💾 Saved to: final_transcript_availability.csv

======================================================================
FINAL STATISTICS
======================================================================

Status breakdown:
  Available: 444 (87.9%)
  Disabled: 55 (10.9%)
  Blocked: 6 (1.2%)

✅ Has transcripts: 444/505 (87.9%)
🇧🇩 Has Bangla: 275/505 (54.5%)
🌐 Has English: 105/505 (20.8%)

Creating filtered CSVs...

🇧🇩 Videos with Bangla: videos_with_bangla.csv (275 videos)
✅ Videos with any transcript: videos_with_transcripts.csv (444 videos)
❌ Videos without transcripts: videos_without_transcripts.csv (61 videos)

======================================================================
✅ MERGE COMPLETE!
======================================================================

Files created:
  1. final_transcript_availability.csv - All results
  2. videos_with_bangla.csv - Only Bangla videos
  3. videos_with_transcripts.csv - All videos with transcripts
  4. videos_without_transcripts.csv - Videos without transcripts
