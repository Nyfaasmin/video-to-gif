from sentence_transformers import SentenceTransformer, util
import moviepy.editor as mp
import os

model = SentenceTransformer('all-MiniLM-L6-v2')

def get_matching_segments(transcript_segments, prompt, top_n=3):
    prompt_embed = model.encode(prompt, convert_to_tensor=True)
    scores = []
    for seg in transcript_segments:
        seg_embed = model.encode(seg['text'], convert_to_tensor=True)
        sim = util.pytorch_cos_sim(prompt_embed, seg_embed).item()
        scores.append((sim, seg))
    top_matches = sorted(scores, key=lambda x: x[0], reverse=True)[:top_n]
    return [seg for _, seg in top_matches]

def make_gif(video_path, segments, output_folder='static/gifs'):
    gifs = []
    clip = mp.VideoFileClip(video_path)
    for idx, seg in enumerate(segments):
        subclip = clip.subclip(seg['start'], seg['end'])
        txt_clip = mp.TextClip(seg['text'], fontsize=24, color='white').set_position('bottom').set_duration(subclip.duration)
        final = mp.CompositeVideoClip([subclip, txt_clip])
        gif_path = os.path.join(output_folder, f"gif_{idx+1}.gif")
        final.write_gif(gif_path)
        gifs.append(gif_path)
    return gifs
