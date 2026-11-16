"""Local face retouch for the lead (no API credit): finds every face with MediaPipe FaceLandmarker, picks the bearded lead by how dark the lower-face region is
compared with his cheeks, evens and cleans his skin (edge-preserving smoothing, texture reduced not removed) and turns the beard jet black.
Other people are left untouched. Usage: python3 retouch_lead.py <in.mp4> <out_video_only.mp4> [debug_dir]"""
import sys, os, subprocess, numpy as np, cv2
import mediapipe as mp
from mediapipe.tasks import python as mpp
from mediapipe.tasks.python import vision
MODEL = os.environ.get("FACE_MODEL", "/tmp/claude-0/work/models/face_landmarker.task")
OVAL = [10,338,297,332,284,251,389,356,454,323,361,288,397,365,379,378,400,377,152,148,176,149,150,136,172,58,132,93,234,127,162,21,54,103,67,109]
LIPS = [61,146,91,181,84,17,314,405,321,375,291,409,270,269,267,0,37,39,40,185]
LEYE = [33,7,163,144,145,153,154,155,133,173,157,158,159,160,161,246]; REYE = [263,249,390,373,374,380,381,382,362,398,384,385,386,387,388,466]
LBROW = [70,63,105,66,107,55,65,52,53,46]; RBROW = [300,293,334,296,336,285,295,282,283,276]
JAW = [234,93,132,58,172,136,150,149,176,148,152,377,400,378,379,365,397,288,361,323,454]; CLOSE = [425,327,98,205]
BEARD_MIN = float(os.environ.get("BEARD_MIN", "0.22"))
def poly(lm, ids, w, h): return np.array([[lm[i].x * w, lm[i].y * h] for i in ids], np.int32)
def fill(shape, pts, grow=0):
    m = np.zeros(shape[:2], np.uint8); cv2.fillPoly(m, [pts], 255)
    if grow: m = cv2.dilate(m, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (grow, grow)))
    return m
def masks(lm, shape):
    h, w = shape[:2]; oval = poly(lm, OVAL, w, h); fw = max(1, oval[:, 0].max() - oval[:, 0].min()); g = max(3, int(fw * 0.05)) | 1
    face = fill(shape, oval); beard = fill(shape, np.concatenate([poly(lm, JAW, w, h), poly(lm, CLOSE, w, h)]))
    lips = fill(shape, poly(lm, LIPS, w, h), g * 2); eyes = fill(shape, np.concatenate([poly(lm, LEYE, w, h)]), g * 2) | fill(shape, poly(lm, REYE, w, h), g * 2)
    brows = fill(shape, poly(lm, LBROW, w, h), g * 2) | fill(shape, poly(lm, RBROW, w, h), g * 2)
    beard = cv2.bitwise_and(beard, face); beard[lips > 0] = 0
    skin = face.copy(); skin[(lips > 0) | (eyes > 0) | (brows > 0)] = 0
    return face, beard, skin, fw, oval
def luma(img): return (0.299 * img[..., 2] + 0.587 * img[..., 1] + 0.114 * img[..., 0]).astype(np.float32)
def beard_score(img, face, beard, skin):
    L = luma(img); cheek = (skin > 0) & (beard == 0); b = beard > 0
    if cheek.sum() < 50 or b.sum() < 80: return 0.0, 0.0
    ls = float(np.median(L[cheek])); return float(np.clip((ls - L[b]) / max(ls, 1), 0, 1).mean()), ls
