#!/usr/bin/env bash
set -euo pipefail

# 사용법: bash bash/run_eval.sh [DATASET_NAME] [TRACKERS_RESULTS_DIR] [GT_TYPE] [MODEL_TYPE]
# 예: bash bash/run_eval.sh MOT17 .../track_results val_half X
if [ "$#" -ne 4 ]; then
    echo "Usage: $0 [DATASET_NAME] [TRACKERS_RESULTS_DIR] [GT_TYPE (e.g., val_half)] [MODEL_TYPE (e.g., X, L, S)]"
    exit 1
fi

DATASET_NAME=$1
TRACKERS_DIR=$2
GT_TYPE=$3
MODEL_TYPE=$4

# GT 타입 접미사 설정
GT_TYPE_SUFFIX=${3:+_$3}
# 트래커 이름 설정 (e.g., FastTracker-X)
TRACKER_NAME="FastTracker-${MODEL_TYPE}"

# FastTracker 루트로 이동
cd -- "$(dirname -- "$(dirname -- "${BASH_SOURCE[0]}")")" &> /dev/null
ROOT_DIR=$(pwd)
echo "Current working directory: $ROOT_DIR"

# 원본 GT 데이터 경로
ORIGINAL_GT_DIR="/home/danny/mot/datasets/${DATASET_NAME}/train"

# --- 필터링된 임시 GT 폴더 생성 ---
FILTERED_GT_DIR=$(mktemp -d)
trap 'rm -rf -- "$FILTERED_GT_DIR"' EXIT

echo "==> Creating a temporary, filtered GT folder for GT type: '$GT_TYPE'"
for f in "$TRACKERS_DIR"/*.txt; do
  seq_name=$(basename "$f" .txt)
  original_seq_dir="$ORIGINAL_GT_DIR/$seq_name"
  
  if [ -d "$original_seq_dir" ]; then
    mkdir -p "$FILTERED_GT_DIR/$seq_name/gt"
    gt_file_to_link="$original_seq_dir/gt/gt${GT_TYPE_SUFFIX}.txt"
    
    if [ -f "$gt_file_to_link" ]; then
      ln -s "$gt_file_to_link" "$FILTERED_GT_DIR/$seq_name/gt/gt.txt"
      if [ -f "$original_seq_dir/seqinfo.ini" ]; then
        ln -s "$original_seq_dir/seqinfo.ini" "$FILTERED_GT_DIR/$seq_name/seqinfo.ini"
      fi
    else
      echo "Warning: GT file not found for $seq_name with type '$GT_TYPE', skipping: $gt_file_to_link"
    fi
  fi
done
# ------------------------------------------

# 각 모델별로 고유한 트래커 평가 폴더 생성
TRACKER_EVAL_DIR="$ROOT_DIR/TrackEval/data/trackers/mot_challenge/${DATASET_NAME}-train/${TRACKER_NAME}"
echo "==> Preparing tracker results for TrackEval in: $TRACKER_EVAL_DIR"
mkdir -p "$TRACKER_EVAL_DIR/data"
cp "$TRACKERS_DIR"/*.txt "$TRACKER_EVAL_DIR/data/"

# 평가 실행
echo "==> Running TrackEval for model ${MODEL_TYPE}..."
python TrackEval/scripts/run_mot_challenge.py \
    --BENCHMARK $DATASET_NAME \
    --SPLIT_TO_EVAL train \
    --TRACKERS_TO_EVAL "$TRACKER_NAME" \
    --METRICS HOTA CLEAR Identity \
    --USE_PARALLEL False \
    --GT_FOLDER "$FILTERED_GT_DIR" \
    --TRACKERS_FOLDER "$ROOT_DIR/TrackEval/data/trackers/mot_challenge/"

echo "==> Eval for ${MODEL_TYPE} finished! Results are in $TRACKER_EVAL_DIR"