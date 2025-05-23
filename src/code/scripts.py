from moviepy import VideoFileClip, concatenate_videoclips
import os, asyncio

async def get_routes(id_building: str, id_cab: str, other=False):
    if other:
        id_cab = id_cab.replace('-', "")
        building=id_cab[0]
        cab_num=id_cab[1:]
        corp_route=f"../videos/{id_building}/{id_building}-{building}b.mp4"
        cab_route=f"../videos/{id_building}/{id_building}-{building}b-{cab_num}.mp4"
        return [corp_route,cab_route]


    match id_building:
        case "av":
            building = id_cab[2]
            floor = id_cab[3]
            cab_num = id_cab[4:]
            corp_route = f"../videos/{id_building}/buildings/{id_building}-{building}b.mp4"
            floor_route = f"../videos/{id_building}/floors/{id_building}-{building}b-0{floor}f.mp4"
            cab_route = f"../videos/{id_building}/offices/{id_building}-{building}b-0{floor}f-{(building + floor + cab_num).zfill(5)}c.mp4"
            return [corp_route, floor_route, cab_route]

        case "mi":
            building = id_cab[1]
            floor = id_cab[2]
            cab_num = id_cab[3:]
            corp_route = f"../videos/{id_building}/buildings/{id_building}-{building}b.mp4"
            floor_route = f"../videos/{id_building}/floors/{id_building}-{building}b-0{floor}f.mp4"
            cab_route = f"../videos/{id_building}/offices/{id_building}-{building}b-0{floor}f-{(building + floor + cab_num).zfill(5)}c.mp4"
            return [corp_route, floor_route, cab_route]

        case "pk":
            building = id_cab[2]
            floor = id_cab[3]
            cab_num = id_cab[4:]
            corp_route = f"../videos/{id_building}/buildings/{id_building}-{building}b.mp4"
            floor_route = f"../videos/{id_building}/floors/{id_building}-{building}b-0{floor}f.mp4"
            cab_route = f"../videos/{id_building}/offices/{id_building}-{building}b-0{floor}f-{(building + floor + cab_num).zfill(5)}c.mp4"
            return [corp_route, floor_route, cab_route]

        case "pr":
            building = id_cab[2]
            floor = id_cab[3]
            cab_num = id_cab[4:]
            corp_route = f"../videos/{id_building}/buildings/{id_building}-{building}b.mp4"
            floor_route = f"../videos/{id_building}/floors/{id_building}-{building}b-0{floor}f.mp4"
            cab_route = f"../videos/{id_building}/offices/{id_building}-{building}b-0{floor}f-{(building + floor + cab_num).zfill(5)}c.mp4"
            return [corp_route, floor_route, cab_route]

        case "bs":
            id_cab= id_cab.replace('-',"")
            building = id_cab[0]
            floor = id_cab[1]
            cab_num = id_cab[3:]
            corp_route = f"../videos/{id_building}/buildings/{id_building}-{building}b.mp4"
            floor_route = f"../videos/{id_building}/floors/{id_building}-{building}b-0{floor}f.mp4"
            cab_route = f"../videos/{id_building}/offices/{id_building}-{building}b-0{floor}f-0{building}{floor}{cab_num}c.mp4"
            return [corp_route, floor_route, cab_route]

    return None



async def make_full_clip(paths):

    if not all(os.path.exists(path) for path in paths):
        print("Некоторые файлы не найдены")
        return None

    full_clip_name = f"{paths[-1][21:].replace('.mp4', '')}-{'all' if len(paths) == 3 else 'small'}.mp4"

    if not os.path.exists(f"../data/cache/{full_clip_name}"):
        clips = [VideoFileClip(path) for path in paths]  # cоздаем список клипов

        full_clip = concatenate_videoclips(clips)  # cклеиваем все клипы

        full_clip = full_clip.without_audio() # удаляем звук
        full_clip = full_clip.time_transform(lambda t: t * 2).with_duration(full_clip.duration / 2)    # ускоряем в 2 раз
        full_clip = full_clip.resized(height=400)

        # рендерим видео с параметрами
        full_clip.write_videofile(f"../data/cache/{full_clip_name}",
                                fps=30,
                                codec="libx264",
                                bitrate="1500k",
                                preset="fast",
                                ffmpeg_params=["-crf", "23"])

    return f"../data/cache/{full_clip_name}"


