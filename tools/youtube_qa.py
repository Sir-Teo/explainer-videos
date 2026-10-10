"""Inspect the actual source renders or finished YouTube export."""
from pathlib import Path
import argparse, importlib, io, json, re, subprocess, sys
from PIL import Image, ImageDraw, ImageStat

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
OUT = ROOT / "renders" / "youtube"
OUT.mkdir(parents=True, exist_ok=True)

def probe(path):
    return json.loads(subprocess.check_output([
        "ffprobe", "-v", "error", "-show_streams", "-show_format", "-show_chapters",
        "-of", "json", str(path)], text=True))

def frame(path, seconds):
    data = subprocess.check_output([
        "ffmpeg", "-v", "error", "-ss", str(seconds), "-i", str(path),
        "-frames:v", "1", "-vf", "scale=640:360", "-f", "image2pipe", "-vcodec", "png", "-"])
    return Image.open(io.BytesIO(data)).convert("RGB")

def sheet(video, partial=False):
    manifest = importlib.import_module(f"videos.{video}.manifest")
    rows=[]
    for module, cls, title in manifest.SCENES:
        p=ROOT / "media" / video / "crf18" / "videos" / module / "1080p30" / f"{cls}.mp4"
        if not p.exists():
            if partial: continue
            raise FileNotFoundError(p)
        data=probe(p)
        duration=float(data["format"]["duration"])
        rows.append((cls, title, p, duration))
    pages=[]
    for page, start in enumerate(range(0, len(rows), 6), 1):
        group=rows[start:start+6]
        image=Image.new("RGB", (1280, 396*len(group)), "#171c26")
        draw=ImageDraw.Draw(image)
        for row,(cls,title,p,duration) in enumerate(group):
            for col,fraction in enumerate((.25,.70)):
                t=max(2,min(duration-2,duration*fraction))
                sample=frame(p,t)
                if max(ImageStat.Stat(sample).stddev)<3:
                    t=max(2,min(duration-2,t+2.5))
                    sample=frame(p,t)
                image.paste(sample,(col*640,row*396))
                draw.text((col*640+8,row*396+367),f"{cls} | {t:.1f}s | {title}",fill="white")
        dst=OUT / f"{video}-qa-{page}.jpg"
        image.save(dst,quality=93)
        pages.append(str(dst))
    return pages

def timestamp(text):
    h,m,s,ms=map(int,re.split(r"[:,]",text))
    return h*3600+m*60+s+ms/1000

def verify(video):
    p=ROOT / "renders" / f"{video}.mp4"
    data=probe(p)
    duration=float(data["format"]["duration"])
    v=next(s for s in data["streams"] if s["codec_type"]=="video")
    a=next(s for s in data["streams"] if s["codec_type"]=="audio")
    assert (v["width"],v["height"],v["r_frame_rate"],v["pix_fmt"]) == (1920,1080,"30/1","yuv420p")
    assert a["sample_rate"]=="48000" and a["channels"]==2
    assert abs(float(a["duration"])-float(v["duration"])) < .1
    cues=re.findall(r"(\d\d:\d\d:\d\d,\d{3}) --> (\d\d:\d\d:\d\d,\d{3})",p.with_suffix(".srt").read_text())
    assert cues, "no captions"
    previous=0
    for start,end in cues:
        start,end=timestamp(start),timestamp(end)
        assert 0<=start<end<=duration+.1,(start,end,duration)
        assert start>=previous-.01,(start,previous)
        previous=start
    subprocess.run(["ffmpeg","-v","error","-threads","2","-i",str(p),
        "-map","0:v:0","-map","0:a:0","-f","null","-"],check=True)
    measured=subprocess.run(["ffmpeg","-v","info","-i",str(p),"-vn","-af",
        "loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json","-f","null","-"],capture_output=True,text=True,check=True).stderr
    loudness=json.loads(measured[measured.rindex("{"):measured.rindex("}")+1])
    report=dict(video=video,duration=duration,width=v["width"],height=v["height"],fps=v["r_frame_rate"],
        captions=len(cues),chapters=len(data["chapters"]),decode="passed",loudness=loudness,contact_sheets=sheet(video))
    (OUT / f"{video}.qa.json").write_text(json.dumps(report,indent=2))
    return report

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("video")
    parser.add_argument("--partial",action="store_true")
    args=parser.parse_args()
    print(json.dumps(sheet(args.video,True) if args.partial else verify(args.video),indent=2),flush=True)
