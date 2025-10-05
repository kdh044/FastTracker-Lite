# FastTracker: SOTA Real-Time MOT for Edge Devices

새 프로젝트에 오신 것을 환영합니다. 이 레포지토리는 [FastTracker](https://github.com/Hamidreza-Hashempoor/FastTracker)를 기반으로, SOTA 모델을 경량화하여 임베디드 보드에 배포하는 것을 목표로 합니다.

##  프로젝트 목표

본 프로젝트의 최종 목표는 **30 TOPS 이하**의 임베디드 보드에서 **30 FPS** 이상의 속도와 **70 HOTA** 이상의 정확도를 달성하는 것입니다.

- **타겟 하드웨어:**
  - NVIDIA Jetson Orin Nano
  - Hailo AI 가속기 탑재 임베디드 보드

##  개발 전략 및 브랜치

목표 달성을 위해, 세 가지 주요 브랜치로 나누어 개발을 진행할 계획입니다.

1.  **`feat/optimize-tensorrt`**: 
    - **전략:** NVIDIA 하드웨어에 최적화된 모델 개발
    - **기술:** 지식 증류(Knowledge Distillation), INT8 양자화(Quantization), ONNX, TensorRT, DeepStream을 이용한 배포

2.  **`feat/optimize-hailo`**:
    - **전략:** Hailo 하드웨어에 최적화된 모델 개발
    - **기술:** Hailo toolchain 및 HailoRT를 이용한 양자화 및 배포

3.  **`feat/backbone-yolo-nas`**:
    - **전략:** YOLOX 디텍터 백본을 더 빠르고 정확한 YOLO-NAS로 교체
    - **목표:** 베이스라인 성능 극대화

##  벤치마크 결과

각 YOLOX 백본 모델(X, L, M, S, Tiny, Nano)에 대한 상세 성능 비교는 [**BENCHMARK_RESULTS.md**](./BENCHMARK_RESULTS.md) 파일을 참고해 주세요.

##  빠른 시작

### 1. 데이터 준비
`datasets/` 폴더 안에 아래와 같은 구조로 MOT17 데이터셋을 준비합니다.
```
datasets/
└── MOT17/
    ├── train/
    └── test/
```

### 2. 추적 실행
`bash/` 폴더에 있는 스크립트를 사용하여 원하는 백본으로 추적을 실행합니다. 예를 들어, YOLOX-S 모델의 경우:
```bash
bash bash/run_mot17_s.sh
```
> **주의:** 실행 전, `pretrained/` 폴더에 해당 모델의 가중치 파일(예: `yolox_s.pth.tar`)이 반드시 있어야 합니다.

### 3. 성능 평가
추적이 완료되면, `run_eval.sh` 스크립트로 HOTA/MOTA 점수를 평가합니다. 2단계에서 생성된 결과 폴더 경로를 사용해야 합니다.
```bash
# 사용법: bash run_eval.sh [데이터셋] [추적_결과_경로] [GT_타입] [모델_타입]
bash bash/run_eval.sh MOT17 YOLOX_outputs/yolox_s_mix_det/runXXX/track_results val_half S
```

##  결과 저장 위치
- **추적 결과 (.txt):** `YOLOX_outputs/<실험_이름>/runXXX/track_results/`
- **최종 평가 결과 (HOTA 등):** `TrackEval/data/trackers/mot_challenge/MOT17-train/FastTracker-[모델_타입]/`
