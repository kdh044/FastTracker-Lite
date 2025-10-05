# FastTracker Backbone Benchmark Results

This document records the performance metrics for the FastTracker framework when paired with different YOLOX backbones on the MOT17 dataset.

**Evaluation Protocol:**
- **Dataset:** MOT17
- **Split:** `val_half`
- **Evaluation Tool:** `TrackEval` (via `run_eval.sh`)

---

## YOLOX-X

- **Experiment File:** `exps/example/mot/yolox_x_mix_det.py`
- **Checkpoint:** `pretrained/bytetrack_x_mot17.pth.tar`

**Performance Metrics:**
| HOTA   | MOTA   | IDF1   | FPS    |
|--------|--------|--------|--------|
| 76.516 | 88.618 | 85.921 | ~35.1   |

**Tracking Parameters (from `run024` using `005_default.json`):**
```json
{
    "track_thresh": 0.7,
    "track_buffer": 30,
    "match_thresh": 0.85,
    "min_box_area": 100,
    "reset_velocity_offset_occ": 5,
    "reset_pos_offset_occ": 3,
    "enlarge_bbox_occ": 1.1,
    "dampen_motion_occ": 0.89,
    "active_occ_to_lost_thresh": 10,
    "init_iou_suppress": 0.7
}
```

---

## YOLOX-L

- **Experiment File:** `exps/default/yolox_l.py`
- **Checkpoint:** `pretrained/yolox_l.pth.tar` (or similar)

**Performance Metrics:**
| HOTA   | MOTA   | IDF1   | FPS    |
|--------|--------|--------|--------|
| TBD    | TBD    | TBD    | TBD    |

**Tracking Parameters:**
*To be recorded.*

---

## YOLOX-M

- **Experiment File:** `exps/default/yolox_m.py`
- **Checkpoint:** `pretrained/bytetrack_m_mot17.pth.tar`

**Performance Metrics:**
| HOTA   | MOTA   | IDF1   | FPS    |
|--------|--------|--------|--------|
| TBD    | TBD    | TBD    | TBD    |

**Tracking Parameters:**
*To be recorded.*

---

## YOLOX-S

- **Experiment File:** `exps/default/yolox_s.py`
- **Checkpoint:** `pretrained/yolox_s.pth.tar` (or similar)

**Performance Metrics:**
| HOTA   | MOTA   | IDF1   | FPS    |
|--------|--------|--------|--------|
| TBD    | TBD    | TBD    | TBD    |

**Tracking Parameters:**
*To be recorded.*

---

## YOLOX-Tiny

- **Experiment File:** `exps/default/yolox_tiny.py`
- **Checkpoint:** `pretrained/yolox_tiny.pth.tar` (or similar)

**Performance Metrics:**
| HOTA   | MOTA   | IDF1   | FPS    |
|--------|--------|--------|--------|
| TBD    | TBD    | TBD    | TBD    |

**Tracking Parameters:**
*To be recorded.*

---

## YOLOX-Nano

- **Experiment File:** `exps/default/nano.py`
- **Checkpoint:** `pretrained/yolox_nano.pth.tar` (or similar)

**Performance Metrics:**
| HOTA   | MOTA   | IDF1   | FPS    |
|--------|--------|--------|--------|
| TBD    | TBD    | TBD    | TBD    |

**Tracking Parameters:**
*To be recorded.*