def smooth(x, k=0.55): return x
def retouch(img, lm):
    face, beard, skin, fw, oval = masks(lm, img.shape); h, w = img.shape[:2]
    x0, y0 = max(0, oval[:, 0].min() - fw // 4), max(0, oval[:, 1].min() - fw // 4); x1, y1 = min(w, oval[:, 0].max() + fw // 4), min(h, oval[:, 1].max() + fw // 4)
    roi = img[y0:y1, x0:x1].astype(np.float32); f = (face[y0:y1, x0:x1] > 0); sk = skin[y0:y1, x0:x1].astype(np.float32) / 255; bd = beard[y0:y1, x0:x1].astype(np.float32) / 255
    k = max(3, int(fw * 0.04)) | 1; feather = lambda m: cv2.GaussianBlur(m, (0, 0), max(1.0, fw * 0.012))
    # 1) clean, even skin: reduce texture/blemishes, keep detail partly, even out the colour
    base = cv2.GaussianBlur(roi, (0, 0), max(1.5, fw * 0.035)); detail = roi - cv2.bilateralFilter(roi, 0, 28, max(2.0, fw * 0.02))
    clean = cv2.bilateralFilter(roi, 0, 32, max(2.0, fw * 0.02)) + detail * 0.35
    a = feather(sk) * 0.85; out = roi * (1 - a[..., None]) + clean * a[..., None]
    out = out * (1 + 0.035 * a[..., None]); out = np.clip(out, 0, 255)
    # 2) jet-black beard: where the lower face is darker than the cheeks, push it to a deep neutral black while keeping some strand texture
    L = luma(out); cheek = (sk > 0.5) & (bd < 0.3); ls = float(np.median(L[cheek])) if cheek.sum() > 30 else float(np.median(L[f]))
    wgt = np.clip((ls * 0.92 - L) / (ls * 0.30), 0, 1) * feather(bd)
    gray = L[..., None] * np.array([1, 1, 1], np.float32); black = gray * 0.32 + 6
    out = out * (1 - wgt[..., None]) + black * wgt[..., None]
    res = img.copy(); res[y0:y1, x0:x1] = np.clip(out, 0, 255).astype(np.uint8); return res
def main(src, dst, dbg=None):
    cap = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height,r_frame_rate", "-of", "csv=p=0", src], capture_output=True, text=True).stdout.strip().split(",")
    W0, H0 = int(cap[0]), int(cap[1]); num, den = cap[2].split("/"); fps = float(num) / float(den); scale = min(1.0, 1920 / W0); W, H = int(W0 * scale) // 2 * 2, int(H0 * scale) // 2 * 2
    dec = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-i", src, "-an", "-vf", f"scale={W}:{H}:flags=lanczos", "-f", "rawvideo", "-pix_fmt", "bgr24", "-"], stdout=subprocess.PIPE)
    enc = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", f"{fps}", "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "14", "-pix_fmt", "yuv420p", dst], stdin=subprocess.PIPE)
    opts = vision.FaceLandmarkerOptions(base_options=mpp.BaseOptions(model_asset_path=MODEL), running_mode=vision.RunningMode.VIDEO, num_faces=6, min_face_detection_confidence=0.3, min_face_presence_confidence=0.3, min_tracking_confidence=0.3)
    lmk = vision.FaceLandmarker.create_from_options(opts); n = 0; last = None; miss = 0; stats = []
    while True:
        raw = dec.stdout.read(W * H * 3)
        if len(raw) < W * H * 3: break
        img = np.frombuffer(raw, np.uint8).reshape(H, W, 3).copy(); res = lmk.detect_for_video(mp.Image(image_format=mp.ImageFormat.SRGB, data=cv2.cvtColor(img, cv2.COLOR_BGR2RGB)), int(n * 1000 / fps))
        best = None
        for lm in res.face_landmarks:
            face, beard, skin, fw, oval = masks(lm, img.shape); s, ls = beard_score(img, face, beard, skin)
            c = (oval[:, 0].mean(), oval[:, 1].mean())
            near = last is not None and np.hypot(c[0] - last[0], c[1] - last[1]) < fw * 0.8
            if (s >= BEARD_MIN or (near and s >= BEARD_MIN * 0.6)) and (best is None or s > best[0]): best = (s, lm, c)
        if best is not None: last = best[2]; miss = 0; img = retouch(img, best[1]); stats.append(round(best[0], 2))
        else: miss += 1; stats.append(None)
        if dbg and n % 12 == 0: cv2.imwrite(os.path.join(dbg, f"f{n:04d}.jpg"), img)
        enc.stdin.write(img.tobytes()); n += 1
    enc.stdin.close(); enc.wait(); hits = sum(1 for s in stats if s is not None); print(f"{os.path.basename(src)}: {hits}/{n} frames retouched")
if __name__ == "__main__":
    if len(sys.argv) > 3: os.makedirs(sys.argv[3], exist_ok=True)
    main(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None)
