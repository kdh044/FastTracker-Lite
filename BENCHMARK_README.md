# FastTracker Backbone Benchmarking Plan

To evaluate and compare the performance of FastTracker with various YOLOX backbones, the following testing plan can be executed.

## Goal
The objective is to measure the trade-off between speed (FPS) and accuracy (HOTA, MOTA) for different model sizes.

## Models to Test
The following YOLOX backbones will be evaluated:
- YOLOX-L
- YOLOX-M
- YOLOX-S
- YOLOX-Tiny
- YOLOX-Nano

## Evaluation Protocol
- **Dataset:** MOT17
- **Evaluation Split:** For fair and standard comparison, all models will be evaluated on the `val_half` split of the training data.
- **Metrics:**
  - **Accuracy:** HOTA, MOTA, IDF1
  - **Speed:** FPS (Frames Per Second)

## Procedure
1.  **Generate Tracking Results:** For each backbone, run the tracking script (`tools/track.py`) to generate the result files. This involves specifying the appropriate experiment file (`-f`) and pre-trained checkpoint (`-c`).
2.  **Evaluate Performance:** Use the `run_eval.sh` script to evaluate the generated results against the `val_half` ground truth to obtain HOTA and MOTA scores.
3.  **Measure Speed:** The FPS for each model is reported in the log output of the tracking script.
