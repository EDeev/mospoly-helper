import os
from scripts import make_full_clip

async def combine_all_videos():
    corpora = ["pr", "pk", "mi", "av", "bs"]

    for corpus in corpora:
        base_path = os.path.join("../videos", corpus)
        offices_path = os.path.join(base_path, "offices")
        if not os.path.exists(offices_path):
            continue

        for filename in os.listdir(offices_path):
            if filename.endswith(".mp4"):
                office_path = os.path.join(offices_path, filename)
                name, _ = os.path.splitext(filename)
                parts = name.split("-")
                if len(parts) != 4:
                    continue
                corpus_id, building, floor, office = parts
                floor_filename = f"{corpus_id}-{building}-{floor}.mp4"
                building_filename = f"{corpus_id}-{building}.mp4"
                floor_path = os.path.join(base_path, "floors", floor_filename)
                building_path = os.path.join(base_path, "buildings", building_filename)
                if os.path.exists(floor_path) and os.path.exists(building_path):
                    clips = [building_path, floor_path, office_path]

                    # ПОЛНОЕ ВИДЕО
                    await make_full_clip(clips)

                    # УРЕЗАННОЕ ВИДЕО
                    await make_full_clip(clips[1:])
                else:
                    print(f"Missing files for {filename} in {corpus}")

import asyncio
asyncio.run(combine_all_videos())